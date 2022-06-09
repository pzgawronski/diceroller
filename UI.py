import tkinter as tk

FONT = ("Lato Semibold", 16, "normal")
SIDES = [2, 4, 6, 8, 10, 100, 12, 20]


class Roller:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Diceroller")
        self.window.config(width=640, height=480, padx=20, pady=20)

        self.dice_buttons = [Button(self, SIDES.index(side), side) for side in SIDES]
        self.dice_labels = [Label(column) for column in range(len(SIDES))]

        self.window.mainloop()


class Button:

    def __init__(self, roller: Roller, column: int, sides: int):
        self.roller = roller
        self.index = column
        self.sides = sides
        self.die_counter = 0
        self.button = tk.Button(text=f"{sides}", font=FONT, height=2, width=4, padx=10, pady=10, command=self.add_die)
        self.button.grid(column=column, row=1)

    def add_die(self):
        self.die_counter += 1
        if self.die_counter:
            self.roller.dice_labels[self.index].label.config(text=f"{self.die_counter}k{self.sides}")


class Label:

    def __init__(self, column: int):
        self.label = tk.Label(text="", font=FONT, padx=10, pady=10, width=8)
        self.label.grid(column=column, row=2)
