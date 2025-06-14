# 🤖 BTK Site Query Bot

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)
![GUI](https://img.shields.io/badge/GUI-CustomTkinter-orange.svg)

**An automated bot for checking domain/IP blocking status through BTK (Information and Communication Technologies Authority) site query system. Features modern CustomTkinter interface with multi-language support (Turkish/English) for user-friendly experience.**

__🇹🇷 [Türkçe README için tıklayın](README_TR.md)__

[🚀 Installation](#-installation) • [📖 Usage](#-usage) • [⚙️ Features](#️-features) • [🖼️ Screenshots](#️-screenshots) • [🤝 Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [🎯 About the Project](#-about-the-project)
- [✨ Features](#-features)
- [🖼️ Screenshots](#️-screenshots)
- [🚀 Installation](#-installation)
- [📖 Usage](#-usage)
- [⚙️ Configuration](#️-configuration)
- [🔧 Technical Details](#-technical-details)
- [🐛 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## 🎯 About the Project

This bot automatically uses the BTK (Information and Communication Technologies Authority) site query system to check whether domain/IP addresses are blocked. It features a modern CustomTkinter interface for a user-friendly experience.

### 🎪 Key Features

- 🤖 **Automatic CAPTCHA Solving**: Advanced OCR technology
- 🌐 **Single and Bulk Testing**: Test multiple domains simultaneously
- 🎨 **Modern Interface**: CustomTkinter with dark/light theme support
- 📊 **Detailed Reporting**: Colorful result analysis and Excel export
- ⚡ **Parallel Processing**: Multi-browser support for fast testing
- 💾 **Auto-save**: Automatic domain list saving
- 🔄 **Unlimited Retry**: Unlimited retry mode for CAPTCHA solving
- 🌍 **Multi-language Support**: Turkish/English interface

## ✨ Features

### 🖥️ User Interface

- ✅ Modern CustomTkinter-based GUI
- ✅ Dark/Light theme support
- ✅ Responsive design
- ✅ Real-time progress tracking
- ✅ Colorful log system
- ✅ **Multi-language support (Turkish/English)**

### 🔧 Bot Features

- ✅ Automatic form filling
- ✅ Advanced CAPTCHA solving algorithm
- ✅ Automatic retry on errors
- ✅ Customizable settings
- ✅ Detailed log output
- ✅ **Dynamic language switching**

### 📊 Testing Features

- ✅ Single domain/IP testing
- ✅ Bulk domain testing
- ✅ Parallel browser support (1-5 browsers)
- ✅ Configurable delay between domains
- ✅ Excel export functionality
- ✅ **Real-time result table updates**

## 🖼️ Screenshots

### Main Interface

![Main Interface](images/Ekran%20görüntüsü%202025-06-14%20201228.png)
*Modern CustomTkinter interface with domain testing screen*

### Test Results

![Test Results](images/Ekran%20görüntüsü%202025-06-14%20201655.png)
*Detailed test results and analysis screen*

### Settings Panel

![Settings](images/Ekran%20görüntüsü%202025-06-14%20201211.png)
*Bot settings and configuration panel*

## 🚀 Installation

### Requirements

- **Python 3.9+**
- **Google Chrome** browser
- **Tesseract OCR** (for CAPTCHA solving)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/btk-site-query-bot.git
cd btk-site-query-bot

```

### 2. Install Python Packages

```bash
pip install -r requirements.txt

```

### 3. Tesseract OCR Installation

#### Windows:

1. Download [Tesseract OCR](https://tesseract-ocr.github.io/tessdoc/Downloads.html)
2. Run the installer (UB Mannheim installer recommended)
3. Add Tesseract to system PATH
4. Default installation path: `C:\Program Files\Tesseract-OCR\tesseract.exe`

#### Linux (Ubuntu/Debian):

```bash
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-eng

```

#### macOS:

```bash
brew install tesseract

```

### 4. Configure Settings (Optional)

```bash
# Copy example settings file
cp bot_settings.example.json bot_settings.json

# Edit settings if needed (language, default domains, etc.)
# The application will create this file automatically on first run if it doesn't exist

```

### 5. Run the Application

```bash
# Modern GUI interface (Recommended)
python ui_app.py

# Command line version
python btk_bot.py

```

## 📖 Usage

### GUI Interface Usage

1. **Single Domain Test**:

   - Go to "Domain Test" tab
   - Enter domain/IP in "Single Domain Test" field
   - Click "Start Test" button

2. **Bulk Domain Test**:

   - Enter one domain per line in "Bulk Domain Test" area
   - Set number of parallel browsers (1-5)
   - Click "Start Test" button

3. **View Results**:

   - Check "Results" tab for detailed analysis
   - Colorful table showing accessible/blocked status
   - Excel export functionality

### Command Line Usage

```python
from btk_bot import BTKBot

# Single domain test
bot = BTKBot(domain="example.com")
success = bot.run()

if success:
    print("Test successful!")
else:
    print("Test failed!")

```

### Language Settings

The application supports both Turkish and English:

- **Default Language**: English
- **Change Language**: Go to Settings → Language Settings → Select "Türkçe" for Turkish
- **Dynamic Switching**: Language can be changed without restarting the application

## ⚙️ Configuration

### config.py Settings

```python
# Default domain to test
DOMAIN_TO_CHECK = "google.com"

# BTK site query URL
BTK_URL = "https://internet2.btk.gov.tr/sitesorgu/"

# CAPTCHA settings
MAX_CAPTCHA_ATTEMPTS = 999  # High value for unlimited attempts
UNLIMITED_CAPTCHA_RETRY = True
CAPTCHA_MIN_LENGTH = 4

# WebDriver settings
HEADLESS_MODE = False  # True for hidden mode
WAIT_TIMEOUT = 15  # Element wait time

# OCR settings
OCR_CONFIG = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

```

### bot_settings.json (Auto-saved Settings)

The application automatically creates and manages a `bot_settings.json` file to store user preferences. You can use the provided `bot_settings.example.json` as a template:

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

__Note__: The `bot_settings.json` file is automatically created on first run and is excluded from version control to protect user privacy.

## 🔧 Technical Details

### Bot Workflow

1. **WebDriver Initialization**: Starts Chrome browser
2. **Site Navigation**: Navigates to BTK query page
3. **Form Filling**: Enters domain/IP address
4. **CAPTCHA Solving**:
   - Downloads CAPTCHA image
   - Applies image processing techniques
   - Converts to text using OCR
   - Submits form

5. **Result Analysis**: Analyzes and reports query results

### CAPTCHA Solving Algorithm

- **Grayscale Conversion**: Converts color image to grayscale
- **Image Scaling**: Enlarges image for better OCR accuracy
- **Noise Reduction**: Uses median blur to reduce noise
- **Contrast Enhancement**: CLAHE algorithm for contrast improvement
- **Thresholding**: OTSU algorithm for binary image conversion
- **OCR**: Tesseract text extraction with custom configuration

### File Structure

```ini
btk-site-query-bot/
├── 📁 images/                 # Screenshots
│   ├── 🖼️ screenshot1.png
│   ├── 🖼️ screenshot2.png
│   └── 🖼️ screenshot3.png
├── 📁 __pycache__/             # Python cache
├── 🐍 btk_bot.py               # Core bot logic
├── 🖥️ ui_app.py                # Modern GUI application
├── ⚙️ config.py                # Configuration settings
├── 🌍 languages.py             # Multi-language support
├── 💾 bot_settings.example.json # Example settings file
├── 📋 requirements.txt         # Python dependencies
├── 📄 LICENSE                  # MIT License
├── 🤝 CONTRIBUTING.md          # Contribution guidelines
├── 📖 README.md               # This file (English)
└── 📖 README_TR.md            # Turkish README

```

## 🐛 Troubleshooting

### Tesseract Error

```ini
TesseractNotFoundError: tesseract is not installed

```

**Solution**: Install Tesseract OCR and add to PATH.

### WebDriver Error

```sh
WebDriverException: 'chromedriver' executable needs to be in PATH

```

**Solution**: Ensure Chrome browser is installed. WebDriver downloads automatically.

### NumPy Compatibility Error

```sh
AttributeError: _ARRAY_API not found

```

**Solution**: Install compatible NumPy version:

```bash
pip uninstall opencv-python numpy -y
pip install "numpy<2.0.0" "opencv-python>=4.8.0,<4.10.0"

```

### GUI Not Starting

```bash
pip install customtkinter>=5.2.0

```

## 🤝 Contributing

This project is open source and welcomes contributions!

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add some amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Contribution Areas

- 🐛 Bug fixes
- ✨ New features
- 📚 Documentation improvements
- 🌍 Translation support
- 🎨 UI/UX improvements

## 📊 Statistics

- ⭐ **CAPTCHA Success Rate**: 85-95%
- 🚀 **Test Speed**: ~30 seconds/domain
- 🔄 **Parallel Processing**: Up to 5 browsers
- 💾 **Supported Formats**: TXT, Excel
- 🌐 **Platform Support**: Windows, Linux, macOS

## ⚠️ Important Notes

- This bot is developed for educational and testing purposes
- Use in accordance with BTK website terms of service
- Avoid excessive requests to prevent server overload
- Use responsibly and respect rate limits

## 💰 Support the Project

If you find this project helpful, you can support its development:

**USDT (TRC20)**: `TYxPh6pZX7Wq9HB6nY2oXhVVnTVPnzxDmR`

Your support helps maintain and improve this project! 🙏

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

## 📞 Contact

- 🐛 **Bug Reports**: [Issues](https://github.com/yourusername/btk-site-query-bot/issues)
- 💡 **Feature Requests**: [Issues](https://github.com/yourusername/btk-site-query-bot/issues)
- 📧 **Email**: your.email@example.com

---

<div align="center">

**❤️ Made with love for the open source community**

[![GitHub stars](https://img.shields.io/github/stars/yourusername/btk-site-query-bot.svg?style=social&label=Star)](https://github.com/yourusername/btk-site-query-bot)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/btk-site-query-bot.svg?style=social&label=Fork)](https://github.com/yourusername/btk-site-query-bot/fork)

</div> 
