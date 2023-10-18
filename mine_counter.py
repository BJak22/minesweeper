from tkinter import *


class MineCounter:
    def __init__(self, place, number_of_mines):
        self.counter = number_of_mines
        self.label = Label(place, text='099', fg='#eb0510', bg='#570206',
                           font='Consolas')
        self.label.grid(row=0, column=0)

    def count_down(self):
        self.counter -= 1
        if self.counter < 10:
            text = "00" + str(self.counter)
        else:
            text = "0" + str(self.counter)
        self.label.config(text=text)

    def count_up(self):
        self.counter += 1
        if self.counter < 10:
            text = "00" + str(self.counter)
        else:
            text = "0" + str(self.counter)
        self.label.config(text=text)

    def restart(self, number):
        self.counter = number
        if self.counter < 10:
            text = "00" + str(self.counter)
        else:
            text = "0" + str(self.counter)
        self.label.config(text=text)
