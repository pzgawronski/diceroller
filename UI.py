import tkinter as tk
import random as rd
from const import *


class Roller:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Diceroller")
        self.window.config(width=640, height=480, padx=PAD_WINDOW, pady=PAD_WINDOW)

        self.dice_buttons = [DiceButton(self, SIDES.index(side), side) for side in SIDES]
        self.dice_labels = [DiceLabel(column) for column in range(len(SIDES))]

        self.result = Label(2, 1, RESULT_FONT, "")
        self.result.label.grid(rowspan=2)

        self.roll_btn = Button(2, 0, "Roll!", self.roll_dice, True)
        self.adv_btn = Button(2, ROWS-3, "Adv. d20", self.advantage)
        self.dadv_btn = Button(2, ROWS-2, "dAdv. d20", self.disadvantage, True)
        self.clear_btn = Button(2, ROWS-1, "Clear", self.clear, True)
        self.short_btns = [self.adv_btn, self.dadv_btn]

        self.window.mainloop()

    def roll_dice(self):
        results = []
        for pool in self.dice_labels:
            if pool.label["text"]:
                pool.label_to_results(results)
        result = sum(results)
        self.result.label.config(text=f"{result}")
        self._disable_rolling()

    def clear(self):
        self._enable_rolling()
        self._enable_dice_btns()
        self._reset_dice_counters()
        self._clear_labels()

    def _double_d20(self):
        self.reset_if_needed()
        self._clear_labels()
        d20_btn = self.dice_buttons[-1]
        d20_label = self.dice_labels[-1]
        for _ in range(2):
            d20_btn.add_die()
        results = []
        d20_label.label_to_results(results)
        return results

    def advantage(self):
        result = max(self._double_d20())
        self.result.update(result)
        self._disable_rolling()

    def disadvantage(self):
        result = min(self._double_d20())
        self.result.update(result)
        self._disable_rolling()

    def _disable_rolling(self):
        self.roll_btn.button.config(state="disabled")

    def _enable_rolling(self):
        self.roll_btn.button.config(state="normal")

    def _disable_dice_btns(self):
        for button in self.dice_buttons:
            button.button.config(state="disabled")

    def _enable_dice_btns(self):
        for button in self.dice_buttons:
            button.button.config(state="normal")

    def _reset_dice_counters(self):
        for button in self.dice_buttons:
            button.die_counter = 0

    def _clear_labels(self):
        for label in self.dice_labels:
            label.label.config(text="")
        self.result.label.config(text="")

    def reset_if_needed(self):
        result_label = self.result.label["text"]
        reset_needed = True if len(result_label) > 0 else False
        if reset_needed:
            self.clear()

class Button:

    def __init__(self, column: int, row: int, text: str, command, wide=True):
        self.width = BTN_WIDE if wide else BTN_WIDTH
        self.button = tk.Button(font=FONT, height=BTN_HEIGHT, width=self.width)
        self.button.config(text=text, command=command)
        self.button.grid(row=row, column=column, padx=PAD, pady=PAD)


class DiceButton(Button):

    def __init__(self, roller: Roller, index: int, sides: int):
        super().__init__(0, index, f"{sides}", self.add_die, wide=False)
        self.roller = roller
        self.index = index
        self.sides = sides
        self.die_counter = 0

    def add_die(self):
        self.roller.reset_if_needed()
        self.die_counter += 1
        die_label = self.roller.dice_labels[self.index].label
        die_label.config(text=f"{self.die_counter}{DICE_MARKER}{self.sides}")
        if self.die_counter == MAX_DICE_POOL:
            die_button = self.roller.dice_buttons[self.index].button
            die_button.config(state="disabled")


class Label:

    def __init__(self, column: int, row: int, font: tuple, text: str):
        self.label = tk.Label(text=text, font=font, padx=PAD, pady=PAD, width=BTN_WIDE, wraplength=75)
        self.label.grid(column=column, row=row)

    def update(self, text):
        self.label.config(text=f"{text}")


class DiceLabel(Label):

    def __init__(self, row: int):
        super().__init__(1, row, FONT, "")

    def label_to_results(self, results: list):
        split_label = self.label["text"].split(DICE_MARKER)
        dice_int = [int(x) for x in split_label]
        pool_count, pool_sides = dice_int
        pool_results = []
        for _ in range(pool_count):
            roll = rd.randrange(pool_sides) + 1
            pool_results.append(roll)
        self.update(pool_results)
        results.extend(pool_results)
