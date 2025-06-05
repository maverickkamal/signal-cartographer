from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum

class LoreCategory(Enum):
    """Categorization for lore fragments."""
    ANCIENT_CIVILIZATION = "Ancient Civilization"
    XENOBIOLOGY = "Xenobiology"
    CORPORATE_HISTORY = "Corporate History"
    MYTHS_LEGENDS = "Myths & Legends"
    TECHNOLOGY = "Technology"
    GALACTIC_GEOGRAPHY = "Galactic Geography"
    PLAYER_JOURNAL = "Player Journal" # For player-discovered or inferred lore
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

    # How this piece of lore is typically discovered or its nature
    source_description: Optional[str] = None

    # Requirements for this lore fragment to become available/discoverable
    # Examples: {"required_signal_analyzed": "ANCIENT_PROBE_01", "player_level": 5, "found_other_lore": ["LORE_ID_PREVIOUS"]}
    unlock_requirements: Dict[str, Any] = field(default_factory=dict)

    # Other lore fragments that this one might lead to or help unlock
    unlocks_lore_ids: List[str] = field(default_factory=list)

    # Narrative Branching
    narrative_choices: Optional[List[Dict[str, Any]]] = field(default_factory=list)
    # Example for a choice dict:
    # {
    #   "choice_text": "Investigate further?",
    #   "unlocks_lore_id_on_choice": "LORE_FURTHER_INVESTIGATION",
    #   "triggers_event_on_choice": "EVENT_PROBE_SITE_COLLAPSE",
    #   "sets_player_flag_on_choice": "PLAYER_FLAG_PROBE_DISTURBED",
    #   "required_flags_for_choice": ["PLAYER_FLAG_SCANNER_MK2"]
    # }

    def __post_init__(self):
        if not self.lore_id:
            raise ValueError("LoreFragment must have a lore_id.")
        if not self.title:
            raise ValueError("LoreFragment must have a title.")
        if not self.content:
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

        if self.narrative_choices is not None:
            if not isinstance(self.narrative_choices, list):
                raise ValueError("narrative_choices must be a list of dictionaries or None.")
            for choice in self.narrative_choices:
                if not isinstance(choice, dict):
                    raise ValueError("Each item in narrative_choices must be a dictionary.")
                if "choice_text" not in choice or not isinstance(choice["choice_text"], str):
                    raise ValueError("Each narrative choice must have a 'choice_text' (string).")

if __name__ == '__main__':
    print("--- Testing LoreFragment Definition (including narrative choices) ---")

    try:
        lore_with_choices = LoreFragment(
            lore_id="LORE_CHOICE_TEST_001",
            title="The Derelict Datapad",
            content="You find a datapad. It flickers with two options:",
            category=LoreCategory.TECHNOLOGY,
            narrative_choices=[
                {
                    "choice_text": "Download core files (risky).",
                    "unlocks_lore_id_on_choice": "LORE_CORE_FILES_DOWNLOADED",
                    "triggers_event_on_choice": "EVENT_VIRUS_DETECTED",
                    "sets_player_flag_on_choice": "FLAG_DATAPAD_CORRUPTED"
                },
                {
                    "choice_text": "Scan for surface logs only.",
                    "unlocks_lore_id_on_choice": "LORE_SURFACE_LOGS_READ",
                    "required_flags_for_choice": ["FLAG_SCANNER_SECURE_MODE"] # Conceptual flag
                }
            ]
        )
        print(f"Created Lore: {lore_with_choices.title}, Choices: {len(lore_with_choices.narrative_choices)}")

        print("\nTesting LoreFragment validation failures (narrative_choices):")
        try: # Test bad choice structure (not a dict)
            LoreFragment(lore_id="LC002", title="T2", content="C2", category=LoreCategory.TECHNOLOGY, narrative_choices=["choice1_text_only"]) # type: ignore
        except ValueError as e:
            print(f"Caught expected: {e}")
        try: # Test choice missing text
            LoreFragment(lore_id="LC003", title="T3", content="C3", category=LoreCategory.TECHNOLOGY, narrative_choices=[{"unlocks_lore_id_on_choice": "LID"}])
        except ValueError as e:
            print(f"Caught expected: {e}")

    except Exception as e:
        print(f"An unexpected error occurred during LoreFragment testing: {e}")

    print("\n--- LoreFragment Definition Test End (including narrative choices) ---")


# --- Story Arc System Types ---

@dataclass
class StoryArc:
    """
    Represents a narrative story arc composed of multiple lore fragments and progression conditions.
    """
    arc_id: str  # Unique string identifier (e.g., "ANCIENT_AWAKENING")
    title: str   # Human-readable title of the story arc
    description: str # A brief overview of the story arc

    lore_fragment_ids: List[str] = field(default_factory=list)
    starting_lore_ids: List[str] = field(default_factory=list)
    completion_lore_ids: List[str] = field(default_factory=list)
    required_arcs_completed: List[str] = field(default_factory=list)
    unlocks_arcs: List[str] = field(default_factory=list)

    # Narrative Branching for Arcs
    arc_flags_set_on_completion: List[str] = field(default_factory=list)
    # Defines how this arc might branch to different next arcs based on player flags
    # Key: player flag that, if set, triggers this branch. Value: next arc_id.
    # A special key like "default" could be used if no flags match, or rely on unlocks_arcs.
    arc_branches: Optional[Dict[str, str]] = field(default_factory=dict)


    def __post_init__(self):
        if not self.arc_id:
            raise ValueError("StoryArc must have an arc_id.")
        if not self.title:
            raise ValueError("StoryArc must have a title.")
        if not self.description:
            raise ValueError("StoryArc must have a description.")
        if not self.lore_fragment_ids:
            raise ValueError("StoryArc must have at least one lore_fragment_id associated with it.")

        for field_name, field_val in [
            ("lore_fragment_ids", self.lore_fragment_ids),
            ("starting_lore_ids", self.starting_lore_ids),
            ("completion_lore_ids", self.completion_lore_ids),
            ("required_arcs_completed", self.required_arcs_completed),
            ("unlocks_arcs", self.unlocks_arcs),
            ("arc_flags_set_on_completion", self.arc_flags_set_on_completion)
        ]:
            if not isinstance(field_val, list):
                raise ValueError(f"StoryArc field '{field_name}' must be a list.")
            if not all(isinstance(item, str) for item in field_val): # Flags also string IDs
                raise ValueError(f"All items in StoryArc field '{field_name}' must be strings.")

        if self.arc_branches is not None:
            if not isinstance(self.arc_branches, dict):
                raise ValueError("arc_branches must be a dictionary or None.")
            if not all(isinstance(k, str) and isinstance(v, str) for k, v in self.arc_branches.items()):
                raise ValueError("All keys and values in arc_branches must be strings.")


if __name__ == '__main__':
    # This __main__ block in lore_types.py is getting crowded.
    # Ideally, tests would be in separate files.
    # For now, just adding new tests for StoryArc branching fields.
    print("\n--- Testing StoryArc Definition (including branching fields) ---")
    try:
        arc_with_branching = StoryArc(
            arc_id="PROBE_MYSTERY_BRANCH_TEST",
            title="Probe Mystery with Branches",
            description="An arc that can branch based on player flags.",
            lore_fragment_ids=["LORE_TEST_001"], # Minimal lore for test
            arc_flags_set_on_completion=["PROBE_MYSTERY_CONCLUDED_PEACEFULLY"],
            arc_branches={
                "PLAYER_CHOSE_AGGRESSION": "PROBE_WAR_ARC",
                "PLAYER_CHOSE_DIPLOMACY": "PROBE_ALLIANCE_ARC"
            },
            unlocks_arcs=["DEFAULT_FOLLOWUP_IF_NO_BRANCH"] # Fallback
        )
        print(f"Created Story Arc: {arc_with_branching.title}, Flags on complete: {arc_with_branching.arc_flags_set_on_completion}")
        print(f"  Branches: {arc_with_branching.arc_branches}")

        print("\nTesting StoryArc validation failures (branching):")
        try:
            StoryArc(arc_id="", title="No ID", description="Desc", lore_fragment_ids=["LORE1"])
        except ValueError as e:
            print(f"Caught expected for empty arc_id: {e}")
        try:
            StoryArc(arc_id="ARC_FAIL", title="T", description="D", lore_fragment_ids=["L1"], arc_branches={"flag_A": 123}) # type: ignore
        except ValueError as e:
            print(f"Caught expected (arc_branches value not str): {e}")
        try:
            StoryArc(arc_id="ARC_FAIL2", title="T", description="D", lore_fragment_ids=["L1"], arc_flags_set_on_completion=[123]) # type: ignore
        except ValueError as e:
            print(f"Caught expected (arc_flags item not str): {e}")


    except Exception as e:
        print(f"An unexpected error occurred during StoryArc testing: {e}")
    print("--- StoryArc Definition Test End (including branching) ---")
