# 🛰️ The Signal Cartographer - Game Guide

## 🚀 How to Start Playing

1. **Launch the game**:
   ```powershell
   .venv\Scripts\activate
   python main.py
   ```

2. **The interface has 6 panels**:
   - **Top Left**: Main Spectrum Analyzer [MSA] 
   - **Top Right**: Signal Focus & Data [SFD]
   - **Middle Left**: Cartography & Navigation [CNP]
   - **Middle Right**: Decoder & Analysis Toolkit [DAT]
   - **Bottom**: Captain's Log & Database [CLD]
   - **Very Bottom**: Command Input (type here!)

## 🎮 Basic Commands

### Essential Commands to Get Started:

1. **`SCAN`** - Scan current sector for signals
   - `SCAN ALPHA-1` - Scan Alpha-1 sector (3 signals)
   - `SCAN BETA-2` - Scan Beta-2 sector (2 signals)  
   - `SCAN GAMMA-3` - Scan Gamma-3 sector (1 signal)

2. **`FOCUS SIG_1`** - Focus on the first detected signal
   - `FOCUS SIG_2` - Focus on second signal
   - `FOCUS SIG_3` - Focus on third signal

3. **`ANALYZE`** - Analyze the currently focused signal

4. **`STATUS`** - Show current system status

5. **`HELP`** - Show available commands

6. **`CLEAR`** - Clear the log

7. **`QUIT`** - Exit the game

## 🎯 Step-by-Step Tutorial

### Step 1: Scan for Signals
```
SCAN
```
This will detect signals in the current sector (Alpha-1). You should see:
- Spectrum analyzer fills with signal patterns
- Log shows "Found X signals"

### Step 2: Focus on a Signal  
```
FOCUS SIG_1
```
This focuses on the first signal. You should see:
- Signal details appear in the Signal Focus panel
- Frequency, strength, modulation type shown

### Step 3: Analyze the Signal
```
ANALYZE
```
This analyzes the focused signal and shows:
- Modulation analysis
- Encoded data detection
- Analysis results

### Step 4: Explore Different Sectors
```
SCAN BETA-2
FOCUS SIG_1
ANALYZE
```

## 🔧 Function Keys (Work Now!)

- **F1** - Focus Main Spectrum Analyzer panel
- **F2** - Focus Signal Focus & Data panel  
- **F3** - Focus Cartography & Navigation panel
- **F4** - Focus Decoder & Analysis Toolkit panel
- **F5** - Focus Captain's Log & Database panel
- **Ctrl+H** - Show help
- **Ctrl+C** - Quit

## 🗺️ Available Sectors

- **ALPHA-1** (default) - 3-4 signals, good for beginners
- **BETA-2** - 2-3 signals, intermediate difficulty  
- **GAMMA-3** - 1-2 signals, advanced/rare signals

## 💡 Pro Tips

1. **Always scan first** - No signals = empty displays
2. **Focus before analyzing** - You need a focused signal to analyze
3. **Check the log** - All command results appear in Captain's Log (F5)
4. **Try different sectors** - Each has unique signal types
5. **Use function keys** - Switch between panels quickly

## 🐛 Troubleshooting

- **Can't type commands?** - Click in the command input at the bottom
- **Function keys not working?** - They should work now globally
- **Empty panels?** - Run `SCAN` first to populate with data
- **"No signal focused" error?** - Use `FOCUS SIG_1` first

## 🎊 You're Ready to Play!

The game is now fully functional. Start with `SCAN`, then `FOCUS SIG_1`, then `ANALYZE` to see the full experience. Have fun exploring the mysterious signals from the void! 🛸 