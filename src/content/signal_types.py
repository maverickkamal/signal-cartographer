from dataclasses import dataclass, field, InitVar
from typing import List, Tuple, Optional, Union, Dict
from enum import Enum

class SignalTier(Enum):
    """Defines the general tier or rarity of a signal."""
    COMMON = "Common"       # Standard, easily found signals
    UNCOMMON = "Uncommon"   # Less frequent, might require specific conditions
    RARE = "Rare"         # Hard to find, possibly unique or very localized
    EPIC = "Epic"         # Signals of great significance or power
    LEGENDARY = "Legendary" # Truly unique, story-defining signals
    # Previous suggestion: BASIC, ADVANCED, EXOTIC, ANCIENT, QUANTUM.
    # Using rarity-based terms might be more intuitive for progression.
    # Let's stick to a slightly modified version of the suggestion for now:
    # BASIC, INTERMEDIATE, ADVANCED, ELITE, ANCIENT (as EXOTIC is a modulation type too)
    # Re-evaluating: Let's use the originally suggested tiers for clarity with requirements.
    BASIC = "Basic"
    ADVANCED = "Advanced"
    EXOTIC_TIER = "Exotic Tier" # Renamed to avoid clash with ModulationType.EXOTIC
    ANCIENT = "Ancient"
    QUANTUM = "Quantum"

class SignalTypeCategory(Enum):
    """Primary categorization for signals based on their perceived origin or nature."""
    TECHNOLOGICAL = "Technological"       # Man-made or artificial origin, clear structure
    BIOLOGICAL = "Biological"           # Originating from organic life forms
    GEOLOGICAL = "Geological"           # Originating from planetary geological activity
    STELLAR = "Stellar"                 # Originating from stars, nebulae, cosmic phenomena
    QUANTUM_PHENOMENA = "Quantum Phenomena" # Related to exotic physics, rifts, anomalies
    CRYSTALLINE = "Crystalline"         # Signals from crystalline entities or structures
    MEMETIC = "Memetic"                 # Signals that affect thought or information itself
    ARCHAEOLOGICAL = "Archaeological"   # Ancient technological signals, distinct from current tech
    DISTRESS = "Distress"               # Signals indicating danger or calls for help
    CIVILIAN = "Civilian"               # Standard, non-hostile traffic, beacons
    PIRATE = "Pirate"                   # Illicit technological signals
    MILITARY = "Military"               # Technological signals with military characteristics
    RESEARCH = "Research"               # Scientific or exploratory signals
    UNKNOWN = "Unknown"                 # Truly unclassifiable or new signals

class ModulationType(Enum):
    """Defines common modulation types for signals."""
    AM = "Amplitude Modulation"
    FM = "Frequency Modulation"
    PULSED = "Pulsed"
    PSK = "Phase-Shift Keying" # Phase Shift Keying
    FSK = "Frequency-Shift Keying" # Frequency Shift Keying
    CW = "Continuous Wave" # e.g. Morse code tones
    DATA_BURST = "Data Burst"
    NOISE = "Broadband Noise"
    EXOTIC = "Exotic/Unknown"

@dataclass
class SignalDefinition:
    """
    Defines the static properties of a type of signal that can be encountered in the game.
    """
    signal_id: str
    name: str
    description: str

    tier: SignalTier
    category: SignalTypeCategory

    base_frequency: float
    bandwidth: float # in KHz for this example context
    modulation_type: ModulationType
    strength_levels: Tuple[float, ...]
    stability: float # 0.0 to 1.0

    tags: List[str] = field(default_factory=list)

    # Identifiers for lore entries unlocked or related to this signal
    lore_fragments_unlocked: List[str] = field(default_factory=list)

    # Identifiers for equipment/upgrades needed to detect or fully analyze
    required_equipment: List[str] = field(default_factory=list)

    lore_fragments_unlocked: List[str] = field(default_factory=list)
    required_equipment: List[str] = field(default_factory=list)
    associated_puzzle_type: Optional[str] = None

    complexity_score: float = field(init=False, default=0.0)

    complexity_score: float = field(init=False, default=0.0)

    complexity_score: float = field(init=False, default=0.0) # Calculated in __post_init__

    # --- Discovery & Rarity Fields ---
    discovery_requirements: Dict[str, Any] = field(default_factory=dict)
    # Example keys: min_player_level, required_scanner_level, required_completed_signals,
    #               required_lore_fragments, required_sector_types, random_encounter_chance
    #   min_player_level: int
    #   required_scanner_level: int
    #   required_completed_signals: List[str] (signal_ids)
    #   required_lore_fragments: List[str] (lore_ids)
    #   required_sector_types: List[str] (sector type names)
    is_event_triggered: bool = False
    event_name: Optional[str] = None

    base_rarity_score: float = 0.5  # Intrinsic rarity (0.0 extremely rare, 1.0 very common)
    spawn_locations: List[str] = field(default_factory=list)
    spawn_conditions_met_bonus: float = 0.0 # Bonus to effective rarity under certain game states

    # --- Interdependency Fields ---
    unlocks_signals: List[str] = field(default_factory=list)
    lore_provided_by_signal: List[str] = field(default_factory=list)
    combination_hint: Optional[str] = None

    # --- Visuals ---
    ascii_signature_category: Optional[str] = None # Key for SIGNAL_SIGNATURES dictionary

    # --- Evolution and Degradation Fields ---
    can_evolve: bool = False
    evolves_to_signal_id: Optional[str] = None
    evolution_conditions: Dict[str, Any] = field(default_factory=dict) # e.g. {"time_elapsed_hours": 72, "player_action": "PROBE_LAUNCHED"}

    can_degrade: bool = False
    degrades_to_signal_id: Optional[str] = None
    degradation_conditions: Dict[str, Any] = field(default_factory=dict) # e.g. {"environmental_interference": "HIGH_RADIATION"}

    current_state_modifiers: Dict[str, Any] = field(default_factory=dict) # e.g. {"strength_modifier": -0.2}


    # --- Complexity Scoring Weights ---
    _TIER_COMPLEXITY_WEIGHTS: Dict[SignalTier, float] = {
        SignalTier.BASIC: 5.0,
        SignalTier.ADVANCED: 15.0,
        SignalTier.EXOTIC_TIER: 30.0,
        SignalTier.ANCIENT: 50.0,
        SignalTier.QUANTUM: 100.0,
    }
    _MODULATION_COMPLEXITY_WEIGHTS: Dict[ModulationType, float] = {
        ModulationType.AM: 1.0,
        ModulationType.FM: 2.0,
        ModulationType.CW: 1.5,
        ModulationType.PULSED: 3.0,
        ModulationType.FSK: 4.0,
        ModulationType.PSK: 5.0,
        ModulationType.DATA_BURST: 8.0,
        ModulationType.NOISE: 0.5, # Noise itself isn't complex to be a signal, but analyzing it might be
        ModulationType.EXOTIC: 10.0,
    }
    _BANDWIDTH_COMPLEXITY_FACTOR: float = 0.01 # Score per KHz of bandwidth
    _STABILITY_COMPLEXITY_FACTOR: float = -10.0 # Inverse: higher stability = lower complexity score adjustment
                                                # Max -10 for perfect stability, 0 for no stability
    _EQUIPMENT_COMPLEXITY_PER_ITEM: float = 3.0
    _PUZZLE_COMPLEXITY_BONUS: float = 10.0


    def _calculate_complexity_score(self) -> float:
        """Calculates a numerical complexity score for the signal."""
        score = 0.0

        # Tier contribution
        score += self._TIER_COMPLEXITY_WEIGHTS.get(self.tier, 0.0)

        # Modulation type contribution
        score += self._MODULATION_COMPLEXITY_WEIGHTS.get(self.modulation_type, 1.0)

        # Bandwidth contribution (score increases by 0.01 for every KHz)
        # Example: 10 KHz = +0.1, 1000 KHz (1MHz) = +10
        score += self.bandwidth * self._BANDWIDTH_COMPLEXITY_FACTOR

        # Stability contribution (inverse: higher stability = lower complexity)
        # Score decreases as stability increases. Max reduction of 10 for stability 1.0
        # (1.0 - stability) ranges from 0 (perfectly stable) to 1 (perfectly unstable)
        # A more unstable signal (lower stability value) gets a higher score.
        score += (1.0 - self.stability) * abs(self._STABILITY_COMPLEXITY_FACTOR)

        # Required equipment contribution
        score += len(self.required_equipment) * self._EQUIPMENT_COMPLEXITY_PER_ITEM

        # Associated puzzle contribution
        if self.associated_puzzle_type:
            score += self._PUZZLE_COMPLEXITY_BONUS

        return round(max(0.0, score), 2) # Ensure score is not negative and round

    def __post_init__(self):
        # Basic validation
        if not self.signal_id:
            raise ValueError("SignalDefinition must have a signal_id.")
        if not isinstance(self.tier, SignalTier):
            raise ValueError(f"tier must be a SignalTier enum member, got {type(self.tier)}.")
        if not isinstance(self.category, SignalTypeCategory):
            raise ValueError(f"category must be a SignalTypeCategory enum member, got {type(self.category)}.")

        # Validation for discovery_requirements
        if not isinstance(self.discovery_requirements, dict):
            raise ValueError("discovery_requirements must be a dictionary.")

        rec = self.discovery_requirements.get("random_encounter_chance")
        if rec is not None and (not isinstance(rec, float) or not (0.0 <= rec <= 1.0)):
            raise ValueError("random_encounter_chance must be a float between 0.0 and 1.0.")

        if self.is_event_triggered and not self.event_name:
            raise ValueError("event_name must be provided if is_event_triggered is True.")

        if not (0.0 <= self.base_rarity_score <= 1.0):
            raise ValueError("base_rarity_score must be between 0.0 and 1.0.")
        if not isinstance(self.spawn_locations, list):
            raise ValueError("spawn_locations must be a list.")
        if not isinstance(self.spawn_conditions_met_bonus, (int, float)):
            raise ValueError("spawn_conditions_met_bonus must be a number.")

        # Validation for new interdependency fields
        if not isinstance(self.unlocks_signals, list):
            raise ValueError("unlocks_signals must be a list.")
        if not all(isinstance(item, str) for item in self.unlocks_signals):
            raise ValueError("All items in unlocks_signals must be strings (signal_ids).")

        if not isinstance(self.lore_provided_by_signal, list):
            raise ValueError("lore_provided_by_signal must be a list.")
        if not all(isinstance(item, str) for item in self.lore_provided_by_signal):
            raise ValueError("All items in lore_provided_by_signal must be strings (lore_ids).")
        if self.combination_hint is not None and not isinstance(self.combination_hint, str):
            raise ValueError("combination_hint must be a string or None.")

        # Validation for evolution/degradation fields
        if self.can_evolve and not self.evolves_to_signal_id:
            raise ValueError("evolves_to_signal_id must be set if can_evolve is True.")
        if self.can_degrade and not self.degrades_to_signal_id:
            raise ValueError("degrades_to_signal_id must be set if can_degrade is True.")
        if not isinstance(self.evolution_conditions, dict):
            raise ValueError("evolution_conditions must be a dictionary.")
        if not isinstance(self.degradation_conditions, dict):
            raise ValueError("degradation_conditions must be a dictionary.")
        if not isinstance(self.current_state_modifiers, dict):
            raise ValueError("current_state_modifiers must be a dictionary.")

        if self.ascii_signature_category is not None and not isinstance(self.ascii_signature_category, str):
            raise ValueError("ascii_signature_category must be a string or None.")

        if self.base_frequency <= 0:
            raise ValueError("Base frequency must be positive.")
        if self.bandwidth <= 0:
            raise ValueError("Bandwidth must be positive.")
        if not (0.0 <= self.stability <= 1.0):
            raise ValueError("Stability must be between 0.0 and 1.0.")
        if not self.strength_levels:
             raise ValueError("Strength levels cannot be empty.")
        for level in self.strength_levels:
            if not isinstance(level, (int, float)):
                 raise ValueError("Strength levels must be numbers.")

        # Calculate and set the complexity score
        self.complexity_score = self._calculate_complexity_score()


if __name__ == '__main__':
    print("--- Testing SignalDefinition with Tiers and Complexity ---")
    try:
        sig_with_art = SignalDefinition(
            signal_id="ART_TEST_01",
            name="Signal with ASCII Art",
            description="A test signal that should have an ASCII signature.",
            tier=SignalTier.BASIC,
            category=SignalTypeCategory.CIVILIAN,
            base_frequency=150.0,
            bandwidth=5.0,
            modulation_type=ModulationType.AM,
            strength_levels=(-80.0,),
            stability=0.9,
            tags=["test", "art"],
            base_rarity_score=0.8,
            ascii_signature_category="AM_STABLE_CLEAR", # Matching a key from ascii_art_library
            # Other new fields can be default
        )
        print(f"Created Signal: {sig_with_art.name}, ASCII Category: {sig_with_art.ascii_signature_category}")
        print(f"  Complexity: {sig_with_art.complexity_score:.2f}")

        # Test validation for ascii_signature_category
        print("\nTesting ASCII signature category validation:")
        try:
            SignalDefinition("FAIL_EVOLVE_ID", "Evolve ID Fail", "Desc", SignalTier.BASIC, SignalTypeCategory.UNKNOWN,
                             100,10,ModulationType.AM,(-50,),0.5, can_evolve=True, evolves_to_signal_id=None)
        except ValueError as e:
            print(f"Caught expected (evolves_to_signal_id missing): {e}")

        try:
            SignalDefinition("FAIL_DEGRADE_ID", "Degrade ID Fail", "Desc", SignalTier.BASIC, SignalTypeCategory.UNKNOWN,
                             100,10,ModulationType.AM,(-50,),0.5, can_degrade=True, degrades_to_signal_id=None)
        except ValueError as e:
            print(f"Caught expected (degrades_to_signal_id missing): {e}")

        try:
            SignalDefinition("FAIL_ASCII_TYPE", "ASCII Type Fail", "Desc", SignalTier.BASIC, SignalTypeCategory.UNKNOWN,
                             100,10,ModulationType.AM,(-50,),0.5, ascii_signature_category=123) # type: ignore
        except ValueError as e:
            print(f"Caught expected (ascii_signature_category not str): {e}")

    except Exception as e:
        print(f"An error occurred during SignalDefinition tests: {e}")

    print("--- SignalDefinition All Features (including ASCII Art Link) Tests End ---")


# --- Lore System Types ---

class LoreCategory(Enum):
    """Categorization for lore fragments."""
    ANCIENT_CIVILIZATION = "Ancient Civilization"
    XENOBIOLOGY = "Xenobiology"
    CORPORATE_HISTORY = "Corporate History"
    MYTHS_LEGENDS = "Myths & Legends"
    TECHNOLOGY = "Technology"
    GALACTIC_GEOGRAPHY = "Galactic Geography"
    PLAYER_JOURNAL = "Player Journal"
    ENVIRONMENTAL = "Environmental Log" # e.g. planetary conditions, stellar phenomena details
    EQUIPMENT_MANUAL = "Equipment Manual" # For specific tech pieces
    UNDEFINED = "Undefined"

@dataclass
class LoreFragment:
    """
    Represents a piece of lore or narrative content discoverable by the player.
    """
    lore_id: str  # Unique string identifier (e.g., "ANCIENT_ORIGINS_PART1")
    title: str    # Human-readable title
    content: str  # Multi-line string containing the lore text

    category: LoreCategory
    tags: List[str] = field(default_factory=list)

    source_description: Optional[str] = None

    unlock_requirements: Dict[str, Any] = field(default_factory=dict)
    # Examples: {"required_signal_analyzed": "ID", "player_level": 5, "found_other_lore": ["ID"]}

    unlocks_lore_ids: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.lore_id:
            raise ValueError("LoreFragment must have a lore_id.")
        if not self.title:
            raise ValueError("LoreFragment must have a title.")
        if not self.content: # Allow empty content for titles/stubs initially? For now, require.
            raise ValueError("LoreFragment content cannot be empty.")
        if not isinstance(self.category, LoreCategory):
            raise ValueError(f"LoreFragment category must be a LoreCategory enum member, got {type(self.category)}.")
        if not isinstance(self.tags, list):
            raise ValueError("LoreFragment tags must be a list.")
        if not isinstance(self.unlock_requirements, dict):
            raise ValueError("LoreFragment unlock_requirements must be a dict.")
        if not isinstance(self.unlocks_lore_ids, list):
            raise ValueError("LoreFragment unlocks_lore_ids must be a list.")
        if self.source_description is not None and not isinstance(self.source_description, str):
            raise ValueError("LoreFragment source_description must be a string or None.")

if __name__ == '__main__':
    # Existing tests for SignalDefinition should remain above this if they are separate.
    # This block will now also test LoreFragment if this is the combined test execution.
    # To keep it clean, let's assume previous SignalDefinition tests were self-contained.

    print("\n--- Testing LoreFragment Definition (within signal_types.py) ---")
    try:
        lore_test1 = LoreFragment(
            lore_id="LORE_TEST_001",
            title="Test Lore Alpha",
            content="This is the first piece of test lore.",
            category=LoreCategory.TECHNOLOGY,
            tags=["test", "alpha_content"],
            source_description="Test data generator.",
            unlock_requirements={"player_level": 1},
            unlocks_lore_ids=["LORE_TEST_002"]
        )
        print(f"Created Lore: {lore_test1.title} (ID: {lore_test1.lore_id}), Category: {lore_test1.category.value}")

        lore_test2 = LoreFragment(
            lore_id="LORE_TEST_002",
            title="Test Lore Beta",
            content="This lore is unlocked by Alpha.",
            category=LoreCategory.MYTHS_LEGENDS,
            tags=["test", "beta_content"],
            unlock_requirements={"found_other_lore": ["LORE_TEST_001"]}
        )
        print(f"Created Lore: {lore_test2.title} (ID: {lore_test2.lore_id}), Requires: {lore_test2.unlock_requirements}")

        print("\nTesting LoreFragment validation failures:")
        try:
            LoreFragment(lore_id="", title="No ID", content="Content", category=LoreCategory.UNDEFINED)
        except ValueError as e:
            print(f"Caught expected for empty lore_id: {e}")
        try:
            LoreFragment(lore_id="ID_OK", title="Title", content="Content", category="NOT_A_REAL_CATEGORY") # type: ignore
        except ValueError as e:
            print(f"Caught expected for invalid category type: {e}")

    except Exception as e:
        print(f"An unexpected error occurred during LoreFragment testing: {e}")
    print("--- LoreFragment Definition Test End (within signal_types.py) ---")
