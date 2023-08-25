import numpy as np

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib import animation, figure

from datetime import date
from calendar import monthrange

class Graph(figure.Figure):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_birthday(date(2008, 9, 7))
        self.set_date(date.today())

        self.axis = self.subplots()
        self.configure()

    def set_birthday(self, birthday):
        self.birthday = birthday

    def set_date(self, date):
        self.date = date
        self.days = monthrange(self.date.year, self.date.month)[-1]

    def configure(self):
        self.axis.clear()
        self.lines = []
        
        self.axis.set_xlim((0, self.days-1))
        self.axis.set_ylim((-1.25, 1.25))
        self.axis.set_xticks(range(self.days), range(1, self.days+1), rotation=-90)

        for i in range(3):
            self.lines.append(self.axis.plot([], ('blue', 'red', 'yellow')[i], label=("Физический", "Эмоциональный", "Интеллектуальный")[i])[0])

        self.axis.grid(axis='y')

        #self.suptitle(f"Биоритмы\n{self.date.month} {self.date.year} года") #Заголовок фигуры.
        self.axis.set_xlabel("День месяца")
        self.axis.set_ylabel("Значение биоритма", rotation=90)

        self.tight_layout() #Вызывает предупреждение.

    def animate(self, frame):
        for line in self.lines:
            line.set_data(np.append(line.get_xdata(), frame[0]),
                          np.append(line.get_ydata(), next(frame[1])))
        if frame[0] == self.days-1:
            legend = self.axis.legend()
            legend.set_draggable(True)
            return self.lines + [legend]
        return self.lines

    def view(self):
        self.configure()
        #При date < birthday вызывает предупреждение. Это связано с передачей "пустого" генератора.
        self.anim = animation.FuncAnimation(self,
                                            self.animate,
                                            ((i, (np.sin(2 * np.pi * (((self.date.replace(day=1+i)) - self.birthday).days)/x) for x in (23, 28, 33))) for i in range(self.days) if self.date.replace(day=1+i) >= self.birthday),
                                            cache_frame_data=False,
                                            interval=0,
                                            blit=True,
                                            repeat=False)

if __name__ == "__main__":
    from tkinter import Tk
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    graph = Graph()
    FigureCanvasTkAgg(graph, Tk()).get_tk_widget().pack(fill='both', expand=True)
    graph.view()
