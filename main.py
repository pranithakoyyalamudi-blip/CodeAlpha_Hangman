"""
=============================================================================
Project Name: CodeAlpha_Hangman_Game
Author: Prani (CodeAlpha Intern)
Description: A modular, console-based Hangman game implemented in Python.
             Developed as part of the CodeAlpha Python Programming Internship.
=============================================================================
"""

import random

# =============================================================================
# GAME CONSTANTS & CONFIGURATION
# =============================================================================

# Requirement 1: Exactly 5 predefined words stored inside a Python list
WORDS = [
    "PYTHON",
    "PROGRAMMING",
    "DEVELOPER",
    "ALGORITHM",
    "COMPUTER"
]

# Requirement 7: Maximum allowed incorrect guesses is 6
MAX_INCORRECT_GUESSES = 6

# Visual stages of the hangman gallows (0 to 6 incorrect guesses)
HANGMAN_STAGES = [
    # Stage 0: 0 incorrect guesses (empty gallows)
    """
       +---+
       |   |
           |
           |
           |
           |
    =========
    """,
    # Stage 1: 1 incorrect guess (head)
    """
       +---+
       |   |
       O   |
           |
           |
           |
    =========
    """,
    # Stage 2: 2 incorrect guesses (head and torso)
    """
       +---+
       |   |
       O   |
       |   |
           |
           |
    =========
    """,
    # Stage 3: 3 incorrect guesses (head, torso, one arm)
    """
       +---+
       |   |
       O   |
      /|   |
           |
           |
    =========
    """,
    # Stage 4: 4 incorrect guesses (head, torso, both arms)
    """
       +---+
       |   |
       O   |
      /|\\  |
           |
           |
    =========
    """,
    # Stage 5: 5 incorrect guesses (head, torso, both arms, one leg)
    """
       +---+
       |   |
       O   |
      /|\\  |
      /    |
           |
    =========
    """,
    # Stage 6: 6 incorrect guesses (full hangman, game over)
    """
       +---+
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    =========
    """
]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_random_word(word_list: list[str]) -> str:
    """
    Selects and returns a random word from the predefined word list.

    Args:
        word_list (list[str]): A list of uppercase word strings.

    Returns:
        str: A randomly chosen word.
    """
    return random.choice(word_list)


def display_word_state(word: str, guessed_letters: set[str]) -> str:
    """
    Constructs the masked representation of the target word.
    Correctly guessed letters are displayed, while unrevealed letters
    are shown as underscores separated by spaces.

    Example:
        For word "PYTHON" and guessed letters {'P', 'O'}:
        Output: "P _ _ _ O _"

    Args:
        word (str): The target secret word.
        guessed_letters (set[str]): Set of letters guessed by the player.

    Returns:
        str: Space-separated revealed letters and underscores.
    """
    display = [letter if letter in guessed_letters else "_" for letter in word]
    return " ".join(display)


def get_valid_guess(guessed_letters: set[str]) -> str:
    """
    Prompts the user for a letter guess and validates the input:
      - Checks that input is not empty.
      - Checks that input is exactly a single character.
      - Checks that the character is alphabetic (rejects numbers & symbols).
      - Checks whether the letter has already been guessed.

    Args:
        guessed_letters (set[str]): Set of letters already guessed.

    Returns:
        str: A single uppercase valid alphabetic character.
    """
    while True:
        try:
            raw_input = input("Enter your guess (a single letter): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nGame interrupted by user. Exiting...")
            raise

        # Check for empty input
        if not raw_input:
            print(">> [Error] Input cannot be empty. Please enter a letter.")
            continue

        # Check length (only 1 character permitted)
        if len(raw_input) != 1:
            print(">> [Error] Please enter exactly one letter at a time.")
            continue

        # Check if alphabetic (reject numbers, punctuation, spaces)
        if not raw_input.isalpha():
            print(">> [Error] Invalid character. Please enter an alphabetic letter (A-Z).")
            continue

        guess = raw_input.upper()

        # Check if already guessed
        if guess in guessed_letters:
            print(f">> [Notice] You already guessed '{guess}'. Try a different letter.")
            continue

        return guess


def play_round() -> None:
    """
    Executes a single complete round of the Hangman game.
    Initializes round state, manages turn-by-turn game loop,
    evaluates win/loss conditions, and displays final outcomes.
    """
    # Select word and initialize tracking state
    secret_word = get_random_word(WORDS)
    secret_letters = set(secret_word)
    guessed_letters: set[str] = set()
    incorrect_guesses = 0

    print("\n" + "=" * 50)
    print("           NEW ROUND STARTED!")
    print("=" * 50)
    print(f"The secret word has {len(secret_word)} letters. Good luck!")

    # Main gameplay loop for the round
    while incorrect_guesses < MAX_INCORRECT_GUESSES:
        remaining_attempts = MAX_INCORRECT_GUESSES - incorrect_guesses

        # Display current hangman visual stage
        print(HANGMAN_STAGES[incorrect_guesses])

        # Display game metrics
        print(f"Word to guess       : {display_word_state(secret_word, guessed_letters)}")
        print(f"Attempts remaining  : {remaining_attempts} / {MAX_INCORRECT_GUESSES}")

        sorted_guesses = sorted(list(guessed_letters))
        guesses_str = ", ".join(sorted_guesses) if sorted_guesses else "None"
        print(f"Letters guessed     : {guesses_str}")
        print("-" * 50)

        # Obtain a validated letter guess
        guess = get_valid_guess(guessed_letters)
        guessed_letters.add(guess)

        # Process guess outcome
        if guess in secret_letters:
            print(f"\n>> Excellent! '{guess}' is in the word!")
            # Check for victory condition (all letters discovered)
            if secret_letters.issubset(guessed_letters):
                print(HANGMAN_STAGES[incorrect_guesses])
                print("*" * 50)
                print("   CONGRATULATIONS! YOU WON THE ROUND!")
                print("*" * 50)
                print(f"You correctly guessed the word: {secret_word}")
                return
        else:
            incorrect_guesses += 1
            print(f"\n>> Sorry! '{guess}' is NOT in the word.")

    # If loop terminates without a win, player has run out of attempts
    print(HANGMAN_STAGES[MAX_INCORRECT_GUESSES])
    print("x" * 50)
    print("          GAME OVER! YOU LOST!")
    print("x" * 50)
    print(f"You have reached {MAX_INCORRECT_GUESSES} incorrect guesses.")
    print(f"The correct word was: {secret_word}")


def ask_play_again() -> bool:
    """
    Asks the player whether they wish to play another round.
    Validates user input to accept 'y', 'yes', 'n', 'no'.

    Returns:
        bool: True if player wants to play again, False otherwise.
    """
    while True:
        try:
            choice = input("\nWould you like to play another round? (y/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return False

        if choice in ("y", "yes"):
            return True
        elif choice in ("n", "no"):
            return False
        else:
            print(">> Please enter 'y' for yes or 'n' for no.")


def main() -> None:
    """
    Main application entry point.
    Displays the game header, manages the replay loop,
    and provides a clean exit message.
    """
    print("*" * 50)
    print("*" + " " * 48 + "*")
    print("*" + "   WELCOME TO CODEALPHA HANGMAN GAME!   ".center(48) + "*")
    print("*" + " " * 48 + "*")
    print("*" * 50)
    print("Rules:")
    print("  - Guess the secret word one letter at a time.")
    print("  - You have a maximum of 6 incorrect guesses.")
    print("  - Only standard alphabetic characters are valid.")
    print("=" * 50)

    try:
        while True:
            play_round()
            if not ask_play_again():
                print("\nThank you for playing CodeAlpha Hangman Game! Goodbye!\n")
                break
    except (EOFError, KeyboardInterrupt):
        print("\n\nGame closed. Thank you for playing!")


if __name__ == "__main__":
    main()