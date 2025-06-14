# 🤝 Katkıda Bulunma Rehberi

BTK Site Sorgu Botu projesine katkıda bulunmak istediğiniz için teşekkür ederiz! Bu rehber, projeye nasıl katkıda bulunabileceğinizi açıklar.

## 📋 İçindekiler

- [🚀 Başlangıç](#-başlangıç)
- [🐛 Bug Raporu](#-bug-raporu)
- [💡 Özellik İsteği](#-özellik-isteği)
- [🔧 Kod Katkısı](#-kod-katkısı)
- [📝 Kod Standartları](#-kod-standartları)
- [🧪 Test Etme](#-test-etme)
- [📚 Dokümantasyon](#-dokümantasyon)

## 🚀 Başlangıç

### Geliştirme Ortamını Kurma

1. **Projeyi fork edin**
   ```bash
   # GitHub'da fork butonuna tıklayın
   ```

2. **Yerel kopyayı oluşturun**
   ```bash
   git clone https://github.com/yourusername/btk-site-sorgu-botu.git
   cd btk-site-sorgu-botu
   ```

3. **Sanal ortam oluşturun**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

4. **Bağımlılıkları kurun**
   ```bash
   pip install -r requirements.txt
   ```

5. **Tesseract OCR'ı kurun**
   - [Kurulum rehberini](README.md#3-tesseract-ocr-kurulumu) takip edin

## 🐛 Bug Raporu

Bug bulduğunuzda lütfen aşağıdaki bilgileri içeren bir issue açın:

### Bug Raporu Şablonu

```markdown
## 🐛 Bug Açıklaması
Bugun kısa ve net bir açıklaması.

## 🔄 Tekrar Etme Adımları
1. '...' gidin
2. '...' tıklayın
3. '...' görün
4. Hata oluşuyor

## ✅ Beklenen Davranış
Ne olmasını bekliyordunuz?

## ❌ Gerçek Davranış
Ne oldu?

## 🖼️ Ekran Görüntüleri
Varsa ekran görüntüleri ekleyin.

## 💻 Sistem Bilgileri
- OS: [örn. Windows 10]
- Python Sürümü: [örn. 3.9.7]
- Chrome Sürümü: [örn. 96.0.4664.110]
- Tesseract Sürümü: [örn. 5.0.0]

## 📝 Ek Bilgiler
Diğer önemli detaylar.
```

## 💡 Özellik İsteği

Yeni özellik önerilerinizi memnuniyetle karşılıyoruz:

### Özellik İsteği Şablonu

```markdown
## 🚀 Özellik Açıklaması
Özelliğin kısa açıklaması.

## 🎯 Motivasyon
Bu özellik neden gerekli?

## 💡 Çözüm Önerisi
Nasıl implement edilebilir?

## 🔄 Alternatifler
Başka çözüm yolları var mı?

## 📋 Ek Bilgiler
Diğer detaylar.
```

## 🔧 Kod Katkısı

### Pull Request Süreci

1. **Feature branch oluşturun**
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Değişikliklerinizi yapın**
   - Kod standartlarına uyun
   - Test ekleyin
   - Dokümantasyonu güncelleyin

3. **Commit edin**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

4. **Push edin**
   ```bash
   git push origin feature/amazing-feature
   ```

5. **Pull Request açın**
   - Açıklayıcı başlık yazın
   - Değişiklikleri detaylandırın
   - İlgili issue'ları bağlayın

### Commit Mesaj Formatı

```
type(scope): description

[optional body]

[optional footer]
```

**Tipler:**
- `feat`: Yeni özellik
- `fix`: Bug düzeltmesi
- `docs`: Dokümantasyon
- `style`: Kod formatı
- `refactor`: Kod yeniden düzenleme
- `test`: Test ekleme/düzeltme
- `chore`: Bakım işleri

**Örnekler:**
```
feat(gui): add dark theme support
fix(captcha): improve OCR accuracy
docs(readme): update installation guide
```

## 📝 Kod Standartları

### Python Kod Stili

- **PEP 8** standartlarına uyun
- **Type hints** kullanın
- **Docstring** yazın
- **Meaningful** değişken isimleri kullanın

```python
def solve_captcha(self, image_data: bytes) -> Optional[str]:
    """
    CAPTCHA görüntüsünü çözer.
    
    Args:
        image_data: CAPTCHA görüntü verisi
        
    Returns:
        Çözülen CAPTCHA metni veya None
    """
    try:
        # Implementation
        pass
    except Exception as e:
        logger.error(f"CAPTCHA çözme hatası: {e}")
        return None
```

### GUI Kod Stili

- **CustomTkinter** widget'larını kullanın
- **Responsive** tasarım yapın
- **Accessibility** düşünün
- **Error handling** ekleyin

## 🧪 Test Etme

### Manuel Test

1. **Tek domain testi**
   ```bash
   python ui_app.py
   # GUI'de tek domain test edin
   ```

2. **Toplu domain testi**
   ```bash
   # Birden fazla domain ile test edin
   ```

3. **Farklı platformlarda test**
   - Windows
   - Linux
   - macOS

### Otomatik Test

```bash
# Test dosyaları oluşturun
python -m pytest tests/
```

## 📚 Dokümantasyon

### README Güncellemeleri

- Yeni özellikler için dokümantasyon ekleyin
- Ekran görüntülerini güncelleyin
- Kurulum talimatlarını kontrol edin

### Kod Dokümantasyonu

- Fonksiyonlar için docstring yazın
- Karmaşık algoritmalar için yorum ekleyin
- Type hints kullanın

## 🎯 Katkı Alanları

### 🔥 Öncelikli Alanlar

- **CAPTCHA Çözme**: Doğruluk oranını artırma
- **Performance**: Hız optimizasyonu
- **UI/UX**: Kullanıcı deneyimi iyileştirme
- **Cross-platform**: Platform uyumluluğu

### 💡 Özellik Fikirleri

- **Proxy Desteği**: Proxy kullanımı
- **API Modu**: REST API desteği
- **Scheduled Tests**: Zamanlanmış testler
- **Email Reports**: E-posta raporları
- **Database Support**: Veritabanı entegrasyonu

## 🏆 Katkıda Bulunanlar

Tüm katkıda bulunanlara teşekkür ederiz! 

## 📞 İletişim

- **Issues**: GitHub Issues kullanın
- **Discussions**: GitHub Discussions
- **Email**: project@example.com

## 📄 Lisans

Katkılarınız [MIT Lisansı](LICENSE) altında lisanslanacaktır.

---

**Katkılarınız için teşekkür ederiz! 🙏** 