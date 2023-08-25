from graph import Graph
from toolbar import Toolbar
from config import *

from tkinter import *
from tkinter import ttk, \
                    messagebox
from tkcalendar import DateEntry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from datetime import date
import webbrowser

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Биоритмы 1.0")
        self['bg'] = "#FFF"

        self.frame = Frame(self, bg=self['bg'])
        
        self.rowconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=1)
        
        self.graph = Graph()
        self.canvas = FigureCanvasTkAgg(self.graph, self)
        self.canvas.get_tk_widget().grid(row=0, column=1, sticky='nsew')

        self.toolbar = toolbar = Toolbar(self.canvas, self)
        toolbar.createToolTip(toolbar._Button('Settings', 'settings.png', False, lambda: messagebox.showwarning("Ой!", "Раздел всё ещё в разработке)")), "Настройки").pack(side='bottom')
        toolbar._Spacer().pack(side='bottom', pady='3p')
        toolbar.createToolTip(toolbar._Button('Help', 'help.png', False, lambda: webbrowser.open_new("https://docs.google.com/presentation/d/1_L568fho0PQA8Z3-WJnXDRxP7ZI64LRw/edit")), "О проекте").pack(side='bottom')
        toolbar.grid(row=0, column=0, sticky='ns')

        Label(self.frame, text="Дата рождения: ", bg=self['bg']).pack()
        self.birthday_field = DateEntry(self.frame, date_pattern="dd.mm.y")
        self.birthday_field._calendar._month_names = months_dict
        for i, d in enumerate(days_list): self.birthday_field._calendar._week_days[i]['text'] = d
        self.birthday_field.pack()

        self.date = Frame(self.frame)
        Label(self.frame, text="Вычислить на: ", bg=self['bg']).pack()
        self.month_field = month_field = ttk.Combobox(self.date, width=10, values=months_list, height=12, justify='center', cursor='hand2', state='readonly')
        month_field.set(months_list[date.today().month-1])
        month_field.grid(row=0, column=0)
        self.year_field = year_field = ttk.Spinbox(self.date, from_=1900, to=2100, width=7, cursor='hand2')
        year_field.insert(0, date.today().year)
        year_field.grid(row=0, column=1)
        self.date.pack()

        self.frame.grid(row=0, column=2, padx='10p')
        
        ttk.Button(self.frame, text="Применить", cursor='hand2', command=self.update_graph).pack()

    def update_graph(self):
        self.graph.set_birthday(self.birthday_field.get_date())
        self.graph.set_date(date(int(self.year_field.get()), months_list.index(self.month_field.get())+1, 1))
        self.graph.view()


if __name__ == '__main__':
    window = App()
    window.mainloop()
