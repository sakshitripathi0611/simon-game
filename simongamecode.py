import tkinter as tk
import random
from functools import partial


class Simon:
    IDLE = ('red', 'blue', 'green', 'yellow')
    TINTED = ('#ff4d4d', '#4d4dff', '#4dff4d', '#ffff4d')

    FLASH_ON = 750  #ms in tinted state
    FLASH_OFF = 250  #ms in idle state

    def __init__(self, title='Simon Memory Game'):
        self.master = tk.Tk()
        self.master.title(title)
        self.master.resizable(False, False)
        self.title = title
        self.buttons = [
            tk.Button(
                self.master,
                height=15,
                width=25,
                background=c,
                activebackground=c,  # remove this line if you want the player to see which button is hovered
                command=partial(self.push, i))
            for i, c in enumerate(self.IDLE)]
        for i, button in enumerate(self.buttons):
            button.grid({'column': i % 2, 'row': i // 2})

    def reset(self):
        self.sequence = []
        self.new_color()

    def push(self, index):
        if index == self.current:
            try:
                self.current = next(self.iterator)
            except StopIteration:
                self.master.title('{} - Score: {}'
                                  .format(self.title, len(self.sequence)))
                self.new_color()
        else:
            self.master.title('{} - Game Over! | Final Score: {}'
                              .format(self.title, len(self.sequence)))
            self.reset()

    def new_color(self):
        for button in self.buttons:
            button.config(state=tk.DISABLED)
        color = random.randrange(0, len(self.buttons))
        self.sequence.append(color)
        self.iterator = iter(self.sequence)
        self.show_tile()

    def show_tile(self):
        try:
            id = next(self.iterator)
        except StopIteration:
            # No more tiles to show, start waiting for user input
            self.iterator = iter(self.sequence)
            self.current = next(self.iterator)
            for button in self.buttons:
                button.config(state=tk.NORMAL)
        else:
            self.buttons[id].config(background=self.TINTED[id])
            self.master.after(self.FLASH_ON, self.hide_tile)

    def hide_tile(self):
        for button, color in zip(self.buttons, self.IDLE):
            button.config(background=color)
        self.master.after(self.FLASH_OFF, self.show_tile)

    def run(self):
        self.reset()
        self.master.mainloop()


if __name__ == '__main__':
    game = Simon()
    game.run()   