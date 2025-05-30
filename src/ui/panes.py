"""
Individual pane managers for the AetherTap interface
"""

from typing import List, Optional, Any, Dict
from textual.widgets import Static, RichLog
from textual.containers import Container, Vertical, ScrollableContainer
from textual.app import ComposeResult
from rich.text import Text
from rich.console import Console
from textual.reactive import reactive

from .colors import AetherTapColors

class BasePane(Static):
    """Base class for all AetherTap panes"""
    
    def __init__(self, title: str, *args, **kwargs):
        self.title = title
        self.content_lines = []
        initial_content = f"[bold cyan]{self.title}[/bold cyan]\n[dim]Initializing...[/dim]"
        super().__init__(initial_content, *args, **kwargs)
    
    def add_content_line(self, line: str):
        """Add a line to the pane content"""
        self.content_lines.append(line)
        self._update_display()
    
    def clear_content(self):
        """Clear the pane content"""
        self.content_lines = []
        self._update_display()
    
    def set_content(self, lines: list):
        """Set the entire content"""
        self.content_lines = lines[:]
        self._update_display()
    
    def _update_display(self):
        """Update the displayed content"""
        content = f"[bold cyan]{self.title}[/bold cyan]\n"
        if self.content_lines:
            content += "\n".join(self.content_lines)
        else:
            content += "[dim]No data[/dim]"
        self.update(content)
    
    def update_content(self, lines: List[str]):
        """Update the content of this pane"""
        self.set_content(lines)

class SpectrumPane(BasePane):
    """Main Spectrum Analyzer pane [MSA]"""
    
    def __init__(self, **kwargs):
        super().__init__("Main Spectrum Analyzer [MSA]", **kwargs)
        self.signals = []
        self.frequency_range = (100, 200)
        self.noise_level = 0.1
        
    def update_spectrum(self, signals: List[Any], freq_range: tuple, noise: float = 0.1):
        """Update the spectrum display with current signals"""
        self.signals = signals
        self.frequency_range = freq_range
        self.noise_level = noise
        
        # Generate ASCII spectrum display
        spectrum_lines = self._generate_spectrum_display()
        self.update_content(spectrum_lines)
    
    def _generate_spectrum_display(self) -> List[str]:
        """Generate ASCII art spectrum display"""
        lines = []
        width = 60
        height = 15
        
        # If no signals, show helpful message
        if not self.signals:
            lines.append(f"Frequency Range: {self.frequency_range[0]}-{self.frequency_range[1]} MHz")
            lines.append("=" * width)
            lines.append("")
            lines.append("[dim]No signals detected[/dim]")
            lines.append("")
            lines.append("[yellow]>> Run 'SCAN' command to detect signals <<[/yellow]")
            lines.append("")
            lines.append("Available sectors:")
            lines.append("  ALPHA-1 - Default sector (3 signals)")
            lines.append("  BETA-2  - Secondary sector (2 signals)")
            lines.append("  GAMMA-3 - Distant sector (1 signal)")
            lines.append("")
            lines.append("Example: Type 'SCAN BETA-2' to scan a different sector")
            lines.append("=" * width)
            lines.append("Detected Signals: 0")
            return lines
        
        # Header
        lines.append(f"Frequency Range: {self.frequency_range[0]}-{self.frequency_range[1]} MHz")
        lines.append("=" * width)
        
        # Generate spectrum
        for row in range(height):
            line = ""
            for col in range(width):
                # Calculate frequency position
                freq = self.frequency_range[0] + (col / width) * (self.frequency_range[1] - self.frequency_range[0])
                
                # Check if any signal is at this frequency
                signal_strength = self.noise_level
                for signal in self.signals:
                    if hasattr(signal, 'frequency') and abs(signal.frequency - freq) < 2:
                        signal_strength = max(signal_strength, getattr(signal, 'strength', 0.5))
                
                # Convert strength to visual representation
                if signal_strength > 0.8:
                    char = "█"
                elif signal_strength > 0.6:
                    char = "▓"
                elif signal_strength > 0.4:
                    char = "▒"
                elif signal_strength > 0.2:
                    char = "░"
                else:
                    char = "·"
                
                line += char
            lines.append(line)
        
        # Footer with signal count
        lines.append("=" * width)
        lines.append(f"Detected Signals: {len(self.signals)}")
        
        return lines

class SignalFocusPane(BasePane):
    """Signal Focus & Data pane [SFD]"""
    
    def __init__(self, **kwargs):
        super().__init__("Signal Focus & Data [SFD]", **kwargs)
        self.focused_signal = None
    
    def focus_signal(self, signal: Any):
        """Focus on a specific signal"""
        self.focused_signal = signal
        if signal:
            self._display_signal_details()
        else:
            placeholder_lines = [
                "[dim]No signal focused[/dim]",
                "",
                "[yellow]How to focus a signal:[/yellow]",
                "1. Run 'SCAN' to detect signals",
                "2. Use 'FOCUS SIG_1' to focus on signal",
                "3. Signal details will appear here",
                "",
                "[cyan]Available commands:[/cyan]",
                "• FOCUS SIG_1 - Focus first signal",
                "• FOCUS SIG_2 - Focus second signal", 
                "• ANALYZE - Analyze focused signal"
            ]
            self.update_content(placeholder_lines)
    
    def _display_signal_details(self):
        """Display detailed information about the focused signal"""
        if not self.focused_signal:
            return
            
        lines = []
        signal = self.focused_signal
        
        lines.append(f"Signal ID: {getattr(signal, 'id', 'Unknown')}")
        lines.append(f"Frequency: {getattr(signal, 'frequency', 'N/A')} MHz")
        lines.append(f"Strength: {getattr(signal, 'strength', 'N/A')}")
        lines.append(f"Modulation: {getattr(signal, 'modulation', 'Unknown')}")
        lines.append("")
        
        # Display signal signature (ASCII art)
        lines.append("Signal Signature:")
        lines.append("-" * 40)
        signature = getattr(signal, 'signature', ['[No signature available]'])
        if isinstance(signature, str):
            signature = [signature]
        lines.extend(signature)
        lines.append("-" * 40)
        
        # Additional properties
        if hasattr(signal, 'stability'):
            lines.append(f"Stability: {signal.stability}")
        if hasattr(signal, 'origin'):
            lines.append(f"Origin: {signal.origin}")
        
        self.update_content(lines)

class CartographyPane(BasePane):
    """Cartography & Navigation pane [CNP]"""
    
    def __init__(self, **kwargs):
        super().__init__("Cartography & Navigation [CNP]", **kwargs)
        self.current_sector = "Alpha-1"
        self.known_locations = {}
        self.zoom_level = 1
    
    def update_map(self, sector: str, locations: Dict[str, Any] = None):
        """Update the star map display"""
        self.current_sector = sector
        if locations:
            self.known_locations.update(locations)
        
        self._generate_map_display()
    
    def _generate_map_display(self):
        """Generate ASCII star map"""
        lines = []
        width = 50
        height = 20
        
        lines.append(f"Current Sector: {self.current_sector}")
        lines.append(f"Zoom Level: {self.zoom_level}x")
        lines.append("=" * width)
        
        # Generate simple star map
        for row in range(height):
            line = ""
            for col in range(width):
                # Add some stars and locations
                if (row + col) % 13 == 0:
                    line += "*"
                elif (row * col) % 17 == 0:
                    line += "·"
                else:
                    line += " "
            lines.append(line)
        
        lines.append("=" * width)
        lines.append(f"Known Locations: {len(self.known_locations)}")
        
        self.update_content(lines)

class DecoderPane(BasePane):
    """Decoder & Analysis Toolkit pane [DAT]"""
    
    def __init__(self, **kwargs):
        super().__init__("Decoder & Analysis Toolkit [DAT]", **kwargs)
        self.current_tool = None
        self.analysis_data = None
    
    def start_analysis(self, tool_name: str, signal: Any):
        """Start analysis with a specific tool"""
        self.current_tool = tool_name
        self.analysis_data = signal
        self._display_analysis_interface()
    
    def _display_analysis_interface(self):
        """Display the analysis interface"""
        lines = []
        
        if self.current_tool:
            lines.append(f"Active Tool: {self.current_tool}")
            lines.append("=" * 40)
            
            if self.current_tool == "pattern_matching":
                lines.extend(self._pattern_matching_display())
            elif self.current_tool == "cipher_analysis":
                lines.extend(self._cipher_analysis_display())
            else:
                lines.append(f"Tool '{self.current_tool}' interface loading...")
                lines.append("")
                lines.append("Available commands:")
                lines.append("  ANALYZE - Start analysis")
                lines.append("  RESET - Reset tool")
        else:
            lines.append("No active analysis tool")
            lines.append("")
            lines.append("Available tools:")
            lines.append("  pattern_matching")
            lines.append("  cipher_analysis")
            lines.append("  frequency_analysis")
        
        self.update_content(lines)
    
    def _pattern_matching_display(self) -> List[str]:
        """Display pattern matching interface"""
        lines = []
        lines.append("Pattern Matching Analysis")
        lines.append("")
        lines.append("Signal pattern:")
        lines.append("▓▒░█▓▒░█▓▒░")
        lines.append("")
        lines.append("Known patterns:")
        lines.append("A: ▓▒░█")
        lines.append("B: █▓▒░")
        lines.append("C: ░▒▓█")
        lines.append("")
        lines.append("Match found: Pattern A-B-A")
        return lines
    
    def _cipher_analysis_display(self) -> List[str]:
        """Display cipher analysis interface"""
        lines = []
        lines.append("Cipher Analysis")
        lines.append("")
        lines.append("Encrypted text:")
        lines.append("KHOOR ZRUOG")
        lines.append("")
        lines.append("Frequency analysis:")
        lines.append("O: 3, R: 2, K: 1, H: 1...")
        lines.append("")
        lines.append("Suggested: Caesar cipher, shift=3")
        lines.append("Decrypted: HELLO WORLD")
        return lines

class LogPane(BasePane):
    """Captain's Log & Database pane [CLD]"""
    
    def __init__(self, **kwargs):
        super().__init__("Captain's Log & Database [CLD]", **kwargs)
        self.log_entries: List[str] = []
    
    def add_log_entry(self, entry: str):
        """Add a new log entry"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_entry = f"[dim]{timestamp}[/dim] {entry}"
        self.log_entries.append(formatted_entry)
        
        # Update the display with all log entries
        self._update_log_display()
    
    def _update_log_display(self):
        """Update the log display with all entries"""
        # Show the last 20 entries to avoid overwhelming the display
        display_entries = self.log_entries[-20:] if len(self.log_entries) > 20 else self.log_entries
        self.update_content(display_entries)
    
    def clear_logs(self):
        """Clear all log entries"""
        self.log_entries.clear()
        self.update_content(["Log cleared."])
    
    def search_logs(self, keyword: str) -> List[str]:
        """Search log entries for a keyword"""
        matching_entries = [entry for entry in self.log_entries if keyword.lower() in entry.lower()]
        return matching_entries
