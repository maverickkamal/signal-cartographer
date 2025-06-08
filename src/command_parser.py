"""
Command parser for the AetherTap CLI interface
Handles parsing and executing player commands
"""

from typing import Optional, Dict, Callable, Any


class CommandParser:
    """
    Parses and executes commands entered in the CLI
    """
    
    def __init__(self):
        self.game_state: Optional[Any] = None
        
        # Command registry
        self.commands: Dict[str, Callable] = {
            'help': self.cmd_help,
            'scan': self.cmd_scan,
            'focus': self.cmd_focus,
            'analyze': self.cmd_analyze,
            'status': self.cmd_status,
            'save': self.cmd_save,
            'load': self.cmd_load,
            'quit': self.cmd_quit,
            'exit': self.cmd_quit,
            'clear': self.cmd_clear,
        }
        
        # Command aliases
        self.aliases = {
            'h': 'help',
            's': 'scan',
            'f': 'focus',
            'a': 'analyze',
            'q': 'quit',
        }
    
    def set_game_state(self, game_state: Any):
        """Set reference to the main game state"""
        self.game_state = game_state
    
    def parse_and_execute(self, command_str: str) -> str:
        """Parse a command string and execute it"""
        if not command_str.strip():
            return ""
        
        # Split command and arguments
        parts = command_str.strip().split()
        cmd_name = parts[0].lower()
        args = parts[1:]
        
        # Check for aliases
        if cmd_name in self.aliases:
            cmd_name = self.aliases[cmd_name]
        
        # Execute command
        if cmd_name in self.commands:
            try:
                return self.commands[cmd_name](args)
            except Exception as e:
                return f"Command execution error: {e}"
        else:
            return f"Unknown command: {cmd_name}. Type HELP for available commands."
    
    def cmd_help(self, args: list) -> str:
        """Show available commands"""
        if args and args[0].lower() in self.commands:
            # Show help for specific command
            cmd = args[0].lower()
            help_text = {
                'scan': 'SCAN [sector] - Scan for signals in current or specified sector',
                'focus': 'FOCUS <signal_id> - Focus on a specific signal for analysis',
                'analyze': 'ANALYZE - Analyze the currently focused signal',
                'status': 'STATUS - Show current system status',
                'save': 'SAVE [filename] - Save current game state',
                'load': 'LOAD [filename] - Load saved game state',
                'help': 'HELP [command] - Show help for all commands or specific command',
                'quit': 'QUIT - Exit the AetherTap interface',
                'clear': 'CLEAR - Clear the command log'
            }
            return help_text.get(cmd, f"No help available for {cmd}")
        
        # Show all commands
        return ("Available commands:\n" +
                "  SCAN [sector] - Scan for signals\n" +
                "  FOCUS <id> - Focus on signal\n" +
                "  ANALYZE - Analyze focused signal\n" +
                "  SAVE [file] - Save game state\n" +
                "  LOAD [file] - Load game state\n" +
                "  STATUS - Show system status\n" +
                "  HELP [cmd] - Show help\n" +
                "  QUIT - Exit interface\n" +
                "Type HELP <command> for detailed information.")
    
    def cmd_scan(self, args: list) -> str:
        """Scan for signals"""
        if not self.game_state:
            return "System error: No game state available"
        
        # Determine sector to scan
        if args:
            sector = args[0].upper()
            target_sector = sector
        else:
            target_sector = self.game_state.get_current_sector()
        
        # Update scan count for progress tracking
        if not hasattr(self.game_state, 'total_scan_count'):
            self.game_state.total_scan_count = 0
        self.game_state.total_scan_count += 1
        
        # Perform scanning
        from .signal_system import SignalDetector
        detector = SignalDetector()
        signals = detector.scan_sector(target_sector)
        
        # Update the spectrum display
        if hasattr(self.game_state, 'aethertap') and self.game_state.aethertap:
            self.game_state.aethertap.update_spectrum(signals)
        
        # Track discovered sectors
        if not hasattr(self.game_state, 'discovered_sectors'):
            self.game_state.discovered_sectors = []
        if target_sector not in self.game_state.discovered_sectors:
            self.game_state.discovered_sectors.append(target_sector)
        
        if signals:
            signal_list = ", ".join([f"SIG_{i+1}" for i in range(len(signals))])
            return f"Scan complete. Found {len(signals)} signals in {target_sector}: {signal_list}"
        else:
            return f"Scan complete. No signals detected in {target_sector}."
    
    def cmd_focus(self, args: list) -> str:
        """Focus on a specific signal"""
        if not args:
            return "Usage: FOCUS <signal_id> (e.g., FOCUS SIG_1)"
        
        signal_id = args[0].upper()
        
        # For now, simulate focusing on a signal
        if signal_id.startswith('SIG_'):
            try:
                signal_num = int(signal_id[4:])  # Extract number from SIG_N
                
                # Create a mock signal object
                from .signal_system import Signal
                mock_signal = Signal(
                    id=signal_id,
                    frequency=100.0 + signal_num * 10.0,
                    strength=0.5 + (signal_num % 5) * 0.1,
                    modulation="Pulsed-Echo",
                    sector=self.game_state.get_current_sector()
                )
                
                # Update game state
                if self.game_state:
                    self.game_state.set_focused_signal(mock_signal)
                
                return f"Signal {signal_id} focused. Frequency: {mock_signal.frequency:.1f} MHz"
                
            except ValueError:
                return f"Invalid signal ID format: {signal_id}"
        else:
            return f"Signal {signal_id} not found. Use SCAN first to detect signals."
    
    def cmd_analyze(self, args: list) -> str:
        """Analyze the currently focused signal"""
        if not self.game_state or not self.game_state.get_focused_signal():
            return "No signal currently focused. Use FOCUS <signal_id> first."
        
        signal = self.game_state.get_focused_signal()
        
        # Update analysis count for progress tracking
        if not hasattr(self.game_state, 'total_analysis_count'):
            self.game_state.total_analysis_count = 0
        self.game_state.total_analysis_count += 1
        
        # Track analyzed signals
        if not hasattr(self.game_state, 'analyzed_signals'):
            self.game_state.analyzed_signals = []
        if signal.id not in self.game_state.analyzed_signals:
            self.game_state.analyzed_signals.append(signal.id)
        
        # Update decoder panel if available
        if hasattr(self.game_state, 'aethertap') and self.game_state.aethertap:
            analysis_result = (f"Signal {signal.id} Analysis:\n" +
                             f"Frequency: {signal.frequency:.1f} MHz\n" +
                             f"Strength: {signal.strength:.2f}\n" +
                             f"Modulation: {signal.modulation}\n" +
                             f"Sector: {signal.sector}")
            self.game_state.aethertap.update_decoder(analysis_result)
        
        # For now, simulate basic analysis
        return (f"Analyzing signal {signal.id}...\n" +
                f"Modulation type: {signal.modulation}\n" +
                f"Signal appears to contain encoded data.\n" +
                "Advanced decoding tools required for full analysis.")
    
    def cmd_status(self, args: list) -> str:
        """Show current system status"""
        if not self.game_state:
            return "System error: No game state available"
        
        sector = self.game_state.get_current_sector()
        freq_range = self.game_state.get_frequency_range()
        focused = self.game_state.get_focused_signal()
        
        # Get progress stats
        scan_count = getattr(self.game_state, 'total_scan_count', 0)
        analysis_count = getattr(self.game_state, 'total_analysis_count', 0)
        discovered = getattr(self.game_state, 'discovered_sectors', [])
        
        status = f"=== AetherTap System Status ===\n"
        status += f"Current Sector: {sector}\n"
        status += f"Frequency Range: {freq_range[0]:.1f} - {freq_range[1]:.1f} MHz\n"
        status += f"Focused Signal: {focused.id if focused else 'None'}\n"
        status += f"Sectors Discovered: {len(discovered)}\n"
        status += f"Total Scans: {scan_count}\n"
        status += f"Total Analyses: {analysis_count}\n"
        status += f"System Status: Operational"
        
        return status
    
    def cmd_save(self, args: list) -> str:
        """Save the current game state"""
        if not self.game_state:
            return "System error: No game state available"
        
        # Import save system
        from .utils.save_system import SaveSystem
        save_system = SaveSystem()
        
        # Determine filename
        filename = None
        if args:
            filename = args[0]
            if not filename.endswith('.json'):
                filename += '.json'
        
        # Perform save
        success = save_system.save_game(self.game_state, filename)
        
        if success:
            save_name = filename if filename else "autosave.json"
            return f"Game saved successfully: {save_name}"
        else:
            return "Save failed. Check permissions and disk space."
    
    def cmd_load(self, args: list) -> str:
        """Load a saved game state"""
        if not self.game_state:
            return "System error: No game state available"
        
        # Import save system
        from .utils.save_system import SaveSystem
        save_system = SaveSystem()
        
        # Determine filename
        filename = None
        if args:
            filename = args[0]
            if not filename.endswith('.json'):
                filename += '.json'
        
        # Load save data
        save_data = save_system.load_game(filename)
        
        if save_data is None:
            save_name = filename if filename else "autosave.json"
            return f"Load failed: {save_name} not found or corrupted."
        
        # Apply save data
        success = save_system.apply_save_data(save_data, self.game_state)
        
        if success:
            save_name = filename if filename else "autosave.json"
            # Update interface if available
            if hasattr(self.game_state, 'aethertap') and self.game_state.aethertap:
                # Force refresh of the interface
                sector = self.game_state.get_current_sector()
                self.game_state.aethertap.update_map(sector)
                
                # Update focused signal display if any
                focused = self.game_state.get_focused_signal()
                if focused:
                    self.game_state.aethertap.focus_signal(focused)
            
            return f"Game loaded successfully: {save_name}"
        else:
            return "Load failed: Error applying save data."

    def cmd_quit(self, args: list) -> str:
        """Quit the game"""
        if self.game_state:
            self.game_state.quit_game()
        return "Shutting down AetherTap interface..."
    
    def cmd_clear(self, args: list) -> str:
        """Clear the command log"""
        if self.game_state and hasattr(self.game_state, 'aethertap') and self.game_state.aethertap:
            self.game_state.aethertap.log_entries = ["Command log cleared."]
            self.game_state.aethertap._update_log_pane()
        return "Command log cleared." 