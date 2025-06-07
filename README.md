# 🛰️ The Signal Cartographer: Echoes from the Void

A sci-fi signal analysis game built with Python and Textual TUI. Explore the void of space, detect mysterious signals, and uncover their secrets using the AetherTap terminal interface.

## 🎮 Game Overview

You are a Signal Cartographer exploring space sectors to detect and analyze mysterious signals from unknown sources. Use advanced tools to scan different sectors, focus on interesting signals, and analyze them to reveal hidden information.

## ✨ Features

- **🖥️ Professional TUI Interface** - Built with Textual for a modern terminal experience
- **📊 6-Panel AetherTap Interface** - Spectrum analyzer, signal focus, cartography, decoder, and more
- **📡 Multi-Sector Exploration** - Explore ALPHA-1, BETA-2, and GAMMA-3 sectors with unique signals
- **🔍 Advanced Signal Analysis** - Focus on signals and analyze them to uncover secrets
- **⌨️ Full Hotkey Support** - F1-F5 for panel switching, Ctrl+H for help
- **📖 Comprehensive Help System** - Full-screen gameplay guide with step-by-step instructions
- **🎯 Real-time Feedback** - Immediate visual feedback for all commands

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Windows, macOS, or Linux

### Installation & Running

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/signal-cartographer.git
   cd signal-cartographer
   ```

2. **Set up virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment:**
   - **Windows:** `.venv\Scripts\activate`
   - **macOS/Linux:** `source .venv/bin/activate`

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the game:**
   ```bash
python main.py
```

   Or use the provided scripts:
   - **Windows:** `.\start_game.ps1`
   - **Unix:** `./run.sh`

## 🎯 How to Play

### Getting Started
1. **Launch the game** and look for the **purple-bordered command input box** at the bottom
2. **Type `HELP`** or press **Ctrl+H** for the comprehensive gameplay guide
3. **Start with `SCAN`** to detect signals in the current sector
4. **Use `FOCUS SIG_1`** to lock onto the first detected signal
5. **Run `ANALYZE`** to reveal hidden information about the focused signal

### Essential Commands
- `SCAN` - Scan current sector for signals
- `SCAN BETA-2` - Scan specific sector (ALPHA-1, BETA-2, GAMMA-3)
- `FOCUS SIG_1` - Focus on a detected signal
- `ANALYZE` - Analyze the currently focused signal
- `STATUS` - Show system status
- `HELP` - Open comprehensive help guide

### Interface Panels
- **📊 Main Spectrum Analyzer** - Shows detected signals as frequency spikes
- **🔍 Signal Focus & Data** - Detailed information about focused signals
- **🗺️ Cartography & Navigation** - Current sector and signal map
- **🛠️ Decoder & Analysis Toolkit** - Analysis results and tools
- **📜 Captain's Log & Database** - Command history and system messages
- **💻 Command Input** - Purple-bordered box for typing commands

### Hotkeys
- **F1-F5** - Switch between different panels
- **Ctrl+H** - Open full-screen help guide
- **Ctrl+C** - Quit game safely
- **Enter/Escape** - (In help screen) Return to main game

## 🌟 Game Features

### Signal Types & Sectors
- **ALPHA-1**: 3 signals, perfect for beginners
- **BETA-2**: 2 stronger, more complex signals  
- **GAMMA-3**: 1 powerful signal with deep secrets

### Signal Properties
- **Frequency** - Signal location in MHz
- **Strength** - Signal power level
- **Modulation** - Signal encoding type (Pulsed-Echo, Bio-Resonant, etc.)
- **Stability** - Signal consistency over time
- **Signature** - Unique signal characteristics

## 🛠️ Technical Details

### Built With
- **Python 3.8+**
- **Textual** - Modern Python TUI framework
- **Rich** - Terminal text formatting
- **Markdown-it-py** - Documentation parsing

### Architecture
- **Modular design** with separate UI, game logic, and signal systems
- **Command parser** for flexible command handling
- **Signal detector** with procedural signal generation
- **Textual TUI** with custom widgets and layouts

## 📁 Project Structure

```
signal-cartographer/
├── src/
│   ├── ui/              # User interface components
│   ├── puzzles/         # Signal analysis puzzles  
│   ├── content/         # Game content and data
│   └── utils/           # Utility functions
├── data/               # Game data files
├── instruction/        # Documentation
├── main.py            # Game entry point
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## 🎮 Advanced Gameplay

Once you master the basics:
- **Explore all three sectors** and compare signal characteristics
- **Analyze multiple signals** in the same sector to find patterns
- **Use function keys** to monitor multiple panels simultaneously
- **Look for hidden messages** in analyzed signal signatures
- **Discover signal relationships** across different sectors

## 🐛 Troubleshooting

- **Can't see signals?** → Run `SCAN` first
- **FOCUS not working?** → Make sure signals exist after scanning
- **ANALYZE gives no results?** → Focus on a signal first using `FOCUS SIG_1`
- **Can't type commands?** → Click in the purple command input box
- **Commands not working?** → Commands are case-insensitive

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with the amazing [Textual](https://github.com/Textualize/textual) framework
- Inspired by classic sci-fi and signal analysis themes
- Thanks to the Python community for excellent tooling

---

**Ready to explore the void? Launch the game and start your signal cartography journey!** 🚀
