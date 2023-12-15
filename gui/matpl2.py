import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTabWidget
from PyQt5.uic import loadUi

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # UI 파일 로드
        loadUi('sample.ui', self)

        aa = mapl()

        # Matplotlib figure를 PyQt 위젯에 삽입
        canvas = FigureCanvas(aa)
        tab_index = 0  # 적절한 탭 인덱스 지정
        tab_widget = self.findChild(QTabWidget, 'tabWidget')
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(canvas)
        tab_page = QWidget()
        tab_page.setLayout(tab_layout)
        tab_widget.addTab(tab_page, "Matplotlib Graph")

def mapl():
    # 데이터 생성
    x = [1, 2, 3, 4, 5]
    y = [2, 3, 5, 7, 11]

    # Matplotlib figure 생성
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title('Matplotlib Plot')
    return fig

def main():
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
