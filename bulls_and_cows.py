from ttkthemes import ThemedStyle
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import random
import data
import images

# Global declarations
DATA_FILE = "data/isograms.txt"
SETTINGS_FILE = "data/settings.txt"
# End global declarations


class BullsAndCows:
    def __init__(self):
        self.current_word = ""
        self.current_guess = ""
        self.current_result = ""
        self.isogram_list = []
        self.guess_number = 0
        self.max_guesses = 0
        self.max_word_length = 0
        self.min_word_length = 0
        self.get_settings()
        self.load_data_file()
        self.game_running = False
        self.guess_history_items = []
        self.result_history_items = []

    def load_data_file(self, debug=False):
        with open(DATA_FILE, "r") as file:
            self.isogram_list = file.readlines()
        for i, word in enumerate(self.isogram_list):
            self.isogram_list[i] = word.lower().strip()  # sanitize word list
        if debug:
            print(self.isogram_list)

    def get_settings(self, debug=False):
        with open(SETTINGS_FILE, "r") as file:
            config = file.readlines()
            for setting in config:
                if debug:
                    print(setting)
                if "max_guesses" in setting:
                    self.max_guesses = int(setting.split("=")[1])
                if "max_word_length" in setting:
                    self.max_word_length = int(setting.split("=")[1])
                if "min_word_length" in setting:
                    self.min_word_length = int(setting.split("=")[1])

    def new_game(self, debug=False):
        self.current_word = ""
        self.current_guess = ""
        self.current_result = ""
        self.isogram_list = []
        self.guess_number = 1
        self.max_guesses = 0
        self.max_word_length = 0
        self.min_word_length = 0
        self.get_settings()
        self.load_data_file()
        self.game_running = True
        for label in self.guess_history_items:
            label.grid_remove()
        for label in self.result_history_items:
            label.grid_remove()

        self.current_word = ""

        while len(self.current_word) < self.min_word_length or len(self.current_word) > self.max_word_length:
            self.current_word = random.choice(self.isogram_list)
        self.max_guesses = len(self.current_word) + 2
        if debug:
            print(len(self.current_word))
            print(self.min_word_length)
            print(self.max_word_length)
            print(self.current_word)
            print(self.guess_number)

        self.current_guess = 1
        player_guess_label.config(text=f"Guess #{self.current_guess} of {self.max_guesses}: ")
        cows_speak_label.config(text=f"We have chosen a secret word with {len(self.current_word)} characters.")

    def set_result(self, current_guess_number: int, current_guess: str, result: str, debug=False):
        if debug:
            print(self.guess_history_items)
        self.guess_history_items[current_guess_number].config(text=current_guess)
        self.guess_history_items[current_guess_number].grid(pady=5)
        self.result_history_items[current_guess_number].config(text=result)
        self.result_history_items[current_guess_number].grid(pady=5)

    @staticmethod
    def split_word(word):
        return [char for char in word]

    @staticmethod
    def intersection(lst1, lst2):
        lst3 = [value for value in lst1 if value in lst2]
        return lst3

    def make_guess(self):
        if self.game_running:
            self.current_guess = player_guess_entry.get()
            self.current_guess = self.current_guess.lower()
            if len(self.current_guess) == len(self.current_word):
                # print(f"Current guess number: {self.guess_number} of {self.max_guesses}")

                guess = self.split_word(self.current_guess)
                secret_word = self.split_word(self.current_word)
                intersection = self.intersection(guess, secret_word)

                # print(f"inter = {intersection}")
                # print(f"guess = {guess}")
                results = ""
                # print(f"Secret word len = {len(secret_word)}")
                for i, letter in enumerate(secret_word):
                    # print(i)
                    if guess[i] not in intersection:
                        results += "X"
                        continue
                    if guess[i] == secret_word[i]:
                        results += "B"
                        continue
                    else:
                        results += "C"

                self.set_result(self.guess_number, self.current_guess, str(results))

                if self.current_guess == self.current_word:
                    if self.play_again(True):
                        self.new_game()
                elif self.guess_number >= self.max_guesses:
                    # print("Player has lost.")
                    if self.play_again(False):
                        self.new_game()
                    else:
                        self.game_running = False
                else:
                    self.guess_number += 1
                    player_guess_label.config(text=f"Guess #{self.guess_number} of {self.max_guesses}: ")
            else:
                messagebox.showinfo(message=f"You gave {len(self.current_guess)} letters instead of {len(self.current_word)}")

    def play_again(self, win_or_lose: str):
        if not win_or_lose:
            return messagebox.askyesno(
                message=f"Sorry, you loose.  The secret word was: {self.current_word}  Try again?",
                icon="question", title="Confirm Quit")
        if win_or_lose:
            return messagebox.askyesno(
                message=f"""
                Congratulations...  You win!
                You got the word: {self.current_word} in {self.guess_number} guesses.
                Play again?""",
                icon="question", title="Confirm Quit")

    @staticmethod
    def about():
        messagebox.showinfo(message="""
        Bulls and cows part Moo v1.0 was written in python
        using tkinter.  This little pet project was created 
        for my wife Dawn, who loved a console version I had 
        written years ago.  I just thought it was about
        time to give her a modern version :)""")

    @staticmethod
    def how_to_play():
        messagebox.showinfo(message="""
        Bulls and cows is a word game where you try to guess
        the secret word of the cows.  Every chosen secret
        word is an isogram (meaning no letters are repeated).
        after each guess you will be presented with results
        like 'XCBXXBC' where 'X' means that letter is not in the
        word.  A 'C' or cow is given for correct letters but in
        the wrong place.  Finally a 'B' or bull is given for
        each correct letter in the right place.  You will be
        given a number of tries equal to 2 plus the length
        of the current secret word.  Get the word right and
        you win!  Good luck!""")


game = BullsAndCows()

root = tk.Tk()
root.resizable(False, False)
root.title("Bulls and cows")
root.option_add('*tearOff', False)

style = ThemedStyle(root)
# print(style.get_themes())
style.set_theme("plastik")

main = ttk.Frame(root)
main.grid(row=0, column=0)

menu_bar = tk.Menu()
root.config(menu=menu_bar)

help_menu = tk.Menu(menu_bar)
menu_bar.add_cascade(menu=help_menu, label="Help")
help_menu.add_command(label="About", command=game.about)
help_menu.add_command(label="How to play", command=game.how_to_play)

logo_image = Image.open("images/Cows.gif")
logo_image = logo_image.resize((300, 300), Image.ANTIALIAS)
logo_image = ImageTk.PhotoImage(logo_image)

left_frame = tk.Frame(main)
center_frame = tk.Frame(main)
right_frame = tk.Frame(main)
bottom_frame = tk.Frame(main)

left_frame.grid(row=0, column=0, sticky="sw", padx=10)
center_frame.grid(row=0, column=1, sticky="nsew")
right_frame.grid(row=0, column=2, sticky="nsew")
bottom_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=10)

title_label = ttk.Label(center_frame, text="Bulls and Cows Part Moo", anchor="center")
title_label.config(font=("Times", 20))
title_label.grid(row=0, column=0, sticky="n")

main_image = tk.Label(center_frame, image=logo_image, anchor="center")
main_image.image = logo_image
main_image.grid(row=1, column=0)

cows_speak_label = ttk.Label(center_frame, text="We have not chosen a word yet.  Please start game.")
cows_speak_label.grid(row=2, column=0)

player_frame = tk.Frame(center_frame)
player_guess_label = ttk.Label(player_frame, text=f"Guess #{game.guess_number} of {game.max_guesses}:")
player_guess_entry = ttk.Entry(player_frame)
submit_guess_button = ttk.Button(player_frame, text="Submit", command=game.make_guess)
player_frame.grid(row=3, column=0)
player_guess_label.grid(row=0, column=0)
player_guess_entry.grid(row=0, column=1)
submit_guess_button.grid(row=0, column=2)

guess_history_label = ttk.Label(right_frame, text="Guesses", font="timesx12")
guess_history_label2 = ttk.Label(right_frame, text="Results", font="timesx12")
guess_history_label.grid(row=0, column=0, padx=10)
guess_history_label2.grid(row=0, column=1, padx=10)

guess1_history = ttk.Label(right_frame, text="", font="timesx8")
result1_history = ttk.Label(right_frame, text="", font="timesx8")
guess2_history = ttk.Label(right_frame, text="", font="timesx8")
result2_history = ttk.Label(right_frame, text="", font="timesx10")
guess3_history = ttk.Label(right_frame, text="", font="timesx10")
result3_history = ttk.Label(right_frame, text="", font="timesx10")
guess4_history = ttk.Label(right_frame, text="", font="timesx10")
result4_history = ttk.Label(right_frame, text="", font="timesx10")
guess5_history = ttk.Label(right_frame, text="", font="timesx10")
result5_history = ttk.Label(right_frame, text="", font="timesx10")
guess6_history = ttk.Label(right_frame, text="", font="timesx10")
result6_history = ttk.Label(right_frame, text="", font="timesx10")
guess7_history = ttk.Label(right_frame, text="", font="timesx10")
result7_history = ttk.Label(right_frame, text="", font="timesx10")
guess8_history = ttk.Label(right_frame, text="", font="timesx10")
result8_history = ttk.Label(right_frame, text="", font="timesx10")
guess9_history = ttk.Label(right_frame, text="", font="timesx10")
result9_history = ttk.Label(right_frame, text="", font="timesx10")
guess10_history = ttk.Label(right_frame, text="", font="timesx10")
result10_history = ttk.Label(right_frame, text="", font="timesx10")
guess11_history = ttk.Label(right_frame, text="", font="timesx10")
result11_history = ttk.Label(right_frame, text="", font="timesx10")
guess12_history = ttk.Label(right_frame, text="", font="timesx10")
result12_history = ttk.Label(right_frame, text="", font="timesx10")
game.guess_history_items.append(guess1_history)
game.result_history_items.append(result1_history)
game.guess_history_items.append(guess2_history)
game.result_history_items.append(result2_history)
game.guess_history_items.append(guess3_history)
game.result_history_items.append(result3_history)
game.guess_history_items.append(guess4_history)
game.result_history_items.append(result4_history)
game.guess_history_items.append(guess5_history)
game.result_history_items.append(result5_history)
game.guess_history_items.append(guess6_history)
game.result_history_items.append(result6_history)
game.guess_history_items.append(guess7_history)
game.result_history_items.append(result7_history)
game.guess_history_items.append(guess8_history)
game.result_history_items.append(result8_history)
game.guess_history_items.append(guess9_history)
game.result_history_items.append(result9_history)
game.guess_history_items.append(guess10_history)
game.result_history_items.append(result10_history)
game.guess_history_items.append(guess11_history)
game.result_history_items.append(result11_history)
game.guess_history_items.append(guess12_history)
game.result_history_items.append(result12_history)

guess1_history.grid(row=1, column=0)
result1_history.grid(row=1, column=1)
guess2_history.grid(row=2, column=0)
result2_history.grid(row=2, column=1)
guess3_history.grid(row=3, column=0)
result3_history.grid(row=3, column=1)
guess4_history.grid(row=4, column=0)
result4_history.grid(row=4, column=1)
guess5_history.grid(row=5, column=0)
result5_history.grid(row=5, column=1)
guess6_history.grid(row=6, column=0)
result6_history.grid(row=6, column=1)
guess7_history.grid(row=7, column=0)
result7_history.grid(row=7, column=1)
guess8_history.grid(row=8, column=0)
result8_history.grid(row=8, column=1)
guess9_history.grid(row=9, column=0)
result9_history.grid(row=9, column=1)
guess10_history.grid(row=10, column=0)
result10_history.grid(row=10, column=1)
guess10_history.grid(row=11, column=0)
result10_history.grid(row=11, column=1)
guess10_history.grid(row=12, column=0)
result10_history.grid(row=12, column=1)


new_game_button = ttk.Button(left_frame, text="New Game", command=game.new_game)
settings_button = ttk.Button(left_frame, text="Settings")
new_game_button.grid(row=0, column=0)
# settings_button.grid(row=1, column=0)


statusbar = tk.Label(
    bottom_frame,
    text=f"data file: {DATA_FILE} loaded. ({len(game.isogram_list)} words.)",
    bd=1, relief=tk.SUNKEN, anchor="se", width=90)
statusbar.grid(row=0, column=0)


root.bind("<Return>", lambda event: game.make_guess())

# define window dimensions width and height
window_width = 635
window_height = 415

# get the screen size of computer
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Get the window position from the top dynamically as well as position from left or right as follows
position_top = int(screen_height/2 - window_height/2)
position_right = int(((screen_width / 2) - 50) - ((window_width / 2) - 50))

# now center that root window!
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
root.iconbitmap(r'images/cow.ico')

# game.set_result(1, True)
root.mainloop()
