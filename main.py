from util import qt_plot
from PyQt5 import QtWidgets
import sys
import os

try:
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
except Exception as ex:
    pass


def qt_plot_main():
    try:
        qapp = QtWidgets.QApplication(sys.argv)
        qt_plot.data(None)
        sys.exit(qapp.exec_())
    except BaseException as ex:
        print(str(ex))


if __name__ == '__main__':
    qt_plot_main()
