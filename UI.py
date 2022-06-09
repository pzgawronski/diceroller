import tkinter as tk
import random as rd

FONT = ("Lato Semibold", 16, "normal")
SIDES = [2, 4, 6, 8, 10, 100, 12, 20]


class Roller:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Diceroller")
        self.window.config(width=640, height=480, padx=20, pady=20)

        self.dice_buttons = [DiceButton(self, SIDES.index(side), side) for side in SIDES]
        self.dice_labels = [Label(column) for column in range(len(SIDES))]

        self.roll_button = Button()
        self.roll_button.button.config(text="Roll!", width=8, command=self.roll_dice)
        self.roll_button.button.grid(column=len(SIDES), row=1)

        self.result = Label(len(SIDES))
        self.result.label.config(width=16)

        self.window.mainloop()

    def roll_dice(self):
        result = 0
        for pool in self.dice_labels:
            if pool.label["text"]:
                sub_result = 0
                dice_int = [int(x) for x in pool.label["text"].split("k")]
                for _ in range(dice_int[0]):
                    sub_result += rd.randrange(dice_int[1])
                pool.label.config(text=f"{sub_result}")
                result += sub_result
        self.result.label.config(text=f"{result}")


class Button:

    def __init__(self):
        self.button = tk.Button(font=FONT, height=2, width=4, padx=10, pady=10)


class DiceButton(Button):

    def __init__(self, roller: Roller, column: int, sides: int):
        super().__init__()
        self.roller = roller
        self.index = column
        self.sides = sides
        self.die_counter = 0
        self.button.config(text=f"{sides}", command=self.add_die)
        self.button.grid(column=column, row=1)

    def add_die(self):
        self.die_counter += 1
        if self.die_counter:
            self.roller.dice_labels[self.index].label.config(text=f"{self.die_counter}k{self.sides}")


class Label:

    def __init__(self, column: int):
        self.label = tk.Label(text="", font=FONT, padx=10, pady=10, width=8)
        self.label.grid(column=column, row=2)
