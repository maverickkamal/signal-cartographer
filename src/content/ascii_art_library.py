# ASCII Art Library for Signal Signatures
# Values are multi-line string literals.

SIGNAL_SIGNATURES = {
    "AM_STABLE_CLEAR": """
      .-'-.
     /     \\
    | (AM)  |
     \\  _  /
      '-.-'
    Frequency: Stable
    Strength: Clear
    """,

    "FM_NOISY_MODERATE": """
     ~~^~^~
    ~/ F M \\~
    ~| MOD |~
     ~\\~~~//~
      ~v~v~
    Frequency: Fluctuating
    Strength: Moderate (Noisy)
    """,

    "PULSED_SHARP_REPEATING": """
    | | | | | |
    | | | | | |
    |-*-*-*-*-*| PULSE
    | | | | | |
    | | | | | |
    Interval: Regular
    Shape: Sharp
    """,

    "DATA_BURST_COMPLEX": """
    >#>[##]>>##>
    [#<###<#]##>
    >##[<#>#]<#> DATA
    <##[##>]<##<
    <<[##]<#<##<
    Encoding: Complex Packets
    Duration: Short Bursts
    """,

    "EXOTIC_SWIRLING_UNSTABLE": """
      )  (
     ( () )
      )  (
    ( ()() ) ))
     (()()) ((
    ( () ) ) ))
      )(() (
    Pattern: Unstable Swirl
    Nature: Unknown, Exotic
    """,

    "WEAK_FADING_GENERIC": """
        .
      .   `
     .  (`) .
      ` . .
        `
    Strength: Very Weak
    Integrity: Fading
    """,

    "CW_STEADY_TONE": """
    ------------------
    ------------------
    ------ CW --------
    ------------------
    ------------------
    Tone: Continuous, Steady
    """
}

UPGRADE_SCHEMATICS = {
    "ANTENNA_MK2_SCHEMATIC": """
      /\\
     |==|
     |  |
    .|--|.
   / |__| \\
  |  ----  |
   \\____/
  ANTENNA - RangeBoost MkII
    """,

    "FILTER_AUDIO_SCHEMATIC": """
    Signal In --> [#####] --> Cleaned Out
                 [# F #]
                 [# I #]
    Noise In --->[# L #]--\\
                 [# T #]  |-> Rejected
                 [#####]--/
      AUDIO FILTER - Clarity Module v1
    """,

    "PROCESSOR_OVERCLOCK_SCHEMATIC": """
    +-----------------+
    | [CPU Core 0]--\\ |
    | [CPU Core 1]---\\|--[Overclock Unit]
    | [CPU Core 2]---/|      ||
    | [CPU Core 3]--/ |      VV
    +-----------------+   [Output Bus]
      PROCESSOR - Overclocking Interface
    """,

    "DECRYPTION_MODULE_SCHEMATIC": """
      KEY --> [Algorithmic Decryptor] --> PLAINTEXT
             |   [Pattern Analyzer]  |
             |-----------------------|
             \\-- [Heuristic Matrix] --/
       DECRYPTION MODULE - Cipher Breaker MkI
    """
}

UI_DECORATIONS = {
    "HORIZONTAL_DIVIDER_THIN": "----------------------------------------",
    "HORIZONTAL_DIVIDER_FANCY": ".oO--=[##]=--Oo.",
    "PANEL_CORNER_TL_SHARP": "/", # Top-Left
    "PANEL_CORNER_TR_SHARP": "\\", # Top-Right
    "PANEL_CORNER_BL_SHARP": "\\", # Bottom-Left
    "PANEL_CORNER_BR_SHARP": "/", # Bottom-Right
    "STATUS_ICON_OK": "[OK]",
    "STATUS_ICON_WARN": "[!!]",
    "STATUS_ICON_ERROR": "[XX]",
    "ARROW_RIGHT": "-->",
    "ARROW_LEFT": "<--",

    # Simple spinner frames
    "LOADING_SPINNER_FRAME_1": "|",
    "LOADING_SPINNER_FRAME_2": "/",
    "LOADING_SPINNER_FRAME_3": "-",
    "LOADING_SPINNER_FRAME_4": "\\",
}

STAR_MAP_ELEMENTS = {
    "STAR_TYPE_G": "(G)", # Yellow dwarf like Sol
    "STAR_TYPE_M": "(M)", # Red dwarf
    "STAR_TYPE_B": "(B)", # Blue giant
    "PLANET_TERRAN": " planète ", # Using simple text for now, can be more iconic
    "PLANET_GAS_GIANT": " géante gazeuse ",
    "PLANET_ROCKY": " planète rocheuse ",
    "ANOMALY_WORMHOLE": "<@>",
    "PLAYER_SHIP_ICON": "^P^",
    "SECTOR_BOUNDARY_SIMPLE": ":", # Used repeatedly to form a line
    "SPACE_STATION_ICON": "[#]",
    "ASTEROID_FIELD_ICON": "%", # Used sparsely in a region
    "NEBULA_ICON": "~",       # Used to fill a region
}

ENVIRONMENTAL_ART = {
    "SPACE_NEBULA_BACKGROUND_TILE": """
~ ~ * ~ ~ . ~
 ~ . ~ ~ * ~ ~
~ * ~ . ~ ~ *
 . ~ ~ * ~ . ~
~ ~ * ~ ~ . ~
    """, # Tileable in theory

    "ASTEROID_FIELD_DENSE": """
      . % % . .
    % . %. % % .
   . % . %  . % .
    %  % . % . %
   . %%%. % . % .
    %  . % % . %
    """,

    "PLANETARY_SURFACE_GENERIC": """
    ^^^^----....____----^^^^
   /                        \\
  |    generic surface     |
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """,

    "ORBITAL_VIEW_PLANET": """
       .--""--.
      /        \\
     |    ()    |
      \\        /
       `--..--'
    Orbiting: Terra Prime
    """
}


if __name__ == '__main__':
    print("--- ASCII Art Library Content ---")

    print(f"\n--- {len(SIGNAL_SIGNATURES)} Signal Signatures ---")
    # for name, art in SIGNAL_SIGNATURES.items():
    #     print(f"\n{name}:\n{art}")
    print("  (Signal Signatures printout skipped for brevity in test runs)")


    print(f"\n--- {len(UPGRADE_SCHEMATICS)} Upgrade Schematics ---")
    # for name, art in UPGRADE_SCHEMATICS.items():
    #     print(f"\n{name}:\n{art}")
    print("  (Upgrade Schematics printout skipped for brevity in test runs)")

    print(f"\n--- {len(UI_DECORATIONS)} UI Decorations ---")
    # for name, art in UI_DECORATIONS.items():
    #     print(f"\n{name}:\n{art}")
    print("  (UI Decorations printout skipped for brevity in test runs)")

    print(f"\n--- {len(STAR_MAP_ELEMENTS)} Star Map Elements ---")
    for name, art in STAR_MAP_ELEMENTS.items():
        print(f"\n{name}:\n{art}")

    print(f"\n--- {len(ENVIRONMENTAL_ART)} Environmental Art Pieces ---")
    for name, art in ENVIRONMENTAL_ART.items():
        print(f"\n{name}:\n{art}")

    print("\n--- Library Test End ---")
