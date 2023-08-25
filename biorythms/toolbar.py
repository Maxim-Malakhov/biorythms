import os

from tkinter import Frame, messagebox
from matplotlib.backends._backend_tk import ToolTip
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

class Toolbar(NavigationToolbar2Tk):
    toolitems = (
        ('Home', 'Вернуть к исходному виду', 'home', 'home'),
        (None, None, None, None),
        ('Back', 'К предыдущему просмотру', 'back', 'back'),
        ('Forward', 'К следующему просмотру', 'forward', 'forward'),
        (None, None, None, None),
        ('Zoom', 'Масштабирование по прямоугольной области\nX/Y фиксирует ось', 'zoom_to_rect', 'zoom'),
        (None, None, None, None),
        ('Save', 'Сохранить график', 'filesave', 'save_figure')
    )

    def __init__(self, canvas, window=None):
        super().__init__(canvas, window, pack_toolbar=False)
        self.children.get('!label').destroy()
        self._message_label.destroy()

    def _Button(self, text, image_file, toggle, command):
        if os.path.isfile(image_file):
            image_file = os.path.join(os.getcwd(), image_file)
        b = super()._Button(text, image_file, toggle, command)
        b.pack(side='top')
        return b

    def _Spacer(self):
        s = Frame(self, width='18p', relief='ridge', bg='DarkGray')
        s.pack(side='top', pady='3p')
        return s

    def edit_parameters(self):
        axes = self.canvas.figure.get_axes()
        if not axes:
            messagebox.showwarning(
                self.canvas.parent(), "Ошибка", "Нет осей для редактирования.")
            return
        else:
            toplevel = LinesEditor(self, axes[0])
            for i, line in enumerate(axes[0].lines):
                pass
            ax = axes[titles.index(item)]
        figureoptions.figure_edit(ax, self)

    @staticmethod
    def createToolTip(button, tooltip_text):
        ToolTip.createToolTip(button, tooltip_text)
        return button

    def set_message(self, s):
        pass

if __name__ == "__main__":
    from tkinter import Tk
    from matplotlib import pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    
    root = Tk()
    figure, axis = plt.subplots()
    
    canvas = FigureCanvasTkAgg(figure, root)
    canvas.get_tk_widget().pack(side='right', fill='both', expand=1)
    
    toolbar = Toolbar(canvas, root)
    toolbar.pack(side='left', fill='y')
