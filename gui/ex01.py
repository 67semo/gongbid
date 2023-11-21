import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # QLineEdit 위젯 생성
        self.line_edit = QLineEdit(self)
        self.line_edit.setValidator(QIntValidator())  # 숫자만 입력되도록 설정
        self.line_edit.setAlignment(Qt.AlignRight)  # 오른쪽 정렬
        self.line_edit.textChanged.connect(self.format_number)

        layout.addWidget(self.line_edit)

        self.setLayout(layout)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('천 단위 쉼표 삽입 예제')

    def format_number(self):
        # QLineEdit의 텍스트 가져오기
        text = self.line_edit.text()

        # 쉼표 제거
        text = text.replace(',', '')

        try:
            # 숫자로 변환 후 천 단위 쉼표 추가
            value = '{:,.0f}'.format(float(text))
            # QLineEdit에 표시
            self.line_edit.setText(value)
        except ValueError:
            # 변환할 수 없는 경우 (예: '1,000'과 같은 형태)
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec_())
