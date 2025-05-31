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
from .tutorial import TutorialMenuScreen

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
        """Display help information - now launches comprehensive tutorial system"""
        if self.aethertap_layout and self.aethertap_layout.log_pane:
            self.aethertap_layout.log_pane.add_log_entry("")
            self.aethertap_layout.log_pane.add_log_entry("🎓 Launching Tutorial Academy...")
            self.aethertap_layout.log_pane.add_log_entry("📚 Choose from 4 comprehensive tutorial sections")
            self.aethertap_layout.log_pane.add_log_entry("⌨️ Use number keys (1-4) or Escape to return")
            self.aethertap_layout.log_pane.add_log_entry("")
        
        # Launch the comprehensive tutorial system
        self.app.push_screen(TutorialMenuScreen())
    
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
    """Legacy help screen - replaced by comprehensive tutorial system"""
    
    BINDINGS = [
        Binding("enter", "back_to_game", "Return to Game"),
        Binding("escape", "back_to_game", "Return to Game"),
        Binding("ctrl+c", "quit", "Quit Game"),
    ]
    
    def compose(self) -> ComposeResult:
        """Compose the help screen - redirects to tutorial system"""
        yield Header(show_clock=False)
        with ScrollableContainer():
            yield Static(self._get_redirect_content(), id="help_content")
        yield Footer()
    
    def _get_redirect_content(self) -> str:
        """Show redirect message to new tutorial system"""
        return """[bold cyan]🎓 TUTORIAL SYSTEM UPGRADE 🎓[/bold cyan]

[bold yellow]═══════════════════════════════════════════════════════════════════════════════[/bold yellow]

[bold green]Welcome to the Enhanced Tutorial Academy![/bold green]

The help system has been upgraded to a comprehensive tutorial academy with:

[bold cyan]📚 Four Complete Tutorial Sections:[/bold cyan]
• 🎮 Gameplay Mechanics Tutorial
• ⌨️ Button Functions & Controls Guide  
• 🔧 Game Systems Overview
• 🔬 Signal Analysis Walkthrough

[bold green]🚀 Access the Tutorial Academy:[/bold green]
• Press [bold yellow]Ctrl+H[/bold yellow] from the main game
• Use the HELP command in the command input
• Navigate between sections with number keys (1-4)

[bold yellow]═══════════════════════════════════════════════════════════════════════════════[/bold yellow]

[bold green]Press Enter or Escape to return to AetherTap and try Ctrl+H![/bold green]

[dim]The comprehensive tutorial system provides much more detailed guidance[/dim]"""

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
        """Open comprehensive tutorial system"""
        self.app.push_screen(TutorialMenuScreen())
