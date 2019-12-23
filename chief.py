import MySQLdb

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt, QObject
from PyQt5 import QtGui, QtWidgets
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QSize, Qt
from additional_modules import *


class NoneConnectionError(AttributeError):
    ''''''


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.workers_table_headers = ['id',
                                      'surname',
                                      'name',
                                      'fathername',
                                      'education',
                                      'town',
                                      'address',
                                      'phonenumber',
                                      'birthday',
                                      'employ_date',
                                      'salary',
                                      'position',
                                      'category',
                                      'unemploy_date']

        self.machines_table_headers = ['model',
                                       'type',
                                       'length',
                                       'width',
                                       'height',
                                       'weight',
                                       'power',
                                       'detail_lenght',
                                       'detail_width',
                                       'detail_thickness',
                                       'tools',
                                       'manufactorer',
                                       'firm',
                                       'contact',
                                       'comments']

        self.connection = self.getConnection()
        while not self.connection:
            QMessageBox.critical(
                None, "Error", "Wrong authorization parameters")
            self.connection = self.getConnection()

        self.connection.autocommit(True)
        self.createWindow()

    def createWindow(self):
        self.setMinimumSize(QSize(480, 80))
        self.setWindowTitle("chief")
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.grid_layout = QGridLayout()
        self.tabWidget = self.createMainTabWidget()
        self.grid_layout.addWidget(self.tabWidget, 0, 0)
        central_widget.setLayout(self.grid_layout)

    def createMainTabWidget(self):
        tabWidget = QTabWidget(self)

        tabWidget.addTab(self.createWorkersTab(), 'Работники')
        tabWidget.addTab(self.createMachinesTab(), 'Станки')
        # TODO: Накидать ещё табов для разных целей

        return tabWidget

# region Workers

    def createWorkersTab(self):
        workersWidget = QWidget(self)

        filterGroup = QGroupBox('filters', self)

        filterLayout = QHBoxLayout(self)

        toolbar = QHBoxLayout(self)

        self.workersFilterColumn = QComboBox(self)
        self.workersFilterColumn.addItems(self.workers_table_headers)
        self.workersFilterValue = QLineEdit(self)
        executeFilterBtn = QPushButton('Show')
        executeFilterBtn.setFixedWidth(70)
        executeFilterBtn.clicked.connect(lambda: self.showWorkersByFilter())

        clearFilterBtn = QPushButton('Clear filters')
        clearFilterBtn.setFixedWidth(70)
        clearFilterBtn.clicked.connect(lambda: self.clearWorkersFilter())

        addWorkerBtn = QPushButton('Add worker', self)
        addWorkerBtn.setFixedWidth(70)
        addWorkerBtn.clicked.connect(lambda: self.addWorker())

        filterLayout.addWidget(self.workersFilterColumn)
        filterLayout.addWidget(self.workersFilterValue)
        filterLayout.addWidget(executeFilterBtn)
        filterLayout.addWidget(clearFilterBtn)

        filterGroup.setLayout(filterLayout)

        toolbar.addWidget(filterGroup)
        toolbar.addWidget(addWorkerBtn)

        table = createTableFromMYSQLDB(headers=self.workers_table_headers)

        self.workers_grid_layout = QGridLayout()
        self.workers_grid_layout.addLayout(toolbar, 0, 0)
        self.workers_grid_layout.addWidget(table, 1, 0)
        workersWidget.setLayout(self.workers_grid_layout)
        self.clearWorkersFilter()
        return workersWidget

    def addWorker(self):
        cursor = self.connection.cursor()
        cursor.execute("CALL GET_SHOPS_IDS()")
        data = cursor.fetchall()
        shops_id = [None]
        # print(data)
        for value in list(data):
            shops_id.append(str(value[0]))
        dialog = AddWorkerDlg(shops_id, self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                # pass
                args = (dialog.surname.text(),
                        dialog.name.text(),
                        dialog.fathername.text(),
                        dialog.education.text(),
                        dialog.town.text(),
                        dialog.address.text(),
                        dialog.phonenumber.text(),
                        dialog.birthday.text(),
                        dialog.employ_date.text(),
                        dialog.salary.text(),
                        dialog.position.text(),
                        dialog.category.text(),
                        dialog.unemploy_date.text(),
                        dialog.shop.currentText())
                cursor.execute(
                    "CALL INSERT_WORKER(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", args)
                # TODO: Есть заготовка для триггера, который будет генерировать ошибку в случае некорректных дат
                self.clearWorkersFilter()
            except Exception as err:
                print(err)

        else:
            print('Cancelled')
            dialog.deleteLater()

    def showWorkersByFilter(self):
        col = self.workersFilterColumn.currentText()
        QMessageBox.critical(None, self.workersFilterValue.text(), col)
        # TODO: Здесь я буду вызывать функцию, которая в зависимости от выбранных параметров
        # будет вызывать хранимую процедуру (или функцию?), которая будет работать тоже
        # в соответсвии с переданными ей параметрами
        # Либо просто вызовет сама ханимую процедуру, а та внутри себя уже определит, что и как ей отображать.

    def clearWorkersFilter(self):
        cursor = self.connection.cursor()
        cursor.execute("CALL SHOW_ALL_WORKERS()")
        data = cursor.fetchall()
        print(data)
        table = createTableFromMYSQLDB(data, self.workers_table_headers, self)
        table.resizeColumnsToContents()
        self.workers_grid_layout.addWidget(table, 1, 0)
        self.workersFilterValue.setText('')
        self.workersFilterColumn.setCurrentIndex(0)

# endregion


# regopn Shops

    def createMachinesTab(self):
        machinesWidget = QWidget(self)

        filterGroup = QGroupBox('filters', self)

        filterLayout = QHBoxLayout(self)

        toolbar = QHBoxLayout(self)

        self.machinesFilterColumn = QComboBox(self)
        self.machinesFilterColumn.addItems(self.machines_table_headers)
        self.machinesFilterValue = QLineEdit(self)
        executeFilterBtn = QPushButton('Show')
        executeFilterBtn.setFixedWidth(70)
        executeFilterBtn.clicked.connect(lambda: self.showMachinesByFilter())

        clearFilterBtn = QPushButton('Clear filters')
        clearFilterBtn.setFixedWidth(70)
        clearFilterBtn.clicked.connect(lambda: self.clearMachineFilter())

        addMachineBtn = QPushButton('Add machine', self)
        addMachineBtn.setFixedWidth(70)
        addMachineBtn.clicked.connect(lambda: self.addMachine())

        filterLayout.addWidget(self.machinesFilterColumn)
        filterLayout.addWidget(self.machinesFilterValue)
        filterLayout.addWidget(executeFilterBtn)
        filterLayout.addWidget(clearFilterBtn)

        filterGroup.setLayout(filterLayout)

        toolbar.addWidget(filterGroup)
        toolbar.addWidget(addMachineBtn)

        table = createTableFromMYSQLDB(headers=self.machines_table_headers)

        self.machines_grid_layout = QGridLayout()
        self.machines_grid_layout.addLayout(toolbar, 0, 0)
        self.machines_grid_layout.addWidget(table, 1, 0)
        machinesWidget.setLayout(self.machines_grid_layout)
        self.clearMachinesFilter()
        return machinesWidget

    def addMachine(self):
        dialog = AddMachineDlg(self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                pass
                # TODO: Вызвать хранимую процедуру и передать ей все необхдимые параметры
                self.clearMachinesFilter()
            except Exception:
                return

        else:
            print('Cancelled')
            dialog.deleteLater()

    def showMachinesByFilter(self):
        col = self.machinesFilterColumn.currentText()
        QMessageBox.critical(None, self.machinesFilterValue.text(), col)
        # TODO: Здесь я буду вызывать функцию, которая в зависимости от выбранных параметров
        # будет вызывать хранимую процедуру (или функцию?), которая будет работать тоже
        # в соответсвии с переданными ей параметрами
        # Либо просто вызовет сама ханимую процедуру, а та внутри себя уже определит, что и как ей отображать.

    def clearMachinesFilter(self):
        cursor = self.connection.cursor()
        cursor.execute("CALL SHOW_ALL_MACHINES()")
        data = cursor.fetchall()
        print(data)
        table = createTableFromMYSQLDB(data, self.machines_table_headers, self)
        table.resizeColumnsToContents()
        self.machines_grid_layout.addWidget(table, 1, 0)
        self.machinesFilterValue.setText('')
        self.machinesFilterColumn.setCurrentIndex(0)

# endregion

    def getConnection(self):

        dialog = AuthorizationDlg(self)
        if dialog.exec_() == QDialog.Accepted:
            print('Login: %s' % dialog.login.text())
            print('Password: %s' % dialog.passwd.text())
            try:
                connection = MySQLdb.connect(host="localhost",
                                             user=dialog.login.text(),
                                             passwd=dialog.passwd.text(),
                                             db="rmc",
                                             charset='utf8')
                return connection
            except Exception:
                return

        else:
            print('Cancelled')
            dialog.deleteLater()
            raise NoneConnectionError


if __name__ == "__main__":
    try:
        import sys
        app = QApplication(sys.argv)
        mw = MainWindow()
        mw.showMaximized()
        sys.exit(app.exec())
    except NoneConnectionError:
        print("Exit")

# db = MySQLdb.connect("localhost", "root", "", "rmc")
# cursor = db.cursor()
# cursor.execute("show tables")
# data = cursor.fetchall()
# print(data)
# db.close()
