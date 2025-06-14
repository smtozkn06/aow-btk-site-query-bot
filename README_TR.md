# 🤖 BTK Site Sorgu Botu

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)
![GUI](https://img.shields.io/badge/GUI-CustomTkinter-orange.svg)

**BTK (Bilgi Teknolojileri ve İletişim Kurumu) site sorgu sistemini otomatik olarak kullanarak domain/IP adreslerinin engelli olup olmadığını kontrol eder. Modern CustomTkinter arayüzü ve çok dilli destek (Türkçe/İngilizce) ile kullanıcı dostu bir deneyim sunar.**

**🇺🇸 [Click here for English README](README.md)**

[🚀 Kurulum](#-kurulum) • [📖 Kullanım](#-kullanım) • [⚙️ Özellikler](#️-özellikler) • [🖼️ Ekran Görüntüleri](#️-ekran-görüntüleri) • [🤝 Katkıda Bulunma](#-katkıda-bulunma)

</div>

---

## 📋 İçindekiler

- [🎯 Proje Hakkında](#-proje-hakkında)
- [✨ Özellikler](#-özellikler)
- [🖼️ Ekran Görüntüleri](#️-ekran-görüntüleri)
- [🚀 Kurulum](#-kurulum)
- [📖 Kullanım](#-kullanım)
- [⚙️ Konfigürasyon](#️-konfigürasyon)
- [🔧 Teknik Detaylar](#-teknik-detaylar)
- [🐛 Sorun Giderme](#-sorun-giderme)
- [🤝 Katkıda Bulunma](#-katkıda-bulunma)
- [📄 Lisans](#-lisans)

## 🎯 Proje Hakkında

Bu bot, BTK (Bilgi Teknolojileri ve İletişim Kurumu) site sorgu sistemini otomatik olarak kullanarak domain/IP adreslerinin engelli olup olmadığını kontrol eder. Modern CustomTkinter arayüzü ile kullanıcı dostu bir deneyim sunar.

### 🎪 Ana Özellikler

- 🤖 **Otomatik CAPTCHA Çözme**: Gelişmiş OCR teknolojisi ile
- 🌐 **Tek ve Toplu Test**: Birden fazla domain'i aynı anda test etme
- 🎨 **Modern Arayüz**: CustomTkinter ile dark/light tema desteği
- 📊 **Detaylı Raporlama**: Renkli sonuç analizi ve Excel export
- ⚡ **Paralel İşleme**: Çoklu tarayıcı desteği ile hızlı test
- 💾 **Otomatik Kaydetme**: Domain listelerini otomatik kaydetme
- 🔄 **Sınırsız Deneme**: CAPTCHA çözümü için sınırsız deneme modu
- 🌍 **Çok Dilli Destek**: Türkçe/İngilizce arayüz

## ✨ Özellikler

### 🖥️ Kullanıcı Arayüzü
- ✅ Modern CustomTkinter tabanlı GUI
- ✅ Dark/Light tema desteği
- ✅ Responsive tasarım
- ✅ Gerçek zamanlı ilerleme takibi
- ✅ Renkli log sistemi
- ✅ **Çok dilli destek (Türkçe/İngilizce)**

### 🔧 Bot Özellikleri
- ✅ Otomatik form doldurma
- ✅ Gelişmiş CAPTCHA çözme algoritması
- ✅ Hata durumunda otomatik yeniden deneme
- ✅ Özelleştirilebilir ayarlar
- ✅ Detaylı log çıktısı
- ✅ **Dinamik dil değiştirme**

### 📊 Test Özellikleri
- ✅ Tek domain/IP testi
- ✅ Toplu domain testi (bulk testing)
- ✅ Paralel tarayıcı desteği (1-5 tarayıcı)
- ✅ Domain arası bekleme süresi ayarı
- ✅ Sonuçları Excel'e aktarma
- ✅ **Gerçek zamanlı sonuç tablosu güncellemeleri**

## 🖼️ Ekran Görüntüleri

### Ana Arayüz
![Ana Arayüz](images/Ekran%20görüntüsü%202025-06-14%20201228.png)
*Modern CustomTkinter arayüzü ile domain test ekranı*

### Test Sonuçları
![Test Sonuçları](images/Ekran%20görüntüsü%202025-06-14%20201655.png)
*Detaylı test sonuçları ve analiz ekranı*

### Ayarlar Paneli
![Ayarlar](images/Ekran%20görüntüsü%202025-06-14%20201211.png)
*Bot ayarları ve konfigürasyon paneli*

## 🚀 Kurulum

### Gereksinimler

- **Python 3.9+**
- **Google Chrome** tarayıcısı
- **Tesseract OCR** (CAPTCHA çözme için)

### 1. Projeyi İndirin

```bash
git clone https://github.com/yourusername/btk-site-query-bot.git
cd btk-site-query-bot
```

### 2. Python Paketlerini Kurun

```bash
pip install -r requirements.txt
```

### 3. Tesseract OCR Kurulumu

#### Windows:
1. [Tesseract OCR](https://tesseract-ocr.github.io/tessdoc/Downloads.html) indirin
2. Kurulum dosyasını çalıştırın (UB Mannheim installer önerilir)
3. Tesseract'ı sistem PATH'ine ekleyin
4. Varsayılan kurulum yolu: `C:\Program Files\Tesseract-OCR\tesseract.exe`

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-eng
```

#### macOS:
```bash
brew install tesseract
```

### 4. Ayarları Yapılandırın (İsteğe Bağlı)

```bash
# Örnek ayar dosyasını kopyalayın
cp bot_settings.example.json bot_settings.json

# Gerekirse ayarları düzenleyin (dil, varsayılan domain'ler, vb.)
# Uygulama ilk çalıştırıldığında bu dosya yoksa otomatik olarak oluşturacaktır
```

### 5. Uygulamayı Başlatın

```bash
# Modern GUI arayüzü (Önerilen)
python ui_app.py

# Komut satırı versiyonu
python btk_bot.py
```

## 📖 Kullanım

### GUI Arayüzü ile Kullanım

1. **Tek Domain Testi**:
   - "Domain Test" sekmesine gidin
   - "Tek Domain Test" alanına domain/IP girin
   - "Test Başlat" butonuna tıklayın

2. **Toplu Domain Testi**:
   - "Toplu Domain Test" alanına her satıra bir domain yazın
   - Paralel tarayıcı sayısını ayarlayın (1-5)
   - "Test Başlat" butonuna tıklayın

3. **Sonuçları Görüntüleme**:
   - "Sonuçlar" sekmesinde detaylı analiz
   - Renkli tablo ile erişilebilir/engelli durumu
   - Excel'e aktarma özelliği

### Komut Satırı Kullanımı

```python
from btk_bot import BTKBot

# Tek domain testi
bot = BTKBot(domain="example.com")
success = bot.run()

if success:
    print("Test başarılı!")
else:
    print("Test başarısız!")
```

### Dil Ayarları

Uygulama hem Türkçe hem İngilizce destekler:

- **Varsayılan Dil**: İngilizce
- **Dil Değiştirme**: Ayarlar → Dil Ayarları → "Türkçe" seçin
- **Dinamik Değiştirme**: Uygulamayı yeniden başlatmadan dil değiştirilebilir

## ⚙️ Konfigürasyon

### config.py Ayarları

```python
# Test edilecek varsayılan domain
DOMAIN_TO_CHECK = "google.com"

# BTK site sorgu URL'si
BTK_URL = "https://internet2.btk.gov.tr/sitesorgu/"

# CAPTCHA ayarları
MAX_CAPTCHA_ATTEMPTS = 999  # Sınırsız deneme için yüksek değer
UNLIMITED_CAPTCHA_RETRY = True
CAPTCHA_MIN_LENGTH = 4

# WebDriver ayarları
HEADLESS_MODE = False  # True = gizli mod
WAIT_TIMEOUT = 15  # Element bekleme süresi

# OCR ayarları
OCR_CONFIG = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
```

### bot_settings.json (Otomatik Kaydedilen Ayarlar)

Uygulama kullanıcı tercihlerini saklamak için otomatik olarak bir `bot_settings.json` dosyası oluşturur ve yönetir. Şablon olarak sağlanan `bot_settings.example.json` dosyasını kullanabilirsiniz:

```json
{
    "language": "en",
    "headless_mode": true,
    "max_captcha_attempts": 5,
    "wait_timeout": 30,
    "default_delay": 3,
    "parallel_browsers": 1,
    "filter_captcha_logs": true,
    "single_domain": "example.com",
    "bulk_domains": "google.com\nfacebook.com\ntwitter.com\ngithub.com"
}
```

**Not**: `bot_settings.json` dosyası ilk çalıştırmada otomatik olarak oluşturulur ve kullanıcı gizliliğini korumak için sürüm kontrolünden hariç tutulur.

## 🔧 Teknik Detaylar

### Bot İş Akışı

1. **WebDriver Başlatma**: Chrome tarayıcısını başlatır
2. **Site Navigasyonu**: BTK sorgu sayfasına gider
3. **Form Doldurma**: Domain/IP adresini girer
4. **CAPTCHA Çözme**:
   - CAPTCHA görüntüsünü indirir
   - Görüntü işleme teknikleri uygular
   - OCR ile metne çevirir
   - Formu gönderir
5. **Sonuç Analizi**: Sorgu sonucunu analiz eder ve raporlar

### CAPTCHA Çözme Algoritması

- **Gri Tonlama**: Renkli görüntüyü gri tonlamaya çevirir
- **Görüntü Büyütme**: OCR doğruluğu için görüntüyü büyütür
- **Gürültü Azaltma**: Median blur ile gürültüyü azaltır
- **Kontrast Artırma**: CLAHE algoritması ile kontrast artırır
- **Threshold**: OTSU algoritması ile binary görüntü oluşturur
- **OCR**: Tesseract ile metin çıkarımı ve özel konfigürasyon

### Dosya Yapısı

```
btk-site-query-bot/
├── 📁 images/                   # Ekran görüntüleri
│   ├── 🖼️ screenshot1.png
│   ├── 🖼️ screenshot2.png
│   └── 🖼️ screenshot3.png
├── 📁 __pycache__/             # Python cache
├── 🐍 btk_bot.py               # Ana bot mantığı
├── 🖥️ ui_app.py                # Modern GUI uygulaması
├── ⚙️ config.py                # Konfigürasyon ayarları
├── 🌍 languages.py             # Çok dilli destek
├── 💾 bot_settings.example.json # Örnek ayar dosyası
├── 📋 requirements.txt         # Python bağımlılıkları
├── 📄 LICENSE                  # MIT Lisansı
├── 🤝 CONTRIBUTING.md          # Katkı rehberi
├── 📖 README.md               # Ana README (İngilizce)
└── 📖 README_TR.md            # Bu dosya (Türkçe)
```

## 🐛 Sorun Giderme

### Tesseract Hatası
```
TesseractNotFoundError: tesseract is not installed
```
**Çözüm**: Tesseract OCR'ı kurun ve PATH'e ekleyin.

### WebDriver Hatası
```
WebDriverException: 'chromedriver' executable needs to be in PATH
```
**Çözüm**: Chrome tarayıcısının kurulu olduğundan emin olun. WebDriver otomatik indirilir.

### NumPy Uyumluluk Hatası
```
AttributeError: _ARRAY_API not found
```
**Çözüm**: Uyumlu NumPy sürümünü kurun:
```bash
pip uninstall opencv-python numpy -y
pip install "numpy<2.0.0" "opencv-python>=4.8.0,<4.10.0"
```

### GUI Başlamıyor
```bash
pip install customtkinter>=5.2.0
```

## 🤝 Katkıda Bulunma

Bu proje açık kaynaklıdır ve katkılarınızı memnuniyetle karşılıyoruz!

1. **Fork** edin
2. **Feature branch** oluşturun (`git checkout -b feature/amazing-feature`)
3. **Commit** edin (`git commit -m 'Add some amazing feature'`)
4. **Push** edin (`git push origin feature/amazing-feature`)
5. **Pull Request** açın

### Katkı Alanları

- 🐛 Bug düzeltmeleri
- ✨ Yeni özellikler
- 📚 Dokümantasyon iyileştirmeleri
- 🌍 Çeviri desteği
- 🎨 UI/UX iyileştirmeleri

## 📊 İstatistikler

- ⭐ **CAPTCHA Başarı Oranı**: %85-95
- 🚀 **Test Hızı**: ~30 saniye/domain
- 🔄 **Paralel İşleme**: 5 tarayıcıya kadar
- 💾 **Desteklenen Formatlar**: TXT, Excel
- 🌐 **Platform Desteği**: Windows, Linux, macOS

## ⚠️ Önemli Notlar

- Bu bot eğitim ve test amaçlı geliştirilmiştir
- BTK web sitesi kullanım koşullarına uygun kullanın
- Sunucu yükünü önlemek için aşırı istek göndermeyin
- Sorumlu kullanım prensiplerine uyun

## 💰 Projeyi Destekleyin

Bu projeyi faydalı bulduysanız, geliştirmeye destek olabilirsiniz:

**USDT (TRC20)**: `TYxPh6pZX7Wq9HB6nY2oXhVVnTVPnzxDmR`

Desteğiniz projenin sürdürülmesi ve geliştirilmesi için çok değerli! 🙏

## 📄 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 📞 İletişim

- 🐛 **Bug Raporu**: [Issues](https://github.com/yourusername/btk-site-query-bot/issues)
- 💡 **Özellik İsteği**: [Issues](https://github.com/yourusername/btk-site-query-bot/issues)
- 📧 **E-posta**: admim@aowsoftware.com

---

<div align="center">

**❤️ Açık kaynak topluluğu için sevgiyle yapıldı**

[![GitHub stars](https://img.shields.io/github/stars/yourusername/btk-site-query-bot.svg?style=social&label=Star)](https://github.com/yourusername/btk-site-query-bot)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/btk-site-query-bot.svg?style=social&label=Fork)](https://github.com/yourusername/btk-site-query-bot/fork)

</div> 
