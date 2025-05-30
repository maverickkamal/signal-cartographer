"""
Layout management for the AetherTap interface
"""

import asyncio
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import Header, Footer, Static, RichLog
from textual.screen import Screen
from textual.binding import Binding

from .panes import SpectrumPane, SignalFocusPane, CartographyPane, DecoderPane, LogPane
from .input_handler import CommandInput, AetherTapInputHandler
from .colors import AetherTapColors

class AetherTapLayout(Container):
    """Main layout container for the AetherTap interface"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spectrum_pane = None
        self.signal_focus_pane = None
        self.cartography_pane = None
        self.decoder_pane = None
        self.log_pane = None
        self.command_input = None
    
    def compose(self) -> ComposeResult:
        """Compose the layout"""
        # Top row: Spectrum and Signal Focus
        with Horizontal(id="top_row"):
            self.spectrum_pane = SpectrumPane(id="spectrum_pane")
            yield self.spectrum_pane
            self.signal_focus_pane = SignalFocusPane(id="signal_focus_pane")
            yield self.signal_focus_pane
        
        # Middle row: Cartography and Decoder
        with Horizontal(id="middle_row"):
            self.cartography_pane = CartographyPane(id="cartography_pane")
            yield self.cartography_pane
            self.decoder_pane = DecoderPane(id="decoder_pane")
            yield self.decoder_pane
        
        # Bottom section: Log and Command Input
        with Vertical(id="bottom_section"):
            self.log_pane = LogPane(id="log_pane")
            yield self.log_pane
            self.command_input = CommandInput(id="command_input")
            yield self.command_input

class AetherTapScreen(Screen):
    """Main screen for the AetherTap interface"""
    
    def __init__(self, game_controller=None, **kwargs):
        super().__init__(**kwargs)
        self.game_controller = game_controller
        self.aethertap_layout = None
    
    def compose(self) -> ComposeResult:
        """Compose the screen"""
        yield Header(show_clock=True)
        self.aethertap_layout = AetherTapLayout()
        yield self.aethertap_layout
        yield Footer()
    
    async def on_mount(self) -> None:
        """Initialize the screen after mounting"""
        # Set window title
        self.title = "AetherTap - Signal Cartographer"
        
        # Wait a moment for widgets to be fully mounted
        await asyncio.sleep(0.1)
        
        # Initialize panes with default content
        await self._initialize_panes()
        
        # Set up command input after panes are initialized
        if self.aethertap_layout and self.aethertap_layout.command_input:
            self.aethertap_layout.command_input.command_handler = self._handle_command
            # Focus on the command input to enable immediate typing
            self.aethertap_layout.command_input.focus()
            # Make sure it's visible
            if self.aethertap_layout.log_pane:
                self.aethertap_layout.log_pane.add_log_entry("")
                self.aethertap_layout.log_pane.add_log_entry("🎮 READY TO PLAY! Type commands in the PURPLE BOX below!")
                self.aethertap_layout.log_pane.add_log_entry("👉 Try: SCAN → FOCUS SIG_1 → ANALYZE")
                self.aethertap_layout.log_pane.add_log_entry("")
    
    def _handle_command(self, command: str):
        """Handle command input"""
        if not command.strip():
            return
            
        parts = command.strip().split()
        command_name = parts[0].lower()
        
        # Show command being executed immediately
        if self.aethertap_layout and self.aethertap_layout.log_pane:
            self.aethertap_layout.log_pane.add_log_entry(f"")
            self.aethertap_layout.log_pane.add_log_entry(f"🚀 EXECUTING: {command.upper()}")
            self.aethertap_layout.log_pane.add_log_entry(f"▶️ " + "="*40)
        
        # Handle basic commands
        if command_name in ['quit', 'exit', 'q']:
            self.app.exit()
        elif command_name == 'help':
            self._show_help()
        elif command_name == 'clear':
            self._clear_logs()
        else:
            # Pass to game's command parser
            if self.game_controller:
                result = self.game_controller.process_command(command)
                if result and self.aethertap_layout and self.aethertap_layout.log_pane:
                    # Show result with clear formatting
                    self.aethertap_layout.log_pane.add_log_entry(f"✅ RESULT:")
                    for line in result.split('\n'):
                        if line.strip():
                            self.aethertap_layout.log_pane.add_log_entry(f"   {line}")
                    self.aethertap_layout.log_pane.add_log_entry(f"◀️ " + "="*40)
                    
                    # Update displays based on command type
                    if command_name == 'scan':
                        # Update spectrum display
                        signals = self.game_controller.signal_detector.scan_sector(
                            self.game_controller.current_sector, self.game_controller.frequency_range
                        )
                        if self.aethertap_layout.spectrum_pane:
                            self.aethertap_layout.spectrum_pane.update_spectrum(
                                signals, self.game_controller.frequency_range
                            )
                        self.aethertap_layout.log_pane.add_log_entry(f"📊 Spectrum display updated!")
                        
                    elif command_name == 'focus':
                        # Update signal focus display
                        focused = self.game_controller.get_focused_signal()
                        if self.aethertap_layout.signal_focus_pane:
                            self.aethertap_layout.signal_focus_pane.focus_signal(focused)
                        self.aethertap_layout.log_pane.add_log_entry(f"🔍 Signal focus display updated!")
                        
                    elif command_name == 'analyze':
                        # Update decoder display with analysis results
                        if self.game_controller.focused_signal:
                            analysis_results = [
                                f"Signal Analysis Results:",
                                f"ID: {self.game_controller.focused_signal.id}",
                                f"Signature: {self.game_controller.focused_signal.signature}",
                                f"Stability: {self.game_controller.focused_signal.stability:.2f}",
                                f"Sector: {self.game_controller.focused_signal.sector}"
                            ]
                            if self.aethertap_layout.decoder_pane:
                                self.aethertap_layout.decoder_pane.update_content(analysis_results)
                            self.aethertap_layout.log_pane.add_log_entry(f"🛠️ Analysis results updated in decoder!")
                        
                else:
                    self.aethertap_layout.log_pane.add_log_entry(f"⚠️  No result returned for command: {command}")
            else:
                if self.aethertap_layout and self.aethertap_layout.log_pane:
                    self.aethertap_layout.log_pane.add_log_entry(f"❌ Unknown command: {command_name}")
                    self.aethertap_layout.log_pane.add_log_entry(f"💡 Type 'help' for available commands")
    
    def _show_help(self):
        """Display help information - now launches comprehensive help screen"""
        if self.aethertap_layout and self.aethertap_layout.log_pane:
            self.aethertap_layout.log_pane.add_log_entry("")
            self.aethertap_layout.log_pane.add_log_entry("🚀 Launching comprehensive help guide...")
            self.aethertap_layout.log_pane.add_log_entry("📖 Use Enter or Escape to return to AetherTap")
            self.aethertap_layout.log_pane.add_log_entry("")
        
        # Launch the detailed help screen
        self.app.push_screen(HelpScreen())
    
    def _clear_logs(self):
        """Clear the log pane"""
        if self.aethertap_layout and self.aethertap_layout.log_pane:
            self.aethertap_layout.log_pane.clear_logs()

    async def _initialize_panes(self):
        """Initialize all panes with default content"""
        if self.aethertap_layout:
            # Show startup sequence in log
            if self.aethertap_layout.log_pane:
                startup_messages = [
                    "=" * 60,
                    "  THE SIGNAL CARTOGRAPHER: ECHOES FROM THE VOID",
                    "  AetherTap Terminal Interface v1.2 - ENHANCED",
                    "=" * 60,
                    "",
                    "🔧 System Status:",
                    "✅ Quantum resonance chambers initialized",
                    "✅ Signal detection arrays calibrated",
                    "✅ Frequency databases loaded",
                    "✅ AetherTap ready for operation",
                    "",
                    "🎮 COMMAND INPUT IS THE PURPLE BOX AT BOTTOM!",
                    "👆 Look for the purple-bordered input box below ↓",
                    "",
                    "🚀 GETTING STARTED:",
                    "1. Type 'SCAN' in the purple box → Press Enter",
                    "2. Type 'FOCUS SIG_1' → Press Enter",
                    "3. Type 'ANALYZE' → Press Enter",  
                    "4. Press F1-F5 to switch between panels",
                    "5. Press Ctrl+H for full help guide",
                    "",
                    "💡 Watch how all 6 panels update as you type commands!",
                    "=" * 60
                ]
                
                for message in startup_messages:
                    self.aethertap_layout.log_pane.add_log_entry(message)
                
            # Initialize spectrum pane
            if self.aethertap_layout.spectrum_pane:
                self.aethertap_layout.spectrum_pane.update_spectrum([], (100, 200))
            
            # Initialize signal focus pane
            if self.aethertap_layout.signal_focus_pane:
                self.aethertap_layout.signal_focus_pane.focus_signal(None)
            
            # Initialize cartography pane
            if self.aethertap_layout.cartography_pane:
                self.aethertap_layout.cartography_pane.update_map("Alpha-1")
            
            # Initialize decoder pane
            if self.aethertap_layout.decoder_pane:
                self.aethertap_layout.decoder_pane.update_content(["No active analysis tool"])

class HelpScreen(Screen):
    """Comprehensive help screen with detailed gameplay instructions"""
    
    BINDINGS = [
        Binding("enter", "back_to_game", "Return to Game"),
        Binding("escape", "back_to_game", "Return to Game"),
        Binding("ctrl+c", "quit", "Quit Game"),
    ]
    
    def compose(self) -> ComposeResult:
        """Compose the help screen"""
        yield Header(show_clock=False)
        with ScrollableContainer():
            yield Static(self._get_help_content(), id="help_content")
        yield Footer()
    
    def _get_help_content(self) -> str:
        """Get comprehensive help content"""
        return """[bold cyan]🚀 THE SIGNAL CARTOGRAPHER - COMPLETE PLAYER GUIDE 🚀[/bold cyan]

[bold yellow]═══════════════════════════════════════════════════════════════════════════════[/bold yellow]

[bold green]🎯 GAME OBJECTIVE[/bold green]
You are a Signal Cartographer exploring the void of space, detecting and analyzing mysterious signals from unknown sources. Your mission is to scan different sectors, focus on interesting signals, and analyze them to uncover their secrets.

[bold green]🖥️ INTERFACE OVERVIEW[/bold green]
The AetherTap interface has 6 main panels:

[bold white]📊 Main Spectrum Analyzer (Top Left)[/bold white]
- Shows detected signals as frequency spikes
- Updates when you run SCAN commands
- Different sectors have different signal patterns

[bold white]🔍 Signal Focus & Data (Top Right)[/bold white]  
- Shows detailed information about a focused signal
- Updates when you use FOCUS commands
- Displays signal strength, frequency, and characteristics

[bold white]🗺️ Cartography & Navigation (Middle Left)[/bold white]
- Shows your current sector and zoom level
- Visual map of signal locations
- Updates based on your scanning activity

[bold white]🛠️ Decoder & Analysis Toolkit (Middle Right)[/bold white]
- Shows results of signal analysis
- Updates when you run ANALYZE commands
- Reveals hidden information about signals

[bold white]📜 Captain's Log & Database (Bottom Left)[/bold white]
- Shows command history and system messages
- Real-time feedback for all your actions
- System status and notifications

[bold white]💻 Command Input (Bottom Right - PURPLE BOX)[/bold white]
- Where you type all commands
- Has a bright purple/violet border
- Shows feedback when commands execute

[bold green]⌨️ ESSENTIAL COMMANDS[/bold green]

[bold cyan]📡 SCANNING COMMANDS:[/bold cyan]
[white]SCAN[/white] - Scan current sector (Alpha-1 by default)
[white]SCAN ALPHA-1[/white] - Scan Alpha-1 sector (3 signals - good for beginners)
[white]SCAN BETA-2[/white] - Scan Beta-2 sector (2 stronger signals)
[white]SCAN GAMMA-3[/white] - Scan Gamma-3 sector (1 powerful signal)

[bold cyan]🔍 SIGNAL ANALYSIS:[/bold cyan]
[white]FOCUS SIG_1[/white] - Focus on the first detected signal
[white]FOCUS SIG_2[/white] - Focus on the second detected signal
[white]FOCUS SIG_3[/white] - Focus on the third detected signal (if available)
[white]ANALYZE[/white] - Analyze the currently focused signal (reveals secrets!)

[bold cyan]📋 SYSTEM COMMANDS:[/bold cyan]
[white]STATUS[/white] - Show current system status and focused signal
[white]HELP[/white] - Show this comprehensive help (same as Ctrl+H)
[white]CLEAR[/white] - Clear the command log for a fresh start
[white]QUIT[/white] - Exit the game safely

[bold green]🎮 HOTKEYS & NAVIGATION[/bold green]

[bold cyan]Function Keys (Work Anywhere):[/bold cyan]
[white]F1[/white] - Focus on Main Spectrum Analyzer panel
[white]F2[/white] - Focus on Signal Focus & Data panel
[white]F3[/white] - Focus on Cartography & Navigation panel
[white]F4[/white] - Focus on Decoder & Analysis Toolkit panel
[white]F5[/white] - Focus on Captain's Log & Database panel

[bold cyan]Control Keys:[/bold cyan]
[white]Ctrl+H[/white] - Open this detailed help screen
[white]Ctrl+C[/white] - Quit the game safely
[white]Enter[/white] - (In help screen) Return to main game
[white]Escape[/white] - (In help screen) Return to main game

[bold green]🎯 HOW TO PLAY - STEP BY STEP[/bold green]

[bold cyan]Step 1: Start Scanning[/bold cyan]
Type: [white]SCAN[/white]
- This detects signals in the current sector
- Watch the Spectrum Analyzer panel update with signal spikes
- You'll see signals labeled as SIG_1, SIG_2, etc.

[bold cyan]Step 2: Focus on a Signal[/bold cyan]
Type: [white]FOCUS SIG_1[/white]
- This locks onto the first detected signal
- The Signal Focus panel shows detailed information
- You'll see frequency, strength, and characteristics

[bold cyan]Step 3: Analyze the Signal[/bold cyan]
Type: [white]ANALYZE[/white]
- This reveals hidden information about the focused signal
- Results appear in the Decoder & Analysis panel
- You might discover signal origins, purposes, or messages

[bold cyan]Step 4: Explore Different Sectors[/bold cyan]
Try: [white]SCAN BETA-2[/white] or [white]SCAN GAMMA-3[/white]
- Each sector has different signals
- Beta-2: Stronger, more complex signals
- Gamma-3: Single powerful signal with deep secrets

[bold cyan]Step 5: Use Hotkeys for Quick Navigation[/bold cyan]
- Press F1-F5 to quickly switch between panels
- Use this to monitor different aspects of your analysis

[bold green]💡 PRO TIPS[/bold green]

🔹 [white]Start with ALPHA-1[/white] - It has 3 signals, perfect for learning
🔹 [white]Always SCAN before FOCUS[/white] - You need signals to focus on
🔹 [white]Use STATUS[/white] to check what signal you're currently focused on
🔹 [white]Try different sectors[/white] - Each has unique signal characteristics
🔹 [white]Watch all panels[/white] - They update in real-time as you work
🔹 [white]Use CLEAR[/white] if your log gets too cluttered
🔹 [white]Press F5[/white] to see your command history anytime

[bold green]🚨 TROUBLESHOOTING[/bold green]

[bold red]Can't see signals?[/bold red] → Run SCAN first
[bold red]FOCUS not working?[/bold red] → Make sure you scanned and signals exist
[bold red]ANALYZE gives no results?[/bold red] → Focus on a signal first
[bold red]Can't type commands?[/bold red] → Click in the purple command box
[bold red]Panels not updating?[/bold red] → Commands are case-sensitive, try uppercase

[bold green]🌟 ADVANCED GAMEPLAY[/bold green]

Once you master the basics, try:
- Scanning all three sectors and comparing signal types
- Analyzing multiple signals in the same sector
- Using function keys to monitor multiple panels simultaneously
- Looking for patterns in signal characteristics across sectors
- Discovering hidden messages in analyzed signals

[bold yellow]═══════════════════════════════════════════════════════════════════════════════[/bold yellow]

[bold green]Ready to explore the void? Press ENTER to return to AetherTap![/bold green]

[dim]Press Enter or Escape to return to the main game interface[/dim]"""

    def action_back_to_game(self):
        """Return to the main game screen"""
        self.app.pop_screen()
    
    def action_quit(self):
        """Quit the application"""
        self.app.exit()

class AetherTapApp(App):
    """Main Textual application for AetherTap"""
    
    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit"),
        Binding("ctrl+h", "help", "Help"),
        Binding("f1", "focus_spectrum", "Focus Spectrum"),
        Binding("f2", "focus_signal", "Focus Signal"),
        Binding("f3", "focus_map", "Focus Map"),
        Binding("f4", "focus_decoder", "Focus Decoder"),
        Binding("f5", "focus_log", "Focus Log"),
    ]
    
    CSS = """
    Screen {
        background: #0d1117;
    }
    
    Container {
        border: solid #30363d;
        margin: 0;
        padding: 1;
    }
    
    .pane-title {
        background: #21262d;
        height: 1;
        text-align: center;
        border-bottom: solid #30363d;
        color: #58a6ff;
    }
    
    RichLog {
        background: #0d1117;
        color: #c9d1d9;
        border: none;
        scrollbar-background: #21262d;
        scrollbar-color: #58a6ff;
        min-height: 5;
    }
    
    BasePane {
        border: solid #58a6ff;
        margin: 0;
    }
    
    #top_row, #middle_row {
        height: 30%;
        min-height: 10;
    }
    
    #bottom_section {
        height: 40%;
        min-height: 12;
    }
    
    #spectrum_pane, #signal_focus_pane, #cartography_pane, #decoder_pane {
        width: 50%;
        min-width: 30;
    }
    
    #log_pane {
        height: 60%;
        min-height: 6;
        max-height: 15;
    }
    
    #command_input {
        height: 40%;
        min-height: 5;
        max-height: 8;
        border: solid #7c3aed;
        background: #1a1a2e;
        margin: 1;
        padding: 1;
    }
    
    CommandInput {
        background: #1a1a2e;
        color: #ffffff;
        border: solid #7c3aed;
        padding: 1;
        min-height: 3;
    }
    
    CommandInput:focus {
        border: solid #58a6ff;
        background: #0f1419;
    }
    
    Input {
        background: #1a1a2e;
        color: #ffffff;
        border: solid #7c3aed;
        padding: 1;
        min-height: 3;
    }
    
    Input:focus {
        border: solid #58a6ff;
        background: #0f1419;
    }
    
    Header {
        background: #21262d;
        color: #7c3aed;
        height: 1;
    }
    
    Footer {
        background: #21262d;
        color: #8b949e;
        height: 1;
    }
    
    /* Help Screen Styling */
    HelpScreen {
        background: #0d1117;
    }
    
    #help_content {
        background: #0d1117;
        color: #c9d1d9;
        padding: 2;
        margin: 1;
        border: solid #58a6ff;
    }
    
    ScrollableContainer {
        background: #0d1117;
        scrollbar-background: #21262d;
        scrollbar-color: #58a6ff;
    }
    """
    
    def __init__(self, game_controller=None, **kwargs):
        super().__init__(**kwargs)
        self.game_controller = game_controller
    
    async def on_mount(self) -> None:
        """Set up the application"""
        # Push the main screen
        await self.push_screen(AetherTapScreen(self.game_controller))
    
    def get_current_screen(self) -> AetherTapScreen:
        """Get the current AetherTap screen"""
        return self.screen
    
    def action_focus_spectrum(self):
        """Focus on the spectrum pane (F1)"""
        screen = self.get_current_screen()
        if screen and screen.aethertap_layout and screen.aethertap_layout.spectrum_pane:
            screen.aethertap_layout.spectrum_pane.focus()
            if screen.aethertap_layout.log_pane:
                screen.aethertap_layout.log_pane.add_log_entry("Focused on Main Spectrum Analyzer [MSA]")
    
    def action_focus_signal(self):
        """Focus on the signal focus pane (F2)"""
        screen = self.get_current_screen()
        if screen and screen.aethertap_layout and screen.aethertap_layout.signal_focus_pane:
            screen.aethertap_layout.signal_focus_pane.focus()
            if screen.aethertap_layout.log_pane:
                screen.aethertap_layout.log_pane.add_log_entry("Focused on Signal Focus & Data [SFD]")
    
    def action_focus_map(self):
        """Focus on the cartography pane (F3)"""
        screen = self.get_current_screen()
        if screen and screen.aethertap_layout and screen.aethertap_layout.cartography_pane:
            screen.aethertap_layout.cartography_pane.focus()
            if screen.aethertap_layout.log_pane:
                screen.aethertap_layout.log_pane.add_log_entry("Focused on Cartography & Navigation [CNP]")
    
    def action_focus_decoder(self):
        """Focus on the decoder pane (F4)"""
        screen = self.get_current_screen()
        if screen and screen.aethertap_layout and screen.aethertap_layout.decoder_pane:
            screen.aethertap_layout.decoder_pane.focus()
            if screen.aethertap_layout.log_pane:
                screen.aethertap_layout.log_pane.add_log_entry("Focused on Decoder & Analysis Toolkit [DAT]")
    
    def action_focus_log(self):
        """Focus on the log pane (F5)"""
        screen = self.get_current_screen()
        if screen and screen.aethertap_layout and screen.aethertap_layout.log_pane:
            screen.aethertap_layout.log_pane.focus()
            if screen.aethertap_layout.log_pane:
                screen.aethertap_layout.log_pane.add_log_entry("Focused on Captain's Log & Database [CLD]")
    
    def action_quit(self):
        """Quit the application (Ctrl+C)"""
        self.exit()
    
    def action_help(self):
        """Show comprehensive help screen (Ctrl+H)"""
        self.push_screen(HelpScreen())
