from typing import Union
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from os import path
import os
import mplcursors

WIDTH = 1000
HEIGHT = 800

BLUE = '#12d4de'
GRAY = '#555657'
BLACK = '#000000'

PLOT_TITLE = 'Data'
X_AXIS_LABEL = 'Sample'
Y_AXIS_LABEL = 'Value'
PLOT_LINE_COLOR = BLUE
PLOT_FACE_COLOR = GRAY
AXES_FACE_COLOR = GRAY
X_TICK_COLOR = BLUE
Y_TICK_COLOR = BLUE


class CustomToolBar(NavigationToolbar2QT):
    def __init__(self, figure_canvas, parent=None):
        # self.icondir = 'C:/Users/Velentium/PycharmProjects/jombleplot/resources'
        self.icondir = ''
        # (button text, tooltip, icon name, function name)
        # ('Home', 'Reset original view', 'home', 'home')
        # ('Back', 'Back to previous view', 'back', 'back')
        # ('Forward', 'Forward to next view', 'forward', 'forward')
        # ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan')
        # ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom')
        # ('Subplots', 'Configure subplots', 'subplots', 'configure_subplots')
        # ('Save', 'Save the figure', 'filesave', 'save_figure')
        # self.toolitems = [t for t in NavigationToolbar2QT.toolitems if
        #                   t[0] in ('Home', 'Back', 'Forward', 'Pan', 'Zoom', 'Subplots', 'Save')]
        self.toolitems = []
        self.toolitems.append(('Home', 'Reset original view', 'home', 'home'))
        self.toolitems.append(('Back', 'Back to previous view', 'back', 'back'))
        self.toolitems.append(('Forward', 'Forward to next view', 'forward', 'forward'))
        self.toolitems.append(('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'))
        self.toolitems.append(('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'))
        self.toolitems.append(('Subplots', 'Configure subplots', 'subplots', 'configure_subplots'))
        self.toolitems.append(('Save', 'Save the figure', 'filesave', 'save_figure'))
        self.toolitems.insert(0, ('Refresh', 'Refresh data', 'refresh', 'refresh'))
        NavigationToolbar2QT.__init__(self, figure_canvas, parent=parent)

    def refresh(self):
        refresh()

    def _icon(self, name):
        pm = QPixmap(path.join(self.icondir, name))
        if hasattr(pm, 'setDevicePixelRatio'):
            pm.setDevicePixelRatio(self.canvas._dpi_ratio)
        return QIcon(pm)


class PlotCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, points=None):
        if points is None:
            points = []
        self.fig = plt.Figure(figsize=(6, 4), dpi=150)
        self.axes = self.fig.add_subplot(111)
        self.crs = None
        self.data_plot = None
        FigureCanvasQTAgg.__init__(self, self.fig)
        FigureCanvasQTAgg.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setParent(parent)
        self.toolbar = CustomToolBar(self.fig.canvas, self)
        self.toolbar.update()
        FigureCanvasQTAgg.updateGeometry(self)
        self.plot(points)
        self.axes.format_coord = lambda x, y: f'!!!!!!!x={x}, y={y}'

    def plot(self, points=None):
        if points is None:
            points = [0]
        self.data_plot = self.axes.plot(points, color=PLOT_LINE_COLOR)
        self.axes.set_title(PLOT_TITLE, color=BLACK)
        self.fig.set_facecolor(color=PLOT_FACE_COLOR)
        self.axes.set_facecolor(color=AXES_FACE_COLOR)
        self.axes.xaxis.label.set_text(X_AXIS_LABEL)
        self.axes.xaxis.label.set_color(BLACK)
        self.axes.tick_params(axis='x', colors=X_TICK_COLOR)
        self.axes.yaxis.label.set_text(Y_AXIS_LABEL)
        self.axes.yaxis.label.set_color(BLACK)
        self.axes.tick_params(axis='y', colors=Y_TICK_COLOR)
        self.axes.spines['bottom'].set_color(BLACK)
        self.axes.spines['top'].set_color(BLACK)
        self.axes.spines['left'].set_color(BLACK)
        self.axes.spines['right'].set_color(BLACK)
        self.crs = mplcursors.cursor(self.axes, hover=True)

        self.crs.connect("add", lambda sel: sel.annotation.set_text(
            'Point {:.3f},{:.3f}'.format(sel.target[0], sel.target[1])))
        self.draw()

    def clear(self):
        self.axes.clear()


_PLOT_CANVAS: Union[PlotCanvas, None] = None


def data(points=None) -> QWidget:
    global _PLOT_CANVAS
    if points is None:
        if not path.exists('data'):
            os.mkdir('data')
        if path.exists('data/data.txt'):
            with open('data/data.txt') as file:
                points = file.readlines()
            points = [float(x.rstrip()) for x in points]
        else:
            with open('data/data.txt', 'w+'):
                pass
        if not points:
            points = [0]
    if _PLOT_CANVAS is None:
        _PLOT_CANVAS = PlotCanvas(points=points)
        layout = QHBoxLayout()
        area = QScrollArea()
        area.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        area.setMinimumSize(QSize(WIDTH, HEIGHT))
        area.setWidgetResizable(True)
        area.setWidget(_PLOT_CANVAS)
        area.setWindowTitle('jombleplot v2')
        icon = QIcon('resources/icon.png')
        area.setWindowIcon(icon)
        layout.addWidget(area, alignment=Qt.AlignHCenter)
        area.show()
    else:
        _PLOT_CANVAS.plot(points)

    show()

    return _PLOT_CANVAS


def clear() -> None:
    if _PLOT_CANVAS is not None:
        _PLOT_CANVAS.clear()


def hide() -> None:
    if _PLOT_CANVAS is not None:
        _PLOT_CANVAS.hide()


def show() -> None:
    if _PLOT_CANVAS is not None:
        _PLOT_CANVAS.show()


def save(file: str) -> None:
    _PLOT_CANVAS.fig.savefig(file)


def refresh() -> None:
    clear()
    data(None)
