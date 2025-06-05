import random
from typing import Optional, TYPE_CHECKING

# To avoid circular imports, if SignalDefinition is needed for type hinting:
if TYPE_CHECKING:
    from src.content.signal_types import SignalDefinition

# Import the art library
from src.content.ascii_art_library import (
    SIGNAL_SIGNATURES,
    UPGRADE_SCHEMATICS,
    UI_DECORATIONS,
    STAR_MAP_ELEMENTS, # New import
    ENVIRONMENTAL_ART  # New import
)

class SignalArtManager:
    """
    Manages retrieval of ASCII art for signals and related visual elements.
    """
    def __init__(self):
        # Store references to the imported dictionaries
        self.signal_signatures_library = SIGNAL_SIGNATURES
        self.upgrade_schematics_library = UPGRADE_SCHEMATICS
        self.ui_decorations_library = UI_DECORATIONS
        self.star_map_elements_library = STAR_MAP_ELEMENTS         # New
        self.environmental_art_library = ENVIRONMENTAL_ART         # New

    def get_signal_signature_art(self, signal_def: 'SignalDefinition') -> Optional[str]:
        """
        Retrieves the ASCII art for a given signal definition based on its
        ascii_signature_category.

        Args:
            signal_def: The SignalDefinition object.

        Returns:
            The ASCII art string if found, otherwise None.
        """
        if not signal_def or not signal_def.ascii_signature_category:
            return None
        
        return self.signal_signatures_library.get(signal_def.ascii_signature_category)

    def get_upgrade_schematic_art(self, schematic_name: str) -> Optional[str]:
        """
        Retrieves ASCII art for a given upgrade schematic name.

        Args:
            schematic_name: The key for the schematic in UPGRADE_SCHEMATICS.

        Returns:
            The ASCII art string if found, otherwise None.
        """
        return self.upgrade_schematics_library.get(schematic_name)

    def get_ui_decoration_art(self, decoration_name: str) -> Optional[str]:
        """
        Retrieves ASCII art for a given UI decoration name.

        Args:
            decoration_name: The key for the decoration in UI_DECORATIONS.

        Returns:
            The ASCII art string if found, otherwise None.
        """
        return self.ui_decorations_library.get(decoration_name)

    def get_ui_spinner_frame(self, frame_number: int, base_name: str = "LOADING_SPINNER_FRAME") -> Optional[str]:
        """
        Retrieves a specific frame for a spinner animation.
        Assumes spinner frames are named like "BASE_NAME_1", "BASE_NAME_2", etc.

        Args:
            frame_number: The 1-indexed frame number to retrieve.
            base_name: The base name of the spinner frames in the library.

        Returns:
            The ASCII art string for the frame if found, otherwise None.
        """
        if frame_number <= 0:
            return None
        frame_key = f"{base_name}_{frame_number}"
        return self.ui_decorations_library.get(frame_key)

    def get_star_map_element_art(self, element_name: str) -> Optional[str]:
        """
        Retrieves ASCII art for a given star map element name.

        Args:
            element_name: The key for the element in STAR_MAP_ELEMENTS.

        Returns:
            The ASCII art string if found, otherwise None.
        """
        return self.star_map_elements_library.get(element_name)

    def get_environmental_art(self, art_name: str) -> Optional[str]:
        """
        Retrieves ASCII art for a given environmental art name.

        Args:
            art_name: The key for the art piece in ENVIRONMENTAL_ART.

        Returns:
            The ASCII art string if found, otherwise None.
        """
        return self.environmental_art_library.get(art_name)

    # --- Procedural Generation ---

    def generate_starfield(self, width: int, height: int, density: float = 0.05) -> str:
        """
        Generates a rectangular string with randomly placed stars.

        Args:
            width: The width of the starfield.
            height: The height of the starfield.
            density: Approximate percentage of characters that will be stars (0.0 to 1.0).

        Returns:
            A string representing the starfield.
        """
        if width <= 0 or height <= 0:
            return ""
        
        lines = []
        star_chars = ['.', '*', '+', "'"] # Different types/brightness of stars
        for _ in range(height):
            line = []
            for _ in range(width):
                if random.random() < density:
                    line.append(random.choice(star_chars))
                else:
                    line.append(' ')
            lines.append("".join(line))
        return "\n".join(lines)

    def generate_simple_horizontal_line(self, width: int, char: str = '-') -> str:
        """
        Creates a simple horizontal line of a given width and character.

        Args:
            width: The desired width of the line.
            char: The character to use for the line. Defaults to '-'.

        Returns:
            A string representing the horizontal line.
        """
        if width <= 0:
            return ""
        if not char or len(char) > 1 : # Ensure single character
            char = '-'
        return char * width
        
    def get_random_static_noise(self, width: int, height: int) -> str:
        """
        Generates a block of random characters to represent background static noise.

        Args:
            width: The desired width of the noise block.
            height: The desired height of the noise block.

        Returns:
            A string representing the block of static noise.
        """
        if width <= 0 or height <= 0:
            return ""

        noise_chars = ['.', ',', '`', ' ', "'", '"', ';', ':', '~', '^', '*', '#'] # Expanded noise chars
        lines = []
        for _ in range(height):
            line = "".join(random.choice(noise_chars) for _ in range(width))
            lines.append(line)
        return "\n".join(lines)

if __name__ == '__main__':
    print("--- Testing SignalArtManager (Full Library) ---")

    from src.content.signal_types import SignalDefinition, SignalTier, SignalTypeCategory, ModulationType # For dummy signal

    art_manager = SignalArtManager()

    # --- Test Star Map Elements ---
    print("\n--- Testing get_star_map_element_art ---")
    star_g = art_manager.get_star_map_element_art("STAR_TYPE_G")
    print(f"Star Type G: '{star_g}'")
    if star_g is None: print("ERROR: Star Type G not found.")

    planet_t = art_manager.get_star_map_element_art("PLANET_TERRAN")
    print(f"Terran Planet: '{planet_t}'")
    if planet_t is None: print("ERROR: Terran Planet not found.")
    
    anomaly_w = art_manager.get_star_map_element_art("ANOMALY_WORMHOLE")
    print(f"Wormhole Anomaly: '{anomaly_w}'")
    if anomaly_w is None: print("ERROR: Wormhole Anomaly not found.")

    player_icon = art_manager.get_star_map_element_art("PLAYER_SHIP_ICON")
    print(f"Player Ship Icon: '{player_icon}'")
    if player_icon is None: print("ERROR: Player Ship Icon not found.")

    # --- Test Environmental Art ---
    print("\n--- Testing get_environmental_art ---")
    nebula_bg = art_manager.get_environmental_art("SPACE_NEBULA_BACKGROUND_TILE")
    print("Nebula Background Tile:\n", nebula_bg)
    if nebula_bg is None: print("ERROR: Nebula Background not found.")
    
    asteroid_field = art_manager.get_environmental_art("ASTEROID_FIELD_DENSE")
    print("\nDense Asteroid Field:\n", asteroid_field)
    if asteroid_field is None: print("ERROR: Asteroid Field art not found.")

    # --- Test Procedural Generation ---
    print("\n--- Testing generate_starfield ---")
    starfield_small = art_manager.generate_starfield(width=40, height=5, density=0.05)
    print("Small Starfield (40x5, 5% density):\n", starfield_small)
    
    starfield_dense = art_manager.generate_starfield(width=30, height=4, density=0.2)
    print("\nDense Starfield (30x4, 20% density):\n", starfield_dense)

    print("\n--- Testing generate_simple_horizontal_line ---")
    line_default = art_manager.generate_simple_horizontal_line(width=30)
    print(f"Default Line (30 chars): '{line_default}'")

    line_custom = art_manager.generate_simple_horizontal_line(width=20, char="=")
    print(f"Custom Line (20 chars, '='): '{line_custom}'")

    line_zero = art_manager.generate_simple_horizontal_line(width=0)
    print(f"Zero Width Line: '{line_zero}' (Expected: '')")
    if line_zero != "": print("ERROR: Expected empty string for zero width line.")

    # Brief re-check of older functions to ensure they still work
    print("\n--- Brief re-check of existing art types ---")
    dummy_signal = SignalDefinition("DUMMY_SIG", "Dummy", "Desc", SignalTier.BASIC, SignalTypeCategory.UNKNOWN, 100, 10, ModulationType.AM, (-50,), 0.9, ascii_signature_category="AM_STABLE_CLEAR", base_rarity_score=0.5)
    sig_art = art_manager.get_signal_signature_art(dummy_signal)
    print(f"Dummy Signal Art: {'Found' if sig_art else 'Not Found'}")

    schematic_art = art_manager.get_upgrade_schematic_art("ANTENNA_MK2_SCHEMATIC")
    print(f"Antenna Schematic: {'Found' if schematic_art else 'Not Found'}")

    ui_art = art_manager.get_ui_decoration_art("HORIZONTAL_DIVIDER_THIN")
    print(f"Thin Divider: {'Found' if ui_art else 'Not Found'}")

    print("\n--- SignalArtManager Full Library Tests End ---")
