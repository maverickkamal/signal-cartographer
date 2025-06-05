from typing import Dict, List, Optional, Any, Union, Set
from src.content.lore_types import LoreFragment, LoreCategory, StoryArc # Ensure StoryArc is imported
from src.content.lore_database import (
    ALL_LORE_FRAGMENTS,
    LORE_FRAGMENTS_BY_ID,
    ALL_STORY_ARCS,
    STORY_ARCS_BY_ID
)
from src.content.signals_database import ALL_SIGNAL_DEFINITIONS # For validation

class LoreManager:
    """
    Manages all known lore fragments and story arcs in the game.
    Provides an interface to access and check unlockability of lore and arc progression.
    """
    def __init__(self):
        self._lore_fragments: Dict[str, LoreFragment] = {}
        self._story_arcs: Dict[str, StoryArc] = {}
        self._load_all_content()

    def _load_all_content(self) -> None:
        """Loads all lore fragments and story arcs from the central database."""
        if LORE_FRAGMENTS_BY_ID:
            self._lore_fragments = dict(LORE_FRAGMENTS_BY_ID)
        elif ALL_LORE_FRAGMENTS:
            for fragment in ALL_LORE_FRAGMENTS: self._lore_fragments[fragment.lore_id] = fragment

        if STORY_ARCS_BY_ID:
            self._story_arcs = dict(STORY_ARCS_BY_ID)
        elif ALL_STORY_ARCS:
            for arc in ALL_STORY_ARCS: self._story_arcs[arc.arc_id] = arc

    def get_lore_fragment(self, lore_id: str) -> Optional[LoreFragment]:
        return self._lore_fragments.get(lore_id)

    def get_all_lore_fragments(self) -> List[LoreFragment]:
        return list(self._lore_fragments.values())

    def get_lore_by_category(self, category_input: Union[LoreCategory, str]) -> List[LoreFragment]:
        target_category_value: Optional[str] = None
        if isinstance(category_input, LoreCategory):
            target_category_value = category_input.value
        elif isinstance(category_input, str):
            try: target_category_value = LoreCategory[category_input.upper().replace(" ", "_")].value
            except KeyError:
                for cat_enum in LoreCategory:
                    if cat_enum.value.lower() == category_input.lower():
                        target_category_value = cat_enum.value
                        break
                if not target_category_value: return []
        if target_category_value is None: return []
        return [f for f in self._lore_fragments.values() if f.category.value == target_category_value]

    def get_lore_by_tag(self, tag_str: str, case_sensitive: bool = False) -> List[LoreFragment]:
        matches: List[LoreFragment] = []
        for fragment in self._lore_fragments.values():
            target_tags = fragment.tags
            tag_to_find = tag_str.lower() if not case_sensitive else tag_str
            if not case_sensitive: target_tags = [t.lower() for t in fragment.tags]
            if tag_to_find in target_tags: matches.append(fragment)
        return matches

    def check_lore_unlockable(self, lore_fragment: LoreFragment, player_status: Dict[str, Any]) -> bool:
        reqs = lore_fragment.unlock_requirements
        if not reqs: return True
        if "required_signal_analyzed" in reqs and reqs["required_signal_analyzed"] not in player_status.get("analyzed_signals", set()): return False
        if "player_level" in reqs and player_status.get("player_level", 0) < reqs["player_level"]: return False
        if "found_other_lore" in reqs and not set(reqs["found_other_lore"]).issubset(player_status.get("found_lore_ids", set())): return False
        return True

    def get_unlockable_lore(self, player_status: Dict[str, Any]) -> List[LoreFragment]:
        return [f for f in self._lore_fragments.values() if self.check_lore_unlockable(f, player_status)]

    def get_story_arc(self, arc_id: str) -> Optional[StoryArc]:
        return self._story_arcs.get(arc_id)

    def get_all_story_arcs(self) -> List[StoryArc]:
        return list(self._story_arcs.values())

    def get_lore_for_arc(self, arc_id: str) -> List[LoreFragment]:
        arc = self.get_story_arc(arc_id)
        if not arc: return []
        return [self.get_lore_fragment(lore_id) for lore_id in arc.lore_fragment_ids if self.get_lore_fragment(lore_id)]

    def check_arc_status(self, arc_id: str, discovered_lore_ids: Set[str], completed_arc_ids: Set[str]) -> str:
        arc = self.get_story_arc(arc_id)
        if not arc: return "INVALID_ARC_ID"
        if not set(arc.required_arcs_completed).issubset(completed_arc_ids): return "LOCKED"

        completion_targets = set(arc.completion_lore_ids if arc.completion_lore_ids else arc.lore_fragment_ids)
        if completion_targets and completion_targets.issubset(discovered_lore_ids): return "COMPLETED"

        has_started = any(start_id in discovered_lore_ids for start_id in arc.starting_lore_ids)
        if not has_started and arc.starting_lore_ids: pass
        elif not arc.starting_lore_ids: has_started = any(lore_id in discovered_lore_ids for lore_id in arc.lore_fragment_ids)
        if has_started: return "IN_PROGRESS"
        return "AVAILABLE"

    def get_player_story_arc_summary(self, discovered_lore_ids: Set[str], completed_arc_ids: Set[str]) -> Dict[str, str]:
        return {arc_id: self.check_arc_status(arc_id, discovered_lore_ids, completed_arc_ids) for arc_id in self._story_arcs.keys()}

    def get_available_narrative_choices(self, lore_id: str, player_flags: Set[str]) -> List[Dict[str, Any]]:
        lore_fragment = self.get_lore_fragment(lore_id)
        if not lore_fragment or not lore_fragment.narrative_choices: return []
        return [choice for choice in lore_fragment.narrative_choices if set(choice.get("required_flags_for_choice", [])).issubset(player_flags)]

    def resolve_narrative_choice(self, lore_id: str, choice_index: int, player_flags: Set[str]) -> Dict[str, Any]:
        available_choices = self.get_available_narrative_choices(lore_id, player_flags)
        if not (0 <= choice_index < len(available_choices)): return {"error": "Invalid choice index."}
        chosen_option = available_choices[choice_index]
        outcomes: Dict[str, Any] = {}
        if "unlocks_lore_id_on_choice" in chosen_option: outcomes["unlocked_lore"] = chosen_option["unlocks_lore_id_on_choice"]
        if "triggers_event_on_choice" in chosen_option: outcomes["triggered_event"] = chosen_option["triggers_event_on_choice"]
        if "sets_player_flag_on_choice" in chosen_option: outcomes["set_flag"] = chosen_option["sets_player_flag_on_choice"]
        return outcomes

    def get_next_arc(self, completed_arc_id: str, player_flags: Set[str]) -> Optional[str]:
        completed_arc = self.get_story_arc(completed_arc_id)
        if not completed_arc: return None
        if completed_arc.arc_branches:
            for flag, next_arc_id in completed_arc.arc_branches.items():
                if flag in player_flags: return next_arc_id
        if completed_arc.unlocks_arcs: return completed_arc.unlocks_arcs[0]
        return None

    def validate_lore_dependencies(self, all_signal_ids: Optional[Set[str]] = None) -> List[str]:
        messages: List[str] = []
        all_lore = set(self._lore_fragments.keys())
        all_arcs = set(self._story_arcs.keys())
        if all_signal_ids is None: all_signal_ids = set(s.signal_id for s in ALL_SIGNAL_DEFINITIONS)

        for id, frag in self._lore_fragments.items():
            for lid in frag.unlocks_lore_ids:
                if lid not in all_lore: messages.append(f"Lore '{id}' unlocks non-existent lore '{lid}'.")
            if frag.narrative_choices:
                for choice in frag.narrative_choices:
                    if choice.get("unlocks_lore_id_on_choice") and choice["unlocks_lore_id_on_choice"] not in all_lore:
                        messages.append(f"Lore '{id}' choice '{choice['choice_text']}' unlocks non-existent lore '{choice['unlocks_lore_id_on_choice']}'.")
            if frag.unlock_requirements.get("required_signal_analyzed") and frag.unlock_requirements["required_signal_analyzed"] not in all_signal_ids:
                messages.append(f"Lore '{id}' requires non-existent signal '{frag.unlock_requirements['required_signal_analyzed']}'.")
            for req_lid in frag.unlock_requirements.get("found_other_lore", []):
                if req_lid not in all_lore: messages.append(f"Lore '{id}' requires non-existent other lore '{req_lid}'.")

        for id, arc in self._story_arcs.items():
            for lid in arc.lore_fragment_ids + arc.starting_lore_ids + arc.completion_lore_ids:
                if lid not in all_lore: messages.append(f"Arc '{id}' references non-existent lore '{lid}'.")
            for aid in arc.required_arcs_completed:
                if aid not in all_arcs: messages.append(f"Arc '{id}' requires non-existent arc '{aid}'.")
                elif aid == id: messages.append(f"Arc '{id}' requires itself.")
            for aid in arc.unlocks_arcs:
                if aid not in all_arcs: messages.append(f"Arc '{id}' unlocks non-existent arc '{aid}'.")
                elif aid == id: messages.append(f"Arc '{id}' unlocks itself.")
                # Check direct mutual unlock/requirement for arcs
                unlocked_arc_obj = self.get_story_arc(aid)
                if unlocked_arc_obj and id in unlocked_arc_obj.required_arcs_completed:
                     messages.append(f"StoryArc Validation (Circular Dep): Arc '{id}' unlocks '{aid}', which requires '{id}'.")

            if arc.arc_branches:
                for aid in arc.arc_branches.values():
                    if aid not in all_arcs: messages.append(f"Arc '{id}' branch points to non-existent arc '{aid}'.")
        return messages

if __name__ == '__main__':
    print("--- Testing LoreManager (including Story Arcs & Narrative Choices) ---")
    lore_manager = LoreManager()
    num_lore_loaded = len(lore_manager.get_all_lore_fragments())
    num_arcs_loaded = len(lore_manager.get_all_story_arcs())
    print(f"Loaded {num_lore_loaded} lore fragments and {num_arcs_loaded} story arcs.")

    if num_lore_loaded > 0 and ALL_LORE_FRAGMENTS and num_arcs_loaded > 0 and ALL_STORY_ARCS:
        print("\n--- Testing Narrative Choices ---")
        lore_with_choices_id = "ANCIENT_STARMAP_FRAGMENT_A"
        player_flags_set_test = {"FLAG_LINGUISTIC_TOOLS_ACQUIRED"}

        print(f"Getting available choices for '{lore_with_choices_id}' with flags: {player_flags_set_test}")
        choices = lore_manager.get_available_narrative_choices(lore_with_choices_id, player_flags_set_test)
        if choices:
            for i, choice in enumerate(choices):
                print(f"  Choice {i}: {choice['choice_text']}")
                if i == 0:
                    print(f"    Resolving choice {i} ('{choice['choice_text']}')...")
                    outcome = lore_manager.resolve_narrative_choice(lore_with_choices_id, i, player_flags_set_test)
                    print(f"    Outcome: {outcome}")
        else:
            print("  No choices available or lore fragment not found.")

        print("\n--- Testing Story Arc Status & Progression ---")
        player_status_test = {
            "discovered_lore_ids": {"ANCIENT_STARMAP_FRAGMENT_A", "LORE_PIRATE_NET_GAMMA"},
            "completed_arc_ids": set(),
            "player_flags": set()
        }
        arc_summary = lore_manager.get_player_story_arc_summary(
            player_status_test["discovered_lore_ids"], player_status_test["completed_arc_ids"]
        )
        print("Initial Arc Summary:")
        for arc_id, status_val in arc_summary.items(): print(f"  Arc '{arc_id}': {status_val}")

        probe_arc_id = "PROBE_ECHOES"
        probe_arc = lore_manager.get_story_arc(probe_arc_id)
        if probe_arc:
            player_status_test["discovered_lore_ids"].update(probe_arc.lore_fragment_ids)
            player_status_test["completed_arc_ids"].add(probe_arc_id)
            player_status_test["player_flags"].update(probe_arc.arc_flags_set_on_completion)

            print(f"\nPlayer completed '{probe_arc_id}', flags set: {probe_arc.arc_flags_set_on_completion}")

            next_arc_id = lore_manager.get_next_arc(probe_arc_id, player_status_test["player_flags"])
            print(f"Next arc after '{probe_arc_id}' (no specific player flag for branching yet): {next_arc_id}")

            player_status_test["player_flags"].add("PLAYER_FLAG_PRECURSOR_ARTEFACT_ACTIVATED")
            print(f"Player now has flag: PLAYER_FLAG_PRECURSOR_ARTEFACT_ACTIVATED")
            next_arc_id_branched = lore_manager.get_next_arc(probe_arc_id, player_status_test["player_flags"])
            print(f"Next arc after '{probe_arc_id}' (with specific flag for branching): {next_arc_id_branched}")

        print("\nUpdated Arc Summary:")
        arc_summary_updated = lore_manager.get_player_story_arc_summary(
             player_status_test["discovered_lore_ids"], player_status_test["completed_arc_ids"]
        )
        for arc_id, status_val in arc_summary_updated.items(): print(f"  Arc '{arc_id}': {status_val}")

        print("\n--- Testing Full Lore & Arc Dependency Validation ---")
        mock_signal_ids = set(s.signal_id for s in ALL_SIGNAL_DEFINITIONS) if ALL_SIGNAL_DEFINITIONS else set()
        validation_msgs_all = lore_manager.validate_lore_dependencies(all_signal_ids=mock_signal_ids)
        if validation_msgs_all:
            print("Validation Issues Found in LoreManager:")
            for msg in validation_msgs_all: print(f"  - {msg}")
        else:
            print("No lore or arc dependency validation issues found in LoreManager.")
    else:
        print("No lore fragments or story arcs loaded, skipping detailed tests.")

    print("\n--- LoreManager (Full Features) Test End ---")
