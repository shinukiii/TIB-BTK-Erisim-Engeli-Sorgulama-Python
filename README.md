# 🚨 TİB BTK Eerişim Engeli Sorgulama Otomasyonu

**EasyOCR + Selenium + Telegram Bildirimi + Sonsuz Döngü + Link
Listesi**

Bu proje, **BTK'nın site sorgu sistemi** üzerinden domain engel durumunu
otomatik olarak kontrol eden bir bottur.\
CAPTCHA otomatik çözme için **EasyOCR**, web etkileşimi için
**Selenium**, bildirimler için **Telegram Bot API** kullanır.

Bot, `links.txt` içerisindeki tüm domainleri sırayla sorgular ve BTK
engeli tespit edilirse Telegram'dan bildirim gönderir.\
Otomasyon **7/24 kesintisiz** döngüde çalışacak şekilde tasarlanmıştır.

------------------------------------------------------------------------

## 📌 Özellikler

-   🧠 **EasyOCR ile CAPTCHA çözme**
-   🌍 BTK **engelli / engelsiz** kontrolü
-   🔔 **Telegram bildirimi** (Domain engellenirse)
-   ♻️ **Sonsuz döngü sistemi** (Her 5 dakikada bir tekrar eder)
-   📄 `links.txt` üzerinden domain listesi yönetimi
-   🧹 CAPTCHA ön işleme (Adaptive Threshold + Morphology + CLAHE)
-   🕵️‍♂️ Anti-Automation bypass (Selenium stealth ayarları)

------------------------------------------------------------------------

## 📂 Dosya Yapısı

    /
    ├── tib.py          # Python bot dosyası (asıl kod)
    ├── links.txt          # Kontrol edilecek domain listesi
    └── README.md

------------------------------------------------------------------------

## 🔧 Gereksinimler

### Windows Kullanıcıları İçin:

-   Python 3.8+\
-   Google Chrome\
-   ChromeDriver (Sürüme uygun)

### Python Kütüphaneleri

Terminalden:

``` bash
pip install selenium
pip install easyocr
pip install opencv-python
pip install pillow
pip install numpy
pip install requests
```

------------------------------------------------------------------------

## 🧩 ChromeDriver Kurulumu

1.  Chrome sürümünü öğren:
2.  
```{=html}
chrome://settings/help
```

3.  Uygun ChromeDriver'ı indir:\
    https://googlechromelabs.github.io/chrome-for-testing/

4.  `chromedriver.exe` dosyasını şu konuma koy:

```{=html}
Proje klasörü /
```

------------------------------------------------------------------------

## 📄 links.txt Örneği

    google.com
    pornhub.com
    youtube.com

------------------------------------------------------------------------

## 🤖 Telegram Bot Ayarları

### 1. Telegram bot oluştur

👉 **@BotFather**

    /newbot

Token örneği:

    123456:ABCDEF_mySuperToken

### 2. Chat ID öğren

👉 **@getmyid_bot**

Örnek:

    123456789

------------------------------------------------------------------------

## 🧷 Ayarların Koda Yazılması

`tib.py` içinde:

``` python
TELEGRAM_BOT_TOKEN = "123456:ABCDEF_mySuperToken"
TELEGRAM_CHAT_ID = "123456789"
```

------------------------------------------------------------------------

## ▶️ Botu Çalıştırma

Windows:

``` bash
python tib.py
```

Linux:

``` bash
python3 tib.py
```

------------------------------------------------------------------------

## 🔁 Bot Nasıl Çalışır?

1.  `links.txt` içindeki tüm site adreslerini okur.
2.  BTK sitesine gider.
3.  CAPTCHA görüntüsünü alır ve OCR ile çözer.
4.  Domaini sorgular.
5.  Sonuç:
    -   🟢 Engel yok → Terminal
    -   🔴 Engel var → Telegram bildirimi\
6.  Liste bitince **5 dakika bekler**.
7.  Döngü sonsuza kadar devam eder.

------------------------------------------------------------------------

TELEGRAM GRUBUMUZ: [UnblockTR](https://t.me/UnblockTR)

------------------------------------------------------------------------

## 📝 Lisans

MIT License

------------------------------------------------------------------------
