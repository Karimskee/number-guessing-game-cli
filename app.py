"""
Task description:
You are required to build a simple number guessing game where the computer
randomly selects a number and the user has to guess it. The user will be given
a limited number of chances to guess the number. If the user guesses the number
correctly, the game will end, and the user will win. Otherwise, the game will
continue until the user runs out of chances.
"""

from helpers import clear_terminal
from random import randint
import time


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


def get_difficulty():
    print()
    global round_difficulty

    print("Please select the difficulty level:")
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
                break
        
        print()
        print("Invalid choice.")
        print("Please choose a numeric value from the list above.")
        print()


def guessing_game():
    print()
    chances = round_difficulty.get("chances")
    random_number = randint(1, 100)
    print(random_number)
    attempts = 1
    is_won = False

    time_before_round = time.perf_counter()

    while chances > 0:
        print(f"Remaining chances: {chances}")
        guessed_number = input("Enter your guess: ").strip()

        try:
            guessed_number = int(guessed_number)
        except ValueError:
            invalid_guessed_number()
            continue
        else:
            if guessed_number < 1 or guessed_number > 100:
                invalid_guessed_number()
                continue
            
            if guessed_number == random_number:
                is_won = True
                break
            else:
                print()
                print(f"Incorrect! The number is {'greater' if random_number > guessed_number else 'less'} than {guessed_number}.")
                print()
                attempts += 1
                chances -= 1
                continue

    time_after_round = time.perf_counter()
    round_time = time_after_round - time_before_round

    if is_won:
        win(attempts, round_time)
    else:
        loss(random_number)


def invalid_guessed_number():
    print()
    print("Invalid input.")
    print("Please enter a numeric value in the range of [1, 100].")
    print()


def hint():
    pass


def loss(random_number):
    print()
    print("You have lost!")
    print(f"The number was {random_number}")
    play_again()


def win(attempts: int, round_time: float):
    print()
    print(f"Congratulations! You guessed the correct number in {attempts} attempt/s.")
    print(f"Time taken: {round_time:.2f} seconds.")
    play_again()


def play_again():
    print()
    while True:
        choice = input("Give it another shot? Y/N\n").strip().lower()

        if choice == 'y':
            get_difficulty()
            guessing_game()
            break
        elif choice == 'n':
            print()
            print("Sorry for wasting your time :>")
            print("Have a great day!")
            break
        else:
            print()
            print("Invalid choice.")
            print("It's clear enough that it's whether Y or N!")
            print("How could you fail to get that!")
            print()


def high_score():
    pass



if __name__ == "__main__":
    main()