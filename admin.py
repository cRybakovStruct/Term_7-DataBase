from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt, QObject
from PyQt5 import QtGui, QtWidgets
import json
import pymysql.cursors


from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QSize, Qt

from additional_modules import *


class NoneConnectionError(AttributeError):
    ''''''


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(480, 80))
        self.setWindowTitle("Admin")
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.grid_layout = QGridLayout()
        central_widget.setLayout(self.grid_layout)

        table = createTableFromPYMYSQL()

        table.resizeColumnsToContents()

        self.okButton = QPushButton("OK", self)
        self.okButton.setFixedWidth(40)
        self.okButton.clicked.connect(lambda: self.onAsk())
        self.request = QLineEdit(self)
        self.requests = QComboBox(self)
        self.requests.setLineEdit(self.request)
        self.hbox = QHBoxLayout(self)
        self.hbox.addWidget(self.requests)
        self.hbox.addWidget(self.okButton)
        self.vid = QWidget(self)
        self.vid.setLayout(self.hbox)
        self.grid_layout.addWidget(self.vid, 0, 0)
        self.grid_layout.addWidget(table, 1, 0)

        self.connection = self.getConnection()
        while not self.connection:
            QMessageBox.critical(
                None, "Error", "Wrong authorization parameters")
            self.connection = self.getConnection()

    def getConnection(self):

        dialog = AuthorizationDlg(self)
        if dialog.exec_() == QDialog.Accepted:
            print('Login: %s' % dialog.login.text())
            print('Password: %s' % dialog.passwd.text())
            try:
                connection = pymysql.connect(
                    host='localhost',
                    user=dialog.login.text(),
                    db='rmc',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor,
                    password=dialog.passwd.text()
                )
                return connection
            except Exception:
                return

        else:
            print('Cancelled')
            dialog.deleteLater()
            raise NoneConnectionError

    def tryToAddRequest(self, request):
        for i in range(self.requests.count()):
            if request == self.requests.itemText(i):
                return
        self.requests.addItem(request)

    def onAsk(self):

        with self.connection.cursor() as cursor:
            request = self.request.displayText()
            self.tryToAddRequest(request)
            self.res = {}
            try:
                cursor.execute(request)
            except Exception as err:
                QMessageBox.critical(
                    None, repr(err).split('(')[0], err.args[1])
                return self.res

            for line in cursor.fetchall():
                for key in line.keys():
                    try:
                        self.res[key].append(line[key])
                    except:
                        self.res[key] = [line[key]]

            print(self.res)

        table = createTableFromPYMYSQL(self.res, self)
        table.resizeColumnsToContents()
        self.grid_layout.addWidget(table, 1, 0)


if __name__ == "__main__":
    try:
        import sys
        app = QApplication(sys.argv)
        mw = MainWindow()
        mw.show()
        sys.exit(app.exec())
    except NoneConnectionError:
        print("Exit")
