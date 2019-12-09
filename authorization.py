from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt, QObject
from PyQt5 import QtGui, QtWidgets
import json
import pymysql.cursors


from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QSize, Qt


class Authorization(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        layout = QVBoxLayout(self)

        self.hbox_layout = QHBoxLayout()
        self.ok_button = QPushButton('Ok', self)
        self.ok_button.clicked.connect(self.accept)
        self.hbox_layout.addWidget(self.ok_button)
        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
        self.hbox_layout.addWidget(self.cancel_button)

        layout.addWidget(QLabel("Логин"))
        self.login = QLineEdit(self)
        layout.addWidget(self.login)
        layout.addWidget(QLabel("Пароль (можно без пароля)"))
        self.passwd = QLineEdit(self)
        layout.addWidget(self.passwd)
        layout.addLayout(self.hbox_layout)


if __name__ == "__main__":
    import sys

    # app = QApplication(sys.argv)

    # mw = Authorization()
    # mw.show()
    # sys.exit(app.exec())

    app = QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 300, 200, 100)
    window.show()
    sys.exit(app.exec_())
