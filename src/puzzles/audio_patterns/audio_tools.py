import random

def generate_pulse_sequence(length: int, num_pulses: int) -> list[int]:
    """
    Generates a sequence of 0s and 1s representing silence and pulses.

    Args:
        length: The total length of the sequence.
        num_pulses: The number of pulses (1s) to place in the sequence.

    Returns:
        A list of integers (0s and 1s) representing the pulse sequence.
    """
    if not isinstance(length, int) or length < 0:
        raise ValueError("Length must be a non-negative integer.")
    if not isinstance(num_pulses, int) or num_pulses < 0:
        raise ValueError("Number of pulses must be a non-negative integer.")

    if num_pulses > length:
        num_pulses = length
    
    sequence = [0] * length
    if num_pulses > 0:
        pulse_indices = random.sample(range(length), num_pulses)
        for index in pulse_indices:
            sequence[index] = 1
    return sequence

if __name__ == '__main__':
    print("--- Testing generate_pulse_sequence from audio_tools.py ---")
    print(f"Test (10, 3): {generate_pulse_sequence(10, 3)}")
    print(f"Test (5, 5): {generate_pulse_sequence(5, 5)}")
    print(f"Test (8, 0): {generate_pulse_sequence(8, 0)}")
    print(f"Test (0, 0): {generate_pulse_sequence(0, 0)}")
    print(f"Test (3, 5) (capped): {generate_pulse_sequence(3, 5)}")
    try:
        generate_pulse_sequence(-5, 2)
    except ValueError as e:
        print(f"Caught expected error: {e}")
    try:
        generate_pulse_sequence(5, -2)
    except ValueError as e:
        print(f"Caught expected error: {e}")
    print("--- Test End ---")


# --- Audio Conversion Puzzle Tools ---

# Simple representation: 1 for short beep, 2 for long beep, 0 for space between letters
# More complex sounds could be represented by different numbers or even tuples, e.g., (freq, duration)
SIMPLE_TONE_MAP = {
    'A': [1, 2],    'B': [2, 1, 1, 1], 'C': [2, 1, 2, 1],
    'D': [2, 1, 1],  'E': [1],          'F': [1, 1, 2, 1],
    'G': [2, 2, 1],  'H': [1, 1, 1, 1], 'I': [1, 1],
    'J': [1, 2, 2, 2],'K': [2, 1, 2],    'L': [1, 2, 1, 1],
    'M': [2, 2],     'N': [2, 1],       'O': [2, 2, 2],
    'P': [1, 2, 2, 1],'Q': [2, 2, 1, 2], 'R': [1, 2, 1],
    'S': [1, 1, 1],  'T': [2],          'U': [1, 1, 2],
    'V': [1, 1, 1, 2],'W': [1, 2, 2],    'X': [2, 1, 1, 2],
    'Y': [2, 1, 2, 2],'Z': [2, 2, 1, 1],
    '0': [2, 2, 2, 2, 2], '1': [1, 2, 2, 2, 2],
    '2': [1, 1, 2, 2, 2], '3': [1, 1, 1, 2, 2],
    '4': [1, 1, 1, 1, 2], '5': [1, 1, 1, 1, 1],
    '6': [2, 1, 1, 1, 1], '7': [2, 2, 1, 1, 1],
    '8': [2, 2, 2, 1, 1], '9': [2, 2, 2, 2, 1],
    ' ': [0, 0] # Represent space between words clearly
}

# For display, we might use symbols:
TONE_DISPLAY_MAP = {
    1: '.', # dot
    2: '-', # dash
    0: ' ', # space
}

def text_to_pseudo_audio(text: str, tone_map: dict = SIMPLE_TONE_MAP, letter_sep_pulse: list = [0]) -> list[list[int]]:
    """
    Converts a text string to a sequence of "pseudo-audio" tones.
    Each character is converted to its tone sequence, and these sequences are collected.
    A letter separator is implicitly handled by the structure (list of lists).
    A word separator (space char in text) is handled by its own tone in tone_map.

    Args:
        text: The input string (alphanumeric, spaces).
        tone_map: A dictionary mapping characters to their tone sequences.
        letter_sep_pulse: A list of pulses to insert between letters (not used in current logic if space is in map).

    Returns:
        A list of lists, where each inner list is the tone sequence for a character.
        e.g., "HI" -> [[1,1,1,1], [1,1]]
    """
    text = text.upper()
    audio_sequence = []
    for char in text:
        if char in tone_map:
            audio_sequence.append(list(tone_map[char])) # Ensure we append a copy
        else:
            # Handle unknown characters, e.g., by skipping or using a placeholder
            # For now, skip unknown characters to avoid errors.
            # audio_sequence.append([-1]) # Or some indicator of unknown char
            pass
    return audio_sequence

def format_pseudo_audio_for_display(pseudo_audio_sequence: list[list[int]],
                                    display_map: dict = TONE_DISPLAY_MAP,
                                    letter_spacing: str = " ",
                                    word_spacing: str = "   ") -> str:
    """
    Formats the pseudo-audio sequence (list of lists of tones) into a human-readable string.

    Args:
        pseudo_audio_sequence: The sequence from text_to_pseudo_audio.
        display_map: Maps tone numbers (1, 2, 0) to display characters ('.', '-', ' ').
        letter_spacing: String to use as space between displayed characters within a letter's tones.
                        (Note: This is different from space between letters themselves)
        word_spacing: String to use for space between words (if space char was mapped to [0,0])

    Returns:
        A string representation like ".-- - / .."
    """
    displayed_output = []
    for char_tones in pseudo_audio_sequence:
        char_display = []
        is_word_space = all(tone == 0 for tone in char_tones) # Check if it's from ' ': [0,0]
        
        for tone in char_tones:
            char_display.append(display_map.get(tone, '?')) # '?' for unknown tones
        
        if is_word_space:
            displayed_output.append(word_spacing)
        else:
            displayed_output.append("".join(char_display))
            
    return letter_spacing.join(displayed_output).replace(word_spacing + letter_spacing, word_spacing) # Ensure word_spacing isn't split


if __name__ == '__main__':
    print("--- Testing generate_pulse_sequence from audio_tools.py ---")
    # ... (previous tests for generate_pulse_sequence remain) ...
    print(f"Test (10, 3): {generate_pulse_sequence(10, 3)}")
    print(f"Test (5, 5): {generate_pulse_sequence(5, 5)}")
    print(f"Test (8, 0): {generate_pulse_sequence(8, 0)}")
    print(f"Test (0, 0): {generate_pulse_sequence(0, 0)}")
    print(f"Test (3, 5) (capped): {generate_pulse_sequence(3, 5)}")
    try:
        generate_pulse_sequence(-5, 2)
    except ValueError as e:
        print(f"Caught expected error: {e}")
    try:
        generate_pulse_sequence(5, -2)
    except ValueError as e:
        print(f"Caught expected error: {e}")
    print("--- generate_pulse_sequence Test End ---\n")

    print("--- Testing Audio Conversion Tools ---")
    example_text = "HI THERE"
    pseudo_audio = text_to_pseudo_audio(example_text)
    print(f"Text: '{example_text}'")
    print(f"Pseudo-audio (raw): {pseudo_audio}")
    
    displayed_audio = format_pseudo_audio_for_display(pseudo_audio)
    print(f"Pseudo-audio (display): '{displayed_audio}'")

    example_text_2 = "SOS 123"
    pseudo_audio_2 = text_to_pseudo_audio(example_text_2)
    print(f"Text: '{example_text_2}'")
    print(f"Pseudo-audio (raw): {pseudo_audio_2}")
    displayed_audio_2 = format_pseudo_audio_for_display(pseudo_audio_2)
    print(f"Pseudo-audio (display): '{displayed_audio_2}'")

    # Test with unknown characters
    example_text_unknown = "HI! THERE?"
    pseudo_audio_unknown = text_to_pseudo_audio(example_text_unknown) # !, ? will be skipped
    print(f"Text: '{example_text_unknown}' (unknowns skipped)")
    print(f"Pseudo-audio (raw): {pseudo_audio_unknown}")
    displayed_audio_unknown = format_pseudo_audio_for_display(pseudo_audio_unknown)
    print(f"Pseudo-audio (display): '{displayed_audio_unknown}'")
    
    # Verify word spacing (space char mapped to [0,0], displayed as '   ')
    # Expected: ".... .." for HI, then "   " for space, then "- .... . .-. ." for THERE
    # H=[1,1,1,1] -> ....
    # I=[1,1] -> ..
    # Space=' ' -> [0,0] -> '   ' (via word_spacing parameter in format_pseudo_audio_for_display)
    # T=[2] -> -
    # H=[1,1,1,1] -> ....
    # E=[1] -> .
    # R=[1,2,1] -> .-.
    # E=[1] -> .
    # Expected formatted: ".... ..   - .... . .-. ."
    # Current format_pseudo_audio_for_display joins with letter_spacing (' ') by default
    # So "H I" would be ".... .." (H, space, I)
    # "H I   T H E R E"
    # The logic in format_pseudo_audio_for_display for word_spacing needs to be precise.
    # It joins all char_displays with letter_spacing, then tries to adjust.
    # If ' ' gives [0,0] and display_map[0] is ' ', then [0,0] becomes "  "
    # This "  " is then joined with other letters by letter_spacing " ".
    # E.g., for "HI THERE", audio is [[1,1,1,1], [1,1], [0,0], [2], [1,1,1,1], [1], [1,2,1], [1]]
    # Displayed: "....", "..", "  ", "-", "....", ".", ".-.", "."
    # Joined by " ": ".... ..     - .... . .-." (if "  " was from word_spacing)
    # The replace logic `replace(word_spacing + letter_spacing, word_spacing)` aims to fix extra spacing.
    # If word_spacing is "   " and letter_spacing is " ", it replaces "    " with "   ".
    # This seems reasonable.

    print("--- Audio Conversion Tools Test End ---\n")


# --- Harmonic Pattern Puzzle Tools ---

def generate_harmonic_series(base_freq: float, count: int, max_harmonic_multiple: int = 8) -> list[float]:
    """
    Generates a list of frequencies mostly belonging to the harmonic series of a base frequency.
    Args:
        base_freq: The fundamental frequency.
        count: The number of frequencies to generate in the list.
        max_harmonic_multiple: The maximum harmonic to consider (e.g., 8 means up to 8 * base_freq).
                               Higher harmonics are possible but less common for simple puzzles.
    Returns:
        A list of frequencies, primarily harmonics. Some might be repeated or from lower octaves
        if count is large relative to max_harmonic_multiple.
    """
    if base_freq <= 0:
        raise ValueError("Base frequency must be positive.")
    if count <= 0:
        return []
    if max_harmonic_multiple < 1:
        raise ValueError("Max harmonic multiple must be at least 1.")

    harmonics = [base_freq * i for i in range(1, max_harmonic_multiple + 1)]
    
    # If we need more frequencies than available unique harmonics, allow repeats or just use what we have.
    # For simplicity, we can sample with replacement if count > len(harmonics).
    output_frequencies = []
    for _ in range(count):
        output_frequencies.append(round(random.choice(harmonics), 2)) # Round to 2 decimal places for display
        
    # Shuffle to make it less obvious if there are repeats or ordered harmonics
    random.shuffle(output_frequencies)
    return output_frequencies

def introduce_inharmonic_frequencies(
    frequency_sequence: list[float],
    num_inharmonic: int,
    base_freq: float,
    inharmonic_range_factor: tuple = (0.1, 2.0), # Range around base_freq for random inharmonics
    detune_factor_range: tuple = (0.15, 0.45) # Percentage for detuning existing harmonics
    ) -> tuple[list[float], list[int]]:
    """
    Replaces a specified number of frequencies in the sequence with inharmonic ones.
    Also returns the indices of these inharmonic frequencies.

    Args:
        frequency_sequence: The original list of frequencies (mostly harmonic).
        num_inharmonic: The number of inharmonic frequencies to introduce.
        base_freq: The fundamental frequency, used to ensure inharmonics are truly not harmonic.
        inharmonic_range_factor: Multiplier for base_freq to define range for *new* random inharmonics.
                                 e.g. (0.1 * base_freq, 2.0 * base_freq).
        detune_factor_range: Min and max percentage (0.0 to 1.0) to detune an *existing* harmonic
                             to make it inharmonic. e.g. (0.15 means 15% detuning).

    Returns:
        A tuple containing:
            - The modified list of frequencies.
            - A list of indices where inharmonic frequencies were introduced.
    """
    if num_inharmonic == 0:
        return frequency_sequence, []
    if num_inharmonic > len(frequency_sequence):
        num_inharmonic = len(frequency_sequence) # Cannot make more items inharmonic than available

    modified_sequence = list(frequency_sequence)
    inharmonic_indices = []
    
    # Get indices that can be replaced
    replaceable_indices = list(range(len(modified_sequence)))
    random.shuffle(replaceable_indices) # Shuffle to pick random indices to change

    for i in range(num_inharmonic):
        if not replaceable_indices: break # Should not happen if num_inharmonic <= len

        idx_to_change = replaceable_indices.pop()
        original_freq = modified_sequence[idx_to_change]

        new_inharmonic_freq = 0
        attempts = 0
        while attempts < 20: # Try to generate a clearly inharmonic frequency
            attempts += 1

            # Strategy 1: Detune an existing harmonic (could be the one at idx_to_change or another)
            if random.random() < 0.7: # 70% chance to detune the current frequency at idx_to_change
                detune_amount = original_freq * random.uniform(detune_factor_range[0], detune_factor_range[1])
                if random.random() < 0.5: # Detune up or down
                    new_inharmonic_freq = original_freq + detune_amount
                else:
                    new_inharmonic_freq = original_freq - detune_amount
                if new_inharmonic_freq < base_freq * 0.5 : # Avoid going too low, make it positive
                    new_inharmonic_freq = original_freq + detune_amount
            else: # 30% chance to generate a more random inharmonic frequency
                min_f = base_freq * inharmonic_range_factor[0]
                max_f = base_freq * inharmonic_range_factor[1]
                new_inharmonic_freq = random.uniform(min_f, max_f)

            new_inharmonic_freq = round(new_inharmonic_freq, 2)
            if new_inharmonic_freq <=0: new_inharmonic_freq = round(base_freq * random.uniform(0.5, 1.5),2) # Ensure positive

            # Check if it's reasonably inharmonic (not too close to a true harmonic)
            is_clearly_inharmonic = True
            for h_mult in range(1, 10): # Check against first few harmonics
                harmonic_freq = base_freq * h_mult
                # If new freq is within ~5% of a true harmonic, it might be confusing
                if abs(new_inharmonic_freq - harmonic_freq) < 0.05 * harmonic_freq:
                    is_clearly_inharmonic = False
                    break
            if is_clearly_inharmonic:
                break
        
        # If after attempts, it's still not clearly inharmonic, it's probably fine, or use last generated.
        modified_sequence[idx_to_change] = new_inharmonic_freq
        inharmonic_indices.append(idx_to_change)
        
    inharmonic_indices.sort() # Return sorted indices
    return modified_sequence, inharmonic_indices


if __name__ == '__main__':
    # ... (previous main tests) ...
    print("--- Testing generate_pulse_sequence from audio_tools.py ---")
    print(f"Test (10, 3): {generate_pulse_sequence(10, 3)}")
    print(f"Test (5, 5): {generate_pulse_sequence(5, 5)}")
    print(f"Test (8, 0): {generate_pulse_sequence(8, 0)}")
    print(f"Test (0, 0): {generate_pulse_sequence(0, 0)}")
    print(f"Test (3, 5) (capped): {generate_pulse_sequence(3, 5)}")
    try:
        generate_pulse_sequence(-5, 2)
    except ValueError as e:
        print(f"Caught expected error: {e}")
    try:
        generate_pulse_sequence(5, -2)
    except ValueError as e:
        print(f"Caught expected error: {e}")
    print("--- generate_pulse_sequence Test End ---\n")

    print("--- Testing Audio Conversion Tools ---")
    example_text = "HI THERE"
    pseudo_audio = text_to_pseudo_audio(example_text)
    print(f"Text: '{example_text}'")
    # print(f"Pseudo-audio (raw): {pseudo_audio}") # Can be verbose
    displayed_audio = format_pseudo_audio_for_display(pseudo_audio)
    print(f"Pseudo-audio (display): '{displayed_audio}'")
    print("--- Audio Conversion Tools Test End ---\n")

    print("--- Testing Harmonic Pattern Tools ---")
    base_f = 100.0
    print(f"Base Frequency: {base_f} Hz")

    harm_series = generate_harmonic_series(base_f, 10, max_harmonic_multiple=5)
    print(f"Generated harmonic series (10 freqs, up to 5th harm): {harm_series}")

    harm_series_2 = generate_harmonic_series(base_f, 5, max_harmonic_multiple=3)
    print(f"Generated harmonic series (5 freqs, up to 3rd harm): {harm_series_2}")

    # Test introducing inharmonic frequencies
    original_sequence = [100.0, 200.0, 300.0, 400.0, 500.0, 150.0, 250.0, 350.0] # Mix of harmonic and already slightly off
    print(f"Original Sequence for inharmonic test: {original_sequence}")
    
    num_to_make_inharmonic = 2
    mod_seq, inharm_indices = introduce_inharmonic_frequencies(list(original_sequence), num_to_make_inharmonic, base_f)
    print(f"After making {num_to_make_inharmonic} inharmonic (target base {base_f}Hz):")
    print(f"  Modified sequence: {mod_seq}")
    print(f"  Inharmonic indices: {inharm_indices}")
    if len(inharm_indices) != num_to_make_inharmonic:
        print(f"Error: Expected {num_to_make_inharmonic} inharmonic indices, got {len(inharm_indices)}")

    # Verify inharmonic nature (simple check)
    for idx in inharm_indices:
        is_harmonic = False
        for h_mult in range(1,11): # Check up to 10th harmonic
            if abs(mod_seq[idx] - base_f * h_mult) < 0.01 * (base_f * h_mult): # within 1%
                is_harmonic = True
                break
        if is_harmonic:
            print(f"Warning: Freq {mod_seq[idx]} at index {idx} may still be perceived as harmonic to {base_f}.")

    print("--- Harmonic Pattern Tools Test End ---")
