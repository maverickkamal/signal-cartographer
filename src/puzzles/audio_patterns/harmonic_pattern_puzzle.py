import random
from typing import Optional, List, Tuple, Any, Dict
from src.puzzles.puzzle_base import PuzzleBase
from src.puzzles.audio_patterns.audio_tools import (
    generate_harmonic_series,
    introduce_inharmonic_frequencies
)

class HarmonicPatternPuzzle(PuzzleBase):
    """
    A puzzle where the player needs to identify inharmonic frequencies in a sequence.
    """
    BASE_FREQUENCIES: List[float] = [50.0, 60.0, 100.0, 110.0, 120.0, 150.0, 200.0, 220.0] # Hz
    SEQUENCE_LENGTH_RANGES: Dict[str, Tuple[int, int]] = { # Min, Max length
        "easy": (5, 7),
        "medium": (7, 10),
        "hard": (9, 12)
    }
    NUM_INHARMONIC_RANGES: Dict[str, Tuple[int, int]] = { # Min, Max number of inharmonic notes
        "easy": (1, 2), # Ensure at least one for the puzzle to make sense
        "medium": (2, 3),
        "hard": (3, 4)
    }
    MAX_HARMONIC_MULTIPLIER: Dict[str, int] = {
        "easy": 5,
        "medium": 7,
        "hard": 10
    }

    def __init__(self, difficulty: str):
        super().__init__(difficulty)
        self.title = "Harmonic Anomaly Detection"
        self.base_frequency: Optional[float] = None
        self.frequency_sequence: Optional[List[float]] = None
        # self.solution will store the list of indices of inharmonic frequencies

    def generate_puzzle(self):
        """
        Generates a harmonic pattern puzzle.
        """
        difficulty_key = self.difficulty if self.difficulty in self.SEQUENCE_LENGTH_RANGES else "medium"

        self.base_frequency = random.choice(self.BASE_FREQUENCIES)
        
        seq_len_min, seq_len_max = self.SEQUENCE_LENGTH_RANGES[difficulty_key]
        sequence_length = random.randint(seq_len_min, seq_len_max)
        
        max_harm_mult = self.MAX_HARMONIC_MULTIPLIER[difficulty_key]
        
        harmonic_sequence = generate_harmonic_series(
            base_freq=self.base_frequency,
            count=sequence_length,
            max_harmonic_multiple=max_harm_mult
        )
        
        num_inharm_min, num_inharm_max = self.NUM_INHARMONIC_RANGES[difficulty_key]
        # Ensure num_to_make_inharmonic does not exceed sequence_length
        num_to_make_inharmonic = random.randint(num_inharm_min, min(num_inharm_max, sequence_length))
        if num_to_make_inharmonic == 0 and sequence_length > 0 : # Ensure at least one if possible
             num_to_make_inharmonic = 1
        
        self.frequency_sequence, inharmonic_indices = introduce_inharmonic_frequencies(
            frequency_sequence=harmonic_sequence,
            num_inharmonic=num_to_make_inharmonic,
            base_freq=self.base_frequency
        )
        
        self.puzzle_data = self.frequency_sequence
        self.solution = sorted(inharmonic_indices)
        
        return self.puzzle_data

    def solve_puzzle(self, player_solution_input: Any) -> bool:
        """
        Checks player's identified indices of inharmonic frequencies.
        Input can be a list of ints or a comma-separated string of ints.
        """
        if self.solution is None: return False

        parsed_player_solution: List[int] = []
        if isinstance(player_solution_input, list):
            if not all(isinstance(item, int) for item in player_solution_input): return False
            parsed_player_solution = player_solution_input
        elif isinstance(player_solution_input, str):
            stripped_input = player_solution_input.strip()
            if not stripped_input: # Empty string means empty list
                parsed_player_solution = []
            else:
                try:
                    parts = [part.strip() for part in stripped_input.split(',') if part.strip()]
                    if not parts and stripped_input : return False # e.g. input was "," or ", ,"
                    parsed_player_solution = [int(part) for part in parts]
                except ValueError: return False
        else:
            return False
            
        return sorted(list(set(parsed_player_solution))) == sorted(list(set(self.solution))) # Use set to handle duplicates from player

    def display_puzzle(self) -> str:
        """
        Presents the puzzle to the player.
        """
        if not self.puzzle_data or not self.frequency_sequence:
            self.generate_puzzle()
            if not self.frequency_sequence: # Should not happen if generate_puzzle is correct
                 return "Error: Puzzle data could not be generated."


        display_freqs = [f"{freq:.2f} Hz" for freq in self.frequency_sequence]
        numbered_freq_list = "\n".join(
            [f"  {i}: {display_freqs[i]}" for i in range(len(display_freqs))]
        )

        instructions = (
            f"A sequence of {len(self.frequency_sequence)} audio frequencies is provided below. Most are harmonically\n"
            f"related to a common fundamental frequency (approx. {self.base_frequency:.2f} Hz).\n"
            f"Some frequencies are inharmonic (not part of the series or detuned).\n"
        )

        return (
            f"Puzzle: {self.title}\n"
            f"Difficulty: {self.difficulty}\n\n"
            f"{instructions}\n"
            f"Frequency Sequence (0-indexed):\n"
            f"{numbered_freq_list}\n\n"
            f"Task: Identify the 0-indexed positions of ALL inharmonic frequencies.\n"
            f"Submit your answer as a comma-separated list of numbers (e.g., 1,4,6)."
        )

if __name__ == '__main__':
    def run_harmonic_test_main(difficulty_level: str):
        print(f"\n--- Testing HarmonicPatternPuzzle: {difficulty_level.upper()} ---")
        puzzle = HarmonicPatternPuzzle(difficulty=difficulty_level)
        
        print(puzzle.display_puzzle())
        
        print(f"\nBase Frequency (internal): {puzzle.base_frequency:.2f} Hz" if puzzle.base_frequency else "N/A")
        # print(f"Full Frequency Sequence (internal): {puzzle.frequency_sequence}") # Can be verbose
        print(f"Inharmonic Indices (Solution): {puzzle.solution}")

        correct_solution_indices = puzzle.solution
        if correct_solution_indices is None:
            print("Error: Solution is None after puzzle generation.")
            return

        test_cases = []
        correct_sol_str = ",".join(map(str, correct_solution_indices))

        test_cases.append({"desc": "Correct (list)", "val": list(correct_solution_indices), "exp": True})
        test_cases.append({"desc": "Correct (string)", "val": correct_sol_str, "exp": True})
        test_cases.append({"desc": "Correct (list with duplicates, if solution not empty)",
                           "val": list(correct_solution_indices) + (correct_solution_indices[:1] if correct_solution_indices else []),
                           "exp": True})


        if correct_solution_indices: # If there are inharmonic notes
            if len(correct_solution_indices) > 1:
                 test_cases.append({"desc": "Partial (miss last)", "val": correct_solution_indices[:-1], "exp": False})
            
            # Find a 'wrong' index (a harmonic one)
            wrong_idx = -1
            if puzzle.frequency_sequence:
                for i in range(len(puzzle.frequency_sequence)):
                    if i not in correct_solution_indices:
                        wrong_idx = i
                        break
            if wrong_idx != -1:
                test_cases.append({"desc": "Partial + One Wrong", "val": (correct_solution_indices[:-1] if len(correct_solution_indices) > 1 else []) + [wrong_idx], "exp": False})
                test_cases.append({"desc": "Completely Wrong (one harmonic index)", "val": [wrong_idx], "exp": False})

        test_cases.append({"desc": "Empty list", "val": [], "exp": len(correct_solution_indices) == 0})
        test_cases.append({"desc": "Empty string", "val": "", "exp": len(correct_solution_indices) == 0})
        test_cases.append({"desc": "Non-numeric string", "val": "a,b,c", "exp": False})
        test_cases.append({"desc": "String with spaces", "val": " 1, 2 ", "exp": sorted([1,2]) == correct_solution_indices})


        for tc in test_cases:
            # Skip if val would be empty and solution is not, or vice versa, if it makes test invalid
            if not tc["val"] and tc["exp"] != (not correct_solution_indices) and isinstance(tc["val"],list):
                # e.g. test case "Partial (miss last)" if solution was just one item, val becomes []
                # if solution was [], then this is fine. if solution was [0], then val [] is !exp.
                if not correct_solution_indices : pass # val [] is exp if solution is []
                else: continue # val [] is not exp if solution is e.g. [0]

            is_correct = puzzle.solve_puzzle(tc["val"])
            result_str = "PASS" if is_correct == tc["exp"] else f"FAIL (got {is_correct}, expected {tc['exp']})"
            print(f"  Test '{tc['desc']}' with {tc['val']!r}: {result_str}")

    run_harmonic_test_main("easy")
    run_harmonic_test_main("medium")
    run_harmonic_test_main("hard")
    
    # Test edge case: what if num_inharmonic is 0 (e.g. if settings allowed it)
    # Current NUM_INHARMONIC_RANGES min is 1. If it was 0:
    print("\n--- Testing Edge Case: Potentially 0 Inharmonic Notes (if settings allowed) ---")
    temp_puzzle = HarmonicPatternPuzzle(difficulty="easy")
    # Manually set solution to empty to simulate this, as current generation always makes >0 inharmonics
    temp_puzzle.generate_puzzle() # Generate some data
    temp_puzzle.solution = [] # Override solution
    print(f"Sequence: {temp_puzzle.frequency_sequence}")
    print(f"Manually set solution to: {temp_puzzle.solution}")
    print(f"  Test empty list []: {temp_puzzle.solve_puzzle([])} (Expected: True)")
    print(f"  Test empty string '': {temp_puzzle.solve_puzzle('')} (Expected: True)")
    print(f"  Test list [0]: {temp_puzzle.solve_puzzle([0])} (Expected: False if sequence not empty)")


    print("\n--- End of HarmonicPatternPuzzle Tests ---")
