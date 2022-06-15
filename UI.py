import tkinter as tk
import random as rd

FONT = ("Lato Semibold", 16, "normal")
RESULT_FONT = ("Lato Semibold", 32, "normal")
SIDES = [2, 4, 6, 8, 10, 100, 12, 20]
MAX_DICE_POOL = 10
BTN_HEIGHT = 2
BTN_WIDTH = BTN_HEIGHT * 2
BTN_WIDE = BTN_HEIGHT * 4
PAD = 5
PAD_WINDOW = PAD*3


class Roller:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Diceroller")
        self.window.config(width=640, height=480, padx=PAD_WINDOW, pady=PAD_WINDOW)

        self.dice_buttons = [DiceButton(self, SIDES.index(side), side) for side in SIDES]
        self.dice_labels = [Label(column) for column in range(len(SIDES))]

        self.roll_btn = Button()
        self.roll_btn.button.config(text="Roll!", width=BTN_WIDE, command=self.roll_dice)
        self.roll_btn.button.grid(column=2, row=0)

        self.result = Label(len(SIDES))
        self.result.label.config(font=RESULT_FONT)
        self.result.label.grid(column=2, row=1, rowspan=2)

        self.adv_btn = Button()
        self.adv_btn.button.config(text="Adv. d20", width=BTN_WIDE, command=self.advantage)
        self.adv_btn.button.grid(column=2, row=len(SIDES) - 2)

        self.dadv_btn = Button()
        self.dadv_btn.button.config(text="dAdv. d20", width=BTN_WIDE, command=self.disadvantage)
        self.dadv_btn.button.grid(column=2, row=len(SIDES) - 3)

        self.clear_btn = Button()
        self.clear_btn.button.config(text="Clear", width=BTN_WIDE, command=self.clear)
        self.clear_btn.button.grid(column=2, row=len(SIDES) - 1)

        self.rolling_buttons = [self.roll_btn, self.adv_btn, self.dadv_btn]

        self.window.mainloop()

    def roll_dice(self):
        results = []
        for pool in self.dice_labels:
            if pool.label["text"]:
                sub_results = []
                dice_int = [int(x) for x in pool.label["text"].split("k")]
                for _ in range(dice_int[0]):
                    roll = rd.randrange(dice_int[1])+1
                    sub_results.append(roll)
                    results.append(roll)
                pool.label.config(text=f"{sub_results}")
        result = sum(results)
        self.result.label.config(text=f"{result}")
        self._disable_rolling()

    def clear(self):
        self._enable_rolling()
        self._enable_dice_btns()
        self._reset_dice_counters()
        self._clear_labels()

    def _double_d20(self):
        d20_btn = self.dice_buttons[-1]
        d20_label = self.dice_labels[-1]
        for _ in range(2):
            d20_btn.add_die()
        results = []
        dice_int = [int(x) for x in d20_label.label["text"].split("k")]
        for _ in range(dice_int[0]):
            roll = rd.randrange(dice_int[1]) + 1
            results.append(roll)
        d20_label.label.config(text=f"{results}")
        return results

    def advantage(self):
        result = max(self._double_d20())
        self.result.label.config(text=f"{result}")
        self._disable_rolling()

    def disadvantage(self):
        result = min(self._double_d20())
        self.result.label.config(text=f"{result}")
        self._disable_rolling()

    def _disable_rolling(self):
        for button in self.rolling_buttons:
            button.button.config(state="disabled")

    def _enable_rolling(self):
        for button in self.rolling_buttons:
            button.button.config(state="normal")

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

    def __init__(self):
        self.button = tk.Button(font=FONT, height=BTN_HEIGHT, width=BTN_WIDTH)


class DiceButton(Button):

    def __init__(self, roller: Roller, row: int, sides: int):
        super().__init__()
        self.roller = roller
        self.index = row
        self.sides = sides
        self.die_counter = 0
        self.button.config(text=f"{sides}", command=self.add_die)
        self.button.grid(row=row, column=0, padx=PAD, pady=PAD)

    def add_die(self):
        self.roller.reset_if_needed()
        self.die_counter += 1
        die_label = self.roller.dice_labels[self.index].label
        die_label.config(text=f"{self.die_counter}k{self.sides}")
        if self.die_counter == MAX_DICE_POOL:
            die_button = self.roller.dice_buttons[self.index].button
            die_button.config(state="disabled")


class Label:

    def __init__(self, row: int):
        self.label = tk.Label(text="", font=FONT, padx=PAD, pady=PAD, width=BTN_WIDE, wraplength=75)
        self.label.grid(row=row, column=1)
