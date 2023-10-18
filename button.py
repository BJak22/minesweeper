from tkinter import*


class PlaceButton:
    def __init__(self, place, value, row, column, index):
        self.value = value
        self.showed = False
        self.flagged = False
        self.button = Label(place, font="Arial", fg="black",
                            bg="#bababa", relief=RAISED, width=2, height=1)
        self.button.grid(row=row, column=column)
        self.index = index

# show clicked button
    def show(self):
        if not self.showed:
            self.showed = True
            if self.value != 0:
                self.button.config(text=self.value, relief=FLAT, bg='#cfcccc', bd=1)
            else:
                self.button.config(text=' ', relief=FLAT, bg='#cfcccc', bd=1)
            if self.value == 1:
                self.button.config(fg='#0262fa')  # different color for each number
            if self.value == 2:
                self.button.config(fg='#0de031')
            if self.value == 3:
                self.button.config(fg='#fa0207')
            if self.value == 4:
                self.button.config(fg='#023e9e')
            if self.value == 5:
                self.button.config(fg='#730305')
            if self.value == 6:
                self.button.config(fg='#04b39b')
            if self.value == 7:
                self.button.config(fg='black')
            if self.value == 8:
                self.button.config(fg='#797a7a')
