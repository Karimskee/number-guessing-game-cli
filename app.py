"""
Task description:
You are required to build a simple number guessing game where the computer
randomly selects a number and the user has to guess it. The user will be given
a limited number of chances to guess the number. If the user guesses the number
correctly, the game will end, and the user will win. Otherwise, the game will
continue until the user runs out of chances.
"""

from helpers import clear_terminal


# Difficulties dictionary
difficulty_levels = {
    1: {
        "title": "Easy",
        "chances": 10
    },
    2: {
        "title": "Medium",
        "chances": 5
    },
    3: {
        "title": "Hard",
        "chances": 3
    },
}
round_difficulty = dict() # Chosen difficulty level for each round


def main():
    """Main program flow."""
    clear_terminal()
    welcome()
    get_difficulty()
    guessing_game()
    print("\n")


def welcome():
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    print("You have some number of chances to guess the correct number.")
    print()


def get_difficulty():
    global round_difficulty

    print("Please select the diffc level:")
    for i, diff in difficulty_levels.items(): 
        print(f"{i}. {diff.get('title')} ({diff.get('chances')} chance/s)")
    print()

    while True:
        chosen_difficulty = input("Enter your choice: ").strip()

        try:
            chosen_difficulty = int(chosen_difficulty)
        except ValueError:
            pass
        else:
            if (1 <= chosen_difficulty <= len(difficulty_levels)):
                round_difficulty = difficulty_levels.get(chosen_difficulty)
                print("Round difficulty level has been set.")
                print(f"You have {round_difficulty.get('chances')} chance/s.")
                print()
                break
        
        print()
        print("Invalid choice.")
        print("Please choose a numeric value from the list above.")
        print()


def guessing_game():
    pass


def hint():
    pass


def loss():
    pass


def win():
    pass


def play_again():
    pass


def high_score():
    pass


def timer():
    pass


if __name__ == "__main__":
    main()