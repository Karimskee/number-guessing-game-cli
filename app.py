"""
Task description:
You are required to build a simple number guessing game where the computer
randomly selects a number and the user has to guess it. The user will be given
a limited number of chances to guess the number. If the user guesses the number
correctly, the game will end, and the user will win. Otherwise, the game will
continue until the user runs out of chances.
"""

from helpers import clear_terminal


def main():
    """Main program flow."""
    clear_terminal()
    welcome()
    difficulty()
    guessing_game()
    print("\n")


def welcome():
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    print("You have some number of chances to guess the correct number.")


def difficulty():
    pass


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