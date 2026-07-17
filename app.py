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
from math import floor
import json
from getpass import getuser


# Difficulties dictionary
difficulty_levels = {
    1: {
        "title": "Easy",
        "chances": 10,
        "multiplier": 1
    },
    2: {
        "title": "Medium",
        "chances": 5,
        "multiplier": 2
    },
    3: {
        "title": "Hard",
        "chances": 3,
        "multiplier": 3
    },
}
round_difficulty = dict() # Chosen difficulty level for each round

hint_on_chance = -1 # Give a hint once rem chances is equal to this value


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
    global hint_on_chance
    hint_on_chance = -1
    chances = round_difficulty.get("chances")
    target_number = randint(1, 100)
    print(target_number)
    attempts = 1
    is_won = False

    time_before_round = time.perf_counter()

    while chances > 0:
        print(f"Remaining chances: {chances}")
        hint(target_number, round_difficulty, chances) # If a hint is available
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
            
            if guessed_number == target_number:
                is_won = True
                break
            else:
                print()
                print(f"Incorrect! The number is {'greater' if target_number > guessed_number else 'less'} than {guessed_number}.")
                print()
                attempts += 1
                chances -= 1
                continue

    time_after_round = time.perf_counter()
    round_time = time_after_round - time_before_round

    if is_won:
        win(attempts, round_time)
    else:
        loss(target_number)


def invalid_guessed_number():
    print()
    print("Invalid input.")
    print("Please enter a numeric value in the range of [1, 100].")
    print()


def hint(target_num: int, round_difficulty: dict, rem_chances: int):
    global hint_on_chance
    total_chances = round_difficulty.get("chances")

    # If hint_on_chance is not determined, give it a rand value
    if hint_on_chance == -1 and rem_chances <= total_chances / 2:
        hint_on_chance = randint(1, floor(total_chances / 2))
        print(hint_on_chance)

    # Give a hint if hint is in this chance
    if rem_chances == hint_on_chance:
        target_num_str = str(target_num)
        num_digits = len(target_num_str)
        rand_digit = target_num_str[randint(0, num_digits - 1)]
        
        if num_digits == 1:
            print(f"Hint: The target number is of {num_digits} digit.")
        else:
            print(f"Hint: The target number is of {num_digits} digit/s, one of which is {rand_digit}.")


def loss(random_number):
    print()
    print("You have lost!")
    print(f"The number was {random_number}")
    play_again()


def win(attempts: int, round_time: float):
    print()
    print(f"Congratulations! You guessed the correct number in {attempts} attempt/s.")
    print(f"Time taken: {round_time:.2f} seconds.")
    score(attempts, round_time)
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


def score(attempts: int, round_time: float):
    SCORES_FILE = "scores.json"
    
    # Calculate score
    multiplier = round_difficulty.get("multiplier")
    score = round(1 / (attempts * round_time) * 100 * multiplier, 2)

    # Print score
    print(f"Your score is: {score} pts.")

    print()

    # Retrieve scores data
    # # Ensure file exists
    try:
        open(file=SCORES_FILE, mode="r", encoding="utf-8")
    except FileNotFoundError:
        file = open(file=SCORES_FILE, mode="w", encoding="utf-8")
        json.dump(fp=file, obj=[])

    # Get scores
    with open(file=SCORES_FILE, mode="r", encoding="utf-8") as file:
        try:
            all_scores = json.load(fp=file)
        except json.decoder.JSONDecodeError:
            all_scores = []

    # If a new high score
    if len(all_scores) > 0:
        highest_score = all_scores[0].get("score")
        
        if score > highest_score:
            print("You have got a new high score!")
        elif score == highest_score:
            print("Woh, you have got the exact same score as the current highest one!")
            print("That's a very rare chance, you are a lucky one!")

    # Insert score
    all_scores.append({"username": getuser(), "score": score})

    # Sort scores
    all_scores.sort(key=lambda x: x.get("score"), reverse=True)

    # Save score
    with open(file=SCORES_FILE, mode="w", encoding="utf-8") as file:
        try:
            json.dump(obj=all_scores, fp=file, indent=4)
        except:
            print("Sorry, we couldn't save your score.")
        else:
            print(f"Score has been saved with the name: {getuser()}")


if __name__ == "__main__":
    main()