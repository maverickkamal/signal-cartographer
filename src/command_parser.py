"""
Command parser for the AetherTap CLI interface
Handles parsing and executing player commands
"""

import time
from typing import Optional, Dict, Callable, Any

# Performance optimization imports
try:
    from .performance_optimizations import (
        performance_monitor,
        debounce,
        memory_manager,
        render_cache,
        error_handler
    )
    PERFORMANCE_AVAILABLE = True
except ImportError:
    PERFORMANCE_AVAILABLE = False
    
    def performance_monitor(func):
        return func
    
    def debounce(wait_time):
        def decorator(func):
            return func
        return decorator


class CommandParser:
    """
    Parses and executes commands entered in the CLI
    """
    
    def __init__(self):
        self.game_state: Optional[Any] = None
        self.last_command_time = {}  # For command throttling
        
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
            'upgrades': self.cmd_upgrades,
            'achievements': self.cmd_achievements,
            'progress': self.cmd_progress,
            'performance': self.cmd_performance,
        }
        
        # Command aliases
        self.aliases = {
            'h': 'help',
            's': 'scan',
            'f': 'focus',
            'a': 'analyze',
            'q': 'quit',
            'perf': 'performance',
        }
    
    def set_game_state(self, game_state: Any):
        """Set reference to the main game state"""
        self.game_state = game_state
    
    @performance_monitor
    def parse_and_execute(self, command_str: str) -> str:
        """Parse a command string and execute it"""
        if not command_str.strip():
            return ""
        
        # Command throttling - prevent spam
        current_time = time.time()
        cmd_hash = hash(command_str.strip().lower())
        
        if cmd_hash in self.last_command_time:
            if current_time - self.last_command_time[cmd_hash] < 0.1:  # 100ms throttle
                return "[dim]Command throttled - please wait[/dim]"
        
        self.last_command_time[cmd_hash] = current_time
        
        try:
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
                    result = self.commands[cmd_name](args)
                    
                    # Memory management for large responses
                    if memory_manager and len(str(result)) > 1000:
                        memory_manager.track_object(result)
                    
                    return result
                except Exception as e:
                    if error_handler:
                        return error_handler.handle_error(
                            e, f"command_{cmd_name}",
                            lambda: f"Command execution error: {e}"
                        )
                    else:
                        return f"Command execution error: {e}"
            else:
                return f"Unknown command: {cmd_name}. Type HELP for available commands."
                
        except Exception as e:
            if error_handler:
                return error_handler.handle_error(
                    e, "command_parsing",
                    lambda: "Command parsing error - please try again"
                )
            else:
                return "Command parsing error - please try again"
    
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
                'clear': 'CLEAR - Clear the command log',
                'upgrades': 'UPGRADES - Show or purchase upgrades',
                'achievements': 'ACHIEVEMENTS - Show achievement progress',
                'progress': 'PROGRESS - Show overall progression summary',
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
                "  UPGRADES - Show or purchase upgrades\n" +
                "  ACHIEVEMENTS - Show achievement progress\n" +
                "  PROGRESS - Show overall progression summary\n" +
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
        
        # Update current sector if changed
        if target_sector != self.game_state.get_current_sector():
            self.game_state.set_current_sector(target_sector)
        
        # Update scan count for progress tracking
        if not hasattr(self.game_state, 'total_scan_count'):
            self.game_state.total_scan_count = 0
        self.game_state.total_scan_count += 1
        
        # Perform scanning
        from .signal_system import SignalDetector
        detector = SignalDetector()
        signals = detector.scan_sector(target_sector)
        
        # Apply upgrade effects if available
        if hasattr(self.game_state, 'get_upgrade_effects'):
            effects = self.game_state.get_upgrade_effects()
            # Apply signal strength boost
            if effects['signal_strength_boost'] > 0:
                for signal in signals:
                    signal.strength = min(1.0, signal.strength * (1 + effects['signal_strength_boost']))
            # Apply noise reduction (could add more noise signals without filter)
            if effects['noise_reduction'] > 0:
                # Remove some noise signals based on filter strength
                signals = [s for s in signals if not (s.modulation in ['Static-Burst', 'Cosmic-Noise', 'Solar-Interference'] and effects['noise_reduction'] > 0.5)]
        
        # Store the scanned signals for the FOCUS command
        if not hasattr(self.game_state, 'last_scan_signals'):
            self.game_state.last_scan_signals = {}
        self.game_state.last_scan_signals[target_sector] = signals
        
        # Update the spectrum display and cartography pane
        if hasattr(self.game_state, 'aethertap') and self.game_state.aethertap:
            self.game_state.aethertap.update_spectrum(signals)
            # Update cartography pane with new sector and signals
            self.game_state.aethertap.update_map(target_sector, signals=signals)
        
        # Track discovered sectors
        if not hasattr(self.game_state, 'discovered_sectors'):
            self.game_state.discovered_sectors = []
        if target_sector not in self.game_state.discovered_sectors:
            self.game_state.discovered_sectors.append(target_sector)
        
        # Progression tracking
        if hasattr(self.game_state, 'on_scan_completed'):
            self.game_state.on_scan_completed(target_sector, len(signals))
        
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
        
        # Try to find the real signal from the last scan
        if signal_id.startswith('SIG_'):
            try:
                signal_num = int(signal_id[4:])  # Extract number from SIG_N
                
                # Get the real signals from the last scan
                current_sector = self.game_state.get_current_sector()
                if (hasattr(self.game_state, 'last_scan_signals') and 
                    current_sector in self.game_state.last_scan_signals):
                    
                    signals = self.game_state.last_scan_signals[current_sector]
                    if 1 <= signal_num <= len(signals):
                        # Use the real signal from the scan
                        real_signal = signals[signal_num - 1]  # Convert to 0-indexed
                        real_signal.id = signal_id  # Update ID to match user input
                        
                        # Update game state
                        self.game_state.set_focused_signal(real_signal)
                        
                        # Update the focus pane if available
                        if hasattr(self.game_state, 'aethertap') and self.game_state.aethertap:
                            self.game_state.aethertap.focus_signal(real_signal)
                        
                        return (f"Signal {signal_id} focused.\n" +
                                f"Frequency: {real_signal.frequency:.1f} MHz\n" +
                                f"Modulation: {real_signal.modulation}\n" +
                                f"Strength: {real_signal.strength:.2f}")
                    else:
                        return f"Signal {signal_id} not found. Only {len(signals)} signals detected in current scan."
                else:
                    return f"No scan data available for {current_sector}. Use SCAN first to detect signals."
                
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
        
        # Progression tracking
        achievement_msg = ""
        if hasattr(self.game_state, 'on_analysis_completed'):
            achievement_msg = self.game_state.on_analysis_completed(signal)
        
        # Basic analysis result
        base_result = (f"Analyzing signal {signal.id}...\n" +
                      f"Modulation type: {signal.modulation}\n" +
                      f"Signal appears to contain encoded data.\n" +
                      "Advanced decoding tools required for full analysis.")
        
        # Add achievement notification if earned
        if achievement_msg:
            base_result += f"\n\n{achievement_msg}"
        
        return base_result
    
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
    
    def cmd_upgrades(self, args: list) -> str:
        """Show or purchase upgrades"""
        if not hasattr(self.game_state, 'progression'):
            return "Progression system not available."
        
        progression = self.game_state.progression
        
        if not args:
            # Show available upgrades
            result = "=== UPGRADE SYSTEM ===\n"
            result += f"Analysis Points: {progression.analysis_points}\n\n"
            
            # Available upgrades
            available = progression.get_available_upgrades()
            if available:
                result += "Available Upgrades:\n"
                for upgrade in available:
                    result += f"  {upgrade.icon} {upgrade.name} (Cost: {upgrade.cost} points)\n"
                    result += f"     {upgrade.description}\n"
            else:
                result += "No upgrades available. Complete more analyses to unlock upgrades.\n"
            
            # Purchased upgrades
            purchased = progression.get_purchased_upgrades()
            if purchased:
                result += "\nPurchased Upgrades:\n"
                for upgrade in purchased:
                    result += f"  ✅ {upgrade.icon} {upgrade.name} - ACTIVE\n"
            
            result += f"\nUsage: UPGRADES BUY <upgrade_name>"
            return result
        
        elif args[0].upper() == 'BUY' and len(args) > 1:
            # Purchase upgrade
            upgrade_name = '_'.join(args[1:]).lower()
            
            if progression.can_purchase_upgrade(upgrade_name):
                if progression.purchase_upgrade(upgrade_name):
                    upgrade = progression.upgrades[upgrade_name]
                    return f"✅ Upgrade purchased: {upgrade.name}!\n{upgrade.description}"
                else:
                    return "❌ Failed to purchase upgrade."
            else:
                return "❌ Cannot purchase upgrade. Check availability and cost."
        
        else:
            return "Usage: UPGRADES or UPGRADES BUY <upgrade_name>"
    
    def cmd_achievements(self, args: list) -> str:
        """Show achievement progress"""
        if not hasattr(self.game_state, 'progression'):
            return "Progression system not available."
        
        progression = self.game_state.progression
        
        result = "=== ACHIEVEMENTS ===\n"
        
        # Unlocked achievements
        unlocked = progression.get_unlocked_achievements()
        if unlocked:
            result += f"Unlocked ({len(unlocked)}/{len(progression.achievements)}):\n"
            for achievement in unlocked:
                unlock_date = achievement.unlock_date or "Unknown"
                result += f"  🏆 {achievement.icon} {achievement.name}\n"
                result += f"     {achievement.description}\n"
        
        # Progress on remaining achievements
        result += "\nProgress:\n"
        for achievement in progression.achievements.values():
            if not achievement.unlocked and not achievement.hidden:
                progress_pct = (achievement.progress / achievement.target) * 100
                result += f"  📊 {achievement.name}: {achievement.progress}/{achievement.target} ({progress_pct:.1f}%)\n"
        
        return result
    
    def cmd_progress(self, args: list) -> str:
        """Show overall progression summary"""
        if not hasattr(self.game_state, 'progression'):
            return "Progression system not available."
        
        summary = self.game_state.progression.get_progression_summary()
        
        result = "=== PROGRESSION SUMMARY ===\n"
        result += f"Analysis Points: {summary['analysis_points']}\n"
        result += f"Achievements: {summary['achievements_unlocked']}/{summary['total_achievements']}\n"
        result += f"Upgrades: {summary['upgrades_purchased']}/{summary['total_upgrades']}\n\n"
        
        result += "Statistics:\n"
        stats = summary['stats']
        result += f"  Total Scans: {stats['total_scans']}\n"
        result += f"  Total Analyses: {stats['total_analyses']}\n"
        result += f"  Sectors Discovered: {stats['sectors_discovered']}\n"
        result += f"  Unique Signals Found: {len(stats['unique_signals'])}\n"
        
        if summary['next_unlock']:
            result += f"\nNext Achievement: {summary['next_unlock']}"
        
        return result
    
    def cmd_performance(self, args: list) -> str:
        """Show performance statistics and controls"""
        try:
            from .performance_optimizations import (
                memory_manager,
                render_cache,
                error_handler
            )
            
            result = "=== PERFORMANCE STATISTICS ===\n"
            
            # Memory stats
            if memory_manager:
                mem_stats = memory_manager.get_memory_stats()
                result += f"Memory - Tracked Objects: {mem_stats['tracked_objects']}\n"
                result += f"Memory - Allocations: {mem_stats['allocation_count']}\n"
                result += f"Memory - Last Cleanup: {mem_stats['last_cleanup']:.1f}s ago\n"
            
            # Cache stats
            if render_cache:
                cache_stats = render_cache.get_stats()
                result += f"Cache - Size: {cache_stats['size']}/{cache_stats['max_size']}\n"
                result += f"Cache - Hit Rate: {cache_stats['hit_rate']:.1%}\n"
                result += f"Cache - Hits: {cache_stats['hit_count']}\n"
            
            # Error stats
            if error_handler:
                error_stats = error_handler.get_error_stats()
                result += f"Errors - Total: {error_stats['total_errors']}\n"
                if error_stats['error_counts']:
                    result += "Error Types:\n"
                    for error_type, count in error_stats['error_counts'].items():
                        result += f"  {error_type}: {count}\n"
            
            # Game performance stats
            if hasattr(self.game_state, 'total_scan_count'):
                result += f"Game - Total Scans: {self.game_state.total_scan_count}\n"
            
            if hasattr(self.game_state, 'progression'):
                stats = self.game_state.progression.get_progression_summary()['stats']
                result += f"Game - Total Analyses: {stats['total_analyses']}\n"
                result += f"Game - Sectors Discovered: {stats['sectors_discovered']}\n"
            
            # Commands
            if args and args[0].lower() == 'cleanup':
                # Perform manual cleanup
                cleanup_count = 0
                if memory_manager:
                    cleanup_count = memory_manager.cleanup()
                if render_cache:
                    cache_size_before = render_cache.get_stats()['size']
                    # Clear old cache entries
                    for _ in range(cache_size_before // 2):
                        render_cache._evict_oldest()
                    cache_size_after = render_cache.get_stats()['size']
                    result += f"\nCleanup completed. Cache reduced from {cache_size_before} to {cache_size_after} entries."
                result += f"\nMemory cleanup freed {cleanup_count} objects."
            
            elif args and args[0].lower() == 'clear':
                # Clear all caches
                if render_cache:
                    render_cache.clear()
                result += "\nAll caches cleared."
            
            else:
                result += "\nCommands: PERFORMANCE CLEANUP, PERFORMANCE CLEAR"
            
            return result
            
        except ImportError:
            return "Performance monitoring not available."
        except Exception as e:
            return f"Performance command error: {str(e)}" 