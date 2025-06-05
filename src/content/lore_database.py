from src.content.lore_types import LoreFragment, LoreCategory, StoryArc # Import all necessary types
from typing import List, Dict

ALL_LORE_FRAGMENTS: List[LoreFragment] = [
    LoreFragment(
        lore_id="CORP_MEGACORPX_ORIGINS",
        title="MegaCorpX: The Early Years",
        content="MegaCorpX, initially a small asteroid mining company known as 'Xylos Minerals',\nrapidly expanded in the late 22nd century through aggressive acquisition strategies\nand breakthroughs in FTL fuel refinement, leading to their current galactic dominance.",
        category=LoreCategory.CORPORATE_HISTORY,
        tags=["MegaCorpX", "corporate", "history", "FTL", "economy"],
        source_description="Archived business journals, Galactic Standard Year 2250.",
        unlock_requirements={"player_level": 2, "visited_location_tag": "CORPORATE_HUB"},
        unlocks_lore_ids=["CORP_MEGACORPX_SCANDAL_2275"]
    ),
    LoreFragment(
        lore_id="ANCIENT_STARMAP_FRAGMENT_A",
        title="Ancient Starmap Fragment (Orion Spur)",
        content="This heavily damaged data chip contains a partial starmap. It depicts a section of\nthe Orion Spur, highlighting several uncharted systems. One system, designated 'Xylos' by\nthe map's creators, shows unusual energy readings. The cartographic style and dating\nsuggests it predates human deep-space exploration by millennia.",
        category=LoreCategory.ANCIENT_CIVILIZATION,
        tags=["Precursors", "starmap", "Orion Spur", "Xylos", "mystery", "artifact"],
        source_description="Recovered from a derelict Precursor survey vessel near an anomaly.",
        unlock_requirements={"required_signal_analyzed": "ANCIENT_PROBE_RETURN_SIGNAL"},
        unlocks_lore_ids=["ANCIENT_STARMAP_FRAGMENT_B", "PRECURSOR_LANGUAGE_BASICS_INTRO"],
        narrative_choices=[
            {
                "choice_text": "Focus on Xylos system data within the starmap.",
                "unlocks_lore_id_on_choice": "LORE_XYLOS_SYSTEM_DEEP_DIVE",
                "sets_player_flag_on_choice": "FLAG_XYLOS_PRIORITIZED"
            },
            {
                "choice_text": "Prioritize Precursor language analysis from map annotations.",
                "unlocks_lore_id_on_choice": "PRECURSOR_LANGUAGE_ADVANCED",
                "required_flags_for_choice": ["FLAG_LINGUISTIC_TOOLS_ACQUIRED"]
            }
        ]
    ),
    LoreFragment(
        lore_id="ANCIENT_STARMAP_FRAGMENT_B",
        title="Ancient Starmap Fragment (Perseus Arm Routes)",
        content="Further decryption of the Precursor starmap fragment reveals potential ancient\nnavigation routes extending towards the Perseus Arm. The complexity of these routes\nsuggests a sophisticated understanding of interstellar topology.",
        category=LoreCategory.ANCIENT_CIVILIZATION,
        tags=["Precursors", "starmap", "Perseus Arm", "navigation"],
        source_description="Decoded from advanced data layers within the Precursor survey vessel's memory core.",
        unlock_requirements={"found_other_lore": ["ANCIENT_STARMAP_FRAGMENT_A"], "player_skill_astronavigation": 3},
        unlocks_lore_ids=["PRECURSOR_HYPERLANE_THEORY"]
    ),
    LoreFragment(
        lore_id="XENO_CRYSTAL_LIFEFORMS_REPORT",
        title="Report: Crystalline Entities of Meridia IV",
        content="Preliminary xenobiological survey of Meridia IV indicates the presence of\nsilicon-based lifeforms exhibiting complex, dynamic crystalline structures...",
        category=LoreCategory.XENOBIOLOGY,
        tags=["crystalline_life", "Meridia IV", "alien_life"],
        source_description="Xeno-Geological Survey Team, initial findings.",
        unlock_requirements={"required_planet_scan": "MERIDIA_IV_BIOSIGNATURE_CONFIRMED"},
    ),
    LoreFragment(
        lore_id="TECH_WARP_DRIVE_THEORY",
        title="Theoretical Basis of Modern Warp Drives",
        content="The contemporary warp drive... remains a significant engineering hurdle...",
        category=LoreCategory.TECHNOLOGY,
        tags=["FTL", "warp_drive", "physics"],
        source_description="Standard Galactic University Physics Textbook Excerpt.",
    ),
    LoreFragment(
        lore_id="DISTRESS_VALIANT_LOG_ENTRY",
        title="Freighter 'Valiant' - Partial Voice Log",
        content="\"Mayday, Mayday! ... under attack... hull breach ... main power failing...\"",
        category=LoreCategory.DISTRESS,
        tags=["Valiant", "distress_call", "SOS"],
        source_description="Recovered from the Valiant's emergency distress beacon.",
        unlock_requirements={"required_signal_analyzed": "DISTRESS_CALL_FREIGHTER_VALIANT"}
    ),
    LoreFragment(
        lore_id="PRECURSOR_LANGUAGE_BASICS_INTRO",
        title="Introduction to Precursor Symbology",
        content="The Precursor written language appears to be logographic...",
        category=LoreCategory.ANCIENT_CIVILIZATION,
        tags=["Precursors", "language", "linguistics"],
        source_description="Compiled from artifact inscriptions.",
        unlock_requirements={"found_other_lore": ["ANCIENT_STARMAP_FRAGMENT_A"]},
        narrative_choices=[
             {
                "choice_text": "Share initial linguistic findings with Universal Archives.",
                "triggers_event_on_choice": "EVENT_ACADEMIC_INTEREST_PRECURSORS",
                "sets_player_flag_on_choice": "FLAG_PRECURSOR_DATA_SHARED_UAG"
            }
        ]
    ),
    LoreFragment(lore_id="LORE_CIV_BEACON_INFO", title="Civilian Beacon Network Overview", content="...", category=LoreCategory.TECHNOLOGY),
    LoreFragment(lore_id="LORE_PIRATE_NET_GAMMA", title="The Gamma Pirate Network", content="...", category=LoreCategory.PIRATE),
    LoreFragment(lore_id="LORE_PROBE_DISCOVERY", title="The \"Echo\" Probe Anomaly", content="...", category=LoreCategory.ARCHAEOLOGICAL),
    LoreFragment(lore_id="LORE_PROBE_ORIGINS_UNCLEAR", title="Origins of Probe \"Echo-1\"", content="...", category=LoreCategory.ARCHAEOLOGICAL),
    LoreFragment(lore_id="LORE_STELLAR_SONG", title="The Chorus of AEgir VII", content="...", category=LoreCategory.STELLAR),
    LoreFragment(lore_id="LORE_COSMIC_HARMONIES", title="Theories on Cosmic Harmonies", content="...", category=LoreCategory.STELLAR),
    LoreFragment(lore_id="LORE_VALIANT_FATE", title="The Freighter 'Valiant' Incident", content="...", category=LoreCategory.DISTRESS),
    # Dummy lore for choices/arcs
    LoreFragment(lore_id="LORE_XYLOS_SYSTEM_DEEP_DIVE", title="Xylos Deep Dive", content="Further Xylos data.", category=LoreCategory.ANCIENT_CIVILIZATION),
    LoreFragment(lore_id="PRECURSOR_LANGUAGE_ADVANCED", title="Advanced Precursor Lang.", content="More symbols translated.", category=LoreCategory.ANCIENT_CIVILIZATION),
    LoreFragment(lore_id="LORE_CORE_FILES_DOWNLOADED", title="Datapad Core Files", content="Encrypted schematics found.", category=LoreCategory.TECHNOLOGY),
    LoreFragment(lore_id="LORE_SURFACE_LOGS_READ", title="Datapad Surface Logs", content="Logs of a smuggler.", category=LoreCategory.PLAYER_JOURNAL),
    LoreFragment(lore_id="PRECURSOR_HYPERLANE_THEORY", title="Precursor Hyperlane Theory", content="Theory about Precursor FTL.", category=LoreCategory.ANCIENT_CIVILIZATION),
    LoreFragment(lore_id="LORE_PIRATE_HIDEOUT_LOC_A", title="Pirate Hideout Alpha", content="Location data for a hideout.", category=LoreCategory.PIRATE),
    LoreFragment(lore_id="LORE_VALIANT_BLACKBOX", title="Valiant Blackbox", content="Blackbox recording from the Valiant.", category=LoreCategory.DISTRESS),
    LoreFragment(lore_id="LORE_PROBE_FULL_MESSAGE", title="Probe Full Message", content="The complete decoded message from the probe.", category=LoreCategory.ARCHAEOLOGICAL),
    LoreFragment(lore_id="CORP_MEGACORPX_SCANDAL_2275", title="MegaCorpX Scandal of 2275", content="Details of the 2275 scandal.", category=LoreCategory.CORPORATE_HISTORY),
]

LORE_FRAGMENTS_BY_ID: Dict[str, LoreFragment] = {
    fragment.lore_id: fragment for fragment in ALL_LORE_FRAGMENTS
}

ALL_STORY_ARCS: List[StoryArc] = [
    StoryArc(
        arc_id="PROBE_ECHOES",
        title="The Echoing Probe",
        description="Unravel the mystery of an ancient probe and its strange, repeating signal.",
        lore_fragment_ids=[
            "ANCIENT_STARMAP_FRAGMENT_A",
            "PRECURSOR_LANGUAGE_BASICS_INTRO",
            "ANCIENT_STARMAP_FRAGMENT_B",
            "LORE_PROBE_DISCOVERY",
            "LORE_PROBE_ORIGINS_UNCLEAR",
            "PRECURSOR_HYPERLANE_THEORY"
        ],
        starting_lore_ids=["ANCIENT_STARMAP_FRAGMENT_A", "LORE_PROBE_DISCOVERY"],
        completion_lore_ids=["PRECURSOR_HYPERLANE_THEORY", "LORE_PROBE_ORIGINS_UNCLEAR"],
        required_arcs_completed=[],
        unlocks_arcs=["LOST_PRECURSOR_HOMEWORLD_ARC"],
        arc_flags_set_on_completion=["PROBE_ECHOES_COMPLETED", "PRECURSORS_DISCOVERED"],
        arc_branches={
            "FLAG_PROBE_DATA_SOLD_TO_CORP": "CORP_PROBE_EXPLOITATION_ARC", # Dummy arc ID
            "FLAG_PROBE_DATA_SHARED_ACADEMY": "ACADEMIC_PROBE_RESEARCH_ARC"  # Dummy arc ID
        }
    ),
    StoryArc(
        arc_id="VALIANT_MYSTERY",
        title="The Fate of the Freighter Valiant",
        description="Investigate the distress call of the Freighter Valiant and discover what happened to its crew.",
        lore_fragment_ids=["DISTRESS_VALIANT_LOG_ENTRY", "LORE_VALIANT_FATE", "LORE_VALIANT_BLACKBOX"],
        starting_lore_ids=["DISTRESS_VALIANT_LOG_ENTRY"],
        completion_lore_ids=["LORE_VALIANT_BLACKBOX"],
        required_arcs_completed=[],
        arc_flags_set_on_completion=["VALIANT_MYSTERY_SOLVED"]
    ),
    StoryArc(
        arc_id="GAMMA_PIRATE_CRACKDOWN",
        title="Cracking Down on Gamma Net",
        description="Disrupt the operations of the Gamma pirate network.",
        lore_fragment_ids=["LORE_PIRATE_NET_GAMMA", "CORP_MEGACORPX_ORIGINS", "LORE_PIRATE_HIDEOUT_LOC_A"],
        starting_lore_ids=["LORE_PIRATE_NET_GAMMA"],
        completion_lore_ids=["LORE_PIRATE_HIDEOUT_LOC_A"],
        arc_flags_set_on_completion=["GAMMA_NET_DISRUPTED"]
    ),
    # Dummy arcs for branching/linking tests
    StoryArc(arc_id="LOST_PRECURSOR_HOMEWORLD_ARC", title="The Lost Homeworld", description="Seek the Precursor homeworld.", lore_fragment_ids=["LORE_PROBE_FULL_MESSAGE"]),
    StoryArc(arc_id="PRECURSOR_TECHNOLOGY_PATH", title="Path of Technology", description="Focus on Precursor tech.", lore_fragment_ids=["LORE_PROBE_FULL_MESSAGE"]),
    StoryArc(arc_id="PRECURSOR_DANGER_PATH", title="Path of Danger", description="Heed Precursor warnings.", lore_fragment_ids=["LORE_PROBE_FULL_MESSAGE"]),
    StoryArc(arc_id="CORP_PROBE_EXPLOITATION_ARC", title="MegaCorpX Probe Exploitation", description="MegaCorpX is exploiting the probe data.", lore_fragment_ids=[]), # Needs at least one lore ID
    StoryArc(arc_id="ACADEMIC_PROBE_RESEARCH_ARC", title="Academic Probe Research", description="Academics study the probe.", lore_fragment_ids=[]), # Needs at least one lore ID
]
# Add minimal lore for dummy arcs if they have no fragments yet
for arc_id_to_check in ["CORP_PROBE_EXPLOITATION_ARC", "ACADEMIC_PROBE_RESEARCH_ARC"]:
    arc = next((a for a in ALL_STORY_ARCS if a.arc_id == arc_id_to_check), None)
    if arc and not arc.lore_fragment_ids:
        dummy_lore_id = f"LORE_FOR_{arc_id_to_check}"
        if dummy_lore_id not in LORE_FRAGMENTS_BY_ID:
            dummy_lore = LoreFragment(lore_id=dummy_lore_id, title=f"Intro to {arc.title}", content="This arc begins.", category=LoreCategory.UNDEFINED)
            ALL_LORE_FRAGMENTS.append(dummy_lore)
            LORE_FRAGMENTS_BY_ID[dummy_lore_id] = dummy_lore
        arc.lore_fragment_ids.append(dummy_lore_id)


STORY_ARCS_BY_ID: Dict[str, StoryArc] = {
    arc.arc_id: arc for arc in ALL_STORY_ARCS
}


if __name__ == '__main__':
    print(f"--- Final count of Lore Fragments: {len(ALL_LORE_FRAGMENTS)} ---")
    starmap_frag_a = LORE_FRAGMENTS_BY_ID.get("ANCIENT_STARMAP_FRAGMENT_A")
    if starmap_frag_a :
        print(f"\nFragment: {starmap_frag_a.title} (ID: {starmap_frag_a.lore_id})")
        if starmap_frag_a.narrative_choices:
            print(f"  Narrative Choices: {len(starmap_frag_a.narrative_choices)}")
            for choice_idx, choice in enumerate(starmap_frag_a.narrative_choices):
                print(f"    {choice_idx+1}. {choice.get('choice_text')}")
        else:
            print("  No narrative choices.")

    lang_frag = LORE_FRAGMENTS_BY_ID.get("PRECURSOR_LANGUAGE_BASICS_INTRO")
    if lang_frag:
        print(f"\nFragment: {lang_frag.title} (ID: {lang_frag.lore_id})")
        if lang_frag.narrative_choices:
            print(f"  Narrative Choices: {len(lang_frag.narrative_choices)}")
            for choice_idx, choice in enumerate(lang_frag.narrative_choices):
                print(f"    {choice_idx+1}. {choice.get('choice_text')}")
        else:
            print("  No narrative choices.")


    print(f"\n--- Loading {len(ALL_STORY_ARCS)} Story Arcs (with Branching Logic) ---")
    # ... (rest of the StoryArc __main__ test) ...
    for i, arc in enumerate(ALL_STORY_ARCS):
        print(f"\n  {i+1}. ID: {arc.arc_id}, Title: {arc.title}")
        print(f"     Flags on Completion: {arc.arc_flags_set_on_completion}")
        print(f"     Branches: {arc.arc_branches}")

    print("\n--- Lore & Story Arc Database Full Test End ---")
