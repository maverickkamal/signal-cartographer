from src.content.signal_types import SignalDefinition, ModulationType, SignalTier, SignalTypeCategory
from typing import List, Dict

ALL_SIGNAL_DEFINITIONS: List[SignalDefinition] = [
    SignalDefinition(
        signal_id="CIV_BEACON_STD_01",
        name="Standard Civilian Beacon",
        tier=SignalTier.BASIC,
        category=SignalTypeCategory.CIVILIAN,
        description="A common navigation and identification beacon used by civilian spacecraft.",
        base_frequency=121.5,
        bandwidth=10.0,
        modulation_type=ModulationType.AM,
        strength_levels=(-90.0, -75.0, -60.0),
        stability=0.95,
        tags=["civilian", "beacon", "navigation", "common"],
        required_equipment=["basic_receiver"],
        discovery_requirements={"random_encounter_chance": 0.8},
        is_event_triggered=False,
        base_rarity_score=0.9,
        spawn_locations=["CIVILIAN_SECTOR", "TRADE_ROUTE_A9", "ORBITAL_STATION_PRIME"],
        spawn_conditions_met_bonus=0.0,
        unlocks_signals=[],
        lore_provided_by_signal=["LORE_CIV_BEACON_INFO"],
        combination_hint=None,
        can_evolve=False,
        can_degrade=False,
        ascii_signature_category="AM_STABLE_CLEAR",
    ),
    SignalDefinition(
        signal_id="PIRATE_DATA_RELAY_GAMMA",
        name="Pirate Data Relay Gamma",
        tier=SignalTier.ADVANCED,
        category=SignalTypeCategory.PIRATE,
        description="An encrypted, rapidly shifting data stream used by pirate cells for covert communication.",
        base_frequency=405.2,
        bandwidth=25.0,
        modulation_type=ModulationType.FSK,
        strength_levels=(-100.0, -85.0),
        stability=0.6,
        tags=["pirate", "covert", "data", "encrypted", "illicit"],
        lore_fragments_unlocked=["LORE_PIRATE_NET_GAMMA"],
        required_equipment=["wideband_receiver", "decryption_module_mk1"],
        associated_puzzle_type="AudioConversionPuzzle",
        discovery_requirements={
            "required_sector_types": ["LAWLESS_SECTOR", "BORDER_REGION"],
            "min_player_level": 3,
            "random_encounter_chance": 0.3
        },
        base_rarity_score=0.4,
        spawn_locations=["LAWLESS_SECTOR", "ASTEROID_HIDEOUT_Z4"],
        spawn_conditions_met_bonus=0.0,
        unlocks_signals=["PIRATE_STRONGHOLD_BEACON_ALPHA"],
        lore_provided_by_signal=["LORE_PIRATE_CODES_GAMMA", "LORE_PIRATE_ACTIVITY_REPORT"],
        combination_hint="Intercepting multiple pirate relays might reveal a pattern.",
        can_degrade=True,
        degrades_to_signal_id="PIRATE_RELAY_GAMMA_CORRUPTED",
        degradation_conditions={"time_unattended_days": 14, "faction_presence": "LOW"},
        can_evolve=False,
        ascii_signature_category="DATA_BURST_COMPLEX", # FSK is a form of data burst
    ),
    SignalDefinition(
        signal_id="ANCIENT_PROBE_RETURN_SIGNAL",
        name="Ancient Probe \"Echo\"",
        tier=SignalTier.ANCIENT,
        category=SignalTypeCategory.ARCHAEOLOGICAL,
        description="A faint, repeating signal from a long-lost deep space probe. Its purpose is unknown.",
        base_frequency=8415.0,
        bandwidth=5.0,
        modulation_type=ModulationType.PULSED,
        strength_levels=(-140.0, -130.0),
        stability=0.99,
        tags=["ancient", "probe", "deep_space", "mystery", "repeating"],
        lore_fragments_unlocked=["LORE_PROBE_DISCOVERY", "LORE_PROBE_ORIGINS_UNCLEAR"],
        required_equipment=["deep_space_antenna", "low_noise_amplifier_adv"],
        associated_puzzle_type="PulseSequencePuzzle",
        discovery_requirements={
            "required_completed_signals": ["CIV_BEACON_STD_01"],
            "required_lore_fragments": ["LORE_ANCIENT_MYTHS"],
            "required_scanner_level": 2,
            "required_sector_types": ["DEEP_SPACE_ANOMALY", "ARTIFACT_SITE"]
        },
        base_rarity_score=0.1,
        spawn_locations=["DEEP_SPACE_ANOMALY", "FORGOTTEN_REALMS"],
        spawn_conditions_met_bonus=0.0,
        unlocks_signals=["ANCIENT_PROBE_TRANSMISSION_DECODED"],
        lore_provided_by_signal=["LORE_PROBE_PARTIAL_DATA_1", "LORE_PROBE_STAR_CHART_FRAGMENT"],
        combination_hint="Its pulse timings might correlate with other ancient artifacts.",
        can_evolve=True,
        evolves_to_signal_id="ANCIENT_PROBE_STABILIZED",
        evolution_conditions={"player_action": "INVESTIGATE_PROBE_SOURCE", "required_item": "PROBE_TUNER_MK2"},
        can_degrade=False,
        ascii_signature_category="PULSED_SHARP_REPEATING", # Weak but distinct
    ),
    SignalDefinition(
        signal_id="STELLAR_NURSERY_CHORUS",
        name="Stellar Nursery Chorus",
        tier=SignalTier.EXOTIC_TIER,
        category=SignalTypeCategory.STELLAR,
        description="Complex, overlapping energy patterns emanating from a dense stellar nursery.",
        base_frequency=1.42,
        bandwidth=1000.0,
        modulation_type=ModulationType.EXOTIC,
        strength_levels=(-120.0, -100.0, -90.0),
        stability=0.3,
        tags=["natural", "stellar_phenomenon", "complex", "research_target"],
        lore_fragments_unlocked=["LORE_STELLAR_SONG", "LORE_COSMIC_HARMONIES"],
        required_equipment=["radio_telescope_array", "correlation_spectrometer"],
        associated_puzzle_type="HarmonicPatternPuzzle",
        discovery_requirements={
             "required_sector_types": ["NEBULA_CORE"],
             "min_player_level": 10,
        },
        is_event_triggered=True,
        event_name="COSMIC_ALIGNMENT_WINDOW",
        base_rarity_score=0.0,
        spawn_locations=["NEBULA_CORE"],
        spawn_conditions_met_bonus=0.0,
        unlocks_signals=[],
        lore_provided_by_signal=["LORE_NEBULA_FORMATION_THEORY", "LORE_EXOTIC_PARTICLES_DETECTED"],
        combination_hint=None,
        can_evolve=False,
        can_degrade=False,
        ascii_signature_category="EXOTIC_SWIRLING_UNSTABLE",
    ),
    SignalDefinition(
        signal_id="DISTRESS_CALL_FREIGHTER_VALIANT",
        name="Freighter 'Valiant' Distress Call",
        tier=SignalTier.ADVANCED,
        category=SignalTypeCategory.DISTRESS,
        description="A standard SOS distress call, but with unusual interference patterns.",
        base_frequency=156.8,
        bandwidth=15.0,
        modulation_type=ModulationType.FM,
        strength_levels=(-115.0, -105.0),
        stability=0.45,
        tags=["distress_call", "SOS", "freighter", "urgent", "interference"],
        lore_fragments_unlocked=["LORE_VALIANT_FATE"],
        required_equipment=["standard_transceiver", "noise_filter_mk2"],
        discovery_requirements={
            "random_encounter_chance": 0.6,
            "required_sector_types": ["TRADE_ROUTE_DANGER", "ASTEROID_FIELD_HAZARD"]
        },
        base_rarity_score=0.5,
        spawn_locations=["TRADE_ROUTE_DANGER", "ASTEROID_FIELD_HAZARD", "UNEXPLORED_SYSTEM_EDGE"],
        spawn_conditions_met_bonus=0.0,
        unlocks_signals=["WRECKAGE_SITE_VALIANT"],
        lore_provided_by_signal=["LORE_VALIANT_LAST_LOG_ENTRY", "LORE_VALIANT_CARGO_MANIFEST"],
        combination_hint=None,
        can_degrade=True,
        degrades_to_signal_id="DISTRESS_CALL_VALIANT_CORRUPTED",
        degradation_conditions={"time_unattended_hours": 24, "environmental_interference": "HIGH"},
        can_evolve=False,
        ascii_signature_category="FM_NOISY_MODERATE", # FM, and likely noisy/interfered
    ),

    # Dummy signals for evolution/degradation/unlock testing:
    SignalDefinition(signal_id="PIRATE_STRONGHOLD_BEACON_ALPHA", name="Pirate Stronghold Beacon Alpha", tier=SignalTier.ADVANCED, category=SignalTypeCategory.PIRATE, base_frequency=410.0, bandwidth=5.0, modulation_type=ModulationType.PULSED, strength_levels=(-90,), stability=0.8, base_rarity_score=0.2, spawn_locations=["LAWLESS_SECTOR"], discovery_requirements={"required_completed_signals":["PIRATE_DATA_RELAY_GAMMA"]}, lore_provided_by_signal=["LORE_PIRATE_HIDEOUT_LOC_A"], ascii_signature_category="PULSED_SHARP_REPEATING"),
    SignalDefinition(signal_id="ANCIENT_PROBE_TRANSMISSION_DECODED", name="Ancient Probe Transmission (Decoded)", tier=SignalTier.ANCIENT, category=SignalTypeCategory.ARCHAEOLOGICAL, base_frequency=8415.0, bandwidth=1.0, modulation_type=ModulationType.DATA_BURST, strength_levels=(-150,), stability=0.99, base_rarity_score=0.05, discovery_requirements={"required_completed_signals":["ANCIENT_PROBE_RETURN_SIGNAL"]}, lore_provided_by_signal=["LORE_PROBE_FULL_MESSAGE"], ascii_signature_category="DATA_BURST_COMPLEX"),
    SignalDefinition(signal_id="WRECKAGE_SITE_VALIANT", name="Wreckage Site - Freighter Valiant", tier=SignalTier.ADVANCED, category=SignalTypeCategory.ARCHAEOLOGICAL, base_frequency=12.0, bandwidth=1.0, modulation_type=ModulationType.NOISE, strength_levels=(-100,), stability=1.0, base_rarity_score=0.0, spawn_locations=["TRADE_ROUTE_DANGER"], discovery_requirements={"required_completed_signals":["DISTRESS_CALL_FREIGHTER_VALIANT"]}, lore_provided_by_signal=["LORE_VALIANT_BLACKBOX"], ascii_signature_category="WEAK_FADING_GENERIC"), # Could be just noise
    SignalDefinition(signal_id="PIRATE_RELAY_GAMMA_CORRUPTED", name="Corrupted Pirate Data Relay Gamma", tier=SignalTier.ADVANCED, category=SignalTypeCategory.PIRATE, base_frequency=405.2, bandwidth=30.0, modulation_type=ModulationType.NOISE, strength_levels=(-110,), stability=0.2, base_rarity_score=0.1, spawn_locations=["LAWLESS_SECTOR", "ASTEROID_HIDEOUT_Z4"], lore_provided_by_signal=["LORE_PIRATE_RELAY_FAILURE"], discovery_requirements={"required_completed_signals":["PIRATE_DATA_RELAY_GAMMA"]}, ascii_signature_category="WEAK_FADING_GENERIC"),
    SignalDefinition(signal_id="ANCIENT_PROBE_STABILIZED", name="Ancient Probe \"Echo\" (Stabilized)", tier=SignalTier.ANCIENT, category=SignalTypeCategory.ARCHAEOLOGICAL, base_frequency=8415.0, bandwidth=4.0, modulation_type=ModulationType.PULSED, strength_levels=(-130,), stability=1.0, base_rarity_score=0.1, spawn_locations=["DEEP_SPACE_ANOMALY"], discovery_requirements={"required_completed_signals":["ANCIENT_PROBE_RETURN_SIGNAL"]}, lore_provided_by_signal=["LORE_PROBE_STABLE_SIGNAL_ACHIEVED"], unlocks_signals=["ANCIENT_PROBE_TRANSMISSION_DECODED"], ascii_signature_category="PULSED_SHARP_REPEATING"),
]

SIGNAL_DEFINITIONS_BY_ID: Dict[str, SignalDefinition] = {
    sig.signal_id: sig for sig in ALL_SIGNAL_DEFINITIONS
}

if __name__ == '__main__':
    print("--- Loading Signal Definitions from signals_database.py (with ASCII Sig Categories) ---")
    if not ALL_SIGNAL_DEFINITIONS:
        print("Error: ALL_SIGNAL_DEFINITIONS list is empty!")
    else:
        print(f"Successfully loaded {len(ALL_SIGNAL_DEFINITIONS)} signal definitions.")
        for i, signal in enumerate(ALL_SIGNAL_DEFINITIONS):
            print(f"  {i+1}. ID: {signal.signal_id}, Name: {signal.name}, ASCII Cat: {signal.ascii_signature_category}")
            # print(f"     Evolves to: {signal.evolves_to_signal_id}, Degrades to: {signal.degrades_to_signal_id}") # Keep if needed
            if signal.signal_id not in SIGNAL_DEFINITIONS_BY_ID:
                print(f"    Error: Signal ID {signal.signal_id} not found in dictionary lookup!")

        if len(ALL_SIGNAL_DEFINITIONS) == len(SIGNAL_DEFINITIONS_BY_ID):
            print("\nDictionary SIGNAL_DEFINITIONS_BY_ID is consistent with the list.")
        else:
            print("\nError: Mismatch between list length and dictionary size!")

    test_id = "PIRATE_DATA_RELAY_GAMMA"
    if test_id in SIGNAL_DEFINITIONS_BY_ID:
        retrieved_signal = SIGNAL_DEFINITIONS_BY_ID[test_id]
        print(f"\nSuccessfully retrieved '{test_id}':")
        print(f"  ASCII Signature Category: {retrieved_signal.ascii_signature_category}")
    else:
        print(f"Error: Test signal ID '{test_id}' not found in database.")

    test_id_no_art = "STELLAR_NURSERY_CHORUS" # Assuming this one might not have a specific category yet
    if test_id_no_art in SIGNAL_DEFINITIONS_BY_ID:
        retrieved_no_art = SIGNAL_DEFINITIONS_BY_ID[test_id_no_art]
        print(f"\nSuccessfully retrieved '{test_id_no_art}':")
        print(f"  ASCII Signature Category: {retrieved_no_art.ascii_signature_category}")


    print("\n--- End of signals_database.py ASCII Sig Cat Tests ---")
