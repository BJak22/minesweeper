import random
import time
import threading
from tkinter import *
from button import PlaceButton
from timer import Timer
from mine_counter import MineCounter
from tkinter import messagebox


class Board:
    def __init__(self, row, number_of_places, number_of_mines, place, timer, mine_counter):
        self.row = row
        self.number_of_places = number_of_places
        self.number_of_mines = number_of_mines
        self.mines_list = list()
        self.buttons_list = list()
        self.board = Frame(place, bg="#bababa")
        self.board.grid(row=0, column=0)
        self.number_of_flags = 0
        self.timer = timer
        self.mine_counter = mine_counter
        self.highlight_list = list()
        self.stop_threads = False
        self.first_click = True
        # reading stats for leaderboard
        f = open("score.txt", 'r')
        self.beginner_score = int(f.readline())
        self.beginner_wins = int(f.readline())
        self.beginner_loses = int(f.readline())
        self.intermediate_score = int(f.readline())
        self.intermediate_wins = int(f.readline())
        self.intermediate_loses = int(f.readline())
        self.expert_score = int(f.readline())
        self.expert_wins = int(f.readline())
        self.expert_loses = int(f.readline())
        f.close()
        # creating list of mines
        for i in range(self.number_of_mines):
            self.mines_list.append(1)
        for i in range(self.number_of_places - self.number_of_mines):
            self.mines_list.append(0)
        for i in range(self.number_of_places):
            button = PlaceButton(self.board, 0, int(i/row),
                                    i % row, i)
            button.button.bind('<ButtonRelease-1>', self.left_click)
            self.buttons_list.append(button)

# help function which is showing generated board
    def show_board(self):
        for i in range(self.number_of_places):
            if i % self.row == 0:
                print('\n')
            print(self.buttons_list[i].value, end=" ")

    def left_click(self, event):
        self.stop_threads = False
        # few lines of code which will change color of every highlighted button
        for i in self.highlight_list:
            if not self.buttons_list[i].showed:
                self.buttons_list[i].button.config(bg="#bababa")
        self.highlight_list.clear()
        info = event.widget.grid_info()
        r = info['row']
        c = info['column']
        i = r*self.row+c
        # code below is made to guarantee that first click wont be on mine
        if self.first_click:
            self.timer.count_start()
            self.first_click = False
            random.shuffle(self.mines_list)
            while self.mines_list[i] == 1:
                random.shuffle(self.mines_list)
            for j in range(self.number_of_places):
                # check if place is mine
                if self.mines_list[j] == 1:
                    self.buttons_list[j].value = 'X'
                    self.buttons_list[j].button.bind('<ButtonRelease-1><ButtonRelease-3>',
                                                     self.both_click)
                    self.buttons_list[j].button.bind('<ButtonRelease-1>', self.left_click)
                    self.buttons_list[j].button.bind('<ButtonRelease-3>', self.right_click)
                else:
                    value = 0
                    # check if previous place is mine
                    if j % self.row != 0 and self.mines_list[j - 1] == 1:
                        value += 1
                    # check if next place is mine
                    if j % self.row != self.row - 1 and self.mines_list[j + 1] == 1:
                        value += 1
                    # check if upper place is mine
                    if j >= self.row and self.mines_list[j - self.row] == 1:
                        value += 1
                    # check if place below is mine
                    if j < self.number_of_places - self.row \
                            and self.mines_list[j + self.row] == 1:
                        value += 1
                    # check if upper - left place is mine
                    if j % self.row != 0 and j >= self.row \
                            and self.mines_list[j - self.row - 1] == 1:
                        value += 1
                    # check if upper - right place is mine
                    if j % self.row != self.row - 1 and j >= self.row \
                            and self.mines_list[j - self.row + 1] == 1:
                        value += 1
                    # check if left - below place is mine
                    if j < self.number_of_places - self.row and \
                            j % self.row != 0 and self.mines_list[j + self.row - 1] == 1:
                        value += 1
                    # check if right - below place is mine
                    if j < self.number_of_places - self.row and \
                            j % self.row != self.row - 1 \
                            and self.mines_list[j + self.row + 1] == 1:
                        value += 1
                    self.buttons_list[j].value = value
                    self.buttons_list[j].button.bind('<ButtonRelease-1><ButtonRelease-3>', self.both_click)
                    self.buttons_list[j].button.bind('<ButtonRelease-1>', self.left_click)
                    self.buttons_list[j].button.bind('<ButtonRelease-3>', self.right_click)
                    self.buttons_list[j].button.bind('<Button-1><Button-3>', self.both_hold)
        self.show_list(i)
        win = 1
        for i in self.buttons_list:
            if not i.showed and i.value != 'X':
                win = 0
        if win == 1:
            self.start_animation(1)

# show every button around
    def show_list(self, i):
        self.buttons_list[i].show()
        if self.buttons_list[i].value == 'X':
            self.start_animation(0)
        else:
            if self.buttons_list[i].value == 0:  # all places around 0 will be showed
                # check if previous place is mine
                if i % self.row != 0 and not self.buttons_list[i - 1].showed:
                    if self.buttons_list[i - 1].value == 0:
                        self.show_list(i - 1)
                    else:
                        self.buttons_list[i - 1].show()
                # check if next place is mine
                if i % self.row != self.row - 1 and not self.buttons_list[i + 1].showed:
                    if self.buttons_list[i + 1].value == 0:
                        self.show_list(i + 1)
                    else:
                        self.buttons_list[i + 1].show()
                # check if upper place is mine
                if i >= self.row and not self.buttons_list[i - self.row].showed:
                    if self.buttons_list[i - self.row].value == 0:
                        self.show_list(i - self.row)
                    else:
                        self.buttons_list[i - self.row].show()
                # check if place below is mine
                if i < self.number_of_places - self.row \
                        and not self.buttons_list[i + self.row].showed:
                    if self.buttons_list[i + self.row].value == 0:
                        self.show_list(i + self.row)
                    else:
                        self.buttons_list[i + self.row].show()
                # check if upper - left place is mine
                if i % self.row != 0 and i >= self.row\
                        and not self.buttons_list[i - self.row - 1].showed:
                    if self.buttons_list[i - self.row - 1].value == 0:
                        self.show_list(i - self.row - 1)
                    else:
                        self.buttons_list[i - self.row - 1].show()
                # check if upper - right place is mine
                if i % self.row != self.row - 1 and i >= self.row\
                        and not self.buttons_list[i - self.row + 1].showed:
                    if self.buttons_list[i - self.row + 1].value == 0:
                        self.show_list(i - self.row + 1)
                    else:
                        self.buttons_list[i - self.row + 1].show()
                # check if left - below place is mine
                if i < self.number_of_places - self.row and \
                    i % self.row != 0\
                        and not self.buttons_list[i + self.row - 1].showed:
                    if self.buttons_list[i + self.row - 1].value == 0:
                        self.show_list(i + self.row - 1)
                    else:
                        self.buttons_list[i + self.row - 1].show()
                # check if right - below place is mine
                if i < self.number_of_places - self.row and \
                    i % self.row != self.row - 1\
                        and not self.buttons_list[i + self.row + 1].showed:
                    if self.buttons_list[i + self.row + 1].value == 0:
                        self.show_list(i + self.row + 1)
                    else:
                        self.buttons_list[i + self.row + 1].show()

# animation after win or lose
    def animation(self, value):
        self.timer.stop_threads = True
        for i in range(self.number_of_places):
            if not self.stop_threads:
                self.buttons_list[i].button.unbind('<ButtonRelease-1><ButtonRelease-3>')
                self.buttons_list[i].button.unbind('<ButtonRelease-1>')
                self.buttons_list[i].button.unbind('<ButtonRelease-3>')
                self.buttons_list[  i].button.unbind('<Button-1><Button-3>')
            else:
                break
        for i in range(self.number_of_places):
            if not self.stop_threads:
                if value == 0:
                    if not self.buttons_list[i].showed:
                        if self.buttons_list[i].value == 'X':
                            self.buttons_list[i].show()
                            time.sleep(0.1)
                else:
                    if not self.buttons_list[i].showed:
                        if self.buttons_list[i].value != 'X':
                            self.buttons_list[i].show()
                            time.sleep(0.1)
                        if self.buttons_list[i].value == 'X':
                            self.buttons_list[i].button.config(text='')
                            time.sleep(0.1)
            else:
                break
        if value == 1:
            if not self.stop_threads:
                messagebox.showinfo(title="WIN", message="You have won in " +
                                str(self.timer.score) + " seconds")
            if self.number_of_mines ==10:
                if int(self.beginner_score) < 0 \
                    or self.timer.score < int(self.beginner_score):
                    self.beginner_score = self.timer.score
                self.beginner_wins +=1
            if self.number_of_mines == 40:
                if int(self.intermediate_score) < 0 \
                        or self.timer.score < int(self.intermediate_score):
                    self.intermediate_score = self.timer.score
                self.intermediate_wins += 1
            if self.number_of_mines == 99:
                if int(self.expert_score) < 0 \
                        or self.timer.score < int(self.expert_score):
                    self.expert_score = self.timer.score
                self.expert_wins += 1
        else:
            if not self.stop_threads:
                messagebox.showwarning(title="LOSE",
                                   message="Unfortunately you have lost, try again")
            if self.number_of_mines ==10:
                self.beginner_loses +=1
            if self.number_of_mines == 40:
                self.intermediate_loses += 1
            if self.number_of_mines == 99:
                self.expert_loses += 1
        self.save_score()

    def start_animation(self, value):
        if value == 1:
            thread = threading.Thread(target=self.animation, args=(1,), daemon = True)
        else:
            thread = threading.Thread(target=self.animation, args=(0,))
        thread.start()

    def check_if_all_flaged(self, i):
        value=0
        # check if previous place is flagged
        if i % self.row != 0 \
                and self.buttons_list[i-1].flagged:
            value += 1
        # check if next place is flagged
        if i % self.row != self.row - 1\
                and self.buttons_list[i + 1].flagged:
            value += 1
        # check if upper place is flagged
        if i >= self.row\
                and self.buttons_list[i - self.row].flagged:
            value += 1
        # check if place below is flagged
        if i < self.number_of_places - self.row\
                and self.buttons_list[i + self.row].flagged:
            value += 1
        # check if upper - left place is flagged
        if i % self.row != 0 and i >= self.row\
                and self.buttons_list[i - self.row - 1].flagged:
            value += 1
        # check if upper - right place is flagged
        if i % self.row != self.row - 1 and i >= self.row\
                and self.buttons_list[i - self.row + 1].flagged:
            value += 1
        # check if left - below place is flagged
        if i < self.number_of_places - self.row and \
                i % self.row != 0\
                and self.buttons_list[i+ self.row - 1].flagged:
            value += 1
        # check if right - below place is flagged
        if i < self.number_of_places - self.row and \
                i % self.row != self.row - 1\
                and self.buttons_list[i + self.row + 1].flagged:
            value += 1
        if value == self.buttons_list[i].value:
            return True
        else:
            return False

    def both_click(self, event):
        self.stop_threads = False
        for i in self.highlight_list:
            if not self.buttons_list[i].showed:
                self.buttons_list[i].button.config(bg="#bababa")
        self.highlight_list.clear()
        info = event.widget.grid_info()
        r = info['row']
        c = info['column']
        i = r * self.row + c
        all_flagged = self.check_if_all_flaged(i)
        if all_flagged:
            if self.buttons_list[i].value != 0:
                if i % self.row != 0 and self.buttons_list[i - 1].flagged \
                        and self.buttons_list[i - 1].value != 'X':
                    self.start_animation(0)
                elif i % self.row != self.row - 1 and self.buttons_list[i + 1].flagged \
                        and self.buttons_list[i + 1].value != 'X':
                    self.start_animation(0)
                elif i >= self.row and self.buttons_list[i - self.row].flagged \
                        and self.buttons_list[i - self.row].value != 'X':
                    self.start_animation(0)
                elif i < self.number_of_places - self.row \
                        and self.buttons_list[i + self.row].flagged \
                        and self.buttons_list[i + self.row].value != 'X':
                    self.start_animation(0)
                elif i % self.row != 0 and i >= self.row \
                        and self.buttons_list[i - self.row - 1].flagged \
                        and self.buttons_list[i - self.row - 1].value != 'X':
                    self.start_animation(0)
                elif i % self.row != self.row - 1 and i >= self.row \
                        and self.buttons_list[i - self.row + 1].flagged \
                        and self.buttons_list[i - self.row + 1].value != 'X':
                    self.start_animation(0)
                elif i < self.number_of_places - self.row \
                        and i % self.row != 0 \
                        and self.buttons_list[i + self.row - 1].flagged \
                        and self.buttons_list[i + self.row - 1].value != 'X':
                    self.start_animation(0)
                elif i < self.number_of_places - self.row \
                        and i % self.row != self.row - 1 \
                        and self.buttons_list[i + self.row + 1].flagged \
                        and self.buttons_list[i + self.row + 1].value != 'X':
                    self.start_animation(0)
                else:
                    # show previous place
                    if i % self.row != 0 and self.mines_list[i - 1] != 1:
                        self.show_list(i - 1)
                    # show next place
                    if i % self.row != self.row - 1 and self.mines_list[i + 1] != 1:
                        self.show_list(i + 1)
                    # show upper place
                    if i >= self.row and self.mines_list[i - self.row] != 1:
                        self.show_list(i - self.row)
                    # show place below
                    if i < self.number_of_places - self.row\
                            and self.mines_list[i + self.row] != 1:
                        self.show_list(i + self.row)
                    # show upper - left place
                    if i % self.row != 0 and i >= self.row\
                            and self.mines_list[i - self.row - 1] != 1:
                        self.show_list(i - self.row - 1)
                    # show upper - right place
                    if i % self.row != self.row - 1 and i >= self.row \
                            and self.mines_list[i - self.row + 1] != 1:
                        self.show_list(i - self.row + 1)
                    # show left - below place
                    if i < self.number_of_places - self.row and \
                            i % self.row != 0 and self.mines_list[i + self.row - 1] != 1:
                        self.show_list(i + self.row - 1)
                    # show right - below place
                    if i < self.number_of_places - self.row and \
                            i % self.row != self.row - 1 \
                            and self.mines_list[i + self.row + 1] != 1:
                        self.show_list(i + self.row + 1)
        win = 1
        for i in self.buttons_list:
            if i.showed == False and i.value != 'X':
                win = 0
        if win == 1:
            self.start_animation(1)

    def both_hold(self, event):
        self.stop_threads = False
        for i in self.highlight_list:
            if not self.buttons_list[i].showed:
                self.buttons_list[i].button.config(bg="#bababa")
        self.highlight_list.clear()
        info = event.widget.grid_info()
        r = info['row']
        c = info['column']
        i = r * self.row + c
        if self.buttons_list[i].showed:
            # check if previous place is not showed
            if i % self.row != 0 and not self.buttons_list[i - 1].showed\
                    and not self.buttons_list[i - 1].flagged:
                self.buttons_list[i - 1].button.config(bg='#edebeb')
                self.highlight_list.append(i - 1)
            # check if next place is not showed
            if i % self.row != self.row - 1 and not self.buttons_list[i + 1].showed\
                    and not self.buttons_list[i + 1].flagged:
                self.buttons_list[i + 1].button.config(bg='#edebeb')
                self.highlight_list.append(i + 1)
            # check if upper place is not showed
            if i >= self.row and not self.buttons_list[i - self.row].showed\
                    and not self.buttons_list[i - self.row].flagged:
                self.buttons_list[i - self.row].button.config(bg='#edebeb')
                self.highlight_list.append(i - self.row)
            # check if place below is not showed
            if i < self.number_of_places - self.row \
                    and not self.buttons_list[i + self.row].showed\
                    and not self.buttons_list[i + self.row].flagged:
                self.buttons_list[i + self.row].button.config(bg='#edebeb')
                self.highlight_list.append(i + self.row)
            # check if upper - left place is not showed
            if i % self.row != 0 and i >= self.row \
                    and not self.buttons_list[i - self.row - 1].showed\
                    and not self.buttons_list[i - self.row - 1].flagged:
                self.buttons_list[i - self.row - 1].button.config(bg='#edebeb')
                self.highlight_list.append(i - self.row - 1)
            # check if upper - right place is not showed
            if i % self.row != self.row - 1 and     i >= self.row \
                    and not self.buttons_list[i - self.row + 1].showed\
                    and not self.buttons_list[i - self.row + 1].flagged:
                self.buttons_list[i - self.row + 1].button.config(bg='#edebeb')
                self.highlight_list.append(i - self.row + 1)
            # check if left - below place is not showed
            if i < self.number_of_places - self.row \
                    and i % self.row != 0 \
                    and not self.buttons_list[i + self.row - 1].showed\
                    and not self.buttons_list[i + self.row - 1].flagged:
                self.buttons_list[i + self.row - 1].button.config(bg='#edebeb')
                self.highlight_list.append(i + self.row - 1)
            # check if right - below place is not showed
            if i < self.number_of_places - self.row \
                    and i % self.row != self.row - 1 \
                    and not self.buttons_list[i + self.row + 1].showed\
                    and not self.buttons_list[i + self.row + 1].flagged:
                self.buttons_list[i + self.row + 1].button.config(bg='#edebeb')
                self.highlight_list.append(i + self.row + 1)
        #both click realse is not always working so i've implemented its code here as well
        all_flagged = self.check_if_all_flaged(i)
        if all_flagged:
            if self.buttons_list[i].value != 0:
                if i % self.row != 0 and self.buttons_list[i - 1].flagged \
                        and self.buttons_list[i - 1].value != 'X':
                    self.start_animation(0)
                elif i % self.row != self.row - 1 and self.buttons_list[i + 1].flagged \
                        and self.buttons_list[i + 1].value != 'X':
                    self.start_animation(0)
                elif i >= self.row and self.buttons_list[i - self.row].flagged \
                        and self.buttons_list[i - self.row].value != 'X':
                    self.start_animation(0)
                elif i < self.number_of_places - self.row \
                        and self.buttons_list[i + self.row].flagged \
                        and self.buttons_list[i + self.row].value != 'X':
                    self.start_animation(0)
                elif i % self.row != 0 and i >= self.row \
                        and self.buttons_list[i - self.row - 1].flagged \
                        and self.buttons_list[i - self.row - 1].value != 'X':
                    self.start_animation(0)
                elif i % self.row != self.row - 1 and i >= self.row \
                        and self.buttons_list[i - self.row + 1].flagged \
                        and self.buttons_list[i - self.row + 1].value != 'X':
                    self.start_animation(0)
                elif i < self.number_of_places - self.row \
                        and i % self.row != 0 \
                        and self.buttons_list[i + self.row - 1].flagged \
                        and self.buttons_list[i + self.row - 1].value != 'X':
                    self.start_animation(0)
                elif i < self.number_of_places - self.row \
                        and i % self.row != self.row - 1 \
                        and self.buttons_list[i + self.row + 1].flagged \
                        and self.buttons_list[i + self.row + 1].value != 'X':
                    self.start_animation(0)
                else:
                    # show previous place
                    if i % self.row != 0 and self.mines_list[i - 1] != 1:
                        self.show_list(i - 1)
                    # show next place
                    if i % self.row != self.row - 1 and self.mines_list[i + 1] != 1:
                        self.show_list(i + 1)
                    # show upper place
                    if i >= self.row and self.mines_list[i - self.row] != 1:
                        self.show_list(i - self.row)
                    # show place below=
                    if i < self.number_of_places - self.row \
                            and self.mines_list[i + self.row] != 1:
                        self.show_list(i + self.row)
                    # show upper - left place
                    if i % self.row != 0 and i >= self.row \
                            and self.mines_list[i - self.row - 1] != 1:
                        self.show_list(i - self.row - 1)
                    # show upper - right place
                    if i % self.row != self.row - 1 and i >= self.row \
                            and self.mines_list[i - self.row + 1] != 1:
                        self.show_list(i - self.row + 1)
                    # show left - below place
                    if i < self.number_of_places - self.row and \
                            i % self.row != 0 and self.mines_list[i + self.row - 1] != 1:
                        self.show_list(i + self.row - 1)
                    # show right - below place
                    if i < self.number_of_places - self.row and \
                            i % self.row != self.row - 1 \
                            and self.mines_list[i + self.row + 1] != 1:
                        self.show_list(i + self.row + 1)
        win = 1
        for i in self.buttons_list:
            if i.showed == False and i.value != 'X':
                win = 0
        if win == 1:
            self.start_animation(1)

    def right_click(self, event):
        self.stop_threads = False
        # unhighlight here as well
        for i in self.highlight_list:
            if not self.buttons_list[i].showed:
                self.buttons_list[i].button.config(bg="#bababa")
        self.highlight_list.clear()
        info = event.widget.grid_info()
        r = info['row']
        c = info['column']
        i = r * self.row + c
        if not self.buttons_list[i].flagged:
            if not self.buttons_list[i].showed:
                self.mine_counter.count_down()
                self.buttons_list[i].button.config(text='F')
                self.buttons_list[i].flagged = True
                self.number_of_flags += 1
                self.buttons_list[i].button.unbind('<ButtonRelease-1>')
        else:
            self.mine_counter.count_up()
            self.buttons_list[i].button.config(text=' ')
            self.buttons_list[i].flagged = False
            self.number_of_flags -= 1
            self.buttons_list[i].button.bind('<ButtonRelease-1>', self.left_click)
        win = 1
        for i in self.buttons_list:
            if i.showed == False and i.value!='X':
                win = 0
        if win ==1:
            self.start_animation(1)

    def unshow(self):
        self.first_click = True
        for i in self.buttons_list:
            i.button.config(fg="black", bg="#bababa", relief=RAISED, width=2, height=1,
                            text='',bd=2)
            i.showed = False
            i.flagged = False
            i.button.bind('<ButtonRelease-1><ButtonRelease-3>', self.both_click)
            i.button.bind('<ButtonRelease-1>', self.left_click)
            i.button.bind('<ButtonRelease-3>', self.right_click)
            i.button.bind('<Button-1><Button-3>', self.both_hold)

    def save_score(self):
        f = open("score.txt", mode='w')
        f.write(str(self.beginner_score)+'\n')
        f.write(str(self.beginner_wins)+'\n')
        f.write(str(self.beginner_loses)+'\n')
        f.write(str(self.intermediate_score)+'\n')
        f.write(str(self.intermediate_wins)+'\n')
        f.write(str(self.intermediate_loses)+'\n')
        f.write(str(self.expert_score)+'\n')
        f.write(str(self.expert_wins)+'\n')
        f.write(str(self.expert_loses)+'\n')
        f.close()