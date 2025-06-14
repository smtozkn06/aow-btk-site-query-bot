#!/usr/bin/env python3
"""
Çok Dilli Destek Sistemi
BTK Site Sorgu Botu için Türkçe/İngilizce dil desteği
"""

import json
import os

class LanguageManager:
    def __init__(self):
        self.current_language = 'tr'  # Varsayılan Türkçe
        self.languages = {
            'tr': {
                # Ana Başlıklar
                'app_title': '🤖 Aow Software - BTK Site Sorgu Botu',
                'app_subtitle': 'Modern ve Hızlı Domain Kontrolü',
                
                # Sekmeler
                'tab_domain_test': '🔍 Domain Test',
                'tab_results': '📊 Sonuçlar',
                'tab_settings': '⚙️ Ayarlar',
                
                # Domain Test Sekmesi
                'domain_ip_test': '🌐 Domain/IP Test',
                'single_domain_test': 'Tek Domain Test:',
                'single_domain_placeholder': 'Örn: google.com',
                'bulk_domain_test': 'Toplu Domain Test (her satıra bir domain):',
                'load_from_file': '📁 Dosyadan Yükle',
                'save_file': '💾 Kaydet',
                'clear_list': '🗑️ Temizle',
                
                # Test Kontrolü
                'test_control': '⚙️ Test Kontrolü',
                'delay_between_domains': '⏱️ Domain arası bekleme (saniye):',
                'parallel_browsers': '🌐 Paralel tarayıcı sayısı (1-5):',
                'headless_mode': '🔕 Gizli mod (Headless)',
                'start_test': '🚀 Test Başlat',
                'stop_test': '⏹️ Durdur',
                
                # İlerleme
                'progress': '📊 İlerleme',
                'ready': 'Hazır',
                'test_logs': '📋 Test Logları',
                
                # Sonuçlar Sekmesi
                'test_summary': '📈 Test Özeti',
                'no_tests_yet': 'Henüz test yapılmadı.',
                'detailed_results': '📋 Detaylı Sonuçlar',
                'domain_ip': 'Domain/IP',
                'test_status': 'Test Durumu',
                'btk_decision': 'BTK Karar Sonucu',
                'test_time': 'Test Zamanı',
                'accessible': 'Erişilebilir',
                'blocked': 'Engellendi',
                
                # Ayarlar Sekmesi
                'bot_settings': '🤖 Bot Ayarları',
                'max_captcha_attempts': 'Maksimum CAPTCHA deneme sayısı:',
                'element_wait_time': 'Element bekleme süresi (saniye):',
                'save_settings': '💾 Ayarları Kaydet',
                'appearance_settings': '🎨 Görünüm Ayarları',
                'theme_mode': 'Tema Modu:',
                'language_settings': '🌍 Dil Ayarları',
                'select_language': 'Dil Seçin:',
                'theme_settings': '🎨 Görünüm Ayarları',
                'about': 'ℹ️ Hakkında',
                
                # Durum Çubuğu
                'status_ready': 'Hazır ✅',
                'status_testing': 'Test ediliyor...',
                'status_completed': 'Test tamamlandı',
                'status_stopped': 'Test durduruldu',
                'status_error': 'Hata',
                
                # Mesajlar ve Loglar
                'webdriver_started': 'WebDriver başarıyla başlatıldı',
                'webdriver_error': 'WebDriver başlatma hatası',
                'navigating_to': 'adresine gidiliyor...',
                'site_loaded': 'Site başarıyla yüklendi',
                'site_load_error': 'Site yükleme hatası',
                'domain_entered': 'başarıyla girildi',
                'domain_entry_error': 'Domain girme hatası',
                'searching_captcha': 'CAPTCHA görüntüsü aranıyor...',
                'captcha_found': 'CAPTCHA görüntüsü bulundu',
                'captcha_solved': 'CAPTCHA çözüldü',
                'captcha_entered': 'CAPTCHA başarıyla girildi',
                'captcha_failed': 'CAPTCHA metni okunamadı veya çok kısa',
                'captcha_error': 'CAPTCHA çözme hatası',
                'captcha_method_found': 'CAPTCHA yöntemi bulundu',
                'captcha_best_result': 'En iyi CAPTCHA sonucu',
                'form_submitted': 'Form başarıyla gönderildi',
                'form_submit_error': 'Form gönderme hatası',
                'bot_completed': 'Bot işlemi tamamlandı!',
                'bot_error': 'Bot çalıştırma hatası',
                'bot_starting': 'Aow Software -BTK Site Sorgu Botu başlatılıyor...',
                'bot_success': 'Bot başarıyla çalıştı!',
                'bot_failed': 'Bot çalışırken hata oluştu!',
                'closing_webdriver': 'WebDriver kapatılıyor...',
                
                # Test Mesajları
                'test_starting': 'için test başlatılıyor...',
                'bulk_test_starting': 'domain için test başlatılıyor...',
                'parallel_test_starting': 'domain için {} paralel tarayıcı ile test başlatılıyor...',
                'test_completed_successfully': 'Test başarıyla tamamlandı',
                'bulk_test_completed': 'Toplu test tamamlandı! {} domain test edildi.',
                'test_stopped_by_user': 'Test kullanıcı tarafından durduruldu',
                'unlimited_captcha_mode': 'Sınırsız CAPTCHA çözme modu aktif - doğru cevap gelene kadar deneyecek',
                'captcha_attempt': 'CAPTCHA çözme denemesi',
                'captcha_retry': 'CAPTCHA başarısız, sayfa yenileniyor...',
                'captcha_solved_attempt': 'CAPTCHA başarıyla çözüldü! (Deneme: {})',
                'max_attempts_reached': 'CAPTCHA çözülemedi, maksimum deneme sayısına ulaşıldı',
                'retrying_domain': 'Domain tekrar denemesi',
                'unlimited_mode': 'Sınırsız mod',
                'retry_captcha_solving': 'Tekrar deneme CAPTCHA çözme',
                'captcha_wrong_retrying': 'CAPTCHA yanlış çözüldü, tüm işlem tekrar deneniyor...',
                'retry_captcha_error': 'Tekrar denemede de CAPTCHA hatası',
                'retry_error': 'Tekrar deneme hatası',
                'attempts_completed': 'deneme tamamlandı',
                'seconds_waiting': 'saniye bekleniyor',
                'domain_attempts_completed': 'domain denemesi tamamlandı',
                'page_refreshing': 'Sayfa yenileniyor...',
                'captcha_could_not_solve': 'CAPTCHA çözülemedi',
                'unlimited_mode_failed': 'Sınırsız modda bile çözülemedi - sistem hatası olabilir',
                
                # BTK Sonuçları
                'btk_no_decision': 'BTK tarafından uygulanan bir karar bulunamadı',
                'btk_court_decision': 'MAHKEME KARARI MEVCUT',
                'btk_court_decision_detected': 'MAHKEME KARARI TESPİT EDİLDİ',
                'btk_result': 'SONUÇ',
                'result_not_found_analyzing': 'Karar sonucu bulunamadı, genel sayfa analizi yapılıyor',
                'general_page_analysis': 'genel sayfa analizi yapılıyor',
                'page_analysis': 'sayfa analizi yapılıyor',
                'analyzing': 'analiz yapılıyor',
                'decision_text_empty': 'Karar metni boş',
                'site_appears_blocked': 'Site engellenmiş görünüyor',
                'site_appears_accessible': 'Site erişilebilir görünüyor',
                'result_get_error': 'Sonuç alma hatası',
                'invalid_result_detected': 'Geçersiz sonuç tespit edildi',
                'result_div_not_found': 'Sonuç div\'i bulunamadı',
                'captcha_error_detected_in_page': 'Sayfada CAPTCHA hatası tespit edildi',
                'page_analysis_invalid': 'Sayfa analizi geçersiz',
                'page_source_error': 'Sayfa kaynak kodu hatası',
                
                # Dosya İşlemleri
                'select_domain_file': 'Domain Listesi Dosyası Seç',
                'text_files': 'Metin Dosyaları',
                'all_files': 'Tüm Dosyalar',
                'domains_loaded': 'domain yüklendi!',
                'file_read_error': 'Dosya okuma hatası',
                'save_domain_list': 'Domain Listesini Kaydet',
                'empty_domain_list': 'Kaydedilecek domain listesi boş!',
                'domain_list_saved': 'Domain listesi kaydedildi!',
                'file_save_error': 'Dosya kaydetme hatası',
                
                # Hata Mesajları
                'error_no_domains': 'Lütfen test edilecek en az bir domain/IP girin!',
                'error_invalid_parallel_count': 'Paralel tarayıcı sayısı 1-5 arasında olmalıdır!',
                'error_invalid_parallel_input': 'Geçerli bir paralel tarayıcı sayısı girin!',
                'error_settings_load': 'Ayarlar yüklenirken hata',
                'error_settings_save': 'Ayarlar kaydedilirken hata',
                'error_test': 'Test hatası',
                'error_domain_test': 'Domain test hatası',
                'error_parallel_test': 'Paralel test hatası',
                'error_result_capture': 'Sonuç yakalama hatası',
                
                # Onay Mesajları
                'confirm_exit': 'Test çalışıyor. Çıkmak istediğinizden emin misiniz?',
                'success': 'Başarılı',
                'error': 'Hata',
                'warning': 'Uyarı',
                'info': 'Bilgi',
                
                # Özet Bilgileri
                'total_tests': 'Toplam Test',
                'accessible_sites': 'Erişilebilir Site',
                'blocked_sites': 'Engellenen Site',
                'success_rate': 'Başarı Oranı',
                'last_update': 'Son Güncelleme',
                'completed': 'tamamlandı',
                
                # Hakkında Metni
                'about_text': '''Aow Software - BTK Site Sorgu Botu

Bu bot, BTK (Bilgi Teknolojileri ve İletişim Kurumu) site sorgu 
sistemini otomatik olarak kullanarak domain/IP adreslerinin 
engelli olup olmadığını kontrol eder.

✨ Yeni Özellikler:
• Modern CustomTkinter arayüzü
• Gelişmiş performans
• Daha iyi kullanıcı deneyimi
• Responsive tasarım
• Çok dilli destek (TR/EN)

🚀 Özellikler:
• Otomatik CAPTCHA çözme
• Tek ve toplu domain testi
• Renkli sonuç analizi
• Excel export desteği
• Paralel işleme

Geliştirici: Aow Software Team
Tarih: 2025'''
            },
            
            'en': {
                # Main Titles
                'app_title': '🤖 Aow Software - BTK Site Query Bot',
                'app_subtitle': 'Modern and Fast Domain Control',
                
                # Tabs
                'tab_domain_test': '🔍 Domain Test',
                'tab_results': '📊 Results',
                'tab_settings': '⚙️ Settings',
                
                # Domain Test Tab
                'domain_ip_test': '🌐 Domain/IP Test',
                'single_domain_test': 'Single Domain Test:',
                'single_domain_placeholder': 'e.g: google.com',
                'bulk_domain_test': 'Bulk Domain Test (one domain per line):',
                'load_from_file': '📁 Load from File',
                'save_file': '💾 Save',
                'clear_list': '🗑️ Clear',
                
                # Test Control
                'test_control': '⚙️ Test Control',
                'delay_between_domains': '⏱️ Delay between domains (seconds):',
                'parallel_browsers': '🌐 Number of parallel browsers (1-5):',
                'headless_mode': '🔕 Headless mode',
                'start_test': '🚀 Start Test',
                'stop_test': '⏹️ Stop',
                
                # Progress
                'progress': '📊 Progress',
                'ready': 'Ready',
                'test_logs': '📋 Test Logs',
                
                # Results Tab
                'test_summary': '📈 Test Summary',
                'no_tests_yet': 'No tests performed yet.',
                'detailed_results': '📋 Detailed Results',
                'domain_ip': 'Domain/IP',
                'test_status': 'Test Status',
                'btk_decision': 'BTK Decision Result',
                'test_time': 'Test Time',
                'accessible': 'Accessible',
                'blocked': 'Blocked',
                
                # Settings Tab
                'bot_settings': '🤖 Bot Settings',
                'max_captcha_attempts': 'Maximum CAPTCHA attempts:',
                'element_wait_time': 'Element wait time (seconds):',
                'save_settings': '💾 Save Settings',
                'appearance_settings': '🎨 Appearance Settings',
                'theme_mode': 'Theme Mode:',
                'language_settings': '🌍 Language Settings',
                'select_language': 'Select Language:',
                'theme_settings': '🎨 Appearance Settings',
                'about': 'ℹ️ About',
                
                # Status Bar
                'status_ready': 'Ready ✅',
                'status_testing': 'Testing...',
                'status_completed': 'Test completed',
                'status_stopped': 'Test stopped',
                'status_error': 'Error',
                
                # Messages and Logs
                'webdriver_started': 'WebDriver successfully started',
                'webdriver_error': 'WebDriver startup error',
                'navigating_to': 'Navigating to',
                'site_loaded': 'Site loaded successfully',
                'site_load_error': 'Site loading error',
                'domain_entered': 'successfully entered',
                'domain_entry_error': 'Domain entry error',
                'searching_captcha': 'Searching for CAPTCHA image...',
                'captcha_found': 'CAPTCHA image found',
                'captcha_solved': 'CAPTCHA solved',
                'captcha_entered': 'CAPTCHA entered successfully',
                'captcha_failed': 'CAPTCHA text could not be read or too short',
                'captcha_error': 'CAPTCHA solving error',
                'captcha_method_found': 'CAPTCHA method found',
                'captcha_best_result': 'Best CAPTCHA result',
                'form_submitted': 'Form submitted successfully',
                'form_submit_error': 'Form submission error',
                'bot_completed': 'Bot operation completed!',
                'bot_error': 'Bot execution error',
                'bot_starting': 'Aow Software -BTK Site Query Bot starting...',
                'bot_success': 'Bot ran successfully!',
                'bot_failed': 'Bot encountered an error while running!',
                'closing_webdriver': 'Closing WebDriver...',
                
                # Test Messages
                'test_starting': 'Starting test for',
                'bulk_test_starting': 'Starting test for {} domains...',
                'parallel_test_starting': 'Starting test for {} domains with {} parallel browsers...',
                'test_completed_successfully': 'Test completed successfully',
                'bulk_test_completed': 'Bulk test completed! {} domains tested.',
                'test_stopped_by_user': 'Test stopped by user',
                'unlimited_captcha_mode': 'Unlimited CAPTCHA solving mode active - will try until correct answer',
                'captcha_attempt': 'CAPTCHA solving attempt',
                'captcha_retry': 'CAPTCHA failed, refreshing page...',
                'captcha_solved_attempt': 'CAPTCHA solved successfully! (Attempt: {})',
                'max_attempts_reached': 'CAPTCHA could not be solved, maximum attempts reached',
                'retrying_domain': 'Domain retry attempt',
                'unlimited_mode': 'Unlimited mode',
                'retry_captcha_solving': 'Retry CAPTCHA solving',
                'captcha_wrong_retrying': 'CAPTCHA solved incorrectly, retrying entire process...',
                'retry_captcha_error': 'CAPTCHA error in retry attempt',
                'retry_error': 'Retry error',
                'attempts_completed': 'attempts completed',
                'seconds_waiting': 'seconds waiting',
                'domain_attempts_completed': 'domain attempts completed',
                'page_refreshing': 'Refreshing page...',
                'captcha_could_not_solve': 'CAPTCHA could not be solved',
                'unlimited_mode_failed': 'Could not solve even in unlimited mode - system error possible',
                
                # BTK Results
                'btk_no_decision': 'No decision found by BTK',
                'btk_court_decision': 'COURT DECISION AVAILABLE',
                'btk_court_decision_detected': 'COURT DECISION DETECTED',
                'btk_result': 'RESULT',
                'result_not_found_analyzing': 'Decision result not found, performing general page analysis',
                'general_page_analysis': 'performing general page analysis',
                'page_analysis': 'page analysis',
                'analyzing': 'analyzing',
                'decision_text_empty': 'Decision text is empty',
                'site_appears_blocked': 'Site appears to be blocked',
                'site_appears_accessible': 'Site appears to be accessible',
                'result_get_error': 'Result retrieval error',
                'invalid_result_detected': 'Invalid result detected',
                'result_div_not_found': 'Result div not found',
                'captcha_error_detected_in_page': 'CAPTCHA error detected in page',
                'page_analysis_invalid': 'Page analysis invalid',
                'page_source_error': 'Page source error',
                
                # File Operations
                'select_domain_file': 'Select Domain List File',
                'text_files': 'Text Files',
                'all_files': 'All Files',
                'domains_loaded': 'domains loaded!',
                'file_read_error': 'File reading error',
                'save_domain_list': 'Save Domain List',
                'empty_domain_list': 'Domain list to save is empty!',
                'domain_list_saved': 'Domain list saved!',
                'file_save_error': 'File saving error',
                
                # Error Messages
                'error_no_domains': 'Please enter at least one domain/IP to test!',
                'error_invalid_parallel_count': 'Number of parallel browsers must be between 1-5!',
                'error_invalid_parallel_input': 'Enter a valid number of parallel browsers!',
                'error_settings_load': 'Error loading settings',
                'error_settings_save': 'Error saving settings',
                'error_test': 'Test error',
                'error_domain_test': 'Domain test error',
                'error_parallel_test': 'Parallel test error',
                'error_result_capture': 'Result capture error',
                
                # Confirmation Messages
                'confirm_exit': 'Test is running. Are you sure you want to exit?',
                'success': 'Success',
                'error': 'Error',
                'warning': 'Warning',
                'info': 'Info',
                
                # Summary Information
                'total_tests': 'Total Tests',
                'accessible_sites': 'Accessible Sites',
                'blocked_sites': 'Blocked Sites',
                'success_rate': 'Success Rate',
                'last_update': 'Last Update',
                'completed': 'completed',
                
                # About Text
                'about_text': '''Aow Software - BTK Site Query Bot

This bot automatically uses the BTK (Information and Communication 
Technologies Authority) site query system to check whether 
domain/IP addresses are blocked.

✨ New Features:
• Modern CustomTkinter interface
• Enhanced performance
• Better user experience
• Responsive design
• Multi-language support (TR/EN)

🚀 Features:
• Automatic CAPTCHA solving
• Single and bulk domain testing
• Colorful result analysis
• Excel export support
• Parallel processing

Developer: Aow Software Team
Date: 2025'''
            }
        }
    
    def set_language(self, lang_code):
        """Dil ayarla"""
        if lang_code in self.languages:
            self.current_language = lang_code
            self.save_language_preference()
    
    def get_text(self, key):
        """Metni al"""
        return self.languages.get(self.current_language, {}).get(key, key)
    
    def get_current_language(self):
        """Mevcut dili al"""
        return self.current_language
    
    def get_available_languages(self):
        """Mevcut dilleri al"""
        return {
            'tr': 'Türkçe',
            'en': 'English'
        }
    
    def load_language_preference(self):
        """Dil tercihini yükle"""
        try:
            if os.path.exists('bot_settings.json'):
                with open('bot_settings.json', 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.current_language = settings.get('language', 'tr')
        except Exception:
            self.current_language = 'tr'
    
    def save_language_preference(self):
        """Dil tercihini kaydet"""
        try:
            settings = {}
            if os.path.exists('bot_settings.json'):
                with open('bot_settings.json', 'r', encoding='utf-8') as f:
                    settings = json.load(f)
            
            settings['language'] = self.current_language
            
            with open('bot_settings.json', 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Language preference save error: {e}")

# Global dil yöneticisi
lang_manager = LanguageManager()

def get_text(key):
    """Kısayol fonksiyon"""
    return lang_manager.get_text(key)

def set_language(lang_code):
    """Dil ayarlama kısayolu"""
    lang_manager.set_language(lang_code)

def get_current_language():
    """Mevcut dil kısayolu"""
    return lang_manager.get_current_language()

def get_available_languages():
    """Mevcut diller kısayolu"""
    return lang_manager.get_available_languages() 