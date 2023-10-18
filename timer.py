from tkinter import *
import threading
import time


class Timer:
    def __init__(self, place):
        self.counter = 0
        self.score = 0
        self.stop_threads = False
        self.place = place
        self.label = Label(place, text='000', fg='#eb0510', bg= '#570206',
                           font= 'Consolas')
        self.label.grid(row=0, column=2)

    def count(self):
        while True:
            if self.stop_threads:
                self.score = self.counter
                self.counter = 0
                break
            time.sleep(1)
            if self.stop_threads:
                self.score = self.counter
                self.counter = 0
                break
            self.counter += 1
            if self.counter < 10:
                text = "00"+str(self.counter)
            elif self.counter >= 10 and self.counter < 100:
                text = "0" + str(self.counter)
            elif self.counter >= 100 and self.counter < 1000:
                text = str(self.counter)
            else:
                text = "999"
            self.label.config(text=text)

    def count_start(self):
        thread = threading.Thread(target=self.count, daemon=True)
        thread.start()
