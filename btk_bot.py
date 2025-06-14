import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import pytesseract
import cv2
import numpy as np
import os
import io
import config
from colorama import Fore, Back, Style, init
from languages import get_text, get_current_language, lang_manager

# Colorama başlat (Windows için)
init(autoreset=True)

class BTKBot:
    def __init__(self, domain=None):
        self.base_url = config.BTK_URL
        self.domain_to_check = domain or config.DOMAIN_TO_CHECK
        self.driver = None
        
        # Dil ayarını yükle
        lang_manager.load_language_preference()
        
    def setup_driver(self):
        """Chrome WebDriver'ı başlat"""
        try:
            # Chrome seçenekleri
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            if config.HEADLESS_MODE:
                chrome_options.add_argument("--headless")
            
            # WebDriver'ı başlat
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print(f"✅ {get_text('webdriver_started')}")
            return True
            
        except Exception as e:
            print(f"❌ {get_text('webdriver_error')}: {e}")
            return False
    
    def navigate_to_site(self):
        try:
            print(f"🌐 {get_text('navigating_to')} {self.base_url}...")
            self.driver.get(self.base_url)
            
            # Sayfanın yüklenmesini bekle
            WebDriverWait(self.driver, config.WAIT_TIMEOUT).until(
                EC.presence_of_element_located((By.ID, "deger"))
            )
            
            print(f"✅ {get_text('site_loaded')}")
            return True
            
        except Exception as e:
            print(f"❌ {get_text('site_load_error')}: {e}")
            return False
    
    def fill_domain_input(self):
        """Domain input alanını doldur"""
        try:
            # Domain input alanını bul ve doldur
            domain_input = self.driver.find_element(By.ID, "deger")
            domain_input.clear()
            domain_input.send_keys(self.domain_to_check)
            
            print(f"✅ Domain '{self.domain_to_check}' {get_text('domain_entered')}")
            return True
            
        except Exception as e:
            print(f"❌ {get_text('domain_entry_error')}: {e}")
            return False
    
    def process_captcha_image(self, image_data):
        """CAPTCHA görüntüsünü işle ve metne çevir"""
        try:
            # Görüntü verilerini kontrol et
            if not image_data or len(image_data) < 100:
                # Sessiz hata - log'a yazmıyoruz
                return None
            
            # Geçici dosya olarak kaydet ve yükle
            temp_filename = "temp_captcha.png"
            with open(temp_filename, 'wb') as f:
                f.write(image_data)
            
            # PIL Image olarak yükle
            image = Image.open(temp_filename)
            
            # Görüntüyü büyüt (OCR performansı için)
            scale_factor = 3  # Eski değere geri döndük
            width = int(image.width * scale_factor)
            height = int(image.height * scale_factor)
            image = image.resize((width, height), Image.LANCZOS)
            
            # OpenCV formatına çevir
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Görüntüyü gri tonlamaya çevir
            gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
            
            # Median blur ile gürültüyü azalt (eski yöntem)
            blurred = cv2.medianBlur(gray, 3)
            
            # Kontrast artır (eski yöntem)
            clahe = cv2.createCLAHE(
                clipLimit=2.0,  # Eski değere geri döndük
                tileGridSize=config.IMAGE_PROCESSING['clahe_tile_grid_size']
            )
            enhanced = clahe.apply(blurred)
            
            # Threshold uygula (eski yöntem)
            _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Tesseract ile OCR (eski yöntem)
            custom_config = config.OCR_CONFIG
            captcha_text = pytesseract.image_to_string(thresh, config=custom_config).strip()
            
            # Temizle ve sadece alfanumerik karakterleri tut
            captcha_text = ''.join(char for char in captcha_text if char.isalnum())
            
            # Geçici dosyayı temizle
            try:
                os.remove(temp_filename)
            except:
                pass
            
            if captcha_text and len(captcha_text) >= config.CAPTCHA_MIN_LENGTH:
                print(f"✅ {get_text('captcha_solved')}: '{captcha_text}'")
                return captcha_text
            else:
                # Sessiz hata - sadece debug için
                return None
            
        except Exception as e:
            # Sessiz hata - sadece kritik durumlar için log
            try:
                os.remove("temp_captcha.png")
            except:
                pass
            return None
    
    def solve_captcha(self):
        """CAPTCHA'yı çöz"""
        try:
            print(f"🔍 {get_text('searching_captcha')}")
            
            # CAPTCHA görüntüsünü bul
            captcha_image = WebDriverWait(self.driver, config.WAIT_TIMEOUT).until(
                EC.presence_of_element_located((By.ID, "security_code_image"))
            )
            
            # CAPTCHA görüntüsünün src'sini al
            captcha_src = captcha_image.get_attribute("src")
            print(f"📷 {get_text('captcha_found')}: {captcha_src}")
            
            # Selenium üzerinden screenshot al
            captcha_screenshot = captcha_image.screenshot_as_png
            
            if captcha_screenshot and len(captcha_screenshot) > 100:
                
                # CAPTCHA'yı çöz
                captcha_text = self.process_captcha_image(captcha_screenshot)
                
                if captcha_text and len(captcha_text) >= config.CAPTCHA_MIN_LENGTH:
                    print(f"🔓 {get_text('captcha_solved')}: '{captcha_text}'")
                    
                    # CAPTCHA input alanını bul ve doldur
                    captcha_input = self.driver.find_element(By.ID, "security_code")
                    captcha_input.clear()
                    captcha_input.send_keys(captcha_text)
                    
                    print(f"✅ {get_text('captcha_entered')}")
                    return True
                else:
                    print(f"❌ {get_text('captcha_failed')}")
                    return False
            else:
                print(f"❌ {get_text('captcha_failed')}")
                return False
                
        except Exception as e:
            print(f"❌ {get_text('captcha_error')}: {e}")
            return False
    
    def submit_form(self):
        """Formu gönder"""
        try:
            # Submit butonunu bul ve tıkla
            submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit' or @type='button']")
            submit_button.click()
            
            print(f"✅ {get_text('form_submitted')}")
            
            # Sonuç sayfasının yüklenmesini bekle
            time.sleep(3)
            
            return True
            
        except Exception as e:
            print(f"❌ {get_text('form_submit_error')}: {e}")
            return False
    
    def get_result(self):
        """Sorgu sonucunu al ve analiz et"""
        try:
            # Sonuç sayfasının yüklenmesini bekle - daha uzun süre
            time.sleep(5)  # 2'den 5'e çıkardık
            
            # Karar sonucu div'ini bul
            try:
                # Önce sayfanın tamamen yüklendiğinden emin ol
                WebDriverWait(self.driver, 15).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
                
                # Karar div'ini bul
                karar_div = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "sorgu_mahkeme"))
                )
                
                # yazi2 class'ındaki asıl BTK kararını bul
                try:
                    yazi2_element = karar_div.find_element(By.CLASS_NAME, "yazi2")
                    karar_text = yazi2_element.text.strip()
                except Exception as yazi2_error:
                    # Fallback: Tüm div'in metnini al
                    karar_text = karar_div.text.strip()
                
                # Karar sonucunu analiz et
                result_text = self.analyze_decision_result(karar_text)
                
                # Eğer geçerli sonuç yoksa (CAPTCHA yanlış çözüldü)
                if self.is_invalid_result(result_text):
                    print(f"⚠️ {get_text('invalid_result_detected')}: {result_text}")
                    return "CAPTCHA_RETRY_NEEDED"
                
            except Exception as e:
                print(f"⚠️ {get_text('result_div_not_found')}: {e}")
                
                # Div bulunamazsa sayfa kaynağını kontrol et
                try:
                    page_source = self.driver.page_source
                    
                    # HTML'den yazi2 class'ını ara
                    import re
                    yazi2_match = re.search(r'<div[^>]*class="yazi2"[^>]*>(.*?)</div>', page_source, re.DOTALL)
                    if yazi2_match:
                        # HTML taglerini temizle
                        yazi2_content = re.sub(r'<[^>]+>', '', yazi2_match.group(1))
                        yazi2_content = yazi2_content.strip()
                        
                        if yazi2_content:
                            result_text = self.analyze_decision_result(yazi2_content)
                            if not self.is_invalid_result(result_text):
                                # Renkli çıktı ver
                                self.print_colored_result(self.domain_to_check, result_text)
                                return result_text
                    
                    # CAPTCHA hatası kontrolü - daha detaylı
                    captcha_error_indicators = [
                        "güvenlik kodu", "security code", "captcha", "doğrulama kodu",
                        "verification code", "hatalı kod", "wrong code", "kod yanlış"
                    ]
                    
                    if any(indicator in page_source.lower() for indicator in captcha_error_indicators):
                        print(f"🔄 {get_text('captcha_error_detected_in_page')}")
                        return "CAPTCHA_RETRY_NEEDED"
                    
                    # Sayfa içeriğini daha detaylı analiz et
                    result_text = get_text('result_not_found_analyzing')
                    
                    # BTK'nın standart cevaplarını ara
                    if "karar bulunamadı" in page_source.lower() or "no decision" in page_source.lower():
                        result_text = get_text('btk_no_decision')
                    elif "engellenmiş" in page_source.lower() or "blocked" in page_source.lower():
                        result_text = get_text('site_appears_blocked')
                    elif "erişilebilir" in page_source.lower() or "accessible" in page_source.lower():
                        result_text = get_text('site_appears_accessible')
                    elif "mahkeme" in page_source.lower() or "court" in page_source.lower():
                        # Mahkeme kararı varsa detayını bul
                        mahkeme_match = re.search(r'(mahkeme.*?karar.*?[^\n]{0,100})', page_source.lower())
                        if mahkeme_match:
                            result_text = f"{get_text('btk_court_decision')}: {mahkeme_match.group(1)[:100]}..."
                        else:
                            result_text = get_text('btk_court_decision')
                    
                    # Bu da geçersiz sonuç olabilir
                    if self.is_invalid_result(result_text):
                        print(f"⚠️ {get_text('page_analysis_invalid')}")
                        return "CAPTCHA_RETRY_NEEDED"
                        
                except Exception as page_error:
                    print(f"❌ {get_text('page_source_error')}: {page_error}")
                    return "CAPTCHA_RETRY_NEEDED"
            
            # Renkli çıktı ver
            if result_text and result_text != "CAPTCHA_RETRY_NEEDED":
                self.print_colored_result(self.domain_to_check, result_text)
            
            return result_text
            
        except Exception as e:
            print(f"❌ {get_text('result_get_error')}: {e}")
            return "CAPTCHA_RETRY_NEEDED"  # Hata durumunda retry yap
    
    def is_invalid_result(self, result_text):
        """Sonucun geçersiz olup olmadığını kontrol et (CAPTCHA hatası)"""
        invalid_indicators = [
            get_text('result_not_found_analyzing'),
            get_text('general_page_analysis'),
            get_text('page_analysis'),
            get_text('analyzing')
        ]
        
        if not result_text:
            return True
            
        result_lower = result_text.lower()
        return any(indicator in result_lower for indicator in invalid_indicators)
    
    def translate_btk_result_to_english(self, turkish_result):
        """BTK sonucunu İngilizceye çevir"""
        if not turkish_result:
            return turkish_result
        
        # Türkçe-İngilizce çeviri sözlüğü
        translations = {
            "Bilgi Teknolojileri ve İletişim Kurumu tarafından uygulanan bir karar bulunamadı.": 
                "No decision found by the Information and Communication Technologies Authority.",
            
            "İlgili Kararlar": "Related Decisions",
            "hakkında uygulanmakta olan kararlar:": "decisions being applied regarding:",
            "tarihli ve": "dated and numbered",
            "sayılı": "",
            "Telekomünikasyon İletişim Başkanlığı kararıyla erişime engellenmiştir": 
                "has been blocked by the decision of Telecommunication Presidency",
            "erişime engellenmiştir": "has been blocked",
            "kararıyla": "by the decision",
            "Telekomünikasyon İletişim Başkanlığı": "Telecommunication Presidency"
        }
        
        result = turkish_result
        
        # Çevirileri uygula
        for turkish, english in translations.items():
            result = result.replace(turkish, english)
        
        return result
    
    def analyze_decision_result(self, karar_text):
        """Karar sonucunu analiz et"""
        if not karar_text:
            return get_text('decision_text_empty')
        
        # Metni temizle ve tam olarak döndür
        karar_text = karar_text.strip()
        
        # İngilizce modda çeviri yap
        if get_current_language() == 'en':
            karar_text = self.translate_btk_result_to_english(karar_text)
        
        # Tam metni döndür - karakter sınırı yok
        return karar_text
    
    def print_colored_result(self, domain, result):
        """Sonucu renkli olarak yazdır"""
        # Mahkeme kararı varsa kırmızı renkte yazdır
        mahkeme_keywords = ["mahkeme", "mahkem", "ağır", "ceza", "sulh", "hüküm", get_text('btk_court_decision')]
        
        if any(keyword.lower() in result.lower() for keyword in mahkeme_keywords):
            # Kırmızı arka plan ile uyarı
            print(f"\n{Back.RED}{Fore.WHITE}{'='*80}{Style.RESET_ALL}")
            print(f"{Back.RED}{Fore.WHITE} ⚠️  {get_text('btk_court_decision_detected')} ⚠️ {Style.RESET_ALL}")
            print(f"{Back.RED}{Fore.WHITE}{'='*80}{Style.RESET_ALL}")
            print(f"{Fore.RED}{Style.BRIGHT}{domain} {result}{Style.RESET_ALL}")
            print(f"{Back.RED}{Fore.WHITE}{'='*80}{Style.RESET_ALL}\n")
        else:
            # Normal yeşil renkte yazdır - sadece domain ve BTK kararını göster
            print(f"{Fore.CYAN}{Style.BRIGHT}{domain}{Style.RESET_ALL} {Fore.GREEN}{result}{Style.RESET_ALL}")
    
    def run(self):
        """Botu çalıştır"""
        try:
            print(f"🤖 {get_text('bot_starting')}")
            
            # WebDriver'ı başlat
            if not self.setup_driver():
                return False
            
            # Siteye git
            if not self.navigate_to_site():
                return False
            
            # Domain'i gir
            if not self.fill_domain_input():
                return False
            
            # CAPTCHA'yı çöz
            captcha_solved = False
            attempt = 0
            
            if config.UNLIMITED_CAPTCHA_RETRY:
                print(f"🔄 {get_text('unlimited_captcha_mode')}")
                
                while not captcha_solved:
                    attempt += 1
                    print(f"🔄 {get_text('captcha_attempt')} #{attempt}")
                    
                    if self.solve_captcha():
                        captcha_solved = True
                        print(f"✅ {get_text('captcha_solved_attempt').format(attempt)}")
                        break
                    else:
                        # Sessiz retry - sadece gerektiğinde mesaj
                        if attempt < config.MAX_CAPTCHA_ATTEMPTS - 1:
                            self.driver.refresh()
                            time.sleep(2)
                            
                            # Domain'i tekrar gir
                            self.fill_domain_input()
                        
                        # Her 10 denemede bir kısa bekleme
                        if attempt % 10 == 0 and attempt > 0:
                            print(f"⏳ {attempt} {get_text('attempts_completed')}, 5 {get_text('seconds_waiting')}...")
                            time.sleep(5)
            else:
                # Eski sınırlı sistem
                max_captcha_attempts = config.MAX_CAPTCHA_ATTEMPTS
                
                for attempt in range(max_captcha_attempts):
                    print(f"🔄 {get_text('captcha_attempt')} {attempt + 1}/{max_captcha_attempts}")
                    
                    if self.solve_captcha():
                        captcha_solved = True
                        break
                    else:
                        if attempt < max_captcha_attempts - 1:
                            print(f"🔄 {get_text('page_refreshing')}")
                            self.driver.refresh()
                            time.sleep(2)
                            
                            # Domain'i tekrar gir
                            self.fill_domain_input()
                
                if not captcha_solved:
                    print(f"❌ {get_text('max_attempts_reached')}")
                    return False
            
            # Formu gönder
            if not self.submit_form():
                return False
            
            # Sonucu al
            result = self.get_result()
            
            # Eğer CAPTCHA hatası varsa tüm işlemi tekrar dene
            if result == "CAPTCHA_RETRY_NEEDED":
                print(f"🔄 {get_text('captcha_wrong_retrying')}")
                self.driver.quit()
                time.sleep(2)
                
                # Sınırsız domain tekrar denemesi
                retry_attempt = 0
                max_domain_retries = 999 if config.UNLIMITED_CAPTCHA_RETRY else 2
                
                while retry_attempt < max_domain_retries:
                    retry_attempt += 1
                    if config.UNLIMITED_CAPTCHA_RETRY:
                        print(f"🔄 {get_text('retrying_domain')} #{retry_attempt} ({get_text('unlimited_mode')})")
                    else:
                        print(f"🔄 {get_text('retrying_domain')} {retry_attempt}/2")
                    
                    try:
                        # WebDriver'ı yeniden başlat
                        if not self.setup_driver():
                            continue
                        
                        # Siteye git
                        if not self.navigate_to_site():
                            continue
                        
                        # Domain'i gir
                        if not self.fill_domain_input():
                            continue
                        
                        # CAPTCHA'yı çöz
                        captcha_solved = False
                        retry_attempt_captcha = 0
                        
                        if config.UNLIMITED_CAPTCHA_RETRY:
                            while not captcha_solved:
                                retry_attempt_captcha += 1
                                print(f"🔄 {get_text('retry_captcha_solving')} #{retry_attempt_captcha}")
                                
                                try:
                                    if self.solve_captcha():
                                        captcha_solved = True
                                        break
                                    else:
                                        # Sessiz retry - sadece sayfa yenile
                                        self.driver.refresh()
                                        time.sleep(3)  # Bekleme süresini artırdık
                                        self.fill_domain_input()
                                        
                                        # Her 5 denemede bir uzun bekleme
                                        if retry_attempt_captcha % 5 == 0:
                                            print(f"⏳ {retry_attempt_captcha} {get_text('attempts_completed')}, 10 {get_text('seconds_waiting')}...")
                                            time.sleep(10)
                                except Exception as e:
                                    # Sessiz hata yönetimi
                                    self.driver.refresh()
                                    time.sleep(3)
                                    self.fill_domain_input()
                        else:
                            for attempt in range(config.MAX_CAPTCHA_ATTEMPTS):
                                print(f"🔄 {get_text('captcha_attempt')} {attempt + 1}/{config.MAX_CAPTCHA_ATTEMPTS}")
                                
                                try:
                                    if self.solve_captcha():
                                        captcha_solved = True
                                        break
                                    else:
                                        if attempt < config.MAX_CAPTCHA_ATTEMPTS - 1:
                                            # Sessiz sayfa yenileme
                                            self.driver.refresh()
                                            time.sleep(3)  # Bekleme süresini artırdık
                                            self.fill_domain_input()
                                except Exception as e:
                                    # Sessiz hata yönetimi
                                    if attempt < config.MAX_CAPTCHA_ATTEMPTS - 1:
                                        self.driver.refresh()
                                        time.sleep(3)
                                        self.fill_domain_input()
                            
                            if not captcha_solved:
                                print(f"❌ {get_text('captcha_could_not_solve')}")
                                continue
                        
                        # Formu gönder
                        if not self.submit_form():
                            print(f"❌ {get_text('form_submit_error')}")
                            continue
                        
                        # Sonucu al - daha güvenli hata yönetimi
                        try:
                            result = self.get_result()
                            
                            # Başarılı sonuç kontrolü
                            if result and result != "CAPTCHA_RETRY_NEEDED":
                                print(f"🎉 {get_text('bot_completed')}")
                                return True
                            else:
                                print(f"❌ {get_text('retry_captcha_error')}")
                                
                        except Exception as e:
                            print(f"❌ {get_text('result_get_error')}: {e}")
                            # Sonuç alma hatası durumunda da devam et
                            
                    except Exception as e:
                        print(f"❌ {get_text('retry_error')}: {e}")
                        
                    finally:
                        if self.driver:
                            try:
                                self.driver.quit()
                            except:
                                pass
                        time.sleep(3)
                        
                        # Her 5 domain denemesinde bir uzun bekleme
                        if config.UNLIMITED_CAPTCHA_RETRY and retry_attempt % 5 == 0:
                            print(f"⏳ {retry_attempt} {get_text('domain_attempts_completed')}, 10 {get_text('seconds_waiting')}...")
                            time.sleep(10)
                
                if not config.UNLIMITED_CAPTCHA_RETRY:
                    print(f"❌ {get_text('max_attempts_reached')}")
                    return False
                else:
                    print(f"❌ {get_text('unlimited_mode_failed')}")
                    return False
            
            print(f"🎉 {get_text('bot_completed')}")
            return True
            
        except Exception as e:
            print(f"❌ {get_text('bot_error')}: {e}")
            return False
            
        finally:
            # WebDriver'ı kapat
            if self.driver:
                print(f"🔄 {get_text('closing_webdriver')}")
                time.sleep(5)  # Sonuçları görmek için bekle
                self.driver.quit()

def main():
    """Ana fonksiyon"""
    print("=" * 60)
    print(f"🤖 {get_text('app_title')}")
    print("=" * 60)
    
    # Bot'u başlat
    bot = BTKBot()
    success = bot.run()
    
    if success:
        print(f"\n✅ {get_text('bot_success')}")
    else:
        print(f"\n❌ {get_text('bot_failed')}")

if __name__ == "__main__":
    main() 