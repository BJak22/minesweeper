from tkinter import *


class MyMenu:
    def __init__(self, window):
        self.menubar = Menu(window)
        self.menu = Menu(self.menubar, tearoff=0)
        self.NewGameMenu = Menu(self.menu, tearoff=0)
        self.LeaderboardMenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='Leaderboard', menu=self.LeaderboardMenu)
        self.menu.add_separator()
        self.menu.add_cascade(label='New Game', menu=self.NewGameMenu)
        self.menubar.add_cascade(label='Game', menu=self.menu)