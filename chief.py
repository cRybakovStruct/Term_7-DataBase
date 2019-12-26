import MySQLdb

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt, QObject
from PyQt5 import QtGui, QtWidgets
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QSize, Qt

from additional_modules import *
from dialogs import *


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
                                       'detail_length',
                                       'detail_width',
                                       'detail_thickness',
                                       'tools',
                                       'manufactorer',
                                       'firm',
                                       'contact',
                                       'comments']

        self.shops_table_headers = ['idshop',
                                    'chief_IP',
                                    'chief_RP',
                                    'chief_DP',
                                    'chief_VP',
                                    'chief_TP',
                                    'chief_PP',
                                    'idshop_RP']

        self.equipment_table_headers = ['idequipment',
                                        'model',
                                        'creation_year',
                                        'placement',
                                        'start_using_date',
                                        'comments']

        self.repairs_table_headers = ['idrepair',
                                      'repair_name',
                                      'is_planned',
                                      'receipt_date',
                                      'start_date',
                                      'finish_date',
                                      'responsible_id',
                                      'equipment_id']

        self.fixations_table_headers = ['worker',
                                        'shop']

        self.performers_table_headers = ['repair_id',
                                         'worker_id']

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
        self.tab_widget = self.createMainTabWidget()
        self.grid_layout.addWidget(self.tab_widget, 0, 0)
        central_widget.setLayout(self.grid_layout)

    def createMainTabWidget(self):
        tab_widget = QTabWidget(self)

        tab_widget.addTab(self.createWorkersTab(), 'Работники')
        tab_widget.addTab(self.createMachinesTab(), 'Станки')
        tab_widget.addTab(self.createShopsTab(), 'Цеха')
        tab_widget.addTab(self.createEquipmentTab(), 'Оборудование')
        tab_widget.addTab(self.createRepairsTab(), 'Ремонты')
        tab_widget.addTab(self.createFixationsTab(), 'Закрепления')
        tab_widget.addTab(self.createPerformersTab(), 'Исполнители')

        return tab_widget

# region Workers

    def createWorkersTab(self):
        workersWidget = QWidget(self)

        filter_group = QGroupBox('filters', self)

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

        filter_group.setLayout(filterLayout)

        toolbar.addWidget(filter_group)
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
        for value in list(data):
            shops_id.append(str(value[0]))
        dialog = AddWorkerDlg(shops_id, self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                args = (dialog.surname.text() if dialog.surname.text() != "" else None,
                        dialog.name.text() if dialog.name.text() != "" else None,
                        dialog.fathername.text() if dialog.fathername.text() != "" else None,
                        dialog.education.text() if dialog.education.text() != "" else None,
                        dialog.town.text() if dialog.town.text() != "" else None,
                        dialog.address.text() if dialog.address.text() != "" else None,
                        dialog.phonenumber.text() if dialog.phonenumber.text() != "" else None,
                        dialog.birthday.text() if dialog.birthday.text() != "" else None,
                        dialog.employ_date.text() if dialog.employ_date.text() != "" else None,
                        dialog.salary.text() if dialog.salary.text() != "" else None,
                        dialog.position.text() if dialog.position.text() != "" else None,
                        dialog.category.text() if dialog.category.text() != "" else None,
                        dialog.unemploy_date.text() if dialog.unemploy_date.text() != "" else None,
                        dialog.shop.currentText() if dialog.shop.text() != "" else None)
                cursor.execute(
                    "CALL INSERT_WORKER(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", args)
                self.clearWorkersFilter()
            except Exception as err:
                QMessageBox.critical(None, 'Error!', str(err))

        else:
            print('Cancelled')
            dialog.deleteLater()

    def showWorkersByFilter(self):
        col = self.workersFilterColumn.currentText()
        cursor = self.connection.cursor()
        cursor.execute("CALL FILTER_WORKERS(%s, %s)",
                       (col, self.workersFilterValue.text()))
        data = cursor.fetchall()
        print(data)
        table = createTableFromMYSQLDB(data, self.workers_table_headers, self)
        table.resizeColumnsToContents()
        self.workers_grid_layout.addWidget(table, 1, 0)
        self.workersFilterValue.setText('')
        self.workersFilterColumn.setCurrentIndex(0)

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


# regopn Machines


    def createMachinesTab(self):
        machines_widget = QWidget(self)

        filter_group = QGroupBox('filters', self)

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

        filter_group.setLayout(filterLayout)

        toolbar.addWidget(filter_group)
        toolbar.addWidget(addMachineBtn)

        table = createTableFromMYSQLDB(headers=self.machines_table_headers)

        self.machines_grid_layout = QGridLayout()
        self.machines_grid_layout.addLayout(toolbar, 0, 0)
        self.machines_grid_layout.addWidget(table, 1, 0)
        machines_widget.setLayout(self.machines_grid_layout)
        self.clearMachinesFilter()
        return machines_widget

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

# region Shops

    def createShopsTab(self):
        shops_widget = QWidget(self)

        filter_group = QGroupBox('filters', self)

        filterLayout = QHBoxLayout(self)

        toolbar = QHBoxLayout(self)

        self.shopsFilterColumn = QComboBox(self)
        self.shopsFilterColumn.addItems(self.shops_table_headers)
        self.shopsFilterValue = QLineEdit(self)
        executeFilterBtn = QPushButton('Show')
        executeFilterBtn.setFixedWidth(70)
        executeFilterBtn.clicked.connect(lambda: self.showShopsByFilter())

        clearFilterBtn = QPushButton('Clear filters')
        clearFilterBtn.setFixedWidth(70)
        clearFilterBtn.clicked.connect(lambda: self.clearShopsFilter())

        addShopsBtn = QPushButton('Add worker', self)
        addShopsBtn.setFixedWidth(70)
        addShopsBtn.clicked.connect(lambda: self.addShop())

        filterLayout.addWidget(self.shopsFilterColumn)
        filterLayout.addWidget(self.shopsFilterValue)
        filterLayout.addWidget(executeFilterBtn)
        filterLayout.addWidget(clearFilterBtn)

        filter_group.setLayout(filterLayout)

        toolbar.addWidget(filter_group)
        toolbar.addWidget(addShopsBtn)

        table = createTableFromMYSQLDB(headers=self.shops_table_headers)

        self.shops_grid_layout = QGridLayout()
        self.shops_grid_layout.addLayout(toolbar, 0, 0)
        self.shops_grid_layout.addWidget(table, 1, 0)
        shops_widget.setLayout(self.shops_grid_layout)
        self.clearShopsFilter()
        return shops_widget

    def addShop(self):
        # cursor = self.connection.cursor()
        # cursor.execute("CALL GET_SHOPS_IDS()")
        # data = cursor.fetchall()
        # shops_id = [None]
        # for value in list(data):
        #     shops_id.append(str(value[0]))
        # dialog = AddWorkerDlg(shops_id, self)
        # if dialog.exec_() == QDialog.Accepted:
        #     try:
        #         args = (dialog.surname.text(),
        #                 dialog.name.text(),
        #                 dialog.fathername.text(),
        #                 dialog.education.text(),
        #                 dialog.town.text(),
        #                 dialog.address.text(),
        #                 dialog.phonenumber.text(),
        #                 dialog.birthday.text(),
        #                 dialog.employ_date.text(),
        #                 dialog.salary.text(),
        #                 dialog.position.text(),
        #                 dialog.category.text(),
        #                 dialog.unemploy_date.text(),
        #                 dialog.shop.currentText())
        #         cursor.execute(
        #             "CALL INSERT_WORKER(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", args)
        #         # TODO: Есть заготовка для триггера, который будет генерировать ошибку в случае некорректных дат
        #         self.clearWorkersFilter()
        #     except Exception as err:
        #         print(err)

        # else:
        #     print('Cancelled')
        #     dialog.deleteLater()
        pass

    def showShopsByFilter(self):
        # col = self.shopsFilterColumn.currentText()
        # cursor = self.connection.cursor()
        # cursor.execute("CALL FILTER_SHOPS(%s, %s)",
        #                (col, self.shopsFilterValue.text()))
        # data = cursor.fetchall()
        # print(data)
        # table = createTableFromMYSQLDB(data, self.shops_table_headers, self)
        # table.resizeColumnsToContents()
        # self.shops_grid_layout.addWidget(table, 1, 0)
        # self.shopsFilterValue.setText('')
        # self.shopsFilterColumn.setCurrentIndex(0)
        pass

    def clearShopsFilter(self):
        cursor = self.connection.cursor()
        cursor.execute("CALL SHOW_ALL_SHOPS()")
        data = cursor.fetchall()
        print(data)
        table = createTableFromMYSQLDB(data, self.shops_table_headers, self)
        table.resizeColumnsToContents()
        self.shops_grid_layout.addWidget(table, 1, 0)
        self.shopsFilterValue.setText('')
        self.shopsFilterColumn.setCurrentIndex(0)

# endregion

# region Equipment

    def createEquipmentTab(self):
        equipment_widget = QWidget(self)

        filter_group = QGroupBox('filters', self)

        filterLayout = QHBoxLayout(self)

        toolbar = QHBoxLayout(self)

        self.equipmentFilterColumn = QComboBox(self)
        self.equipmentFilterColumn.addItems(self.equipment_table_headers)
        self.equipmentFilterValue = QLineEdit(self)
        executeFilterBtn = QPushButton('Show')
        executeFilterBtn.setFixedWidth(70)
        executeFilterBtn.clicked.connect(lambda: self.showEquipmentByFilter())

        clearFilterBtn = QPushButton('Clear filters')
        clearFilterBtn.setFixedWidth(70)
        clearFilterBtn.clicked.connect(lambda: self.clearEquipmentFilter())

        addEquipmentBtn = QPushButton('Add equipment', self)
        addEquipmentBtn.setFixedWidth(70)
        addEquipmentBtn.clicked.connect(lambda: self.addEquipment())

        filterLayout.addWidget(self.equipmentFilterColumn)
        filterLayout.addWidget(self.equipmentFilterValue)
        filterLayout.addWidget(executeFilterBtn)
        filterLayout.addWidget(clearFilterBtn)

        filter_group.setLayout(filterLayout)

        toolbar.addWidget(filter_group)
        toolbar.addWidget(addEquipmentBtn)

        table = createTableFromMYSQLDB(headers=self.equipment_table_headers)

        self.equipment_grid_layout = QGridLayout()
        self.equipment_grid_layout.addLayout(toolbar, 0, 0)
        self.equipment_grid_layout.addWidget(table, 1, 0)
        equipment_widget.setLayout(self.equipment_grid_layout)
        self.clearEquipmentFilter()
        return equipment_widget

    def addEquipment(self):
        # cursor = self.connection.cursor()
        # cursor.execute("CALL GET_SHOPS_IDS()")
        # data = cursor.fetchall()
        # shops_id = [None]
        # for value in list(data):
        #     shops_id.append(str(value[0]))
        # dialog = AddWorkerDlg(shops_id, self)
        # if dialog.exec_() == QDialog.Accepted:
        #     try:
        #         args = (dialog.surname.text(),
        #                 dialog.name.text(),
        #                 dialog.fathername.text(),
        #                 dialog.education.text(),
        #                 dialog.town.text(),
        #                 dialog.address.text(),
        #                 dialog.phonenumber.text(),
        #                 dialog.birthday.text(),
        #                 dialog.employ_date.text(),
        #                 dialog.salary.text(),
        #                 dialog.position.text(),
        #                 dialog.category.text(),
        #                 dialog.unemploy_date.text(),
        #                 dialog.shop.currentText())
        #         cursor.execute(
        #             "CALL INSERT_WORKER(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", args)
        #         # TODO: Есть заготовка для триггера, который будет генерировать ошибку в случае некорректных дат
        #         self.clearWorkersFilter()
        #     except Exception as err:
        #         print(err)

        # else:
        #     print('Cancelled')
        #     dialog.deleteLater()
        pass

    def showEquipmentByFilter(self):
        # col = self.shopsFilterColumn.currentText()
        # cursor = self.connection.cursor()
        # cursor.execute("CALL FILTER_SHOPS(%s, %s)",
        #                (col, self.shopsFilterValue.text()))
        # data = cursor.fetchall()
        # print(data)
        # table = createTableFromMYSQLDB(data, self.shops_table_headers, self)
        # table.resizeColumnsToContents()
        # self.shops_grid_layout.addWidget(table, 1, 0)
        # self.shopsFilterValue.setText('')
        # self.shopsFilterColumn.setCurrentIndex(0)
        pass

    def clearEquipmentFilter(self):
        cursor = self.connection.cursor()
        cursor.execute("CALL SHOW_ALL_EQUIPMENT()")
        data = cursor.fetchall()
        print(data)
        table = createTableFromMYSQLDB(
            data, self.equipment_table_headers, self)
        table.resizeColumnsToContents()
        self.equipment_grid_layout.addWidget(table, 1, 0)
        self.equipmentFilterValue.setText('')
        self.equipmentFilterColumn.setCurrentIndex(0)

# endregion

# region Repairs

    def createRepairsTab(self):
        repairs_widget = QWidget(self)

        filter_group = QGroupBox('filters', self)

        filterLayout = QHBoxLayout(self)

        toolbar = QHBoxLayout(self)

        self.repairsFilterColumn = QComboBox(self)
        self.repairsFilterColumn.addItems(self.repairs_table_headers)
        self.repairsFilterValue = QLineEdit(self)
        executeFilterBtn = QPushButton('Show')
        executeFilterBtn.setFixedWidth(70)
        executeFilterBtn.clicked.connect(lambda: self.showRepairsByFilter())

        clearFilterBtn = QPushButton('Clear filters')
        clearFilterBtn.setFixedWidth(70)
        clearFilterBtn.clicked.connect(lambda: self.clearRepairsFilter())

        addRepairsBtn = QPushButton('Add repair', self)
        addRepairsBtn.setFixedWidth(70)
        addRepairsBtn.clicked.connect(lambda: self.addRepairs())

        filterLayout.addWidget(self.repairsFilterColumn)
        filterLayout.addWidget(self.repairsFilterValue)
        filterLayout.addWidget(executeFilterBtn)
        filterLayout.addWidget(clearFilterBtn)

        filter_group.setLayout(filterLayout)

        toolbar.addWidget(filter_group)
        toolbar.addWidget(addRepairsBtn)

        table = createTableFromMYSQLDB(headers=self.equipment_table_headers)

        self.repairs_grid_layout = QGridLayout()
        self.repairs_grid_layout.addLayout(toolbar, 0, 0)
        self.repairs_grid_layout.addWidget(table, 1, 0)
        repairs_widget.setLayout(self.repairs_grid_layout)
        self.clearRepairsFilter()
        return repairs_widget

    def addRepairs(self):
        # cursor = self.connection.cursor()
        # cursor.execute("CALL GET_SHOPS_IDS()")
        # data = cursor.fetchall()
        # shops_id = [None]
        # for value in list(data):
        #     shops_id.append(str(value[0]))
        # dialog = AddWorkerDlg(shops_id, self)
        # if dialog.exec_() == QDialog.Accepted:
        #     try:
        #         args = (dialog.surname.text(),
        #                 dialog.name.text(),
        #                 dialog.fathername.text(),
        #                 dialog.education.text(),
        #                 dialog.town.text(),
        #                 dialog.address.text(),
        #                 dialog.phonenumber.text(),
        #                 dialog.birthday.text(),
        #                 dialog.employ_date.text(),
        #                 dialog.salary.text(),
        #                 dialog.position.text(),
        #                 dialog.category.text(),
        #                 dialog.unemploy_date.text(),
        #                 dialog.shop.currentText())
        #         cursor.execute(
        #             "CALL INSERT_WORKER(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", args)
        #         # TODO: Есть заготовка для триггера, который будет генерировать ошибку в случае некорректных дат
        #         self.clearWorkersFilter()
        #     except Exception as err:
        #         print(err)

        # else:
        #     print('Cancelled')
        #     dialog.deleteLater()
        pass

    def showRepairsByFilter(self):
        # col = self.shopsFilterColumn.currentText()
        # cursor = self.connection.cursor()
        # cursor.execute("CALL FILTER_SHOPS(%s, %s)",
        #                (col, self.shopsFilterValue.text()))
        # data = cursor.fetchall()
        # print(data)
        # table = createTableFromMYSQLDB(data, self.shops_table_headers, self)
        # table.resizeColumnsToContents()
        # self.shops_grid_layout.addWidget(table, 1, 0)
        # self.shopsFilterValue.setText('')
        # self.shopsFilterColumn.setCurrentIndex(0)
        pass

    def clearRepairsFilter(self):
        cursor = self.connection.cursor()
        cursor.execute("CALL SHOW_ALL_REPAIRS()")
        data = cursor.fetchall()
        print(data)
        table = createTableFromMYSQLDB(
            data, self.repairs_table_headers, self)
        table.resizeColumnsToContents()
        self.repairs_grid_layout.addWidget(table, 1, 0)
        self.repairsFilterValue.setText('')
        self.repairsFilterColumn.setCurrentIndex(0)

# endregion

# region Fixations

    def createFixationsTab(self):
        fixations_widget = QWidget(self)

        filter_group = QGroupBox('filters', self)

        filterLayout = QHBoxLayout(self)

        toolbar = QHBoxLayout(self)

        self.fixationsFilterColumn = QComboBox(self)
        self.fixationsFilterColumn.addItems(self.fixations_table_headers)
        self.fixationsFilterValue = QLineEdit(self)
        executeFilterBtn = QPushButton('Show')
        executeFilterBtn.setFixedWidth(70)
        executeFilterBtn.clicked.connect(lambda: self.showFixationsByFilter())

        clearFilterBtn = QPushButton('Clear filters')
        clearFilterBtn.setFixedWidth(70)
        clearFilterBtn.clicked.connect(lambda: self.clearFixationsFilter())

        addFixationsBtn = QPushButton('Add fixation', self)
        addFixationsBtn.setFixedWidth(70)
        addFixationsBtn.clicked.connect(lambda: self.addFixations())

        filterLayout.addWidget(self.fixationsFilterColumn)
        filterLayout.addWidget(self.fixationsFilterValue)
        filterLayout.addWidget(executeFilterBtn)
        filterLayout.addWidget(clearFilterBtn)

        filter_group.setLayout(filterLayout)

        toolbar.addWidget(filter_group)
        toolbar.addWidget(addFixationsBtn)

        table = createTableFromMYSQLDB(headers=self.fixations_table_headers)

        self.fixations_grid_layout = QGridLayout()
        self.fixations_grid_layout.addLayout(toolbar, 0, 0)
        self.fixations_grid_layout.addWidget(table, 1, 0)
        fixations_widget.setLayout(self.fixations_grid_layout)
        self.clearFixationsFilter()
        return fixations_widget

    def addFixations(self):
        # cursor = self.connection.cursor()
        # cursor.execute("CALL GET_SHOPS_IDS()")
        # data = cursor.fetchall()
        # shops_id = [None]
        # for value in list(data):
        #     shops_id.append(str(value[0]))
        # dialog = AddWorkerDlg(shops_id, self)
        # if dialog.exec_() == QDialog.Accepted:
        #     try:
        #         args = (dialog.surname.text(),
        #                 dialog.name.text(),
        #                 dialog.fathername.text(),
        #                 dialog.education.text(),
        #                 dialog.town.text(),
        #                 dialog.address.text(),
        #                 dialog.phonenumber.text(),
        #                 dialog.birthday.text(),
        #                 dialog.employ_date.text(),
        #                 dialog.salary.text(),
        #                 dialog.position.text(),
        #                 dialog.category.text(),
        #                 dialog.unemploy_date.text(),
        #                 dialog.shop.currentText())
        #         cursor.execute(
        #             "CALL INSERT_WORKER(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", args)
        #         # TODO: Есть заготовка для триггера, который будет генерировать ошибку в случае некорректных дат
        #         self.clearWorkersFilter()
        #     except Exception as err:
        #         print(err)

        # else:
        #     print('Cancelled')
        #     dialog.deleteLater()
        pass

    def showFixationsByFilter(self):
        # col = self.shopsFilterColumn.currentText()
        # cursor = self.connection.cursor()
        # cursor.execute("CALL FILTER_SHOPS(%s, %s)",
        #                (col, self.shopsFilterValue.text()))
        # data = cursor.fetchall()
        # print(data)
        # table = createTableFromMYSQLDB(data, self.shops_table_headers, self)
        # table.resizeColumnsToContents()
        # self.shops_grid_layout.addWidget(table, 1, 0)
        # self.shopsFilterValue.setText('')
        # self.shopsFilterColumn.setCurrentIndex(0)
        pass

    def clearFixationsFilter(self):
        cursor = self.connection.cursor()
        cursor.execute("CALL SHOW_ALL_FIXATIONS()")
        data = cursor.fetchall()
        print(data)
        table = createTableFromMYSQLDB(
            data, self.fixations_table_headers, self)
        table.resizeColumnsToContents()
        self.fixations_grid_layout.addWidget(table, 1, 0)
        self.fixationsFilterValue.setText('')
        self.fixationsFilterColumn.setCurrentIndex(0)

# endregion

# region Performers

    def createPerformersTab(self):
        performers_widget = QWidget(self)

        filter_group = QGroupBox('filters', self)

        filterLayout = QHBoxLayout(self)

        toolbar = QHBoxLayout(self)

        self.performersFilterColumn = QComboBox(self)
        self.performersFilterColumn.addItems(self.performers_table_headers)
        self.performersFilterValue = QLineEdit(self)
        executeFilterBtn = QPushButton('Show')
        executeFilterBtn.setFixedWidth(70)
        executeFilterBtn.clicked.connect(lambda: self.showPerformersByFilter())

        clearFilterBtn = QPushButton('Clear filters')
        clearFilterBtn.setFixedWidth(70)
        clearFilterBtn.clicked.connect(lambda: self.clearPerformersFilter())

        addPerformersBtn = QPushButton('Add performer', self)
        addPerformersBtn.setFixedWidth(70)
        addPerformersBtn.clicked.connect(lambda: self.addPerformers())

        filterLayout.addWidget(self.performersFilterColumn)
        filterLayout.addWidget(self.performersFilterValue)
        filterLayout.addWidget(executeFilterBtn)
        filterLayout.addWidget(clearFilterBtn)

        filter_group.setLayout(filterLayout)

        toolbar.addWidget(filter_group)
        toolbar.addWidget(addPerformersBtn)

        table = createTableFromMYSQLDB(headers=self.performers_table_headers)

        self.performers_grid_layout = QGridLayout()
        self.performers_grid_layout.addLayout(toolbar, 0, 0)
        self.performers_grid_layout.addWidget(table, 1, 0)
        performers_widget.setLayout(self.performers_grid_layout)
        self.clearPerformersFilter()
        return performers_widget

    def addPerformers(self):
        # cursor = self.connection.cursor()
        # cursor.execute("CALL GET_SHOPS_IDS()")
        # data = cursor.fetchall()
        # shops_id = [None]
        # for value in list(data):
        #     shops_id.append(str(value[0]))
        # dialog = AddWorkerDlg(shops_id, self)
        # if dialog.exec_() == QDialog.Accepted:
        #     try:
        #         args = (dialog.surname.text(),
        #                 dialog.name.text(),
        #                 dialog.fathername.text(),
        #                 dialog.education.text(),
        #                 dialog.town.text(),
        #                 dialog.address.text(),
        #                 dialog.phonenumber.text(),
        #                 dialog.birthday.text(),
        #                 dialog.employ_date.text(),
        #                 dialog.salary.text(),
        #                 dialog.position.text(),
        #                 dialog.category.text(),
        #                 dialog.unemploy_date.text(),
        #                 dialog.shop.currentText())
        #         cursor.execute(
        #             "CALL INSERT_WORKER(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", args)
        #         # TODO: Есть заготовка для триггера, который будет генерировать ошибку в случае некорректных дат
        #         self.clearWorkersFilter()
        #     except Exception as err:
        #         print(err)

        # else:
        #     print('Cancelled')
        #     dialog.deleteLater()
        pass

    def showPerformersByFilter(self):
        # col = self.shopsFilterColumn.currentText()
        # cursor = self.connection.cursor()
        # cursor.execute("CALL FILTER_SHOPS(%s, %s)",
        #                (col, self.shopsFilterValue.text()))
        # data = cursor.fetchall()
        # print(data)
        # table = createTableFromMYSQLDB(data, self.shops_table_headers, self)
        # table.resizeColumnsToContents()
        # self.shops_grid_layout.addWidget(table, 1, 0)
        # self.shopsFilterValue.setText('')
        # self.shopsFilterColumn.setCurrentIndex(0)
        pass

    def clearPerformersFilter(self):
        cursor = self.connection.cursor()
        cursor.execute("CALL SHOW_ALL_PERFORMERS()")
        data = cursor.fetchall()
        print(data)
        table = createTableFromMYSQLDB(
            data, self.performers_table_headers, self)
        table.resizeColumnsToContents()
        self.performers_grid_layout.addWidget(table, 1, 0)
        self.performersFilterValue.setText('')
        self.performersFilterColumn.setCurrentIndex(0)

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
