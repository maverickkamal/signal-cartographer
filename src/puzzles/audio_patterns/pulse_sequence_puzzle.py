import random
from src.puzzles.puzzle_base import PuzzleBase
from src.puzzles.audio_patterns.audio_tools import generate_pulse_sequence

class PulseSequencePuzzle(PuzzleBase):
    def __init__(self, difficulty):
        super().__init__(difficulty)
        self.puzzle_data = None # Stores the sequence (e.g., [1,0,1,0,0])
        self.solution = None    # Stores the indices of pulses (e.g., [0,2])
        self.title = "Pulse Sequence Puzzle"

    def generate_puzzle(self):
        """
        Generates a pulse sequence puzzle based on the difficulty level.
        """
        if self.difficulty == "easy":
            length = random.randint(4, 6)
            num_pulses = random.randint(2, 3)
        elif self.difficulty == "medium":
            length = random.randint(6, 9)
            num_pulses = random.randint(3, 5)
        elif self.difficulty == "hard":
            length = random.randint(8, 12)
            num_pulses = random.randint(4, 6)
        else: # Default to medium if difficulty is unknown or invalid
            # print(f"Warning: Unknown difficulty '{self.difficulty}', defaulting to medium.")
            self.difficulty = "medium" # Correct the difficulty
            length = random.randint(6, 9)
            num_pulses = random.randint(3, 5)

        self.puzzle_data = generate_pulse_sequence(length, num_pulses)
        self.solution = self._calculate_solution(self.puzzle_data)
        return self.puzzle_data

    def solve_puzzle(self, player_solution_input):
        """
        Checks if the player's solution matches the actual solution.
        Player's solution can be a list of integers or a comma-separated string of integers.
        """
        if self.solution is None:
            # This implies generate_puzzle was not called or failed.
            return False

        parsed_player_solution = []
        if isinstance(player_solution_input, list):
            # Ensure all elements are integers if it's a list
            if not all(isinstance(item, int) for item in player_solution_input):
                return False # Contains non-integer elements
            parsed_player_solution = player_solution_input
        elif isinstance(player_solution_input, str):
            stripped_input = player_solution_input.strip()
            if not stripped_input: # Empty string input (e.g., "" or "   ")
                parsed_player_solution = []
            else:
                try:
                    # Filter out empty strings that result from trailing commas or multiple commas (e.g. "1,,2" or "1,")
                    parts = [part.strip() for part in stripped_input.split(',') if part.strip()]
                    # If after stripping and filtering, parts is empty but original input was not (e.g. input was just "," or ",,"),
                    # this means it's not a valid representation of a list of numbers.
                    if not parts and stripped_input: # e.g. input was "," or ", ,"
                        return False # Invalid input format
                    parsed_player_solution = [int(part) for part in parts]
                except ValueError:
                    return False # Contains non-integer values (e.g. "1,a,2")
        else:
            return False # Unsupported solution type (not list or string)

        return sorted(parsed_player_solution) == sorted(self.solution)

    def display_puzzle(self):
        """
        Returns a string representation of the puzzle for the player.
        This includes an ASCII representation and instructions.
        """
        if not self.puzzle_data:
            self.generate_puzzle() # Ensure puzzle is generated if not already

        visual_representation = "".join(["|" if p == 1 else "-" for p in self.puzzle_data])

        instructions = (
            f"Puzzle: {self.title}\n"
            f"Difficulty: {self.difficulty}\n"
            f"Length of sequence: {len(self.puzzle_data)}\n"
            f"Visual: {visual_representation}\n"
            f"Task: Identify the 0-indexed positions of the pulses ('|').\n"
            f"Submit your answer as a comma-separated list of numbers (e.g., 0,2,4)."
        )
        return instructions

    def _calculate_solution(self, puzzle_data):
        """
        Helper function to determine the solution from the puzzle data.
        The solution is a list of 0-indexed positions of pulses.
        """
        return [i for i, pulse in enumerate(puzzle_data) if pulse == 1]

if __name__ == '__main__':
    # A very minimal test to ensure basic functionality
    print("--- Minimal Pulse Sequence Puzzle Instantiation Test ---")
    # Ensure the imported generate_pulse_sequence is used.
    # The PulseSequencePuzzle class should now use the imported function.

    # Temporarily re-assign to test the global module function if needed for __main__
    # However, the class itself will use the imported one.
    # from src.puzzles.audio_patterns.audio_tools import generate_pulse_sequence as imported_gps
    # original_main_gps = globals().get('generate_pulse_sequence')
    # if 'generate_pulse_sequence' in globals():
    #     del globals()['generate_pulse_sequence'] # remove to ensure class uses its import

    try:
        easy_puzzle = PulseSequencePuzzle(difficulty="easy")
        print("Easy puzzle instance created.")
        # The generate_puzzle method within easy_puzzle should use the imported version
        # of generate_pulse_sequence.
        displayed_easy = easy_puzzle.display_puzzle()
        print(f"Easy puzzle display:\n{displayed_easy}")
        print(f"Easy puzzle internal data: {easy_puzzle.puzzle_data}")
        print(f"Easy puzzle solution: {easy_puzzle.solution}")

        if easy_puzzle.solution is not None:
            correct_solution_str = ",".join(map(str, easy_puzzle.solution))
            print(f"Solving with '{correct_solution_str}': {easy_puzzle.solve_puzzle(correct_solution_str)}")
            print(f"Solving with {easy_puzzle.solution}: {easy_puzzle.solve_puzzle(list(easy_puzzle.solution))}")
            print(f"Solving with empty string '': {easy_puzzle.solve_puzzle('')}")
            print(f"Solving with empty list []: {easy_puzzle.solve_puzzle([])}")

        if easy_puzzle.solution == []:
             print("The generated easy puzzle happened to have no pulses.")
             print(f"Solving '' for no-pulse solution: {easy_puzzle.solve_puzzle('')}")
             print(f"Solving [] for no-pulse solution: {easy_puzzle.solve_puzzle([])}")

    except Exception as e:
        print(f"An error occurred during minimal testing: {e}")
    finally:
        # Restore original generate_pulse_sequence in globals if it was changed for main
        # if original_main_gps:
        #    globals()['generate_pulse_sequence'] = original_main_gps
        pass # No actual change to globals was made in this version of the test.

    print("--- Minimal Test End ---")
