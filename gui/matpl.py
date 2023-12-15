import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

def md_plt():
    x = [1,2,3,4,5]
    y = [2,4,5,3,11]

    fig, ax = plt.subplots()
    ax.plot(x,y)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title('Matplotlib Plot')
    ax.grid(True)
    return fig

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        loadUi('sample.ui', self)
        figa = md_plt()
        canvas = FigureCanvas(figa)
        tab_index = 0
        tab_widget = self.findChild(QTabWidget, tabWidget)
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(canvas)
        tab_page = QWidget()
        tab_page.setLayout(tab_layout)
        tab_widget.addTab(tab_page, "Matplotlib Graph")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())