# BTK Bot Konfigürasyon Dosyası
# BTK Bot Configuration File

# Test edilecek domain/IP adresi / Default domain/IP to test
DOMAIN_TO_CHECK = "google.com"

# BTK site sorgu URL'si / BTK site query URL
BTK_URL = "https://internet2.btk.gov.tr/sitesorgu/"

# CAPTCHA çözme ayarları / CAPTCHA solving settings
MAX_CAPTCHA_ATTEMPTS = 999  # Sınırsız deneme için yüksek değer / High value for unlimited attempts
CAPTCHA_MIN_LENGTH = 4  # Eski değere geri döndük / Back to original value
UNLIMITED_CAPTCHA_RETRY = True  # Sınırsız CAPTCHA denemesi / Unlimited CAPTCHA attempts

# WebDriver ayarları / WebDriver settings
HEADLESS_MODE = False  # True yaparsanız tarayıcı gözükmez / True for headless mode
WAIT_TIMEOUT = 15  # Elementleri beklerken maksimum süre (saniye) / Max wait time for elements (seconds) - 10'dan 15'e çıkardık

# OCR ayarları (Tesseract) / OCR settings (Tesseract)
OCR_CONFIG = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

# Görüntü işleme ayarları / Image processing settings
IMAGE_PROCESSING = {
    'clahe_clip_limit': 2.0,  # Eski değere geri döndük / Back to original value
    'clahe_tile_grid_size': (8, 8),
    'threshold_type': 'OTSU'
} 