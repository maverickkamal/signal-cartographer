import random
from typing import Optional, List, Dict
from src.puzzles.puzzle_base import PuzzleBase
from src.puzzles.audio_patterns.audio_tools import (
    SIMPLE_TONE_MAP,
    TONE_DISPLAY_MAP,
    text_to_pseudo_audio,
    format_pseudo_audio_for_display
)

class AudioConversionPuzzle(PuzzleBase):
    """
    A puzzle where the player needs to convert a pseudo-audio sequence back to text.
    The 'audio' is represented by sequences of symbolic tones (like Morse code).
    """
    WORD_LISTS: Dict[str, List[str]] = {
        "easy": ["HELLO", "WORLD", "TEST", "CODE", "GAME", "PLAY", "CAT", "DOG", "SUN", "MOON"],
        "medium": ["SIGNAL", "PUZZLE", "PYTHON", "AGENT", "SECRET", "MESSAGE", "BEACON", "CIPHER"],
        "hard": ["ENCRYPTION", "ALGORITHM", "TRANSMISSION", "CARTOGRAPHER", "FREQUENCY", "SEQUENCE", "PROTOCOL"]
    }
    NUM_WORDS: Dict[str, int] = {
        "easy": 1,
        "medium": 2,
        "hard": 2 # Hard could also be 3, or use longer words from its list
    }
    NUMBER_CHANCE: Dict[str, float] = {
        "easy": 0.15,
        "medium": 0.30,
        "hard": 0.50
    }

    def __init__(self, difficulty: str):
        super().__init__(difficulty)
        self.title = "Audio-to-Text Conversion"
        self.original_text: Optional[str] = None
        self.pseudo_audio_sequence: Optional[List[List[int]]] = None
        self.displayed_audio: Optional[str] = None
        # self.solution will store self.original_text

    def generate_puzzle(self):
        """
        Generates an audio-to-text conversion puzzle.
        - Selects a word or words based on difficulty.
        - May add numbers based on difficulty.
        - Converts the text to a pseudo-audio sequence.
        """
        # Use self.difficulty, defaulting to "medium" if not found (though PuzzleBase should validate)
        current_difficulty_key = self.difficulty if self.difficulty in self.WORD_LISTS else "medium"

        word_list = self.WORD_LISTS[current_difficulty_key]
        num_words = self.NUM_WORDS[current_difficulty_key]
        
        selected_words = [random.choice(word_list) for _ in range(num_words)]
        
        if random.random() < self.NUMBER_CHANCE[current_difficulty_key]:
            num_to_add = str(random.randint(1, 999))
            target_idx = random.randrange(len(selected_words)) if selected_words else 0
            
            if selected_words and random.random() < 0.7: # Add to existing word
                if random.random() < 0.5:
                    selected_words[target_idx] = num_to_add + selected_words[target_idx]
                else:
                    selected_words[target_idx] = selected_words[target_idx] + num_to_add
            else: # Add as a new "word" or if selected_words is empty
                selected_words.insert(target_idx, num_to_add) # Insert to make it more varied
        
        self.original_text = " ".join(selected_words)
        
        self.pseudo_audio_sequence = text_to_pseudo_audio(self.original_text, SIMPLE_TONE_MAP)
        self.displayed_audio = format_pseudo_audio_for_display(
            self.pseudo_audio_sequence,
            TONE_DISPLAY_MAP
        )
        
        self.puzzle_data = self.displayed_audio
        self.solution = self.original_text
        
        return self.puzzle_data

    def solve_puzzle(self, player_solution: str) -> bool:
        """
        Checks if the player's transcribed text matches the original text.
        Comparison is case-insensitive and ignores leading/trailing/excess internal whitespace.
        """
        if self.solution is None:
            return False
        
        normalized_player_solution = " ".join(player_solution.strip().upper().split())
        normalized_actual_solution = " ".join(self.solution.strip().upper().split())
        
        return normalized_player_solution == normalized_actual_solution

    def display_puzzle(self) -> str:
        """
        Presents the puzzle to the player, showing the pseudo-audio representation.
        """
        if not self.puzzle_data: # Should imply self.displayed_audio is also None
            self.generate_puzzle()

        legend = (
            "Legend:\n"
            "  '.' represents a short tone (like Morse dot)\n"
            "  '-' represents a long tone (like Morse dash)\n"
            "  Tones for each character are grouped (e.g., '.-' is one letter).\n"
            "  Spaces between these groups represent separation between letters.\n"
            "  A wider gap (e.g., ' / ' or '   ') separates words.\n"
            "The following sequence of tones was detected:"
        )

        return (
            f"Puzzle: {self.title}\n"
            f"Difficulty: {self.difficulty}\n\n"
            f"{legend}\n\n"
            f"Audio Signal: '{self.displayed_audio}'\n\n" # self.puzzle_data is self.displayed_audio
            f"Task: Transcribe the text from the pseudo-audio signal.\n"
            f"Enter the transcribed text below."
        )

if __name__ == '__main__':
    def run_conversion_test(difficulty_level):
        print(f"\n--- Testing AudioConversionPuzzle: {difficulty_level.upper()} ---")
        puzzle = AudioConversionPuzzle(difficulty=difficulty_level)
        
        # Test display before generation (should auto-generate)
        print("Displaying puzzle (auto-generates if needed):")
        print(puzzle.display_puzzle())
        
        print(f"\nOriginal Text (Solution): '{puzzle.original_text}'")
        # print(f"Pseudo-audio (raw internal): {puzzle.pseudo_audio_sequence}") # Can be verbose

        correct_answer = puzzle.original_text
        if correct_answer is None:
            print("Error: original_text is None after puzzle generation and display.")
            return

        test_attempts = {
            "Exact Match": correct_answer,
            "Lowercase": correct_answer.lower(),
            "Leading/Trailing Space": f" {correct_answer} ",
            "Extra Internal Space": "  ".join(correct_answer.split(" ")) if " " in correct_answer else correct_answer,
            "Slightly Incorrect": correct_answer[:-1] + "X" if len(correct_answer) > 1 else "X",
            "Empty String": ""
        }
        
        if not correct_answer: # Handle case where original_text might be empty (e.g. if word lists were empty)
             test_attempts["Empty String (Correct if solution is empty)"] = ""


        for desc, attempt_str in test_attempts.items():
            # Skip "Slightly Incorrect" if it accidentally matches the solution after normalization
            if desc == "Slightly Incorrect" and \
               (" ".join(attempt_str.strip().upper().split()) == " ".join(correct_answer.strip().upper().split())):
                print(f"Skipping '{desc}' test as it matched solution after normalization.")
                continue

            is_correct = puzzle.solve_puzzle(attempt_str)
            expected_correct = (" ".join(attempt_str.strip().upper().split()) == \
                                " ".join(correct_answer.strip().upper().split()))

            status = "Correct" if is_correct else "Incorrect"
            expectation_met = (is_correct == expected_correct)

            print(f"Attempt '{desc}' ('{attempt_str}'): {status} "
                  f"({'OK' if expectation_met else 'FAIL - Expected: ' + ('Correct' if expected_correct else 'Incorrect')})")

    run_conversion_test("easy")
    run_conversion_test("medium")
    run_conversion_test("hard")

    print("\n--- Specific Test: Puzzle with Numbers ---")
    number_puzzle_made = False
    for i in range(10): # Try a few times to get a number
        num_puzzle = AudioConversionPuzzle(difficulty="hard")
        num_puzzle.generate_puzzle()
        if num_puzzle.original_text and any(char.isdigit() for char in num_puzzle.original_text):
            print(f"Generated Text with Numbers: '{num_puzzle.original_text}'")
            print(f"Displayed Audio: '{num_puzzle.displayed_audio}'")
            is_ok = num_puzzle.solve_puzzle(num_puzzle.original_text)
            print(f"Self-solve with numbers: {'Correct' if is_ok else 'Incorrect'}")
            number_puzzle_made = True
            break
    if not number_puzzle_made:
        print("Could not generate a puzzle with numbers through random chance for test.")

    print("\n--- End of AudioConversionPuzzle Tests ---")
