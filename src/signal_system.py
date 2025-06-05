import random
from typing import Dict, List, Optional, Set # Added Set
from src.content.signal_types import SignalDefinition
from src.content.signals_database import ALL_SIGNAL_DEFINITIONS, SIGNAL_DEFINITIONS_BY_ID
# For __main__ testing, to validate against actual lore data
from src.content.lore_manager import LoreManager

class SignalManager:
    """
    Manages all known signal definitions in the game.
    Provides an interface to access signal properties.
    """
    def __init__(self):
        self._signal_definitions: Dict[str, SignalDefinition] = {}
        self._load_all_signals()

    def _load_all_signals(self) -> None:
        if SIGNAL_DEFINITIONS_BY_ID:
            self._signal_definitions = dict(SIGNAL_DEFINITIONS_BY_ID)
        elif ALL_SIGNAL_DEFINITIONS:
            for signal_def in ALL_SIGNAL_DEFINITIONS:
                self._signal_definitions[signal_def.signal_id] = signal_def

    def get_signal_definition(self, signal_id: str) -> Optional[SignalDefinition]:
        return self._signal_definitions.get(signal_id)

    def get_all_signal_definitions(self) -> List[SignalDefinition]:
        return list(self._signal_definitions.values())

    def get_signal_ids_by_tag(self, tag: str, case_sensitive: bool = False) -> List[str]:
        matching_ids = []
        for sig_id, sig_def in self._signal_definitions.items():
            target_tags = sig_def.tags
            if not case_sensitive:
                tag_to_find = tag.lower()
                target_tags = [t.lower() for t in sig_def.tags]
            else:
                tag_to_find = tag
            if tag_to_find in target_tags:
                matching_ids.append(sig_id)
        return matching_ids

    def get_signals_by_complexity(self, min_score: float, max_score: float) -> List[SignalDefinition]:
        return [s for s in self._signal_definitions.values() if min_score <= s.complexity_score <= max_score]

    def get_signals_by_tier(self, target_tier: 'SignalTier') -> List[SignalDefinition]: # type: ignore
        return [s for s in self._signal_definitions.values() if s.tier == target_tier]

    def get_signals_by_category(self, target_category: 'SignalTypeCategory') -> List[SignalDefinition]: # type: ignore
        return [s for s in self._signal_definitions.values() if s.category == target_category]

    def validate_signal_interdependencies(self, all_lore_ids: Optional[Set[str]] = None) -> List[str]:
        messages = []
        all_signal_ids = set(self._signal_definitions.keys())

        for sig_id, sig_def in self._signal_definitions.items():
            for unlocked_id in sig_def.unlocks_signals:
                if unlocked_id not in all_signal_ids:
                    messages.append(f"Signal Validation: '{sig_id}' ({sig_def.name}) unlocks non-existent signal ID '{unlocked_id}'.")
                else:
                    unlocked_sig = self.get_signal_definition(unlocked_id)
                    if unlocked_sig and sig_id in unlocked_sig.discovery_requirements.get("required_completed_signals", []):
                        messages.append(f"Signal Validation (Circular Dep): '{sig_id}' ({sig_def.name}) unlocks '{unlocked_id}' ({unlocked_sig.name}), which requires '{sig_id}'.")

            for req_id in sig_def.discovery_requirements.get("required_completed_signals", []):
                if req_id not in all_signal_ids:
                    messages.append(f"Signal Validation (Req Sigs): '{sig_id}' ({sig_def.name}) requires non-existent signal ID '{req_id}'.")

            if sig_def.can_evolve:
                if not sig_def.evolves_to_signal_id:
                     messages.append(f"Signal Data Error (Evolve): '{sig_id}' ({sig_def.name}) can_evolve=True but no evolves_to_signal_id.")
                elif sig_def.evolves_to_signal_id not in all_signal_ids:
                    messages.append(f"Signal Validation (Evolve): '{sig_id}' ({sig_def.name}) evolves to non-existent signal ID '{sig_def.evolves_to_signal_id}'.")
            
            if sig_def.can_degrade:
                if not sig_def.degrades_to_signal_id:
                    messages.append(f"Signal Data Error (Degrade): '{sig_id}' ({sig_def.name}) can_degrade=True but no degrades_to_signal_id.")
                elif sig_def.degrades_to_signal_id not in all_signal_ids:
                    messages.append(f"Signal Validation (Degrade): '{sig_id}' ({sig_def.name}) degrades to non-existent signal ID '{sig_def.degrades_to_signal_id}'.")

            if all_lore_ids is not None:
                for lore_id in sig_def.lore_provided_by_signal:
                    if lore_id not in all_lore_ids:
                        messages.append(f"Signal Validation (Lore Links): '{sig_id}' ({sig_def.name}) provides non-existent lore ID '{lore_id}'.")
            
            if all_lore_ids is not None and "required_lore_fragments" in sig_def.discovery_requirements :
                for req_lore_id in sig_def.discovery_requirements.get("required_lore_fragments",[]):
                    if req_lore_id not in all_lore_ids:
                        messages.append(f"Signal Validation (Req Lore): '{sig_id}' ({sig_def.name}) requires non-existent lore ID '{req_lore_id}'.")
        return messages

    def get_unlocked_signals_by(self, completed_signal_id: str) -> List[SignalDefinition]:
        unlocked_list = []
        source_signal = self.get_signal_definition(completed_signal_id)
        if not source_signal: return []
        for unlocked_id in source_signal.unlocks_signals:
            sig_def = self.get_signal_definition(unlocked_id)
            if sig_def: unlocked_list.append(sig_def)
        return unlocked_list

    def apply_runtime_modifiers(self, signal_instance_data: Dict, signal_def: SignalDefinition) -> Dict:
        modified_data = dict(signal_instance_data)
        strength_mod = signal_def.current_state_modifiers.get("strength_modifier", 0.0)
        base_strength = signal_instance_data.get("current_strength", signal_def.strength_levels[0] if signal_def.strength_levels else -100.0)
        modified_data["current_strength"] = base_strength + strength_mod
        stability_mod = signal_def.current_state_modifiers.get("stability_modifier", 0.0)
        base_stability = signal_instance_data.get("current_stability", signal_def.stability)
        modified_data["current_stability"] = max(0.0, min(1.0, base_stability + stability_mod))
        return modified_data

    def check_signal_evolution(self, signal_def: SignalDefinition, game_state: Dict) -> Optional[str]:
        if not signal_def.can_evolve or not signal_def.evolves_to_signal_id: return None
        return None

    def check_signal_degradation(self, signal_def: SignalDefinition, game_state: Dict) -> Optional[str]:
        if not signal_def.can_degrade or not signal_def.degrades_to_signal_id: return None
        return None

    def check_signal_discoverable(self, signal_def: SignalDefinition, current_player_status: Dict) -> bool:
        if signal_def.is_event_triggered: return False
        reqs = signal_def.discovery_requirements
        if not reqs: return True
        player_level = current_player_status.get("player_level", 0)
        if reqs.get("min_player_level", 0) > player_level: return False
        scanner_level = current_player_status.get("scanner_level", 0)
        if reqs.get("required_scanner_level", 0) > scanner_level: return False
        completed_signals = set(current_player_status.get("completed_signals", []))
        if not set(reqs.get("required_completed_signals", [])).issubset(completed_signals): return False
        found_lore = set(current_player_status.get("found_lore", []))
        if not set(reqs.get("required_lore_fragments", [])).issubset(found_lore): return False
        current_sector = current_player_status.get("current_sector_type", "")
        required_sectors = reqs.get("required_sector_types", [])
        if required_sectors and current_sector not in required_sectors:
            if not reqs.get("random_encounter_chance", 0) > 0: return False
        return True

    def get_discoverable_signals(self, current_player_status: Dict) -> List[SignalDefinition]:
        discoverable = []
        for signal_def in self._signal_definitions.values():
            if self.check_signal_discoverable(signal_def, current_player_status):
                discoverable.append(signal_def)
        return discoverable

    def get_signals_for_location(
            self, location: str,
            current_player_status: Dict,
            num_signals_to_select: int = 5
        ) -> List[SignalDefinition]:
        discoverable_signals = self.get_discoverable_signals(current_player_status)
        candidate_signals = []
        weights = []
        for sig_def in discoverable_signals:
            is_location_match = (not sig_def.spawn_locations or location in sig_def.spawn_locations)
            can_be_random_encounter = sig_def.discovery_requirements.get("random_encounter_chance", 0) > 0
            if is_location_match or can_be_random_encounter:
                effective_rarity = sig_def.base_rarity_score + sig_def.spawn_conditions_met_bonus
                if not is_location_match and can_be_random_encounter:
                    effective_rarity *= 0.1
                if effective_rarity > 0:
                    candidate_signals.append(sig_def)
                    weights.append(effective_rarity)
        if not candidate_signals: return []
        actual_num_to_select = min(num_signals_to_select, len(candidate_signals))
        if actual_num_to_select == 0: return []
        if sum(weights) == 0:
            if candidate_signals and actual_num_to_select > 0:
                 return random.sample(candidate_signals, actual_num_to_select)
            return []
        selected_signals = random.choices(candidate_signals, weights=weights, k=actual_num_to_select)
        unique_selected_signals_map = {sig.signal_id: sig for sig in selected_signals}
        final_selection = list(unique_selected_signals_map.values())
        return final_selection

if __name__ == '__main__':
    from src.content.signal_types import SignalTier, SignalTypeCategory
    from src.content.lore_manager import LoreManager

    print("--- Testing SignalManager (with Full Validation including Lore) ---")
    signal_manager = SignalManager()
    lore_manager_for_validation = LoreManager()
    all_lore_ids_for_validation = set(lore_manager_for_validation._lore_fragments.keys())

    num_loaded = len(signal_manager.get_all_signal_definitions())

    if num_loaded > 0:
        print(f"Successfully loaded {num_loaded} signals.")
        
        print("\n--- Testing Signal Interdependency (including Lore Links) Validation ---")
        validation_messages = signal_manager.validate_signal_interdependencies(all_lore_ids=all_lore_ids_for_validation)
        if validation_messages:
            print("Validation Issues Found in SignalManager:")
            for msg in validation_messages: print(f"  - {msg}")
        else:
            print("No interdependency or lore link validation issues found in SignalManager.")

        print("\n--- Testing LoreManager's Internal Dependency Validation ---")
        lore_validation_msgs = lore_manager_for_validation.validate_lore_dependencies(
            all_signal_ids=set(signal_manager._signal_definitions.keys())
        )
        if lore_validation_msgs:
            print("LoreManager Validation Issues Found:")
            for msg in lore_validation_msgs: print(f"  - {msg}")
        else:
            print("No internal dependency validation issues found in LoreManager.")

        print("\n--- Testing Get Unlocked Signals By (Brief) ---")
        pirate_relay_id = "PIRATE_DATA_RELAY_GAMMA"
        unlocked_by_pirate = signal_manager.get_unlocked_signals_by(pirate_relay_id)
        print(f"Signals directly unlocked by '{pirate_relay_id}': {len(unlocked_by_pirate)} found.")
        expected_pirate_unlock = "PIRATE_STRONGHOLD_BEACON_ALPHA"
        source_sig_pirate = signal_manager.get_signal_definition(pirate_relay_id)
        if source_sig_pirate and expected_pirate_unlock in source_sig_pirate.unlocks_signals and \
           not any(s.signal_id == expected_pirate_unlock for s in unlocked_by_pirate):
             print(f"  ERROR: Expected {expected_pirate_unlock} to be unlocked by {pirate_relay_id}")
        
        print("\n--- Testing Conceptual Stubs (Evolution/Degradation/Modifiers) ---")
        mock_game_state = {"player_actions_log": ["INVESTIGATE_PROBE_SOURCE"], "current_environment_hazard": "HIGH_RADIATION_STORM", "time_elapsed_total_hours": 100}
        example_signal_to_evolve = signal_manager.get_signal_definition("ANCIENT_PROBE_RETURN_SIGNAL")
        if example_signal_to_evolve:
            print(f"Evolution check for {example_signal_to_evolve.name}: {signal_manager.check_signal_evolution(example_signal_to_evolve, mock_game_state)}")
            live_data = {"current_strength": example_signal_to_evolve.strength_levels[0], "current_stability": example_signal_to_evolve.stability}
            print(f"Runtime modifiers for {example_signal_to_evolve.name} (original: {live_data}): {signal_manager.apply_runtime_modifiers(live_data, example_signal_to_evolve)}")
        
        example_signal_to_degrade = signal_manager.get_signal_definition("PIRATE_DATA_RELAY_GAMMA")
        if example_signal_to_degrade:
            print(f"Degradation check for {example_signal_to_degrade.name}: {signal_manager.check_signal_degradation(example_signal_to_degrade, mock_game_state)}")
        
        print("\n--- Testing Signal Discovery & Location Spawning (Abridged) ---")
        player_status_example_corrected = {
            "player_level": 5, "scanner_level": 2, "completed_signals": ["CIV_BEACON_STD_01"],
            "found_lore": ["LORE_ANCIENT_MYTHS"], "current_sector_type": "LAWLESS_SECTOR"
        }
        selected_signals = signal_manager.get_signals_for_location("LAWLESS_SECTOR", player_status_example_corrected, num_signals_to_select=2)
        print(f"Selected signals for 'LAWLESS_SECTOR': {[s.name for s in selected_signals]}")

        tags_to_test = ["pirate"]
        for tag_val in tags_to_test:
            print(f"\nSignals tagged with '{tag_val}' (default case-insensitive):")
            results = signal_manager.get_signal_ids_by_tag(tag_val)
            if results:
                for sig_id in results:
                    sig = signal_manager.get_signal_definition(sig_id)
                    print(f"  Found: {sig_id} - {sig.name if sig else 'Error'}")
            else:
                print(f"  No signals found with tag '{tag_val}'.")
    else:
        print("Warning: No signals loaded, cannot run detailed tests.")

    print("\n--- SignalManager Full Test Suite End ---")
