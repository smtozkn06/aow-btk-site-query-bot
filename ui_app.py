#!/usr/bin/env python3
"""
Aow Software - BTK Site Sorgu Botu
CustomTkinter ile modern arayüz ve toplu domain test özelliği
Çok dilli destek (Türkçe/İngilizce)
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
import tkinter as tk
from tkinter import ttk
import threading
import queue
import time
from datetime import datetime
import json
import os
from btk_bot import BTKBot
import config
import re
import unicodedata
from languages import lang_manager, get_text, set_language, get_current_language, get_available_languages

# Modern tema ayarları
ctk.set_appearance_mode("dark")  # "light" veya "dark"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

class LogCapture:
    """Log yakalama sınıfı"""
    def __init__(self, callback):
        self.callback = callback
    
    def write(self, text):
        if text.strip():
            self.callback(text.strip())
    
    def flush(self):
        pass

class LanguageSelectionDialog:
    """Dil seçimi dialog'u"""
    def __init__(self, parent):
        self.result = None
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Language / Dil Seçimi")
        self.dialog.geometry("450x400")
        self.dialog.resizable(False, False)
        
        # Dialog'u merkeze al
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Dialog'u ekranın merkezine yerleştir
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (400 // 2)
        self.dialog.geometry(f"450x400+{x}+{y}")
        
        # Ana frame
        main_frame = ctk.CTkFrame(self.dialog)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Başlık
        title_label = ctk.CTkLabel(main_frame, 
                                  text="🌍 Select Language / Dil Seçin", 
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(20, 30))
        
        # Açıklama
        desc_label = ctk.CTkLabel(main_frame, 
                                 text="Please select your preferred language\nLütfen tercih ettiğiniz dili seçin", 
                                 font=ctk.CTkFont(size=14))
        desc_label.pack(pady=(0, 30))
        
        # Dil butonları
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=20, fill='x')
        
        # Türkçe butonu
        tr_button = ctk.CTkButton(button_frame, 
                                 text="🇹🇷 Türkçe", 
                                 font=ctk.CTkFont(size=16, weight="bold"),
                                 width=200, height=60,
                                 command=lambda: self.select_language('tr'))
        tr_button.pack(pady=15, padx=20)
        
        # İngilizce butonu
        en_button = ctk.CTkButton(button_frame, 
                                 text="🇺🇸 English", 
                                 font=ctk.CTkFont(size=16, weight="bold"),
                                 width=200, height=60,
                                 command=lambda: self.select_language('en'))
        en_button.pack(pady=15, padx=20)
        
        # Alt bilgi
        info_label = ctk.CTkLabel(main_frame, 
                                 text="You can change this later in settings\nBunu daha sonra ayarlardan değiştirebilirsiniz", 
                                 font=ctk.CTkFont(size=11),
                                 text_color="gray")
        info_label.pack(pady=(30, 10))
    
    def select_language(self, lang_code):
        """Dil seç ve dialog'u kapat"""
        self.result = lang_code
        self.dialog.destroy()
    
    def show(self):
        """Dialog'u göster ve sonucu döndür"""
        self.dialog.wait_window()
        return self.result

class BTKBotGUI:
    def __init__(self, root):
        self.root = root
        
        # Dil tercihini yükle
        lang_manager.load_language_preference()
        
        # Eğer dil tercihi yoksa, dil seçimi dialog'unu göster
        show_language_dialog = True
        try:
            if os.path.exists('bot_settings.json'):
                with open('bot_settings.json', 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    if 'language' in settings:
                        show_language_dialog = False
        except:
            pass
        
        if show_language_dialog:
            dialog = LanguageSelectionDialog(root)
            selected_lang = dialog.show()
            if selected_lang:
                set_language(selected_lang)
            else:
                set_language('tr')  # Varsayılan Türkçe
        
        # Pencere ayarları
        self.root.title(get_text('app_title'))
        self.root.geometry("1200x800")
        
        # CustomTkinter tema ayarları
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Ayarları yükle
        self.load_settings()
        
        # Değişkenler
        self.is_running = False
        self.current_bot = None
        self.queue = queue.Queue()
        self.test_results = []
        self.current_domain_result = {}
        
        # GUI'yi oluştur
        self.create_widgets()
        
        # Queue kontrolü için timer
        self.root.after(100, self.check_queue)
    
    def load_settings(self):
        """Ayarları JSON dosyasından yükle"""
        try:
            if os.path.exists('bot_settings.json'):
                with open('bot_settings.json', 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                
                # Ayarları güncelle
                config.HEADLESS_MODE = settings.get('headless_mode', True)
                config.MAX_CAPTCHA_ATTEMPTS = settings.get('max_captcha_attempts', 5)
                config.WAIT_TIMEOUT = settings.get('wait_timeout', 30)
                
                # Domain bilgilerini kaydet
                self.settings = settings
            else:
                # Varsayılan ayarlar
                self.settings = {
                    'headless_mode': True,
                    'max_captcha_attempts': 5,
                    'wait_timeout': 30,
                    'default_delay': 3,
                    'parallel_browsers': 1,
                    'filter_captcha_logs': True,
                    'single_domain': 'example.com',
                    'bulk_domains': 'google.com\nfacebook.com\ntwitter.com\ngithub.com',
                    'language': get_current_language()
                }
                self.save_settings()
        except Exception as e:
            print(f"{get_text('error_settings_load')}: {e}")
            # Varsayılan ayarlar
            self.settings = {
                'headless_mode': True,
                'max_captcha_attempts': 5,
                'wait_timeout': 30,
                'default_delay': 3,
                'parallel_browsers': 1,
                'filter_captcha_logs': True,
                'single_domain': 'example.com',
                'bulk_domains': 'google.com\nfacebook.com\ntwitter.com\ngithub.com',
                'language': get_current_language()
            }
    
    def save_settings(self):
        """Ayarları JSON dosyasına kaydet"""
        try:
            # GUI'den güncel değerleri al
            self.settings.update({
                'headless_mode': self.single_headless_var.get() if hasattr(self, 'single_headless_var') else True,
                'max_captcha_attempts': int(self.captcha_attempts_var.get()) if hasattr(self, 'captcha_attempts_var') else 5,
                'wait_timeout': int(self.timeout_var.get()) if hasattr(self, 'timeout_var') else 30,
                'default_delay': int(self.delay_var.get()) if hasattr(self, 'delay_var') else 3,
                'parallel_browsers': int(self.parallel_browsers_var.get()) if hasattr(self, 'parallel_browsers_var') else 1,
                'filter_captcha_logs': True,
                'single_domain': self.single_domain_var.get() if hasattr(self, 'single_domain_var') else 'example.com',
                'bulk_domains': self.bulk_domains_text.get('1.0', 'end').strip() if hasattr(self, 'bulk_domains_text') else 'google.com\nfacebook.com\ntwitter.com\ngithub.com',
                'language': get_current_language()
            })
            
            with open('bot_settings.json', 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"{get_text('error_settings_save')}: {e}")
    
    def refresh_ui_language(self):
        """UI dilini yenile"""
        # Pencere başlığını güncelle
        self.root.title(get_text('app_title'))
        
        # Tüm widget'ları yeniden oluştur
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.create_widgets()
    
    def create_widgets(self):
        """Modern widget'ları oluştur"""
        # Ana başlık
        header_frame = ctk.CTkFrame(self.root, height=80, corner_radius=0)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        header_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_container.pack(expand=True, fill='both', padx=20, pady=20)
        
        title_label = ctk.CTkLabel(header_container, text=get_text('app_title'), 
                                  font=ctk.CTkFont(size=28, weight="bold"))
        title_label.pack(side='left')
        
        subtitle_label = ctk.CTkLabel(header_container, text=get_text('app_subtitle'), 
                                     font=ctk.CTkFont(size=14))
        subtitle_label.pack(side='left', padx=(10, 0))
        
        # Ana container
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Tab view oluştur
        self.tabview = ctk.CTkTabview(main_frame, width=1000, height=600)
        self.tabview.pack(fill='both', expand=True)
        
        # Sekmeler
        self.create_test_tab()
        self.create_results_tab()
        self.create_settings_tab()
        
        # Durum çubuğu
        self.create_status_bar()
    
    def create_test_tab(self):
        """Birleşik test sekmesi - tek ve toplu domain testi"""
        tab = self.tabview.add(get_text('tab_domain_test'))
        
        # Ana layout - sol panel ve sağ panel
        content_frame = ctk.CTkFrame(tab, fg_color="transparent")
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Sol panel - Domain giriş ve kontrol paneli
        left_panel = ctk.CTkFrame(content_frame, width=400)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Domain giriş bölümü
        domain_frame = ctk.CTkFrame(left_panel)
        domain_frame.pack(fill='x', pady=(0, 20))
        
        domain_label = ctk.CTkLabel(domain_frame, text=get_text('domain_ip_test'), 
                                   font=ctk.CTkFont(size=18, weight="bold"))
        domain_label.pack(pady=(20, 15))
        
        # Tek domain test
        single_frame = ctk.CTkFrame(domain_frame, fg_color="transparent")
        single_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        single_label = ctk.CTkLabel(single_frame, text=get_text('single_domain_test'))
        single_label.pack(anchor='w', pady=(0, 5))
        
        # Kayıtlı tek domain'i yükle
        saved_single_domain = self.settings.get('single_domain', config.DOMAIN_TO_CHECK)
        self.single_domain_var = ctk.StringVar(value=saved_single_domain)
        self.single_domain_entry = ctk.CTkEntry(single_frame, textvariable=self.single_domain_var,
                                               placeholder_text=get_text('single_domain_placeholder'),
                                               height=40, font=ctk.CTkFont(size=14))
        self.single_domain_entry.pack(fill='x', pady=(0, 10))
        
        # Toplu domain test
        bulk_label = ctk.CTkLabel(single_frame, text=get_text('bulk_domain_test'))
        bulk_label.pack(anchor='w', pady=(10, 5))
        
        self.bulk_domains_text = ctk.CTkTextbox(single_frame, height=150, 
                                               font=ctk.CTkFont(size=14))
        self.bulk_domains_text.pack(fill='x', pady=(0, 10))
        
        # Kayıtlı toplu domain'leri yükle
        saved_bulk_domains = self.settings.get('bulk_domains', 'google.com\nfacebook.com\ntwitter.com\ngithub.com')
        self.bulk_domains_text.delete('1.0', 'end')
        self.bulk_domains_text.insert('1.0', saved_bulk_domains)
        
        # Domain değişikliklerini otomatik kaydet
        self.single_domain_var.trace('w', lambda *args: self.save_settings())
        self.bulk_domains_text.bind('<KeyRelease>', lambda e: self.save_settings())
        
        # Dosya işlemleri butonları
        file_btn_frame = ctk.CTkFrame(single_frame, fg_color="transparent")
        file_btn_frame.pack(fill='x', pady=(0, 20))
        
        load_btn = ctk.CTkButton(file_btn_frame, text=get_text('load_from_file'), 
                                command=self.load_domains_from_file,
                                width=120, height=35)
        load_btn.pack(side='left', padx=(0, 5))
        
        save_btn = ctk.CTkButton(file_btn_frame, text=get_text('save_file'), 
                                command=self.save_domains_to_file,
                                width=100, height=35)
        save_btn.pack(side='left', padx=(0, 5))
        
        clear_btn = ctk.CTkButton(file_btn_frame, text=get_text('clear_list'), 
                                 command=lambda: self.bulk_domains_text.delete('1.0', 'end'),
                                 width=100, height=35)
        clear_btn.pack(side='left')
        
        # Test kontrol paneli
        control_frame = ctk.CTkFrame(left_panel)
        control_frame.pack(fill='x', pady=(0, 20))
        
        control_label = ctk.CTkLabel(control_frame, text=get_text('test_control'), 
                                    font=ctk.CTkFont(size=18, weight="bold"))
        control_label.pack(pady=(20, 15))
        
        # Test ayarları
        settings_container = ctk.CTkFrame(control_frame, fg_color="transparent")
        settings_container.pack(fill='x', padx=20, pady=(0, 15))
        
        # Domain arası bekleme
        delay_frame = ctk.CTkFrame(settings_container, fg_color="transparent")
        delay_frame.pack(fill='x', pady=(0, 10))
        
        delay_label = ctk.CTkLabel(delay_frame, text=get_text('delay_between_domains'))
        delay_label.pack(anchor='w', pady=(0, 5))
        
        self.delay_var = ctk.StringVar(value="3")
        delay_entry = ctk.CTkEntry(delay_frame, textvariable=self.delay_var, 
                                  width=100, height=35)
        delay_entry.pack(anchor='w')
        
        # Paralel tarayıcı ayarı
        parallel_frame = ctk.CTkFrame(settings_container, fg_color="transparent")
        parallel_frame.pack(fill='x', pady=(0, 10))
        
        parallel_label = ctk.CTkLabel(parallel_frame, text=get_text('parallel_browsers'))
        parallel_label.pack(anchor='w', pady=(0, 5))
        
        self.parallel_browsers_var = ctk.StringVar(value="1")
        parallel_entry = ctk.CTkEntry(parallel_frame, textvariable=self.parallel_browsers_var, 
                                     width=100, height=35)
        parallel_entry.pack(anchor='w')
        
        # Headless mode
        self.single_headless_var = ctk.BooleanVar(value=config.HEADLESS_MODE)
        headless_switch = ctk.CTkSwitch(settings_container, text=get_text('headless_mode'), 
                                       variable=self.single_headless_var,
                                       font=ctk.CTkFont(size=14))
        headless_switch.pack(anchor='w', pady=(0, 15))
        
        # Test butonları
        button_container = ctk.CTkFrame(control_frame, fg_color="transparent")
        button_container.pack(fill='x', padx=20, pady=(0, 20))
        
        self.test_btn = ctk.CTkButton(button_container, text=get_text('start_test'), 
                                     command=self.start_test,
                                     font=ctk.CTkFont(size=16, weight="bold"),
                                     height=50)
        self.test_btn.pack(fill='x', pady=(0, 10))
        
        self.stop_btn = ctk.CTkButton(button_container, text=get_text('stop_test'), 
                                     command=self.stop_test,
                                     font=ctk.CTkFont(size=16, weight="bold"),
                                     height=50, state='disabled')
        self.stop_btn.pack(fill='x')
        
        # İlerleme paneli
        progress_frame = ctk.CTkFrame(left_panel)
        progress_frame.pack(fill='x')
        
        progress_label = ctk.CTkLabel(progress_frame, text=get_text('progress'), 
                                     font=ctk.CTkFont(size=18, weight="bold"))
        progress_label.pack(pady=(20, 15))
        
        progress_container = ctk.CTkFrame(progress_frame, fg_color="transparent")
        progress_container.pack(fill='x', padx=20, pady=(0, 20))
        
        self.progress_var = ctk.StringVar(value=get_text('ready'))
        progress_status = ctk.CTkLabel(progress_container, textvariable=self.progress_var,
                                      font=ctk.CTkFont(size=14))
        progress_status.pack(anchor='w', pady=(0, 10))
        
        self.progress_bar = ctk.CTkProgressBar(progress_container, height=20)
        self.progress_bar.pack(fill='x')
        self.progress_bar.set(0)
        
        # Sağ panel - Test logları
        right_panel = ctk.CTkFrame(content_frame)
        right_panel.pack(side='right', fill='both', expand=True)
        
        log_label = ctk.CTkLabel(right_panel, text=get_text('test_logs'), 
                                font=ctk.CTkFont(size=18, weight="bold"))
        log_label.pack(pady=(20, 15))
        
        # Log text widget
        self.log_text = ctk.CTkTextbox(right_panel, font=ctk.CTkFont(family="Courier", size=12))
        self.log_text.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Log renklerini ayarla
        self.setup_log_colors(self.log_text)
    
    def create_results_tab(self):
        """Modern sonuçlar sekmesi"""
        tab = self.tabview.add(get_text('tab_results'))
        
        # Ana container
        content_frame = ctk.CTkFrame(tab, fg_color="transparent")
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Sonuç özeti
        summary_frame = ctk.CTkFrame(content_frame)
        summary_frame.pack(fill='x', pady=(0, 20))
        
        summary_label = ctk.CTkLabel(summary_frame, text=get_text('test_summary'), 
                                    font=ctk.CTkFont(size=18, weight="bold"))
        summary_label.pack(pady=(20, 15))
        
        self.summary_text = ctk.CTkLabel(summary_frame, text=get_text('no_tests_yet'), 
                                        font=ctk.CTkFont(size=14), justify='left')
        self.summary_text.pack(padx=20, pady=(0, 20), anchor='w')
        
        # Detaylı sonuçlar
        details_frame = ctk.CTkFrame(content_frame)
        details_frame.pack(fill='both', expand=True)
        
        details_label = ctk.CTkLabel(details_frame, text=get_text('detailed_results'), 
                                    font=ctk.CTkFont(size=18, weight="bold"))
        details_label.pack(pady=(20, 15))
        
        # TreeView için wrapper frame (tema uyumluluğu için)
        self.tree_container = tk.Frame(details_frame, bg='#212121')
        self.tree_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Treeview oluştur
        columns = ('Domain', 'Status', 'Result', 'Time')
        self.results_tree = ttk.Treeview(self.tree_container, columns=columns, show='headings', height=12)
        
        # TreeView stilini ayarla
        style = ttk.Style()
        # Font ayarları
        default_font = ('Segoe UI', 11)  # Windows için varsayılan font
        heading_font = ('Segoe UI', 12, 'bold')
        
        if ctk.get_appearance_mode() == "dark":
            style.configure("Treeview", 
                          background='#2b2b2b',
                          foreground='white',
                          fieldbackground='#2b2b2b',
                          font=default_font,
                          rowheight=40)  # Satır yüksekliği
            style.configure("Treeview.Heading",
                          background='#404040',
                          foreground='white',
                          font=heading_font,
                          padding=(10, 5))  # Başlık padding'i
            # Başarılı/Başarısız renkleri - yazı rengi siyah
            self.results_tree.tag_configure('success_row', background='#1b5e20', foreground='black')
            self.results_tree.tag_configure('error_row', background='#b71c1c', foreground='black')
        else:
            style.configure("Treeview", 
                          background='white',
                          foreground='black',
                          fieldbackground='white',
                          font=default_font,
                          rowheight=40)  # Satır yüksekliği
            style.configure("Treeview.Heading",
                          background='#e1e1e1',
                          foreground='black',
                          font=heading_font,
                          padding=(10, 5))  # Başlık padding'i
            # Başarılı/Başarısız renkleri - yazı rengi siyah
            self.results_tree.tag_configure('success_row', background='#c8e6c9', foreground='black')
            self.results_tree.tag_configure('error_row', background='#ffcdd2', foreground='black')
        
        # Başlıkları ayarla
        self.results_tree.heading('Domain', text=get_text('domain_ip'))
        self.results_tree.heading('Status', text=get_text('test_status'))
        self.results_tree.heading('Result', text=get_text('btk_decision'))
        self.results_tree.heading('Time', text=get_text('test_time'))
        
        # Sütun genişlikleri ve minimum genişlikler
        self.results_tree.column('Domain', width=250, minwidth=150, stretch=True)
        self.results_tree.column('Status', width=120, minwidth=100, stretch=False)
        self.results_tree.column('Result', width=400, minwidth=200, stretch=True)
        self.results_tree.column('Time', width=160, minwidth=120, stretch=False)
        
        # TreeView tag'lerini yapılandır
        self.results_tree.tag_configure('accessible', foreground='#4CAF50')
        self.results_tree.tag_configure('blocked', foreground='#F44336')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tree_container, orient='vertical', command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        # Widget'ları yerleştir
        self.results_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def create_settings_tab(self):
        """Modern ayarlar sekmesi"""
        tab = self.tabview.add(get_text('tab_settings'))
        
        # Ana ayarlar paneli
        settings_frame = ctk.CTkScrollableFrame(tab)
        settings_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Bot ayarları
        bot_frame = ctk.CTkFrame(settings_frame)
        bot_frame.pack(fill='x', pady=(0, 20))
        
        bot_label = ctk.CTkLabel(bot_frame, text=get_text('bot_settings'), 
                                font=ctk.CTkFont(size=18, weight="bold"))
        bot_label.pack(pady=(20, 15))
        
        # CAPTCHA ayarları
        captcha_frame = ctk.CTkFrame(bot_frame, fg_color="transparent")
        captcha_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        captcha_label = ctk.CTkLabel(captcha_frame, text=get_text('max_captcha_attempts'))
        captcha_label.pack(anchor='w', pady=(0, 5))
        
        self.captcha_attempts_var = ctk.StringVar(value=str(config.MAX_CAPTCHA_ATTEMPTS))
        captcha_entry = ctk.CTkEntry(captcha_frame, textvariable=self.captcha_attempts_var, 
                                    width=100, height=35)
        captcha_entry.pack(anchor='w')
        
        # Timeout ayarı
        timeout_frame = ctk.CTkFrame(bot_frame, fg_color="transparent")
        timeout_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        timeout_label = ctk.CTkLabel(timeout_frame, text=get_text('element_wait_time'))
        timeout_label.pack(anchor='w', pady=(0, 5))
        
        self.timeout_var = ctk.StringVar(value=str(config.WAIT_TIMEOUT))
        timeout_entry = ctk.CTkEntry(timeout_frame, textvariable=self.timeout_var, 
                                    width=100, height=35)
        timeout_entry.pack(anchor='w')
        
        # Ayarları kaydet
        save_settings_btn = ctk.CTkButton(bot_frame, text=get_text('save_settings'), 
                                         command=self.save_settings,
                                         font=ctk.CTkFont(size=14, weight="bold"),
                                         height=40)
        save_settings_btn.pack(pady=(0, 20))
        
        # Tema ayarları
        theme_frame = ctk.CTkFrame(settings_frame)
        theme_frame.pack(fill='x', pady=(0, 20))
        
        theme_label = ctk.CTkLabel(theme_frame, text=get_text('theme_settings'), 
                                  font=ctk.CTkFont(size=18, weight="bold"))
        theme_label.pack(pady=(20, 15))
        
        appearance_frame = ctk.CTkFrame(theme_frame, fg_color="transparent")
        appearance_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        appearance_label = ctk.CTkLabel(appearance_frame, text=get_text('theme_mode'))
        appearance_label.pack(anchor='w', pady=(0, 5))
        
        self.appearance_var = ctk.StringVar(value="dark")
        appearance_menu = ctk.CTkOptionMenu(appearance_frame, values=["light", "dark", "system"],
                                           variable=self.appearance_var,
                                           command=self.change_appearance_mode)
        appearance_menu.pack(anchor='w', pady=(0, 20))
        
        # Dil ayarları
        language_frame = ctk.CTkFrame(settings_frame)
        language_frame.pack(fill='x', pady=(0, 20))
        
        language_label = ctk.CTkLabel(language_frame, text=get_text('language_settings'), 
                                     font=ctk.CTkFont(size=18, weight="bold"))
        language_label.pack(pady=(20, 15))
        
        lang_selection_frame = ctk.CTkFrame(language_frame, fg_color="transparent")
        lang_selection_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        lang_selection_label = ctk.CTkLabel(lang_selection_frame, text=get_text('select_language'))
        lang_selection_label.pack(anchor='w', pady=(0, 5))
        
        # Mevcut dil seçenekleri
        available_langs = get_available_languages()
        lang_values = list(available_langs.values())
        current_lang_display = available_langs[get_current_language()]
        
        self.language_var = ctk.StringVar(value=current_lang_display)
        language_menu = ctk.CTkOptionMenu(lang_selection_frame, 
                                         values=lang_values,
                                         variable=self.language_var,
                                         command=self.change_language)
        language_menu.pack(anchor='w', pady=(0, 20))
        
        # Hakkında
        about_frame = ctk.CTkFrame(settings_frame)
        about_frame.pack(fill='x')
        
        about_label = ctk.CTkLabel(about_frame, text=get_text('about'), 
                                  font=ctk.CTkFont(size=18, weight="bold"))
        about_label.pack(pady=(20, 15))
        
        about_text = f"""{get_text('about_text')}

🚀 Özellikler:
• Otomatik CAPTCHA çözme
• Tek ve toplu domain testi
• Renkli sonuç analizi
• Excel export desteği

Geliştirici: Aow Software Team
Tarih: 2025"""
        
        about_text_widget = ctk.CTkLabel(about_frame, text=about_text, justify='left', 
                                        font=ctk.CTkFont(size=12))
        about_text_widget.pack(anchor='w', padx=20, pady=(0, 20))
    
    def create_status_bar(self):
        """Modern durum çubuğu"""
        self.status_frame = ctk.CTkFrame(self.root, height=50, corner_radius=0)
        self.status_frame.pack(fill='x', side='bottom')
        self.status_frame.pack_propagate(False)
        
        status_container = ctk.CTkFrame(self.status_frame, fg_color="transparent")
        status_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Durum metni
        self.status_label = ctk.CTkLabel(status_container, text=get_text('ready'), 
                                        font=ctk.CTkFont(size=12, weight="bold"))
        self.status_label.pack(side='left')
        
        # Saat
        self.time_label = ctk.CTkLabel(status_container, font=ctk.CTkFont(size=12))
        self.time_label.pack(side='right')
        self.update_time()
    
    def change_language(self, selected_language: str):
        """Dil değiştir"""
        # Seçilen dili kod'a çevir
        available_langs = get_available_languages()
        lang_code = None
        for code, name in available_langs.items():
            if name == selected_language:
                lang_code = code
                break
        
        if lang_code and lang_code != get_current_language():
            set_language(lang_code)
            self.save_settings()
            
            # UI'yi yenile
            self.refresh_ui_language()
    
    def change_appearance_mode(self, new_appearance_mode: str):
        """Tema modunu değiştir"""
        ctk.set_appearance_mode(new_appearance_mode)
        
        # TreeView stilini güncelle
        if hasattr(self, 'tree_container'):
            style = ttk.Style()
            # Font ayarları
            default_font = ('Segoe UI', 11)
            heading_font = ('Segoe UI', 12, 'bold')
            
            if new_appearance_mode == "dark":
                self.tree_container.configure(bg='#212121')
                style.configure('Treeview', 
                               background='#2b2b2b',
                               foreground='white',
                               fieldbackground='#2b2b2b',
                               font=default_font,
                               rowheight=40)
                style.configure('Treeview.Heading',
                               background='#404040',
                               foreground='white',
                               font=heading_font,
                               padding=(10, 5))
                # Başarılı/Başarısız renkleri - yazı rengi siyah
                self.results_tree.tag_configure('success_row', background='#1b5e20', foreground='black')
                self.results_tree.tag_configure('error_row', background='#b71c1c', foreground='black')
            else:  # light mode
                self.tree_container.configure(bg='#f0f0f0')
                style.configure('Treeview', 
                               background='white',
                               foreground='black',
                               fieldbackground='white',
                               font=default_font,
                               rowheight=40)
                style.configure('Treeview.Heading',
                               background='#e1e1e1',
                               foreground='black',
                               font=heading_font,
                               padding=(10, 5))
                # Başarılı/Başarısız renkleri - yazı rengi siyah
                self.results_tree.tag_configure('success_row', background='#c8e6c9', foreground='black')
                self.results_tree.tag_configure('error_row', background='#ffcdd2', foreground='black')
    
    def update_time(self):
        """Saati güncelle"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=f"🕐 {current_time}")
        self.root.after(1000, self.update_time)
    
    def setup_log_colors(self, textbox):
        """Log widget'ı için renk tag'lerini ayarla"""
        # CTkTextbox'ın içindeki tkinter Text widget'ına erişim
        text_widget = textbox._textbox
        
        # Renk tag'lerini tanımla
        text_widget.tag_configure("success", foreground="#4CAF50", font=("Courier", 12, "bold"))
        text_widget.tag_configure("error", foreground="#F44336", font=("Courier", 12, "bold"))
        text_widget.tag_configure("warning", foreground="#FF9800", font=("Courier", 12, "bold"))
        text_widget.tag_configure("info", foreground="#2196F3", font=("Courier", 12, "bold"))
        text_widget.tag_configure("loading", foreground="#9C27B0", font=("Courier", 12, "bold"))
    
    def log_message(self, message, log_widget=None, color='default'):
        """Modern renkli log mesajı ekle"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if log_widget is None:
            log_widget = self.log_text
        
        # BTK sonuçları için özel formatla
        if "BTK tarafından uygulanan bir karar bulunamadı" in message:
            # Domain ve sonucu ayır
            parts = message.split(" ", 1)
            if len(parts) >= 2:
                domain = parts[0]
                result = parts[1]
                
                # Timestamp ekle
                log_widget.insert('end', f"[{timestamp}] ")
                
                # Domain ismini mavi renkte ekle
                domain_start = log_widget.index('end-1c')
                log_widget.insert('end', domain)
                domain_end = log_widget.index('end-1c')
                text_widget = log_widget._textbox
                text_widget.tag_add('info', domain_start, domain_end)
                
                # Ayırıcı ekle
                log_widget.insert('end', " - ")
                
                # Sonucu yeşil renkte ekle (erişilebilir)
                result_start = log_widget.index('end-1c')
                log_widget.insert('end', f"{result}\n")
                result_end = log_widget.index('end-1c')
                text_widget.tag_add('success', result_start, result_end)
            else:
                formatted_message = f"[{timestamp}] {message}\n"
                start_index = log_widget.index('end-1c')
                log_widget.insert('end', formatted_message)
                end_index = log_widget.index('end-1c')
                if color != 'default':
                    text_widget = log_widget._textbox
                    text_widget.tag_add('success', start_index, end_index)
        elif "engellendi" in message.lower() or "kısıtlandı" in message.lower() or "erişim engellendi" in message.lower():
            # Engellenen siteler için özel formatla
            parts = message.split(" ", 1)
            if len(parts) >= 2:
                domain = parts[0]
                result = parts[1]
                
                # Timestamp ekle
                log_widget.insert('end', f"[{timestamp}] ")
                
                # Domain ismini mavi renkte ekle
                domain_start = log_widget.index('end-1c')
                log_widget.insert('end', domain)
                domain_end = log_widget.index('end-1c')
                text_widget = log_widget._textbox
                text_widget.tag_add('info', domain_start, domain_end)
                
                # Ayırıcı ekle
                log_widget.insert('end', " - ")
                
                # Sonucu kırmızı renkte ekle (engellendi)
                result_start = log_widget.index('end-1c')
                log_widget.insert('end', f"{result}\n")
                result_end = log_widget.index('end-1c')
                text_widget.tag_add('error', result_start, result_end)
            else:
                formatted_message = f"[{timestamp}] {message}\n"
                start_index = log_widget.index('end-1c')
                log_widget.insert('end', formatted_message)
                end_index = log_widget.index('end-1c')
                text_widget = log_widget._textbox
                text_widget.tag_add('error', start_index, end_index)
        else:
            # Normal mesajlar
            formatted_message = f"[{timestamp}] {message}\n"
            start_index = log_widget.index('end-1c')
            log_widget.insert('end', formatted_message)
            end_index = log_widget.index('end-1c')
            
            # Renk uygula
            if color != 'default':
                text_widget = log_widget._textbox
                text_widget.tag_add(color, start_index, end_index)
        
        log_widget.see('end')
    
    def update_status(self, message, status_type="info"):
        """Modern durum güncelleme"""
        icons = {
            "info": "ℹ️",
            "success": "✅", 
            "error": "❌",
            "warning": "⚠️",
            "loading": "🔄"
        }
        icon = icons.get(status_type, "ℹ️")
        self.status_label.configure(text=f"{icon} {message}")

    def start_test(self):
        """Birleşik testi başlat - tek domain veya toplu test otomatik algılanır"""
        single_domain = self.single_domain_var.get().strip()
        domains_text = self.bulk_domains_text.get('1.0', 'end').strip()
        
        # Test edilecek domain'leri belirle
        domains = []
        
        # Önce tek domain kontrolü
        if single_domain:
            domains.append(single_domain)
        
        # Sonra toplu domain kontrolü
        if domains_text:
            bulk_domains = [line.strip() for line in domains_text.split('\n') if line.strip()]
            # Tek domain zaten varsa ve bulk domain'ler farklıysa ekle
            if single_domain and bulk_domains:
                if single_domain not in bulk_domains:
                    domains.extend(bulk_domains)
                else:
                    # Tek domain bulk listede varsa sadece bulk listeyi kullan
                    domains = bulk_domains
            elif not single_domain and bulk_domains:
                domains = bulk_domains
        
        if not domains:
            messagebox.showerror(get_text('error'), get_text('error_no_domains'))
            return
        
        # Paralel tarayıcı sayısını kontrol et
        try:
            parallel_count = int(self.parallel_browsers_var.get())
            if parallel_count < 1 or parallel_count > 5:
                messagebox.showerror(get_text('error'), get_text('error_invalid_parallel_count'))
                return
        except ValueError:
            messagebox.showerror(get_text('error'), get_text('error_invalid_parallel_input'))
            return
        
        self.is_running = True
        self.test_btn.configure(state='disabled')
        self.stop_btn.configure(state='normal')
        
        self.log_text.delete('1.0', 'end')
        
        # Test tipini belirle ve log mesajı
        if len(domains) == 1:
            self.log_message(f"🚀 {get_text('test_starting')} {domains[0]}...", color='info')
            self.update_status(f"{domains[0]} {get_text('status_testing')}", "loading")
        else:
            if parallel_count > 1:
                self.log_message(f"🚀 {get_text('parallel_test_starting').format(len(domains), parallel_count)}", color='info')
            else:
                self.log_message(f"🚀 {get_text('bulk_test_starting').format(len(domains))}", color='info')
            self.update_status(f"{len(domains)} domain {get_text('status_testing')}", "loading")
        
        self.progress_bar.set(0)
        self.progress_var.set(f"0 / {len(domains)} tamamlandı")
        
        # Thread'de test çalıştır
        thread = threading.Thread(target=self.run_test, args=(domains, parallel_count))
        thread.daemon = True
        thread.start()
    
    def run_test(self, domains, parallel_count=1):
        """Birleşik testi çalıştır - tek veya toplu domain"""
        try:
            delay = int(self.delay_var.get())
            config.HEADLESS_MODE = self.single_headless_var.get()
            config.MAX_CAPTCHA_ATTEMPTS = int(self.captcha_attempts_var.get())
            config.WAIT_TIMEOUT = int(self.timeout_var.get())
            
            if len(domains) == 1:
                # Tek domain için özel işlem
                self._run_single_domain(domains[0])
            else:
                # Toplu domain testi
                if parallel_count > 1:
                    self._run_parallel_test(domains, parallel_count, delay)
                else:
                    self._run_sequential_test(domains, delay)
            
        except Exception as e:
            self.queue.put(('error', f"Test hatası: {str(e)}"))
    
    def _run_single_domain(self, domain):
        """Tek domain testini çalıştır"""
        try:
            bot = BTKBot(domain=domain)
            self.current_bot = bot
            
            # Bot çıktılarını yakalamak için
            
            # Log yakalama
            import sys
            original_stdout = sys.stdout
            original_stderr = sys.stderr
            sys.stdout = LogCapture(lambda msg: self.queue.put(('log', msg)))
            sys.stderr = LogCapture(lambda msg: self.queue.put(('log', msg)))
            
            try:
                success = bot.run()
                
                # BTK sonucunu gerçek zamanlı olarak al
                btk_result = self._get_btk_result_for_domain(domain)
                if success and btk_result == "Test başarısız":
                    btk_result = "BTK tarafından uygulanan bir karar bulunamadı"
                
                # Sonucu kaydet
                result = {
                    'domain': domain,
                    'success': success,
                    'result': btk_result,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                self.test_results.append(result)
                
                # Test tamamlandı mesajı
                self.queue.put(('bulk_complete', 1))
                
            finally:
                sys.stdout = original_stdout
                sys.stderr = original_stderr
                
        except Exception as e:
            self.queue.put(('error', f"Domain test hatası: {str(e)}"))
        finally:
            self.current_bot = None
    
    def _run_sequential_test(self, domains, delay):
        """Sıralı domain testi"""
        for i, domain in enumerate(domains):
            if not self.is_running:
                break
            
            self.queue.put(('bulk_progress', f"🔄 Test {i+1}/{len(domains)}: {domain}"))
            
            try:
                bot = BTKBot(domain=domain)
                self.current_bot = bot
                
                # Log yakalama
                import sys
                original_stdout = sys.stdout
                original_stderr = sys.stderr
                sys.stdout = LogCapture(lambda msg: self.queue.put(('log', msg)))
                sys.stderr = LogCapture(lambda msg: self.queue.put(('log', msg)))
                
                try:
                    success = bot.run()
                    
                    # BTK sonucunu gerçek zamanlı olarak al
                    btk_result = self._get_btk_result_for_domain(domain)
                    if success and btk_result == "Test başarısız":
                        btk_result = "BTK tarafından uygulanan bir karar bulunamadı"
                    
                    # Sonucu kaydet
                    result = {
                        'domain': domain,
                        'success': success,
                        'result': btk_result,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    self.test_results.append(result)
                    
                    # Log mesajını BTK sonucuna göre belirle
                    if "BTK tarafından uygulanan bir karar bulunamadı" in btk_result:
                        self.queue.put(('bulk_log', (f"{domain}: ✅ Erişilebilir", 'success')))
                    else:
                        self.queue.put(('bulk_log', (f"{domain}: ❌ Engellendi", 'error')))
                    self.queue.put(('bulk_update', (i + 1) / len(domains)))
                
                finally:
                    sys.stdout = original_stdout
                    sys.stderr = original_stderr
                
            except Exception as e:
                self.queue.put(('bulk_log', (f"{domain}: ❌ Hata - {str(e)}", 'error')))
                self.queue.put(('bulk_update', (i + 1) / len(domains)))
            
            finally:
                self.current_bot = None
            
            # Domain'ler arası bekleme
            if i < len(domains) - 1 and self.is_running:
                for j in range(delay):
                    if not self.is_running:
                        break
                    time.sleep(1)
        
        # Test tamamlandı mesajı gönder
        if self.is_running:
            self.queue.put(('bulk_complete', len(domains)))
    
    def _run_parallel_test(self, domains, parallel_count, delay):
        """Paralel domain testi"""
        import concurrent.futures
        from threading import Lock
        
        # Thread-safe değişkenler
        completed_count = 0
        results_lock = Lock()
        
        # Log yakalama sınıfı (yukarıda tanımlanmış)
        
        def test_single_domain(domain):
            if not self.is_running:
                return
            
            try:
                bot = BTKBot(domain=domain)
                
                # Log yakalama
                import sys
                original_stdout = sys.stdout
                original_stderr = sys.stderr
                sys.stdout = LogCapture(lambda msg: self.queue.put(('log', msg)))
                sys.stderr = LogCapture(lambda msg: self.queue.put(('log', msg)))
                
                try:
                    success = bot.run()
                    
                    # BTK sonucunu gerçek zamanlı olarak al
                    btk_result = self._get_btk_result_for_domain(domain)
                    if success and btk_result == "Test başarısız":
                        btk_result = "BTK tarafından uygulanan bir karar bulunamadı"
                
                finally:
                    sys.stdout = original_stdout
                    sys.stderr = original_stderr
                
                # Thread-safe sonuç kaydetme
                with results_lock:
                    nonlocal completed_count
                    completed_count += 1
                    
                    result = {
                        'domain': domain,
                        'success': success,
                        'result': btk_result,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    self.test_results.append(result)
                    
                    # Log mesajını BTK sonucuna göre belirle
                    if "BTK tarafından uygulanan bir karar bulunamadı" in btk_result:
                        self.queue.put(('bulk_log', (f"{domain}: ✅ Erişilebilir", 'success')))
                    else:
                        self.queue.put(('bulk_log', (f"{domain}: ❌ Engellendi", 'error')))
                    
                    self.queue.put(('bulk_update', completed_count / len(domains)))
                    self.queue.put(('bulk_progress', f"🔄 {completed_count}/{len(domains)} tamamlandı (Paralel)"))
                
            except Exception as e:
                with results_lock:
                    completed_count += 1
                    self.queue.put(('bulk_log', (f"{domain}: ❌ Hata - {str(e)}", 'error')))
                    self.queue.put(('bulk_update', completed_count / len(domains)))
        
        # Paralel işleme
        with concurrent.futures.ThreadPoolExecutor(max_workers=parallel_count) as executor:
            # Bütün domain'leri paralel olarak başlat
            futures = [executor.submit(test_single_domain, domain) for domain in domains]
            
            # İşlemlerin tamamlanmasını bekle
            for future in concurrent.futures.as_completed(futures):
                if not self.is_running:
                    # Çalışan işlemleri durdur
                    for f in futures:
                        f.cancel()
                    break
                
                try:
                    future.result()  # Exception varsa burda yakalanır
                except Exception as e:
                    self.queue.put(('bulk_log', (f"Paralel test hatası: {str(e)}", 'error')))
        
        # Test tamamlandı mesajı gönder
        if self.is_running:
            self.queue.put(('bulk_complete', len(domains)))
    
    def stop_test(self):
        """Testi durdur"""
        self.is_running = False
        if self.current_bot and hasattr(self.current_bot, 'driver') and self.current_bot.driver:
            try:
                self.current_bot.driver.quit()
            except:
                pass
        
        self.test_btn.configure(state='normal')
        self.stop_btn.configure(state='disabled')
        
        self.update_status(get_text('status_stopped'), "warning")
        self.log_message(f"⏹️ {get_text('test_stopped_by_user')}", color='warning')
    
    def check_queue(self):
        """Queue'dan mesajları kontrol et"""
        try:
            while True:
                message_type, data = self.queue.get_nowait()
                
                if message_type == 'log':
                    # BTK sonuçlarını yakala - yeni format ile
                    if (any(pattern in data for pattern in [
                        "Bilgi Teknolojileri ve İletişim Kurumu tarafından uygulanan bir karar bulunamadı",
                        "No decision found by the Information and Communication Technologies Authority",
                        "İlgili Kararlar",
                        "Related Decisions",
                        "has been blocked by the decision",
                        "erişime engellenmiştir",
                        "MAHKEME KARARI",
                        "COURT DECISION"
                    ])):
                        self._capture_btk_result(data)
                    
                    # Mesajı filtrele ve göster
                    filtered_message = self.filter_log_message(data)
                    if filtered_message:
                        if ("BTK tarafından uygulanan bir karar bulunamadı" in filtered_message or
                            "No decision found by" in filtered_message):
                            self.log_message(filtered_message, color='success')
                        elif ("MAHKEME KARARI" in filtered_message or
                              "COURT DECISION" in filtered_message or
                              "has been blocked" in filtered_message or
                              "erişime engellenmiştir" in filtered_message):
                            self.log_message(filtered_message, color='error')
                        elif "engellendi" in filtered_message.lower() or "kısıtlandı" in filtered_message.lower():
                            self.log_message(filtered_message, color='error')
                        elif "✅" in filtered_message:
                            self.log_message(filtered_message, color='success')
                        elif "❌" in filtered_message:
                            self.log_message(filtered_message, color='error')
                        elif "🚀" in filtered_message:
                            self.log_message(filtered_message, color='info')
                        elif "⚠️" in filtered_message:
                            self.log_message(filtered_message, color='warning')
                        elif "🔄" in filtered_message:
                            self.log_message(filtered_message, color='loading')
                        else:
                            self.log_message(filtered_message)
                
                elif message_type == 'bulk_progress':
                    self.progress_var.set(data)
                    self.update_status(data, "loading")
                
                elif message_type == 'bulk_log':
                    # Bulk log mesajlarını işleme
                    if isinstance(data, tuple) and len(data) == 2:
                        message, color = data
                        # Erişilebilir/Engellendi mesajlarını yoksay
                        if ": ✅ Erişilebilir" in message or ": ❌ Engellendi" in message:
                            continue
                        filtered_message = self.filter_log_message(message)
                        if filtered_message:
                            self.log_message(filtered_message, self.log_text, color=color)
                    else:
                        filtered_message = self.filter_log_message(data)
                        if filtered_message:
                            self.log_message(filtered_message, self.log_text)
                
                elif message_type == 'bulk_update':
                    self.progress_bar.set(data)
                    completed = int(data * len([line.strip() for line in self.bulk_domains_text.get('1.0', 'end').split('\n') if line.strip()]))
                    total = len([line.strip() for line in self.bulk_domains_text.get('1.0', 'end').split('\n') if line.strip()])
                    self.progress_var.set(f"{completed} / {total} {get_text('completed')}")
                
                elif message_type == 'bulk_complete':
                    self.test_btn.configure(state='normal')
                    self.stop_btn.configure(state='disabled')
                    self.is_running = False
                    
                    if data == 1:
                        # Tek domain testi
                        self.update_status(get_text('test_completed_successfully'), "success")
                        self.log_message(f"✅ {get_text('test_completed_successfully')}", color='success')
                    else:
                        # Toplu domain testi
                        self.update_status(f"{get_text('bulk_test_completed').format(data)}", "success")
                        self.log_message(f"🎉 {get_text('bulk_test_completed').format(data)}", color='success')
                
                elif message_type == 'error':
                    self.log_message(f"❌ {get_text('error')}: {data}", color='error')
                    self.update_status(f"{get_text('error')}: {data}", "error")
                    
                    self.test_btn.configure(state='normal')
                    self.stop_btn.configure(state='disabled')
                    self.is_running = False
                
        except queue.Empty:
            pass
        
        self.root.after(100, self.check_queue)
    
    def clean_ansi_codes(self, text):
        """ANSI renk kodlarını ve özel karakterleri temizle"""
        # ANSI renk kodlarını temizle
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        cleaned = ansi_escape.sub('', text)
        # Diğer özel karakterleri temizle
        cleaned = re.sub(r'\[[\d;]*[mK]', '', cleaned)
        # Unicode kontrol karakterlerini temizle
        cleaned = "".join(ch for ch in cleaned if not unicodedata.category(ch).startswith('C'))
        return cleaned.strip()

    def _capture_btk_result(self, message):
        try:
            message = self.clean_ansi_codes(message)
            
            # Yeni format: "domain.com Bilgi Teknolojileri ve İletişim Kurumu tarafından uygulanan bir karar bulunamadı."
            if "Bilgi Teknolojileri ve İletişim Kurumu tarafından uygulanan bir karar bulunamadı" in message:
                # Domain'i mesajın başından çıkar
                parts = message.split(" ", 1)
                if len(parts) >= 1:
                    domain = self.clean_ansi_codes(parts[0].strip())
                    btk_decision = "Bilgi Teknolojileri ve İletişim Kurumu tarafından uygulanan bir karar bulunamadı."
                    self.current_domain_result[domain] = btk_decision
                    self.update_single_result(domain, True, btk_decision)
                return
            
            # İngilizce format: "domain.com No decision found by the Information and Communication Technologies Authority."
            if "No decision found by the Information and Communication Technologies Authority" in message:
                parts = message.split(" ", 1)
                if len(parts) >= 1:
                    domain = self.clean_ansi_codes(parts[0].strip())
                    btk_decision = "No decision found by the Information and Communication Technologies Authority."
                    self.current_domain_result[domain] = btk_decision
                    self.update_single_result(domain, True, btk_decision)
                return
            
            # Mahkeme kararı - Türkçe format
            if "İlgili Kararlar" in message and ("erişime engellenmiştir" in message or "hakkında uygulanmakta olan kararlar" in message):
                # Domain'i mesajın başından çıkar
                parts = message.split(" ", 1)
                if len(parts) >= 1:
                    domain = self.clean_ansi_codes(parts[0].strip())
                    # Tam mahkeme kararını al
                    full_result = message.replace(domain, "").strip()
                    self.current_domain_result[domain] = full_result
                    self.update_single_result(domain, False, full_result)
                return
            
            # Mahkeme kararı - İngilizce format
            if "Related Decisions" in message and ("has been blocked by the decision" in message or "decisions being applied regarding" in message):
                # Domain'i mesajın başından çıkar
                parts = message.split(" ", 1)
                if len(parts) >= 1:
                    domain = self.clean_ansi_codes(parts[0].strip())
                    # Tam mahkeme kararını al
                    full_result = message.replace(domain, "").strip()
                    self.current_domain_result[domain] = full_result
                    self.update_single_result(domain, False, full_result)
                return
            
            # Eski format desteği: "domain - result"
            if " - " in message:
                parts = message.split(" - ", 1)
                if len(parts) == 2:
                    domain = self.clean_ansi_codes(parts[0].strip())
                    btk_decision = self.clean_ansi_codes(parts[1].strip())
                    self.current_domain_result[domain] = btk_decision
                    # Başarılı mı kontrolü
                    is_accessible = ("BTK tarafından uygulanan bir karar bulunamadı" in btk_decision or 
                                   "No decision found by" in btk_decision)
                    self.update_single_result(domain, is_accessible, btk_decision)
                return
            
        except Exception as e:
            print(f"❌ Sonuç yakalama hatası: {str(e)}")

    def update_single_result(self, domain, success, result):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        domain = self.clean_ansi_codes(domain)
        result = self.clean_ansi_codes(result)
        # test_results güncelle
        domain_clean = self.clean_ansi_codes(domain)
        self.test_results = [r for r in self.test_results if self.clean_ansi_codes(r['domain']) != domain_clean]
        self.test_results.append({
            'domain': domain,
            'success': success,
            'result': result,
            'timestamp': timestamp
        })
        self.update_results_display()

    def update_results_display(self):
        # Treeview'ı temizle
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        accessible_count = 0
        blocked_count = 0
        for result in self.test_results:
            btk_result = result['result']
            # Hem Türkçe hem İngilizce "karar bulunamadı" kontrolü
            if (get_text('btk_no_decision') in btk_result or 
                "No decision found by BTK" in btk_result or
                "No decision found by the Information and Communication Technologies Authority" in btk_result or
                "BTK tarafından uygulanan bir karar bulunamadı" in btk_result or
                "Bilgi Teknolojileri ve İletişim Kurumu tarafından uygulanan bir karar bulunamadı" in btk_result):
                status = get_text('accessible')
                tag = ('accessible', 'success_row')
                accessible_count += 1
            else:
                status = get_text('blocked')
                tag = ('blocked', 'error_row')
                blocked_count += 1
            item = self.results_tree.insert('', 'end', values=(
                result['domain'],
                status,
                btk_result,
                result['timestamp']
            ), tags=tag)
        # Özet güncelle
        total = len(self.test_results)
        if not self.test_results:
            self.summary_text.configure(text=get_text('no_tests_yet'))
        else:
            success_rate = (accessible_count / total) * 100 if total > 0 else 0
            summary = f"""📊 {get_text('total_tests')}: {total}
✅ {get_text('accessible_sites')}: {accessible_count}
❌ {get_text('blocked_sites')}: {blocked_count}

📈 {get_text('success_rate')}: %{success_rate:.1f}

🕐 {get_text('last_update')}: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"""
            self.summary_text.configure(text=summary)
    
    def _get_btk_result_for_domain(self, domain):
        """Domain için BTK sonucunu getir"""
        return self.current_domain_result.get(domain, "Test başarısız")

    def extract_btk_result(self, html_content):
        """BTK sonucundan yazi2 metnini çıkar"""
        try:
            # yazi2 class'ına sahip div'i bul
            yazi2_match = re.search(r'<div[^>]*class="yazi2"[^>]*>(.*?)</div>', html_content)
            if yazi2_match:
                # HTML taglerini temizle
                result = re.sub(r'<[^>]+>', '', yazi2_match.group(1))
                return result.strip()
            return html_content  # Eğer yazi2 bulunamazsa orijinal içeriği döndür
        except:
            return html_content

    def filter_log_message(self, message):
        """Log mesajlarını filtrele - sadece önemli olanları göster"""
        # Önce ANSI kodlarını temizle
        message = self.clean_ansi_codes(message)
        
        # CAPTCHA ile ilgili gereksiz mesajları filtrele
        if self.settings.get('filter_captcha_logs', True):
            captcha_noise = [
                # Türkçe CAPTCHA hata mesajları
                "CAPTCHA metni okunamadı",
                "CAPTCHA başarısız",
                "Tekrar denemede de CAPTCHA hatası",
                "CAPTCHA sorunu - Deneme",
                "CAPTCHA yanlış çözüldü",
                "CAPTCHA görüntüsü",
                # İngilizce CAPTCHA hata mesajları
                "CAPTCHA text could not be read or too short",
                "CAPTCHA failed",
                "CAPTCHA error in retry attempt",
                "CAPTCHA solving error",
                "CAPTCHA image not found",
                "CAPTCHA failed, refreshing page"
            ]
            
            if any(noise in message for noise in captcha_noise):
                return None
        
        # Önemli mesajlar (her zaman gösterilecek)
        important_patterns = [
            "🚀",  # Test başlatma
            "🎉",  # Tamamlanma
            "✅",  # Başarılı sonuç
            "❌",  # Başarısız sonuç (sadece önemli olanlar)
            "📊",  # Sonuç başlığı
            # Türkçe BTK sonuçları
            "BTK tarafından",  # BTK sonucu
            "MAHKEME KARARI",  # Mahkeme kararı
            "engellendi",  # Engellendi
            "kısıtlandı",  # Kısıtlandı
            # İngilizce BTK sonuçları
            "No decision found by BTK",  # BTK sonucu
            "COURT DECISION",  # Mahkeme kararı
            "blocked",  # Engellendi
            "restricted"  # Kısıtlandı
        ]
        
        # Önemli mesajları kontrol et
        for pattern in important_patterns:
            if pattern in message:
                return message
        
        return None
    
    def clean_message(self, message):
        """Mesajı temizle ve formatla"""
        # ANSI kodlarını ve özel karakterleri temizle
        message = self.clean_ansi_codes(message)
        
        # Fazla boşlukları temizle
        message = ' '.join(message.split())
        
        return message.strip()

    def load_domains_from_file(self):
        """Dosyadan domain listesi yükle"""
        file_path = filedialog.askopenfilename(
            title=get_text('select_domain_file'),
            filetypes=[(get_text('text_files'), "*.txt"), (get_text('all_files'), "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.bulk_domains_text.delete('1.0', 'end')
                self.bulk_domains_text.insert('1.0', content)
                lines = len([line for line in content.split('\n') if line.strip()])
                messagebox.showinfo(get_text('success'), f"📁 {lines} {get_text('domains_loaded')}")
            except Exception as e:
                messagebox.showerror(get_text('error'), f"{get_text('file_read_error')}: {str(e)}")

    def save_domains_to_file(self):
        """Domain listesini dosyaya kaydet"""
        content = self.bulk_domains_text.get('1.0', 'end').strip()
        if not content:
            messagebox.showwarning(get_text('warning'), get_text('empty_domain_list'))
            return
        file_path = filedialog.asksaveasfilename(
            title=get_text('save_domain_list'),
            defaultextension=".txt",
            filetypes=[(get_text('text_files'), "*.txt"), (get_text('all_files'), "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo(get_text('success'), f"💾 {get_text('domain_list_saved')}")
            except Exception as e:
                messagebox.showerror(get_text('error'), f"{get_text('file_save_error')}: {str(e)}")

def main():
    """Ana fonksiyon"""
    # CustomTkinter root oluştur
    root = ctk.CTk()
    app = BTKBotGUI(root)
    
    # Pencere kapatılırken çalışan testleri durdur
    def on_closing():
        if app.is_running:
            if messagebox.askokcancel(get_text('info'), get_text('confirm_exit')):
                app.stop_test()
                root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Başlangıç mesajı
    print("🚀 Aow Software -BTK Site Sorgu Botu başlatılıyor...")
    print("✨ CustomTkinter ile modern arayüz")
    
    root.mainloop()

if __name__ == "__main__":
    main()