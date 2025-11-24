from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from PIL import Image, ImageEnhance, ImageFilter
import easyocr
import numpy as np
import cv2
import io
import time
import base64
import requests

"""
KENDİ TELEGRAM BOT TOKEN VE CHAT ID'NİZİ GİRİN!!!
"""
TELEGRAM_BOT_TOKEN = " "
TELEGRAM_CHAT_ID = " "


def telegram_send(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg})
    except:
        pass


class BTKDomainQuery:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "https://internet.btk.gov.tr/sitesorgu/"

        print("EasyOCR başlatılıyor...")
        self.reader = easyocr.Reader(['en'], gpu=False)
        print("EasyOCR hazır!")

    # -----------------------------------
    # CAPTCHA ÖN İŞLEME
    # -----------------------------------
    def preprocess_captcha_image(self, image):
        if isinstance(image, Image.Image):
            image = np.array(image)
        if len(image.shape) == 3 and image.shape[2] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        height, width = gray.shape
        gray = cv2.resize(gray, (width * 3, height * 3), interpolation=cv2.INTER_CUBIC)

        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        thresh = cv2.adaptiveThreshold(
            blurred, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11, 2
        )
        kernel = np.ones((2, 2), np.uint8)
        morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        morphed = cv2.morphologyEx(morphed, cv2.MORPH_OPEN, kernel)

        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(morphed)

        return enhanced

    # -----------------------------------
    # CAPTCHA OKUMA
    # -----------------------------------
    def get_captcha_text(self):
        try:
            captcha_img = self.wait.until(
                EC.presence_of_element_located((By.ID, "security_code_image"))
            )

            screenshot = self.driver.get_screenshot_as_png()
            full_image = Image.open(io.BytesIO(screenshot))

            loc = captcha_img.location
            size = captcha_img.size
            left = loc['x']
            top = loc['y']
            right = left + size['width']
            bottom = top + size['height']

            captcha_image = full_image.crop((left, top, right, bottom))

            processed = self.preprocess_captcha_image(captcha_image)
            results = self.reader.readtext(processed)

            if not results:
                return None

            best = max(results, key=lambda x: x[2])
            text = ''.join(filter(str.isalnum, best[1]))
            confidence = best[2]

            if confidence < 0.3 or len(text) < 3:
                return None

            return text

        except:
            return None

    # -----------------------------------
    # SONUÇ ANALİZİ
    # -----------------------------------
    def check_result_status(self):
        time.sleep(2)
        src = self.driver.page_source

        if "Güvenlik kodunu yanlış" in src:
            return 'captcha_wrong'

        if "karar bulunamadı" in src:
            return 'success_no_block'

        if "uygulanmakta olan kararlar" in src:
            return 'success_blocked'

        return "unknown"

    # -----------------------------------
    # DOMAIN SORGULAMA
    # -----------------------------------
    def query_domain(self, domain):
        print(f"\n🌍 Sorgulanıyor: {domain}")
        self.driver.get(self.url)
        time.sleep(1)

        retry = 0

        while retry < 10:
            try:
                inp = self.wait.until(EC.presence_of_element_located((By.ID, "deger")))
                inp.clear()
                inp.send_keys(domain)

                captcha_text = self.get_captcha_text()

                if not captcha_text:
                    retry += 1
                    self.driver.refresh()
                    continue

                captcha_input = self.wait.until(
                    EC.presence_of_element_located((By.ID, "security_code"))
                )
                captcha_input.clear()
                captcha_input.send_keys(captcha_text)

                btn = self.wait.until(
                    EC.element_to_be_clickable((By.ID, "submit1"))
                )
                btn.click()

                status = self.check_result_status()

                if status == "captcha_wrong":
                    retry += 1
                    self.driver.refresh()
                    continue

                elif status == "success_no_block":
                    print(f"🟢 ENGEL YOK → {domain}")
                    return "no_block"

                elif status == "success_blocked":
                    print(f"🔴 ENGEL VAR! → {domain}")
                    telegram_send(f"🚨 BTK ENGEL TESPİT EDİLDİ!\nDomain: {domain}")
                    return "blocked"

                else:
                    retry += 1
                    self.driver.refresh()

            except:
                retry += 1
                self.driver.refresh()

        print("❌ 10 denemede sonuç alınamadı")
        return "fail"

    def close(self):
        try:
            self.driver.quit()
        except:
            pass


# ======================================================================
#  ANA LOOP – links.txt OKUMA + SONSUZ DÖNGÜ
# ======================================================================
def main_loop():
    print("\n\n🚀 BTK DOMAIN KONTROL BOTU BAŞLADI • 7/24 ÇALIŞIYOR...\n")

    while True:
        try:
            with open("links.txt", "r", encoding="utf-8") as f:
                domains = [i.strip() for i in f.readlines() if i.strip()]
        except:
            print("links.txt okunamadı!")
            time.sleep(10)
            continue

        bot = BTKDomainQuery()

        for domain in domains:
            bot.query_domain(domain)
            time.sleep(2)

        bot.close()

        print("\n⏳ Liste tamamlandı → 5 dakika bekleniyor...\n")
        time.sleep(600)  # 5 dakika


if __name__ == "__main__":
    main_loop()
