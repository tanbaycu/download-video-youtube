# 🎥 YouTube Downloader CLI

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Last Updated](https://img.shields.io/badge/last%20updated-05/08/2025-orange)]()

A powerful command-line YouTube video and playlist downloader built with Python. This tool provides a beautiful CLI interface for downloading YouTube content with various format options.

## ✨ Features

- 📥 Download single videos or entire playlists
- 🎵 Multiple format options (video/audio)
- 🔄 Automatic yt-dlp updates
- 🎨 Beautiful CLI interface with progress tracking
- 📁 Custom download directory support
- 🌐 Geo-bypass support
- 🎯 Format selection with detailed information

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/yt-downloader-py.git
cd yt-downloader-py
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## 📋 Requirements

- Python 3.8 or higher
- yt-dlp
- rich
- pyfiglet
- ffmpeg (for audio conversion)

## 💻 Usage

1. Run the program:
```bash
python app.py
```

2. Follow the menu options:
   - Option 1: Download a single video
   - Option 2: Download a playlist
   - Option 3: About
   - Option 4: Update yt-dlp
   - Option 5: Exit

3. For video downloads:
   - Enter the YouTube URL
   - Select your preferred format
   - Choose download location
   - Enter custom filename (optional)

## 🛠️ Configuration

The default download directory is set to `downloads/`. You can change this by modifying the `DEFAULT_DOWNLOAD_DIR` constant in `app.py`.

## 📝 Changelog

### Version 1.02 (05/08/2025)
- Added yt-dlp auto-update feature
- Improved error handling
- Enhanced user interface
- Added playlist download optimization
- Added format selection improvements
- Changed default download directory to 'downloads'

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

- **tanbay**
- Email: dev.tanbaycu@gmail.com

## ⚠️ Disclaimer

This tool is for educational purposes only. Please respect YouTube's terms of service and copyright laws when downloading content.

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The core downloader engine
- [rich](https://github.com/Textualize/rich) - For beautiful terminal formatting
- [pyfiglet](https://github.com/pwaller/pyfiglet) - For ASCII art text

## 📞 Support

If you encounter any issues or have suggestions, please:
1. Check the [Issues](https://github.com/yourusername/yt-downloader-py/issues) section
2. Create a new issue if your problem isn't already listed
3. Contact the author at dev.tanbaycu@gmail.com

---

⭐ Star this repository if you find it useful! 
