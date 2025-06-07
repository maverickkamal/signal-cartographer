"""
Input handler for the AetherTap interface
"""

from typing import Optional, Callable
from textual.widgets import Input
from textual.events import Key

class CommandInput(Input):
    """Command input widget for AetherTap"""
    
    def __init__(self, command_handler: Optional[Callable] = None, **kwargs):
        super().__init__(
            placeholder="🎮 TYPE COMMANDS HERE → Try: SCAN, HELP, FOCUS SIG_1...", 
            **kwargs
        )
        self.command_handler = command_handler
        self.last_command = ""
    
    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle command submission when Enter is pressed"""
        command = event.value.strip()
        if command:
            self.last_command = command
            
            # Show command being executed (immediate feedback)
            self.placeholder = f"🚀 EXECUTING: {command.upper()}..."
            
            # Call the command handler if set
            if self.command_handler:
                try:
                    self.command_handler(command)
                    # Success feedback
                    self.placeholder = f"✅ EXECUTED: {command.upper()} | Type next command..."
                except Exception as e:
                    # Error feedback  
                    self.placeholder = f"❌ ERROR: {str(e)} | Try again..."
            
            # Clear the input for next command
            self.value = ""
            
            # Reset placeholder after 4 seconds
            self.set_timer(4.0, self._reset_placeholder)
    
    def _reset_placeholder(self):
        """Reset placeholder to default"""
        self.placeholder = "🎮 TYPE COMMANDS HERE → Try: SCAN, HELP, FOCUS SIG_1..."

class AetherTapInputHandler:
    """Basic input handler for compatibility"""
    
    def __init__(self, app):
        self.app = app
        self.commands = {}
    
    def register_command_callback(self, command: str, callback: Callable):
        """Register a command callback"""
        self.commands[command] = callback
    
    async def handle_command(self, command: str):
        """Handle a command"""
        parts = command.split()
        if parts:
            cmd = parts[0].lower()
            if cmd in self.commands:
                await self.commands[cmd](parts[1:])
            else:
                await self._handle_default_command(cmd, parts[1:])
    
    async def _handle_default_command(self, command: str, args: list):
        """Handle unknown commands"""
        await self._add_log_entry(f"Unknown command: {command}")
    
    async def _show_help(self):
        """Show help"""
        help_text = """
Available Commands:
  SCAN [sector] - Scan for signals
  FOCUS <signal_id> - Focus on a signal
  ANALYZE - Analyze focused signal
  STATUS - Show system status
  HELP - Show this help
  QUIT - Exit application
"""
        await self._add_log_entry(help_text)
    
    async def _clear_logs(self):
        """Clear logs"""
        await self._add_log_entry("Logs cleared")
    
    async def _add_log_entry(self, message: str):
        """Add a log entry"""
        # This would be implemented to add to the log pane
        print(f"LOG: {message}")
