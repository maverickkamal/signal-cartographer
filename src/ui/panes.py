"""
Individual pane managers for the AetherTap interface - PHASE 10 ENHANCED
"""

from typing import List, Optional, Any, Dict, Tuple
from textual.widgets import Static, RichLog
from textual.containers import Container, Vertical, ScrollableContainer
from textual.app import ComposeResult
from rich.text import Text
from rich.console import Console
from textual.reactive import reactive
import random
import math
import time

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
    """Enhanced Main Spectrum Analyzer pane [MSA] - Phase 10.1"""
    
    def __init__(self, **kwargs):
        super().__init__("Main Spectrum Analyzer [MSA]", **kwargs)
        self.signals = []
        self.frequency_range = (100, 200)
        self.noise_level = 0.1
        self.animation_frame = 0
        self.signal_animations = {}
        self.noise_pattern = []
        self.last_update = time.time()
        
        # Generate persistent noise background
        self._generate_noise_background()
    
    def _generate_noise_background(self):
        """Generate persistent noise background pattern"""
        width = 64
        self.noise_pattern = []
        for i in range(width):
            # Create realistic noise using multiple frequency components
            noise_val = 0
            noise_val += 0.3 * math.sin(i * 0.1) * random.uniform(0.7, 1.3)
            noise_val += 0.2 * math.sin(i * 0.05) * random.uniform(0.8, 1.2)
            noise_val += 0.1 * random.uniform(-1, 1)
            noise_val = max(0, min(1, 0.1 + noise_val * 0.1))  # Keep noise level reasonable
            self.noise_pattern.append(noise_val)
        
    def update_spectrum(self, signals: List[Any], freq_range: tuple, noise: float = 0.1):
        """Update the spectrum display with enhanced visualization and animation"""
        self.signals = signals
        self.frequency_range = freq_range
        self.noise_level = noise
        
        # Initialize signal animations for new signals
        for signal in signals:
            if hasattr(signal, 'id') and signal.id not in self.signal_animations:
                self.signal_animations[signal.id] = {
                    'phase': random.random() * 2 * math.pi,
                    'pulse_rate': random.uniform(0.05, 0.15),
                    'drift_rate': random.uniform(-0.02, 0.02),
                    'stability_variance': getattr(signal, 'stability', 1.0)
                }
        
        # Generate enhanced spectrum display
        spectrum_lines = self._generate_enhanced_spectrum()
        self.update_content(spectrum_lines)
    
        # Increment animation frame
        self.animation_frame += 1
        self.last_update = time.time()
    
    def _generate_enhanced_spectrum(self) -> List[str]:
        """Generate enhanced ASCII art spectrum with animations and noise"""
        lines = []
        width = 64
        height = 12
        
        if not self.signals:
            return self._generate_no_signal_display(width)
        
        # Enhanced header with comprehensive information
        lines.append(f"[bold yellow]Frequency Range:[/bold yellow] {self.frequency_range[0]:.1f}-{self.frequency_range[1]:.1f} MHz")
        lines.append(f"[dim]Noise Floor:[/dim] {self.noise_level:.3f} | [dim]Sensitivity:[/dim] High | [dim]Bandwidth:[/dim] {self.frequency_range[1]-self.frequency_range[0]:.1f} MHz")
        lines.append("[cyan]" + "█" * width + "[/cyan]")
        
        # Generate spectrum visualization with enhanced graphics
        spectrum_data = self._calculate_spectrum_data(width, height)
        
        for row in range(height):
            line = ""
            row_intensity = (height - row) / height  # Higher rows = higher intensity
            
            for col in range(width):
                intensity = spectrum_data[col]
                char, color = self._get_spectrum_char(intensity, row_intensity)
                if color:
                    line += f"[{color}]{char}[/{color}]"
                else:
                    line += char
            
            lines.append(line)
        
        # Enhanced footer with signal information
        lines.append("[cyan]" + "█" * width + "[/cyan]")
        lines.append(f"[bold green]Active Signals:[/bold green] {len(self.signals)}")
        
        # Signal details bar
        signal_info = []
        for i, signal in enumerate(self.signals[:3]):  # Show first 3 signals
            signal_id = getattr(signal, 'id', f'SIG_{i+1}')
            freq = getattr(signal, 'frequency', 0)
            strength = getattr(signal, 'strength', 0)
            signal_info.append(f"[yellow]{signal_id}[/yellow]:{freq:.1f}MHz([white]{strength:.2f}[/white])")
        
        if signal_info:
            lines.append(" | ".join(signal_info))
        
        # Real-time status indicators
        lines.append(f"[dim]Frame:[/dim] {self.animation_frame} | [dim]Last Update:[/dim] {time.time() - self.last_update:.1f}s ago")
        
        return lines
    
    def _calculate_spectrum_data(self, width: int, height: int) -> List[float]:
        """Calculate spectrum intensity data for enhanced visualization with animation"""
        spectrum_data = []
        freq_step = (self.frequency_range[1] - self.frequency_range[0]) / width
        
        for col in range(width):
            freq = self.frequency_range[0] + col * freq_step
            intensity = self.noise_pattern[col % len(self.noise_pattern)]
            
            # Add signal contributions with enhanced animation
            for signal in self.signals:
                if hasattr(signal, 'frequency'):
                    signal_freq = signal.frequency
                    signal_strength = getattr(signal, 'strength', 0.5)
                    signal_id = getattr(signal, 'id', 'unknown')
                    
                    # Calculate distance from signal frequency
                    freq_distance = abs(freq - signal_freq)
                    if freq_distance < 5:  # Signal influence range
                        # Get animation parameters
                        anim = self.signal_animations.get(signal_id, {})
                        phase = anim.get('phase', 0)
                        pulse_rate = anim.get('pulse_rate', 0.1)
                        drift_rate = anim.get('drift_rate', 0)
                        stability = anim.get('stability_variance', 1.0)
                        
                        # Calculate animated signal strength with pulsing
                        time_factor = self.animation_frame * pulse_rate
                        pulse_modifier = 0.8 + 0.2 * math.sin(phase + time_factor)
                        
                        # Apply stability variance
                        stability_modifier = 1.0 + (1.0 - stability) * 0.3 * math.sin(time_factor * 0.7)
                        
                        # Calculate signal contribution with Gaussian falloff
                        signal_contribution = signal_strength * pulse_modifier * stability_modifier
                        signal_contribution *= math.exp(-0.5 * (freq_distance / 2.0) ** 2)
                        
                        intensity += signal_contribution
                        
                        # Update animation phase for next frame
                        anim['phase'] = phase + drift_rate
            
            spectrum_data.append(min(1.0, max(0.0, intensity)))
        
        return spectrum_data
    
    def _get_spectrum_char(self, intensity: float, row_intensity: float) -> Tuple[str, Optional[str]]:
        """Convert intensity to appropriate character and color with enhanced visualization"""
        # Determine if this row should show the signal based on intensity
        show_signal = intensity >= row_intensity
        
        if not show_signal:
            return "·", "dim"
        
        # Enhanced character selection based on signal strength with color coding
        if intensity > 0.9:
            return "█", "bright_red"
        elif intensity > 0.8:
            return "█", "red"
        elif intensity > 0.7:
            return "▓", "bright_yellow"
        elif intensity > 0.6:
            return "▓", "yellow"
        elif intensity > 0.5:
            return "▒", "bright_green"
        elif intensity > 0.4:
            return "▒", "green"
        elif intensity > 0.3:
            return "░", "bright_cyan"
        elif intensity > 0.2:
            return "░", "cyan"
        else:
            return "·", "blue"
    
    def _generate_no_signal_display(self, width: int) -> List[str]:
        """Generate enhanced display when no signals are detected"""
        lines = []
        lines.append(f"[bold yellow]Frequency Range:[/bold yellow] {self.frequency_range[0]:.1f}-{self.frequency_range[1]:.1f} MHz")
        lines.append(f"[dim]Noise Floor:[/dim] {self.noise_level:.3f} | [dim]Status:[/dim] Scanning... | [dim]Sensitivity:[/dim] Maximum")
        lines.append("[cyan]" + "█" * width + "[/cyan]")
        lines.append("")
        
        # Show animated scanning pattern
        scan_pos = (self.animation_frame // 2) % width
        scan_line = "·" * scan_pos + "▓▒░" + "·" * (width - scan_pos - 3)
        if scan_pos > width - 3:
            scan_line = "·" * width
        lines.append(f"[yellow]{scan_line}[/yellow]")
        
        for _ in range(6):
            # Show enhanced noise floor with subtle animation
            noise_line = ""
            for i in range(width):
                if random.random() < 0.05:
                    noise_line += random.choice(["·", "░"])
                else:
                    noise_line += "·"
            lines.append(f"[dim]{noise_line}[/dim]")
        
        lines.append("")
        lines.append("[cyan]" + "█" * width + "[/cyan]")
        lines.append("[bold red]No signals detected[/bold red]")
        lines.append("")
        lines.append("[yellow]>>> Run 'SCAN' command to detect signals <<<[/yellow]")
        lines.append("")
        lines.append("[green]Available sectors:[/green]")
        lines.append("  [cyan]ALPHA-1[/cyan] - Training sector (3 weak signals)")
        lines.append("  [cyan]BETA-2[/cyan] - Standard sector (2 medium signals)")
        lines.append("  [cyan]GAMMA-3[/cyan] - Deep space sector (1 strong signal)")
        lines.append("")
        lines.append("[dim]Example:[/dim] Type 'SCAN BETA-2' to scan a different sector")
        lines.append(f"[dim]Animation Frame:[/dim] {self.animation_frame} | [dim]Noise Samples:[/dim] {len(self.noise_pattern)}")
        
        return lines

class SignalFocusPane(BasePane):
    """Enhanced Signal Focus & Data pane [SFD] - Phase 10.2"""
    
    def __init__(self, **kwargs):
        super().__init__("Signal Focus & Data [SFD]", **kwargs)
        self.focused_signal = None
        self.signal_history = []
        self.analysis_frame = 0
        self.last_analysis_time = time.time()
        
        # Signal classification systems
        self.modulation_types = {
            'AM': {'name': 'Amplitude Modulation', 'complexity': 1},
            'FM': {'name': 'Frequency Modulation', 'complexity': 2}, 
            'PSK': {'name': 'Phase Shift Keying', 'complexity': 3},
            'QAM': {'name': 'Quadrature Amplitude', 'complexity': 4},
            'Pulsed': {'name': 'Pulse Modulated', 'complexity': 2},
            'Pulsed-Echo': {'name': 'Echo Pulse System', 'complexity': 5},
            'Unknown': {'name': 'Unclassified Pattern', 'complexity': 1}
        }
        
        self.band_classifications = {
            'Low-Band': (50, 120),
            'Mid-Band': (120, 180), 
            'High-Band': (180, 250)
        }
    
    def focus_signal(self, signal: Any):
        """Enhanced signal focusing with comprehensive analysis"""
        self.focused_signal = signal
        self.analysis_frame += 1
        self.last_analysis_time = time.time()
        
        if signal:
            # Add to signal history for tracking
            if hasattr(signal, 'id'):
                signal_entry = {
                    'id': signal.id,
                    'timestamp': time.time(),
                    'frequency': getattr(signal, 'frequency', 0),
                    'strength': getattr(signal, 'strength', 0)
                }
                self.signal_history.append(signal_entry)
                
                # Keep only last 10 entries
                if len(self.signal_history) > 10:
                    self.signal_history = self.signal_history[-10:]
            
            self._display_enhanced_signal_details()
        else:
            self._display_focus_placeholder()
    
    def _display_focus_placeholder(self):
        """Enhanced placeholder display with focusing instructions"""
        placeholder_lines = [
            "[bold yellow]🎯 Signal Focus & Analysis System[/bold yellow]",
            "",
            "[dim]Status:[/dim] No signal focused",
            "[dim]Analysis Frame:[/dim] " + str(self.analysis_frame),
            "[dim]Signal History:[/dim] " + str(len(self.signal_history)) + " entries",
            "",
            "[cyan]═══ HOW TO FOCUS SIGNALS ═══[/cyan]",
            "",
            "[green]Step 1:[/green] Run '[yellow]SCAN[/yellow]' to detect signals",
            "[green]Step 2:[/green] Use '[yellow]FOCUS SIG_1[/yellow]' to focus on signal",
            "[green]Step 3:[/green] Signal analysis will appear here",
            "[green]Step 4:[/green] Use '[yellow]ANALYZE[/yellow]' for deep analysis",
            "",
            "[cyan]Available Focus Commands:[/cyan]",
            "• [yellow]FOCUS SIG_1[/yellow] - Focus first detected signal",
            "• [yellow]FOCUS SIG_2[/yellow] - Focus second detected signal", 
            "• [yellow]FOCUS SIG_3[/yellow] - Focus third detected signal",
            "• [yellow]ANALYZE[/yellow] - Analyze currently focused signal",
            "",
            "[cyan]Analysis Capabilities:[/cyan]",
            "• Signal strength & stability monitoring",
            "• Modulation type classification",
            "• ASCII signal signature generation",
            "• Frequency precision analysis",
            "• Origin coordinate estimation",
            "• Quality assessment & recommendations"
        ]
        self.update_content(placeholder_lines)
    
    def _display_enhanced_signal_details(self):
        """Display comprehensive signal analysis with visual indicators"""
        if not self.focused_signal:
            return
            
        lines = []
        signal = self.focused_signal
        
        # Header with signal identification
        lines.append(f"[bold cyan]🎯 SIGNAL ANALYSIS: {getattr(signal, 'id', 'UNKNOWN')}[/bold cyan]")
        lines.append("═" * 60)
        
        # Core signal properties with enhanced display
        frequency = getattr(signal, 'frequency', 0)
        strength = getattr(signal, 'strength', 0)
        stability = getattr(signal, 'stability', 1.0)
        modulation = getattr(signal, 'modulation', 'Unknown')
        
        lines.append(f"[yellow]Frequency:[/yellow] {frequency:.3f} MHz")
        lines.append(f"[yellow]Strength:[/yellow] {strength:.3f} ({self._get_strength_description(strength)})")
        lines.append(f"[yellow]Stability:[/yellow] {stability:.3f} ({self._get_stability_description(stability)})")
        lines.append(f"[yellow]Modulation:[/yellow] {modulation} - {self.modulation_types.get(modulation, {'name': 'Unknown'})['name']}")
        
        # Visual strength and stability indicators
        lines.append("")
        lines.append("[cyan]═══ SIGNAL METRICS ═══[/cyan]")
        lines.append(f"[green]Strength:[/green] {self._create_progress_bar(strength, 50, '█', '░')}")
        lines.append(f"[blue]Stability:[/blue] {self._create_progress_bar(stability, 50, '█', '░')}")
        
        # Signal classification system
        lines.append("")
        lines.append("[cyan]═══ CLASSIFICATION ═══[/cyan]")
        band_class = self._classify_frequency_band(frequency)
        power_level = self._classify_power_level(strength)
        complexity = self.modulation_types.get(modulation, {'complexity': 1})['complexity']
        
        lines.append(f"[yellow]Band Class:[/yellow] {band_class}")
        lines.append(f"[yellow]Power Level:[/yellow] {power_level}")
        lines.append(f"[yellow]Complexity:[/yellow] {'●' * complexity}{'○' * (5-complexity)} ({complexity}/5)")
        
        # Enhanced ASCII signal signature based on modulation type
        lines.append("")
        lines.append("[cyan]═══ SIGNAL SIGNATURE ═══[/cyan]")
        signature = self._generate_enhanced_signature(signal)
        lines.extend(signature)
        
        # Signal quality assessment and analysis recommendations
        lines.append("")
        lines.append("[cyan]═══ ANALYSIS ASSESSMENT ═══[/cyan]")
        quality_score = self._calculate_quality_score(signal)
        lines.append(f"[green]Overall Quality:[/green] {quality_score:.1f}/10.0")
        lines.append(f"[green]Assessment:[/green] {self._get_quality_assessment(quality_score)}")
        
        # Analysis recommendations
        recommendations = self._generate_recommendations(signal)
        if recommendations:
            lines.append("")
            lines.append("[yellow]📋 Recommendations:[/yellow]")
            lines.extend([f"  • {rec}" for rec in recommendations])
        
        # Signal origin and coordinate estimation
        lines.append("")
        lines.append("[cyan]═══ ORIGIN ANALYSIS ═══[/cyan]")
        origin_data = self._analyze_signal_origin(signal)
        lines.extend(origin_data)
        
        # Technical details and precision metrics
        lines.append("")
        lines.append("[cyan]═══ TECHNICAL DETAILS ═══[/cyan]")
        lines.append(f"[dim]Analysis Frame:[/dim] {self.analysis_frame}")
        lines.append(f"[dim]Focus Time:[/dim] {time.time() - self.last_analysis_time:.1f}s ago")
        lines.append(f"[dim]Signal History:[/dim] {len(self.signal_history)} entries")
        lines.append(f"[dim]Frequency Precision:[/dim] ±{self._calculate_frequency_precision(signal):.4f} MHz")
        
        self.update_content(lines)
    
    def _get_strength_description(self, strength: float) -> str:
        """Get descriptive text for signal strength"""
        if strength >= 0.9: return "Extremely Strong"
        elif strength >= 0.7: return "Strong"
        elif strength >= 0.5: return "Moderate" 
        elif strength >= 0.3: return "Weak"
        else: return "Very Weak"
    
    def _get_stability_description(self, stability: float) -> str:
        """Get descriptive text for signal stability"""
        if stability >= 0.95: return "Rock Solid"
        elif stability >= 0.85: return "Very Stable"
        elif stability >= 0.70: return "Stable"
        elif stability >= 0.50: return "Fluctuating"
        else: return "Highly Unstable"
    
    def _create_progress_bar(self, value: float, width: int, fill_char: str, empty_char: str) -> str:
        """Create a visual progress bar"""
        filled = int(value * width)
        empty = width - filled
        bar = fill_char * filled + empty_char * empty
        percentage = value * 100
        return f"│{bar}│ {percentage:.1f}%"
    
    def _classify_frequency_band(self, frequency: float) -> str:
        """Classify frequency into band categories"""
        for band, (low, high) in self.band_classifications.items():
            if low <= frequency <= high:
                return band
        return "Extended-Band"
    
    def _classify_power_level(self, strength: float) -> str:
        """Classify signal power level"""
        if strength >= 0.8: return "High Power"
        elif strength >= 0.5: return "Medium Power"
        elif strength >= 0.2: return "Low Power"
        else: return "Minimal Power"
    
    def _generate_enhanced_signature(self, signal: Any) -> List[str]:
        """Generate enhanced ASCII signal signatures based on modulation type"""
        modulation = getattr(signal, 'modulation', 'Unknown')
        strength = getattr(signal, 'strength', 0.5)
        
        signatures = {
            'AM': [
                "     ▁▂▄█▄▂▁     ▁▂▄█▄▂▁     ",
                "   ▁▂█████▂▁   ▁▂█████▂▁   ",
                " ▁▂███████▂▁ ▁▂███████▂▁ ",
                "▂██████████▂██████████▂",
                "Amplitude Modulated Carrier"
            ],
            'FM': [
                "▁▂▃▄▅▆▇█▇▆▅▄▃▂▁▂▃▄▅▆▇█▇▆▅▄▃▂▁",
                "▂▄▆█▆▄▂▁▂▄▆█▆▄▂▁▂▄▆█▆▄▂▁▂▄▆█",
                "█▆▄▂▁▂▄▆█▆▄▂▁▂▄▆█▆▄▂▁▂▄▆█▆▄▂",
                "Frequency Modulated Signal"
            ],
            'PSK': [
                "██▁▁██▁▁████▁▁██▁▁████▁▁██▁▁",
                "██  ██  ████  ██  ████  ██  ",
                "▀▀▄▄▀▀▄▄▀▀▀▀▄▄▀▀▄▄▀▀▀▀▄▄▀▀▄▄",
                "Phase Shift Keyed Data"
            ],
            'Pulsed': [
                "█ █ █   █ █   █ █ █   █ █   ",
                "█ █ █   █ █   █ █ █   █ █   ",
                "▀ ▀ ▀   ▀ ▀   ▀ ▀ ▀   ▀ ▀   ",
                "Pulsed Transmission Pattern"
            ],
            'Pulsed-Echo': [
                "█ ▄ ▁   █ ▄ ▁   █ ▄ ▁   █ ▄ ▁",
                "█ ▄ ▁   █ ▄ ▁   █ ▄ ▁   █ ▄ ▁",
                "▀ ▀ ▀   ▀ ▀ ▀   ▀ ▀ ▀   ▀ ▀ ▀",
                "Pulse-Echo Response System"
            ]
        }
        
        default_signature = [
            "▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░█▓▒░",
            "░▒▓█░▒▓█░▒▓█░▒▓█░▒▓█░▒▓█░▒▓",
            "▒▓█░▒▓█░▒▓█░▒▓█░▒▓█░▒▓█░▒▓█",
            "Unclassified Signal Pattern"
        ]
        
        signature = signatures.get(modulation, default_signature)
        
        # Add strength-based visual enhancement
        if strength > 0.8:
            signature = [f"[bright_red]{line}[/bright_red]" for line in signature[:-1]] + [signature[-1]]
        elif strength > 0.6:
            signature = [f"[yellow]{line}[/yellow]" for line in signature[:-1]] + [signature[-1]]
        elif strength > 0.4:
            signature = [f"[green]{line}[/green]" for line in signature[:-1]] + [signature[-1]]
        else:
            signature = [f"[dim]{line}[/dim]" for line in signature[:-1]] + [signature[-1]]
        
        # Add border
        border_line = "─" * 32
        return [border_line] + signature + [border_line]
    
    def _calculate_quality_score(self, signal: Any) -> float:
        """Calculate overall signal quality score"""
        strength = getattr(signal, 'strength', 0)
        stability = getattr(signal, 'stability', 1.0)
        modulation = getattr(signal, 'modulation', 'Unknown')
        
        # Base score from strength and stability
        score = (strength * 4) + (stability * 4)
        
        # Modulation complexity bonus
        complexity = self.modulation_types.get(modulation, {'complexity': 1})['complexity']
        score += (complexity / 5) * 2
        
        return min(10.0, score)
    
    def _get_quality_assessment(self, score: float) -> str:
        """Get quality assessment text"""
        if score >= 9.0: return "Exceptional - Ideal for analysis"
        elif score >= 7.5: return "Excellent - High confidence results"
        elif score >= 6.0: return "Good - Reliable analysis possible"
        elif score >= 4.5: return "Fair - Some analysis limitations"
        elif score >= 3.0: return "Poor - Enhanced filtering recommended"
        else: return "Critical - Signal enhancement required"
    
    def _generate_recommendations(self, signal: Any) -> List[str]:
        """Generate analysis recommendations based on signal properties"""
        recommendations = []
        strength = getattr(signal, 'strength', 0)
        stability = getattr(signal, 'stability', 1.0)
        modulation = getattr(signal, 'modulation', 'Unknown')
        
        if strength < 0.3:
            recommendations.append("Apply signal amplification filters")
            recommendations.append("Consider closer approach to source")
        
        if stability < 0.7:
            recommendations.append("Use stability enhancement protocols")
            recommendations.append("Multiple sampling recommended")
        
        if modulation == 'Unknown':
            recommendations.append("Run extended modulation analysis")
            recommendations.append("Check for non-standard encoding")
        
        complexity = self.modulation_types.get(modulation, {'complexity': 1})['complexity']
        if complexity >= 4:
            recommendations.append("Advanced decoding tools required")
            recommendations.append("Prepare for multi-stage analysis")
        
        if not recommendations:
            recommendations.append("Signal ready for standard analysis")
            recommendations.append("All parameters within normal range")
        
        return recommendations
    
    def _analyze_signal_origin(self, signal: Any) -> List[str]:
        """Analyze and estimate signal origin coordinates"""
        origin_lines = []
        
        # Mock coordinate analysis (in real implementation, this would use triangulation)
        frequency = getattr(signal, 'frequency', 0)
        strength = getattr(signal, 'strength', 0)
        
        # Estimate coordinates based on signal properties
        estimated_x = (frequency - 100) * 2.5
        estimated_y = strength * 100
        estimated_z = random.uniform(-50, 50)  # Mock Z coordinate
        
        origin_lines.append(f"[yellow]Estimated Coordinates:[/yellow]")
        origin_lines.append(f"  X: {estimated_x:.2f} units")
        origin_lines.append(f"  Y: {estimated_y:.2f} units") 
        origin_lines.append(f"  Z: {estimated_z:.2f} units")
        
        # Distance estimation
        distance = math.sqrt(estimated_x**2 + estimated_y**2 + estimated_z**2)
        origin_lines.append(f"[yellow]Distance:[/yellow] {distance:.1f} units")
        
        # Confidence assessment
        confidence = min(100, strength * 80 + 20)
        origin_lines.append(f"[yellow]Confidence:[/yellow] {confidence:.1f}%")
        
        # Direction indicator
        if estimated_x > 0:
            direction = "Starboard" 
        else:
            direction = "Port"
        origin_lines.append(f"[yellow]Direction:[/yellow] {direction} sector")
        
        return origin_lines
    
    def _calculate_frequency_precision(self, signal: Any) -> float:
        """Calculate frequency measurement precision"""
        strength = getattr(signal, 'strength', 0)
        stability = getattr(signal, 'stability', 1.0)
        
        # Higher strength and stability = better precision
        base_precision = 0.1
        precision = base_precision / (strength * stability + 0.1)
        return min(1.0, precision)

class CartographyPane(BasePane):
    """Enhanced Cartography & Navigation pane [CNP] - Phase 10.3"""
    
    def __init__(self, **kwargs):
        super().__init__("Cartography & Navigation [CNP]", **kwargs)
        self.current_sector = "ALPHA-1"
        self.known_locations = {}
        self.zoom_level = 1
        self.map_center_x = 0
        self.map_center_y = 0
        self.signal_sources = []
        self.anomalies = []
        self.exploration_data = {
            'sectors_discovered': ['ALPHA-1'],
            'total_sectors': 7,
            'signals_mapped': 0,
            'anomalies_found': 0,
            'exploration_percentage': 14.3
        }
        
        # Sector definitions with coordinates and difficulty
        self.sector_map = {
            'ALPHA-1': {'coords': (0, 0, 0), 'difficulty': 'Trainig', 'signals': 3, 'status': 'explored'},
            'BETA-2': {'coords': (50, 30, 10), 'difficulty': 'Standard', 'signals': 2, 'status': 'partially_explored'},
            'GAMMA-3': {'coords': (-30, 60, -20), 'difficulty': 'Deep Space', 'signals': 1, 'status': 'unexplored'},
            'DELTA-4': {'coords': (80, -40, 50), 'difficulty': 'High Risk', 'signals': 4, 'status': 'unexplored'},
            'EPSILON-5': {'coords': (-60, -30, 30), 'difficulty': 'Ancient', 'signals': 2, 'status': 'unexplored'},
            'ZETA-6': {'coords': (20, 90, -60), 'difficulty': 'Quantum', 'signals': 1, 'status': 'unexplored'},
            'ETA-7': {'coords': (0, 0, 100), 'difficulty': 'Void', 'signals': 5, 'status': 'unexplored'}
        }
        
        # Map marker types
        self.marker_types = {
            'signal': {'char': '📡', 'color': 'yellow'},
            'anomaly': {'char': '🌟', 'color': 'red'},
            'station': {'char': '🛰️', 'color': 'cyan'},
            'beacon': {'char': '🏮', 'color': 'green'},
            'hazard': {'char': '⚠️', 'color': 'bright_red'},
            'unknown': {'char': '❓', 'color': 'dim'}
        }
    
    def update_map(self, sector: str, locations: Dict[str, Any] = None, signals: List[Any] = None):
        """Enhanced map update with signal plotting and exploration tracking"""
        if sector in self.sector_map:
            self.current_sector = sector
            
            # Update exploration data
            if sector not in self.exploration_data['sectors_discovered']:
                self.exploration_data['sectors_discovered'].append(sector)
                self.exploration_data['exploration_percentage'] = (
                    len(self.exploration_data['sectors_discovered']) / 
                    self.exploration_data['total_sectors'] * 100
                )
            
            # Mark sector as at least partially explored
            if self.sector_map[sector]['status'] == 'unexplored':
                self.sector_map[sector]['status'] = 'partially_explored'
        
        if locations:
            self.known_locations.update(locations)
        
        if signals:
            self._update_signal_sources(signals)
        
        self._generate_enhanced_map_display()
    
    def _update_signal_sources(self, signals: List[Any]):
        """Update signal source plotting on the map"""
        self.signal_sources = []
        for signal in signals:
            if hasattr(signal, 'frequency') and hasattr(signal, 'strength'):
                # Convert signal properties to map coordinates
                freq = signal.frequency
                strength = signal.strength
                signal_id = getattr(signal, 'id', 'Unknown')
                
                # Mock coordinate calculation based on signal properties
                x = (freq - 150) * 0.5
                y = strength * 40
                z = random.uniform(-10, 10)
                
                signal_source = {
                    'id': signal_id,
                    'coords': (x, y, z),
                    'frequency': freq,
                    'strength': strength,
                    'marker_type': 'signal'
                }
                self.signal_sources.append(signal_source)
        
        self.exploration_data['signals_mapped'] = len(self.signal_sources)
    
    def zoom_in(self):
        """Increase zoom level for detailed view"""
        if self.zoom_level < 5:
            self.zoom_level += 1
            self._generate_enhanced_map_display()
    
    def zoom_out(self):
        """Decrease zoom level for wider view"""
        if self.zoom_level > 1:
            self.zoom_level -= 1
            self._generate_enhanced_map_display()
    
    def pan_map(self, dx: int, dy: int):
        """Pan the map view"""
        self.map_center_x += dx
        self.map_center_y += dy
        self._generate_enhanced_map_display()
    
    def _generate_enhanced_map_display(self):
        """Generate comprehensive ASCII star map with all enhanced features"""
        lines = []
        map_width = 60
        map_height = 20
        
        # Enhanced header with navigation information
        lines.append(f"[bold cyan]🗺️ STELLAR CARTOGRAPHY & NAVIGATION[/bold cyan]")
        lines.append("═" * 60)
        
        # Current position and navigation data
        current_coords = self.sector_map.get(self.current_sector, {'coords': (0, 0, 0)})['coords']
        lines.append(f"[yellow]Current Sector:[/yellow] {self.current_sector} | [yellow]Coordinates:[/yellow] {current_coords[0]:+.1f}, {current_coords[1]:+.1f}, {current_coords[2]:+.1f}")
        lines.append(f"[yellow]Zoom Level:[/yellow] {self.zoom_level}x | [yellow]View Center:[/yellow] ({self.map_center_x:+d}, {self.map_center_y:+d})")
        
        # Exploration progress
        exploration_pct = self.exploration_data['exploration_percentage']
        progress_bar = self._create_exploration_progress_bar(exploration_pct, 30)
        lines.append(f"[green]Exploration:[/green] {progress_bar} {exploration_pct:.1f}%")
        
        lines.append("─" * 60)
        
        # Generate star map grid
        star_map = self._generate_star_map_grid(map_width, map_height)
        
        # Add coordinate grid markers
        lines.append(self._generate_coordinate_header(map_width))
        
        for row_idx, row in enumerate(star_map):
            # Add Y coordinate marker every 5 rows
            if row_idx % 5 == 0:
                y_coord = (map_height // 2 - row_idx) * self.zoom_level + self.map_center_y
                row_line = f"{y_coord:+3d}│{row}│"
            else:
                row_line = f"   │{row}│"
            lines.append(row_line)
        
        lines.append("─" * (map_width + 8))
        
        # Map legend with all marker types
        lines.append(self._generate_map_legend())
        
        # Sector information panel
        lines.append("")
        lines.append("[cyan]═══ SECTOR DATABASE ═══[/cyan]")
        lines.extend(self._generate_sector_info())
        
        # Signal source tracking
        if self.signal_sources:
            lines.append("")
            lines.append("[cyan]═══ SIGNAL SOURCES ═══[/cyan]")
            lines.extend(self._generate_signal_tracking_info())
        
        # Navigation commands
        lines.append("")
        lines.append("[cyan]═══ NAVIGATION CONTROLS ═══[/cyan]")
        lines.append("[yellow]Zoom:[/yellow] + (zoom in) | - (zoom out)")
        lines.append("[yellow]Pan:[/yellow] ↑↓←→ (move view) | HOME (center)")
        lines.append("[yellow]Sectors:[/yellow] SCAN <sector> to explore")
        
        self.update_content(lines)
    
    def _generate_star_map_grid(self, width: int, height: int) -> List[str]:
        """Generate the main ASCII star map with markers and features"""
        star_map = []
        
        for row in range(height):
            line = ""
            for col in range(width):
                # Calculate actual coordinates for this position
                actual_x = (col - width // 2) * self.zoom_level + self.map_center_x
                actual_y = (height // 2 - row) * self.zoom_level + self.map_center_y
                
                char = self._get_map_character(actual_x, actual_y, col, row)
                line += char
            
            star_map.append(line)
        
        return star_map
    
    def _get_map_character(self, x: float, y: float, col: int, row: int) -> str:
        """Determine the character to display at this map position"""
        # Check for current sector marker
        current_coords = self.sector_map.get(self.current_sector, {'coords': (0, 0, 0)})['coords']
        if abs(x - current_coords[0]) < 2 and abs(y - current_coords[1]) < 2:
            return "[bright_green]⦿[/bright_green]"  # Current position
        
        # Check for other sector markers
        for sector, data in self.sector_map.items():
            sector_x, sector_y, _ = data['coords']
            if abs(x - sector_x) < 3 and abs(y - sector_y) < 3:
                if data['status'] == 'explored':
                    return "[green]●[/green]"
                elif data['status'] == 'partially_explored':
                    return "[yellow]◐[/yellow]"
                else:
                    return "[dim]◯[/dim]"
        
        # Check for signal sources
        for source in self.signal_sources:
            src_x, src_y, _ = source['coords']
            if abs(x - src_x) < 1.5 and abs(y - src_y) < 1.5:
                strength = source['strength']
                if strength > 0.7:
                    return "[bright_yellow]◆[/bright_yellow]"
                elif strength > 0.4:
                    return "[yellow]◇[/yellow]"
                else:
                    return "[dim]◇[/dim]"
        
        # Check for anomalies
        for anomaly in self.anomalies:
            ano_x, ano_y, _ = anomaly['coords']
            if abs(x - ano_x) < 2 and abs(y - ano_y) < 2:
                return "[red]✦[/red]"
        
        # Generate background stars and space
        if (x + y) % 17 == 0:
            return "[bright_white]✦[/bright_white]"  # Bright star
        elif (x * y) % 23 == 0:
            return "[white]·[/white]"  # Distant star
        elif (x + y * 2) % 31 == 0:
            return "[dim]·[/dim]"  # Very distant star
        elif abs(x) % 10 == 0 and abs(y) % 10 == 0:
            return "[dim]┼[/dim]"  # Grid reference
        else:
            return " "  # Empty space
    
    def _generate_coordinate_header(self, width: int) -> str:
        """Generate coordinate header for the map"""
        header = "   │"
        for col in range(0, width, 10):
            coord = (col - width // 2) * self.zoom_level + self.map_center_x
            header += f"{coord:+4.0f}     "
        header += "│"
        return f"[dim]{header}[/dim]"
    
    def _create_exploration_progress_bar(self, percentage: float, width: int) -> str:
        """Create exploration progress bar"""
        filled = int((percentage / 100) * width)
        empty = width - filled
        bar = "█" * filled + "░" * empty
        return f"│{bar}│"
    
    def _generate_map_legend(self) -> str:
        """Generate comprehensive map legend"""
        legend_lines = []
        legend_lines.append("[cyan]═══ MAP LEGEND ═══[/cyan]")
        legend_lines.append("[bright_green]⦿[/bright_green] Current Position  [green]●[/green] Explored Sector  [yellow]◐[/yellow] Partially Explored  [dim]◯[/dim] Unexplored")
        legend_lines.append("[bright_yellow]◆[/bright_yellow] Strong Signal     [yellow]◇[/yellow] Medium Signal    [dim]◇[/dim] Weak Signal        [red]✦[/red] Anomaly")
        legend_lines.append("[bright_white]✦[/bright_white] Major Star        [white]·[/white] Star             [dim]·[/dim] Distant Star       [dim]┼[/dim] Grid Reference")
        return "\n".join(legend_lines)
    
    def _generate_sector_info(self) -> List[str]:
        """Generate sector information display"""
        info_lines = []
        
        # Current sector detailed info
        current_sector_data = self.sector_map.get(self.current_sector, {})
        coords = current_sector_data.get('coords', (0, 0, 0))
        difficulty = current_sector_data.get('difficulty', 'Unknown')
        signals = current_sector_data.get('signals', 0)
        status = current_sector_data.get('status', 'unknown')
        
        info_lines.append(f"[yellow]Current: {self.current_sector}[/yellow]")
        info_lines.append(f"  Coordinates: ({coords[0]:+.1f}, {coords[1]:+.1f}, {coords[2]:+.1f})")
        info_lines.append(f"  Difficulty: {difficulty} | Signals: {signals} | Status: {status.title()}")
        
        # Nearby sectors
        info_lines.append("")
        info_lines.append("[yellow]Nearby Sectors:[/yellow]")
        
        # Calculate distances to other sectors
        distances = []
        current_coords = current_sector_data.get('coords', (0, 0, 0))
        
        for sector, data in self.sector_map.items():
            if sector != self.current_sector:
                sector_coords = data['coords']
                distance = math.sqrt(
                    (current_coords[0] - sector_coords[0])**2 +
                    (current_coords[1] - sector_coords[1])**2 +
                    (current_coords[2] - sector_coords[2])**2
                )
                distances.append((distance, sector, data))
        
        # Sort by distance and show closest 3
        distances.sort(key=lambda x: x[0])
        for distance, sector, data in distances[:3]:
            status_icon = {'explored': '✓', 'partially_explored': '~', 'unexplored': '?'}
            icon = status_icon.get(data['status'], '?')
            info_lines.append(f"  {icon} {sector}: {distance:.1f} units ({data['difficulty']})")
        
        return info_lines
    
    def _generate_signal_tracking_info(self) -> List[str]:
        """Generate signal source tracking information"""
        tracking_lines = []
        
        for i, source in enumerate(self.signal_sources[:5]):  # Show first 5 signals
            signal_id = source['id']
            coords = source['coords']
            frequency = source['frequency']
            strength = source['strength']
            
            # Calculate distance from current position
            current_coords = self.sector_map.get(self.current_sector, {'coords': (0, 0, 0)})['coords']
            distance = math.sqrt(
                (coords[0] - current_coords[0])**2 +
                (coords[1] - current_coords[1])**2 +
                (coords[2] - current_coords[2])**2
            )
            
            tracking_lines.append(f"[yellow]{signal_id}:[/yellow] {frequency:.1f}MHz | Str:{strength:.2f} | Dist:{distance:.1f}u")
            tracking_lines.append(f"  Position: ({coords[0]:+.1f}, {coords[1]:+.1f}, {coords[2]:+.1f})")
        
        if len(self.signal_sources) > 5:
            tracking_lines.append(f"... and {len(self.signal_sources) - 5} more signals")
        
        return tracking_lines

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
