import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import QDate, QAbstractTableModel, Qt
from PyQt5 import uic
from back import conductor

form_class = uic.loadUiType("./ui/main_form.ui")[0]

class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
          return str(self._data.iloc[index.row(), index.column()])

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            else:
                return str(section)

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.serchRufBid)
        self.presmptPrceBgn.setValidator(QIntValidator())   # 숫자만 입력
        self.presmptPrceBgn.textChanged.connect(self.format_num)
        self.presmptPrceEnd.setValidator(QIntValidator())  # 숫자만 입력
        self.presmptPrceEnd.textChanged.connect(self.format_num)
        self.days.setValidator(QIntValidator())  # 숫자만 입력

    def serchRufBid(self):
        delt_day = int(self.days.text())

        bgnDt = (QDate.currentDate().addDays(-delt_day)).toString('yyyyMMdd0000')
        endDt = (QDate.currentDate().addDays(-1)).toString('yyyyMMdd2359')

        rqDic = {
            'inqryBgnDt': bgnDt,
            'inqryEndDt': endDt,
            'prtcptLmtRgnNm': self.region.text(),
            'indstrytyNm': self.indus_cb.currentText(),
            'presmptPrceBgn': self.presmptPrceBgn.text().replace(',', ''),
            'presmptPrceEnd': self.presmptPrceEnd.text().replace(',', ''),
        }
        valA = self.valuA_chk.isChecked()

        conductor.bidsData(rqDic, valA)

        '''  개발중 잠
        dfs = conductor.bidsData(rqDic, valA)
        self.df = dfs[0]
        model = PandasModel(self.df)
        self.table_view.setModel(model)
        '''


    def format_num(self):           # 입력된 숫자에 천단위 구분기호 삽입(솟수점포함)
        sender = self.sender()
        text = sender.text()
        text = text.replace(',', '')

        try:
            value = '{:,.0f}'.format(float(text))
            sender.setText(value)
        except ValueError:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywin = WindowClass()
    mywin.show()
    app.exec_()