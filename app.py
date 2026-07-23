"""
Task description:
You are required to build a simple number guessing game where the computer
randomly selects a number and the user has to guess it. The user will be given
a limited number of chances to guess the number. If the user guesses the number
correctly, the game will end, and the user will win. Otherwise, the game will
continue until the user runs out of chances.
"""

# RUN DEV COMMAND
# textual-hmr app.py:GuessingGameApp

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.reactive import reactive
from textual.containers import HorizontalGroup, VerticalScroll, VerticalGroup, Horizontal
from textual.widgets import Static, MaskedInput, Input, Select, Button, Label, Footer, Header

from getpass import getuser  # Getting system username
import json
from math import floor
from random import randint
import time  # Calculating round time

from helpers import clear_terminal


class WelcomeScreen(Screen):
    """Welcoming screen."""

    def compose(self) -> ComposeResult:
        """Called to add widgets to this container."""
        with VerticalScroll():
            yield Label("Welcome to the Number Guessing Game!", classes="header")
            yield Label("I'm thinking of a number between 1 and 100.\nYou have some number of chances to guess the correct number.", classes="explain")
            yield Label("Please choose a difficulty level", classes="difficulty-prompt")
            with HorizontalGroup(classes="difficulty-options"):
                for diff_level in self.app.difficulty_levels:
                    yield DifficultyButton(diff_level)

        self.start_prompt_flash()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id

        self.log(f"Button pressed ID: {button_id}")
        self.log.debug("Hey")

        match button_id:
            case "easy-diff-btn":
                self.app.round_difficulty = self.app.difficulty_levels[0]
            case "medium-diff-btn":
                self.app.round_difficulty = self.app.difficulty_levels[1]
            case "hard-diff-btn":
                self.app.round_difficulty = self.app.difficulty_levels[2]
    
        self.app.switch_screen("game")

    def start_prompt_flash(self):
        self.set_interval(1, self.flash_prompt)

    def flash_prompt(self):
        label = self.query_one(".difficulty-prompt", Label)
        label.visible = not label.visible


class GameScreen(Screen):
    """Guessing game screen."""

    rem_chances = reactive(0)

    def on_mount(self):
        self.rem_chances = self.app.round_difficulty.get("chances")
        self.target_number = randint(1, 100)
        self.guessed_number = 0
        self.attempts = 1
        self.time = 0
        self.invalid_label = self.query_one("#invalid-label", Label)
        self.incorrect_guess = self.query_one("#incorrect-guess", Label)
        self.notify(f"{self.target_number}")
        self.query_one("#guess-input", MaskedInput).focus()

    def compose(self) -> ComposeResult:
        """Called to add widgets to this container."""

        yield Label("Remaining Chances: ", id="remaining-chances", classes="remaining-chances")

        with VerticalScroll():

            with HorizontalGroup():
                yield Label("Enter your guess: ", classes="guess-prompt")
                yield MaskedInput("000", placeholder="000", id="guess-input", classes="guess-input")
            
            yield Label("Invalid input.\nPlease enter a numeric value in the range of [1, 100].", id="invalid-label", classes="invalid-label")
            yield Label(f"Incorrect! The number is greater than INPUT.", id="incorrect-guess", classes="incorrect-guess")
    
    def on_input_submitted(self, event: MaskedInput.Submitted):
        if event.input.id != "guess-input": return

        self.guessed_number = int(event.value)
        
        if not (1 <= self.guessed_number <= 100):
            self.invalid_guess()
        else:
            self.check_guessed_number()

        if self.rem_chances == 0:
            self.update_global_vars()
            self.app.switch_screen("loss")

    def invalid_guess(self):
        self.incorrect_guess.display = False
        self.invalid_label.display = True

    def check_guessed_number(self):
        self.invalid_label.display = False

        if self.guessed_number == self.target_number:
            self.update_global_vars()
            self.app.switch_screen("win")
            return

        self.incorrect_guess.update(f"Incorrect! The number is {'greater' if self.guessed_number < self.target_number else 'less'} than {self.guessed_number}.")
        self.incorrect_guess.display = True
        self.rem_chances -= 1
        self.attempts += 1

    def watch_rem_chances(self, value: int):
        rem_chances_label = self.query_one("#remaining-chances", Label)
        rem_chances_label.update(f"Remaining Chances: {value}")

    def update_global_vars(self):
        self.app.round_attempts = self.attempts
        self.app.round_target_number = self.target_number
        self.app.round_time = self.time
        self.app.round_rem_chances = self.rem_chances
        self.app.round_guessed_number = self.guessed_number


class WinScreen(Screen):
    """Game won screen."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rem_chances = self.app.round_rem_chances
        self.attempts = self.app.round_attempts
        self.time = self.app.round_time

    def on_mount(self):
        pass

    def compose(self) -> ComposeResult:
        """Called to add widgets to this container."""

        yield Label(f"Congratulations! You guessed the correct number in {self.attempts} attempt/s.")


class LossScreen(Screen):
    """Game loss screen."""

    def on_mount(self):
        pass

    def compose(self) -> ComposeResult:
        """Called to add widgets to this container."""

        yield Label(f"You ran out of chances! The correct number was {self.app.round_target_number}.")


class DifficultyButton(Button):
    """Difficulty button widget."""

    def __init__(self, diff_level: dict, **kwargs):
        super().__init__(**kwargs)

        t = diff_level.get("title")
        ch = diff_level.get("chances")
        co = diff_level.get("color")

        variant = {
            "green": "success",
            "yellow": "warning",
            "red": "error",
        }.get(co, "default")

        self.label = f"{t}\n[dim]{ch} {"chances" if ch > 1 else "chance"}[/]"
        self.id = f"{t}-diff-btn"
        self.variant = variant


class GuessingGameApp(App):
    """Managing the guessing game CLI app."""        

    CSS_PATH = "style.tcss"

    SCREENS = {
        "welcome": WelcomeScreen,
        "game": GameScreen,
        "win": WinScreen,
        "loss": LossScreen
    }

    # Difficulties dictionary
    difficulty_levels = [
        {"title": "easy", "chances": 10, "multiplier": 1, "color": "green"},
        {"title": "medium", "chances": 5, "multiplier": 2, "color": "yellow"},
        {"title": "hard", "chances": 3, "multiplier": 3, "color": "red"},
    ]

    round_difficulty = {}  # Chosen difficulty level for each round

    SCORES_FILE = "scores.json"
    hint_on_chance = -1  # Give a hint once rem chances is equal to this value

    round_attempts = 0
    round_target_number = 0
    round_time = 0.0
    round_rem_chances = 0
    round_guessed_number = 0

    def on_mount(self):
        self.push_screen(screen="welcome")


if __name__ == "__main__":
    GuessingGameApp().run()

# RUN DEV COMMAND
# textual-hmr app.py:GuessingGameApp
