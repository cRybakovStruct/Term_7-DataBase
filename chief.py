import MySQLdb

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, QObject
from PyQt5 import QtGui, QtWidgets
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QSize

from additional_modules import *
from dialogs import *


from classes_for_alchemy_orm import Base, Fixation, Machine, Repair, Shop, Worker, Equipment
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


BUTTON_WIDTH = 95
FILTERS_BUTTON = 70


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
                                       'manufacturer',
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

        self.equipment_table_headers = ['model',
                                        'creation_year',
                                        'serial_number',
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
                                      'surname',
                                      'name',
                                      'equipment_id'
                                      'model',
                                      'placement']

        self.fixations_table_headers = ['worker',
                                        'surname',
                                        'name',
                                        'shop']

        self.performers_table_headers = ['repair_id',
                                         'worker_id',
                                         'surname',
                                         'name']

        self.connection, self.engine = self.getConnection()
        while not self.connection:
            self.connection, self.engine = self.getConnection()

        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

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
        executeFilterBtn.setFixedWidth(FILTERS_BUTTON)
        executeFilterBtn.clicked.connect(lambda: self.showWorkersByFilter())

        clearFilterBtn = QPushButton('Clear filters')
        clearFilterBtn.setFixedWidth(FILTERS_BUTTON)
        clearFilterBtn.clicked.connect(lambda: self.clearWorkersFilter())

        controlls = QVBoxLayout(self)
        addWorkerBtn = QPushButton('Add worker', self)
        addWorkerBtn.setFixedWidth(BUTTON_WIDTH)
        addWorkerBtn.clicked.connect(lambda: self.addWorker())
        controlls.addWidget(addWorkerBtn)

        editWorkerBtn = QPushButton('Edit worker', self)
        editWorkerBtn.setFixedWidth(BUTTON_WIDTH)
        editWorkerBtn.clicked.connect(lambda: self.editWorker())
        controlls.addWidget(editWorkerBtn)

        delWorkerBtn = QPushButton('Delete worker', self)
        delWorkerBtn.setFixedWidth(BUTTON_WIDTH)
        delWorkerBtn.clicked.connect(lambda: self.deleteWorker())
        controlls.addWidget(delWorkerBtn)

        filterLayout.addWidget(self.workersFilterColumn)
        filterLayout.addWidget(self.workersFilterValue)
        filterLayout.addWidget(executeFilterBtn)
        filterLayout.addWidget(clearFilterBtn)

        filter_group.setLayout(filterLayout)

        toolbar.addWidget(filter_group)
        toolbar.addLayout(controlls)

        self.workers_table = createTableFromMYSQLDB(
            headers=self.workers_table_headers)
        # self.workers_table.itemDoubleClicked.connect(lambda: self.deleteWorker())

        self.workers_grid_layout = QGridLayout()
        self.workers_grid_layout.addLayout(toolbar, 0, 0)
        self.workers_grid_layout.addWidget(self.workers_table, 1, 0)
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
                new_worker = Worker(dialog.surname.text() if dialog.surname.text() != "" else None,
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
                                    dialog.unemploy_date.text() if dialog.unemploy_date.text() != "" else None)
                self.session = self.Session()
                self.session.add(new_worker)
                self.session.commit()

                if dialog.shop.currentText() != "":
                    new_fixation = Fixation(
                        new_worker.idworker, dialog.shop.currentText())
                    print(new_fixation)
                    self.session.add(new_fixation)
                    self.session.commit()

                self.clearWorkersFilter()
            except Exception as err:
                QMessageBox.critical(None, 'Error!', str(err))
            finally:
                self.session.close()

        else:
            print('Cancelled')
            dialog.deleteLater()

    def editWorker(self):
        items = self.workers_table.selectedItems()
        row, res = getRow(items)
        if (not res) or (row is None):
            QMessageBox.critical(
                None, 'Warning!', 'Please, select cells in single row')
            return
        else:
            dialog = EditWorkerDlg(self)
            dialog.surname.setText(self.workers_table.item(row, 1).text())
            dialog.name.setText(self.workers_table.item(row, 2).text())
            dialog.fathername.setText(self.workers_table.item(row, 3).text())
            dialog.education.setText(self.workers_table.item(row, 4).text())
            dialog.town.setText(self.workers_table.item(row, 5).text())
            dialog.address.setText(self.workers_table.item(row, 6).text())
            dialog.phonenumber.setText(self.workers_table.item(row, 7).text())
            dialog.birthday.setText(self.workers_table.item(row, 8).text())
            dialog.employ_date.setText(self.workers_table.item(row, 9).text())
            dialog.salary.setText(self.workers_table.item(row, 10).text())
            dialog.position.setText(self.workers_table.item(row, 11).text())
            dialog.category.setText(self.workers_table.item(row, 12).text())
            dialog.unemploy_date.setText(
                self.workers_table.item(row, 13).text())
            if dialog.exec_() == QDialog.Accepted:
                try:
                    self.session = self.Session()
                    editing_worker = self.session.query(Worker).filter_by(
                        idworker=self.workers_table.item(row, 0).text()).first()
                    editing_worker.surname = dialog.surname.text(
                    ) if dialog.surname.text() != "" else None
                    editing_worker.name = dialog.name.text() if dialog.name.text() != "" else None
                    editing_worker.fathername = dialog.fathername.text(
                    ) if dialog.fathername.text() != "" else None
                    editing_worker.education = dialog.education.text(
                    ) if dialog.education.text() != "" else None
                    editing_worker.town = dialog.town.text() if dialog.town.text() != "" else None
                    editing_worker.address = dialog.address.text(
                    ) if dialog.address.text() != "" else None
                    editing_worker.phonenumber = dialog.phonenumber.text(
                    ) if dialog.phonenumber.text() != "" else None
                    editing_worker.birthday = dialog.birthday.text(
                    ) if dialog.birthday.text() != "" else None
                    editing_worker.employ_date = dialog.employ_date.text(
                    ) if dialog.employ_date.text() != "" else None
                    editing_worker.salary = dialog.salary.text() if dialog.salary.text() != "" else None
                    editing_worker.position = dialog.position.text(
                    ) if dialog.position.text() != "" else None
                    editing_worker.category = dialog.category.text(
                    ) if dialog.category.text() != "" else None
                    editing_worker.unemploy_date = dialog.unemploy_date.text(
                    ) if dialog.unemploy_date.text() != "" else None
                    self.session.commit()
                    self.clearWorkersFilter()
                except Exception as err:
                    QMessageBox.critical(None, 'Error!', str(err))
                finally:
                    self.session.close()

    def deleteWorker(self):
        items = self.workers_table.selectedItems()
        row, res = getRow(items)
        if (not res) or (row is None):
            QMessageBox.critical(
                None, 'Warning!', 'Please, select cells in single row')
            return
        else:
            self.session = self.Session()

            deleting_worker = self.session.query(Worker).filter_by(
                idworker=self.workers_table.item(row, 0).text()).first()
            dialog = YesNoDlg(
                'Worker deleting', f'Are you really want to delete worker:\n{deleting_worker}?')
            if dialog.exec_() == QDialog.Accepted:
                try:
                    self.session.delete(deleting_worker)
                    self.session.commit()
                    self.clearWorkersFilter()
                except Exception as err:
                    QMessageBox.critical(None, 'Error!', str(err))
            self.session.close()

    def showWorkersByFilter(self):
        col = self.workersFilterColumn.currentText()
        cursor = self.connection.cursor()
        cursor.execute("CALL FILTER_WORKERS(%s, %s)",
                       (col, self.workersFilterValue.text()))
        data = cursor.fetchall()
        self.workers_table = createTableFromMYSQLDB(
            data, self.workers_table_headers, self)
        self.workers_table.resizeColumnsToContents()
        self.workers_grid_layout.addWidget(self.workers_table, 1, 0)
        self.workersFilterValue.setText('')
        self.workersFilterColumn.setCurrentIndex(0)

    def clearWorkersFilter(self):
        cursor = self.connection.cursor()
        cursor.execute("CALL SHOW_ALL_WORKERS()")
        data = cursor.fetchall()
        self.workers_table = createTableFromMYSQLDB(
            data, self.workers_table_headers, self)
        self.workers_table.resizeColumnsToContents()
        self.workers_grid_layout.addWidget(self.workers_table, 1, 0)
        self.workersFilterValue.setText('')
        self.workersFilterColumn.setCurrentIndex(0)

# endregion

# region Machines

    def createMachinesTab(self):
        machines_widget = QWidget(self)

        filter_group = QGroupBox('filters', self)

        filterLayout = QHBoxLayout(self)

        toolbar = QHBoxLayout(self)

        self.machinesFilterColumn = QComboBox(self)
        self.machinesFilterColumn.addItems(self.machines_table_headers)
        self.machinesFilterValue = QLineEdit(self)
        executeFilterBtn = QPushButton('Show')
        executeFilterBtn.setFixedWidth(FILTERS_BUTTON)
        executeFilterBtn.clicked.connect(lambda: self.showMachinesByFilter())

        clearFilterBtn = QPushButton('Clear filters')
        clearFilterBtn.setFixedWidth(FILTERS_BUTTON)
        clearFilterBtn.clicked.connect(lambda: self.clearMachineFilter())

        controlls = QVBoxLayout(self)
        addMachineBtn = QPushButton('Add machine', self)
        addMachineBtn.setFixedWidth(BUTTON_WIDTH)
        addMachineBtn.clicked.connect(lambda: self.addMachine())
        controlls.addWidget(addMachineBtn)

        editMachineBtn = QPushButton('Edit machine', self)
        editMachineBtn.setFixedWidth(BUTTON_WIDTH)
        editMachineBtn.clicked.connect(lambda: self.editMachine())
        controlls.addWidget(editMachineBtn)

        delMachineBtn = QPushButton('Delete machine', self)
        delMachineBtn.setFixedWidth(BUTTON_WIDTH)
        delMachineBtn.clicked.connect(lambda: self.deleteMachine())
        controlls.addWidget(delMachineBtn)

        filterLayout.addWidget(self.machinesFilterColumn)
        filterLayout.addWidget(self.machinesFilterValue)
        filterLayout.addWidget(executeFilterBtn)
        filterLayout.addWidget(clearFilterBtn)

        filter_group.setLayout(filterLayout)

        toolbar.addWidget(filter_group)
        toolbar.addLayout(controlls)

        self.machines_table = createTableFromMYSQLDB(
            headers=self.machines_table_headers)

        self.machines_grid_layout = QGridLayout()
        self.machines_grid_layout.addLayout(toolbar, 0, 0)
        self.machines_grid_layout.addWidget(self.machines_table, 1, 0)
        machines_widget.setLayout(self.machines_grid_layout)
        self.clearMachinesFilter()
        return machines_widget

    def addMachine(self):
        dialog = AddMachineDlg(self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                new_machine = Machine(dialog.model.text() if dialog.model.text() != "" else None,
                                      dialog.type.text() if dialog.type.text() != "" else None,
                                      dialog.length.text() if dialog.length.text() != "" else None,
                                      dialog.width.text() if dialog.width.text() != "" else None,
                                      dialog.height.text() if dialog.height.text() != "" else None,
                                      dialog.weight.text() if dialog.weight.text() != "" else None,
                                      dialog.power.text() if dialog.power.text() != "" else None,
                                      dialog.detail_length.text() if dialog.detail_length.text() != "" else None,
                                      dialog.detail_width.text() if dialog.detail_width.text() != "" else None,
                                      dialog.detail_thickness.text() if dialog.detail_thickness.text() != "" else None,
                                      dialog.tools.text() if dialog.tools.text() != "" else None,
                                      dialog.manufacturer.text() if dialog.manufacturer.text() != "" else None,
                                      dialog.firm.text() if dialog.firm.text() != "" else None,
                                      dialog.contact.text() if dialog.contact.text() != "" else None,
                                      dialog.comments.text() if dialog.comments.text() != "" else None)
                self.session = self.Session()
                self.session.add(new_machine)
                self.session.commit()

                self.clearMachinesFilter()
            except Exception as err:
                QMessageBox.critical(None, 'Error!', str(err))

        else:
            print('Cancelled')
            dialog.deleteLater()

    def editMachine(self):
        items = self.machines_table.selectedItems()
        row, res = getRow(items)
        if (not res) or (row is None):
            QMessageBox.critical(
                None, 'Warning!', 'Please, select cells in single row')
            return
        else:
            dialog = AddMachineDlg(self)

            dialog.model.setText(self.machines_table.item(row, 0).text())
            dialog.type.setText(self.machines_table.item(row, 1).text())
            dialog.length.setText(self.machines_table.item(row, 2).text())
            dialog.width.setText(self.machines_table.item(row, 3).text())
            dialog.height.setText(self.machines_table.item(row, 4).text())
            dialog.weight.setText(self.machines_table.item(row, 5).text())
            dialog.power.setText(self.machines_table.item(row, 6).text())
            dialog.detail_length.setText(
                self.machines_table.item(row, 7).text())
            dialog.detail_width.setText(
                self.machines_table.item(row, 8).text())
            dialog.detail_thickness.setText(
                self.machines_table.item(row, 9).text())
            dialog.tools.setText(self.machines_table.item(row, 10).text()),
            dialog.manufacturer.setText(
                self.machines_table.item(row, 11).text())
            dialog.firm.setText(self.machines_table.item(row, 12).text())
            dialog.contact.setText(self.machines_table.item(row, 13).text())
            dialog.comments.setText(self.machines_table.item(row, 14).text())

            if dialog.exec_() == QDialog.Accepted:
                try:
                    self.session = self.Session()
                    editing_machine = self.session.query(Machine).filter_by(
                        model=self.machines_table.item(row, 0).text()).first()

                    editing_machine.model = dialog.model.text() if dialog.model.text() != "" else None
                    editing_machine.type = dialog.type.text() if dialog.type.text() != "" else None
                    editing_machine.length = dialog.length.text(
                    ) if dialog.length.text() != "" else None
                    editing_machine.width = dialog.width.text() if dialog.width.text() != "" else None
                    editing_machine.height = dialog.height.text(
                    ) if dialog.height.text() != "" else None
                    editing_machine.weight = dialog.weight.text(
                    ) if dialog.weight.text() != "" else None
                    editing_machine.power = dialog.power.text() if dialog.power.text() != "" else None
                    editing_machine.detail_length = dialog.detail_length.text(
                    ) if dialog.detail_length.text() != "" else None
                    editing_machine.detail_width = dialog.detail_width.text(
                    ) if dialog.detail_width.text() != "" else None
                    editing_machine.detail_thickness = dialog.detail_thickness.text(
                    ) if dialog.detail_thickness.text() != "" else None
                    editing_machine.tools = dialog.tools.text() if dialog.tools.text() != "" else None,
                    editing_machine.manufacturer = dialog.manufacturer.text(
                    ) if dialog.manufacturer.text() != "" else None
                    editing_machine.firm = dialog.firm.text() if dialog.firm.text() != "" else None
                    editing_machine.contact = dialog.contact.text(
                    ) if dialog.contact.text() != "" else None
                    editing_machine.comments = dialog.comments.text(
                    ) if dialog.comments.text() != "" else None

                    self.session.commit()
                    self.clearMachinesFilter()
                except Exception as err:
                    QMessageBox.critical(None, 'Error!', str(err))
                finally:
                    self.session.close()

    def deleteMachine(self):
        items = self.machines_table.selectedItems()
        row, res = getRow(items)
        if (not res) or (row is None):
            QMessageBox.critical(
                None, 'Warning!', 'Please, select cells in single row')
            return
        else:
            self.session = self.Session()

            deleting_machine = self.session.query(Machine).filter_by(
                model=self.machines_table.item(row, 0).text()).first()
            dialog = YesNoDlg(
                'Machine deleting', f'Are you really want to delete machine:\n{deleting_machine}?')
            if dialog.exec_() == QDialog.Accepted:
                try:
                    self.session.delete(deleting_machine)
                    self.session.commit()
                    self.clearMachinesFilter()
                except Exception as err:
                    QMessageBox.critical(None, 'Error!', str(err))
            self.session.close()

    def showMachinesByFilter(self):
        col = self.machinesFilterColumn.currentText()
        cursor = self.connection.cursor()
        cursor.execute("CALL FILTER_MACHINES(%s, %s)",
                       (col, self.machinesFilterValue.text()))
        data = cursor.fetchall()
        self.machines_table = createTableFromMYSQLDB(
            data, self.machines_table_headers, self)
        self.machines_table.resizeColumnsToContents()
        self.machines_grid_layout.addWidget(self.machines_table, 1, 0)
        self.machinesFilterValue.setText('')
        self.machinesFilterColumn.setCurrentIndex(0)

    def clearMachinesFilter(self):
        cursor = self.connection.cursor()
        cursor.execute("CALL SHOW_ALL_MACHINES()")
        data = cursor.fetchall()
        self.machines_table = createTableFromMYSQLDB(
            data, self.machines_table_headers, self)
        self.machines_table.resizeColumnsToContents()
        self.machines_grid_layout.addWidget(self.machines_table, 1, 0)
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
        executeFilterBtn.setFixedWidth(FILTERS_BUTTON)
        executeFilterBtn.clicked.connect(lambda: self.showShopsByFilter())

        clearFilterBtn = QPushButton('Clear filters')
        clearFilterBtn.setFixedWidth(FILTERS_BUTTON)
        clearFilterBtn.clicked.connect(lambda: self.clearShopsFilter())

        controlls = QVBoxLayout(self)
        addShopBtn = QPushButton('Add shop', self)
        addShopBtn.setFixedWidth(BUTTON_WIDTH)
        addShopBtn.clicked.connect(lambda: self.addShop())
        controlls.addWidget(addShopBtn)

        editShopBtn = QPushButton('Edit shop', self)
        editShopBtn.setFixedWidth(BUTTON_WIDTH)
        editShopBtn.clicked.connect(lambda: self.editShop())
        controlls.addWidget(editShopBtn)

        delShopBtn = QPushButton('Delete shop', self)
        delShopBtn.setFixedWidth(BUTTON_WIDTH)
        delShopBtn.clicked.connect(lambda: self.deleteShop())
        controlls.addWidget(delShopBtn)

        filterLayout.addWidget(self.shopsFilterColumn)
        filterLayout.addWidget(self.shopsFilterValue)
        filterLayout.addWidget(executeFilterBtn)
        filterLayout.addWidget(clearFilterBtn)

        filter_group.setLayout(filterLayout)

        toolbar.addWidget(filter_group)
        toolbar.addLayout(controlls)

        self.shops_table = createTableFromMYSQLDB(
            headers=self.shops_table_headers)

        self.shops_grid_layout = QGridLayout()
        self.shops_grid_layout.addLayout(toolbar, 0, 0)
        self.shops_grid_layout.addWidget(self.shops_table, 1, 0)
        shops_widget.setLayout(self.shops_grid_layout)
        self.clearShopsFilter()
        return shops_widget

    def addShop(self):
        dialog = AddShopDlg(self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                new_shop = Shop(dialog.idshop.text() if dialog.idshop.text() != "" else None,
                                dialog.chief_IP.text() if dialog.chief_IP.text() != "" else None,
                                dialog.chief_RP.text() if dialog.chief_RP.text() != "" else None,
                                dialog.chief_DP.text() if dialog.chief_DP.text() != "" else None,
                                dialog.chief_VP.text() if dialog.chief_VP.text() != "" else None,
                                dialog.chief_TP.text() if dialog.chief_TP.text() != "" else None,
                                dialog.chief_PP.text() if dialog.chief_PP.text() != "" else None,
                                dialog.idshop_RP.text() if dialog.idshop_RP.text() != "" else None)
                self.session = self.Session()
                self.session.add(new_shop)
                self.session.commit()
                self.clearShopsFilter()
            except Exception as err:
                QMessageBox.critical(None, 'Error!', str(err))

        else:
            print('Cancelled')
            dialog.deleteLater()

    def editShop(self):
        items = self.shops_table.selectedItems()
        row, res = getRow(items)
        if (not res) or (row is None):
            QMessageBox.critical(
                None, 'Warning!', 'Please, select cells in single row')
            return
        else:
            dialog = AddShopDlg(self)
            dialog.idshop.setText(self.shops_table.item(row, 0).text())
            dialog.chief_IP.setText(self.shops_table.item(row, 1).text())
            dialog.chief_RP.setText(self.shops_table.item(row, 2).text())
            dialog.chief_DP.setText(self.shops_table.item(row, 3).text())
            dialog.chief_VP.setText(self.shops_table.item(row, 4).text())
            dialog.chief_TP.setText(self.shops_table.item(row, 5).text())
            dialog.chief_PP.setText(self.shops_table.item(row, 6).text())
            dialog.idshop_RP.setText(self.shops_table.item(row, 7).text())
            if dialog.exec_() == QDialog.Accepted:
                try:
                    self.session = self.Session()
                    editing_shop = self.session.query(Shop).filter_by(
                        idshop=self.shops_table.item(row, 0).text()).first()
                    editing_shop.idshop = dialog.idshop.text() if dialog.idshop.text() != "" else None
                    editing_shop.chief_IP = dialog.chief_IP.text(
                    ) if dialog.chief_IP.text() != "" else None
                    editing_shop.chief_RP = dialog.chief_RP.text(
                    ) if dialog.chief_RP.text() != "" else None
                    editing_shop.chief_DP = dialog.chief_DP.text(
                    ) if dialog.chief_DP.text() != "" else None
                    editing_shop.chief_VP = dialog.chief_VP.text(
                    ) if dialog.chief_VP.text() != "" else None
                    editing_shop.chief_TP = dialog.chief_TP.text(
                    ) if dialog.chief_TP.text() != "" else None
                    editing_shop.chief_PP = dialog.chief_PP.text(
                    ) if dialog.chief_PP.text() != "" else None
                    editing_shop.idshop_RP = dialog.idshop_RP.text(
                    ) if dialog.idshop_RP.text() != "" else None
                    self.session.commit()
                    self.clearShopsFilter()
                except Exception as err:
                    QMessageBox.critical(None, 'Error!', str(err))
                finally:
                    self.session.close()

    def deleteShop(self):
        items = self.shops_table.selectedItems()
        row, res = getRow(items)
        if (not res) or (row is None):
            QMessageBox.critical(
                None, 'Warning!', 'Please, select cells in single row')
            return
        else:
            self.session = self.Session()

            deleting_shop = self.session.query(Shop).filter_by(
                idshop=self.shops_table.item(row, 0).text()).first()
            dialog = YesNoDlg(
                'Shop deleting', f'Are you really want to delete shop:\n{deleting_shop}?')
            if dialog.exec_() == QDialog.Accepted:
                try:
                    self.session.delete(deleting_shop)
                    self.session.commit()
                    self.clearShopsFilter()
                except Exception as err:
                    QMessageBox.critical(None, 'Error!', str(err))
            self.session.close()

    def showShopsByFilter(self):
        col = self.shopsFilterColumn.currentText()
        cursor = self.connection.cursor()
        cursor.execute("CALL FILTER_SHOPS(%s, %s)",
                       (col, self.shopsFilterValue.text()))
        data = cursor.fetchall()
        self.shops_table = createTableFromMYSQLDB(
            data, self.shops_table_headers, self)
        self.shops_table.resizeColumnsToContents()
        self.shops_grid_layout.addWidget(self.shops_table, 1, 0)
        self.shopsFilterValue.setText('')
        self.shopsFilterColumn.setCurrentIndex(0)

    def clearShopsFilter(self):
        cursor = self.connection.cursor()
        cursor.execute("CALL SHOW_ALL_SHOPS()")
        data = cursor.fetchall()
        self.shops_table = createTableFromMYSQLDB(
            data, self.shops_table_headers, self)
        self.shops_table.resizeColumnsToContents()
        self.shops_grid_layout.addWidget(self.shops_table, 1, 0)
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
        executeFilterBtn.setFixedWidth(FILTERS_BUTTON)
        executeFilterBtn.clicked.connect(lambda: self.showEquipmentByFilter())

        clearFilterBtn = QPushButton('Clear filters')
        clearFilterBtn.setFixedWidth(FILTERS_BUTTON)
        clearFilterBtn.clicked.connect(lambda: self.clearEquipmentFilter())

        controlls = QVBoxLayout(self)
        addEquipmentBtn = QPushButton('Add equipment', self)
        addEquipmentBtn.setFixedWidth(BUTTON_WIDTH)
        addEquipmentBtn.clicked.connect(lambda: self.addEquipment())
        controlls.addWidget(addEquipmentBtn)

        editEquipmentBtn = QPushButton('Edit equipment', self)
        editEquipmentBtn.setFixedWidth(BUTTON_WIDTH)
        editEquipmentBtn.clicked.connect(lambda: self.editEquipment())
        controlls.addWidget(editEquipmentBtn)

        delEquipmentBtn = QPushButton('Delete equipment', self)
        delEquipmentBtn.setFixedWidth(BUTTON_WIDTH)
        delEquipmentBtn.clicked.connect(lambda: self.deleteEquipment())
        controlls.addWidget(delEquipmentBtn)

        filterLayout.addWidget(self.equipmentFilterColumn)
        filterLayout.addWidget(self.equipmentFilterValue)
        filterLayout.addWidget(executeFilterBtn)
        filterLayout.addWidget(clearFilterBtn)

        filter_group.setLayout(filterLayout)

        toolbar.addWidget(filter_group)
        toolbar.addLayout(controlls)

        self.equipment_table = createTableFromMYSQLDB(
            headers=self.equipment_table_headers)

        self.equipment_grid_layout = QGridLayout()
        self.equipment_grid_layout.addLayout(toolbar, 0, 0)
        self.equipment_grid_layout.addWidget(self.equipment_table, 1, 0)
        equipment_widget.setLayout(self.equipment_grid_layout)
        self.clearEquipmentFilter()
        return equipment_widget

    def addEquipment(self):
        cursor = self.connection.cursor()
        cursor.execute("CALL GET_SHOPS_IDS()")
        data = cursor.fetchall()
        shops_id = [None]
        for value in list(data):
            shops_id.append(str(value[0]))
        dialog = AddEquipmentDlg(shops_id, self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                new_equipment = Equipment(dialog.model.text() if dialog.model.text() != "" else None,
                                          dialog.creation_year.text() if dialog.creation_year.text() != "" else None,
                                          dialog.serial_number.text() if dialog.serial_number.text() != "" else None,
                                          dialog.placement.currentText() if dialog.placement.currentText() != "" else None,
                                          dialog.start_using_date.text() if dialog.start_using_date.text() != "" else None,
                                          dialog.comments.text() if dialog.comments.text() != "" else None)
                self.session = self.Session()
                self.session.add(new_equipment)
                self.session.commit()

                self.clearEquipmentFilter()
            except Exception as err:
                QMessageBox.critical(None, 'Error!', str(err))
            finally:
                self.session.close()

        else:
            print('Cancelled')
            dialog.deleteLater()

    def editEquipment(self):
        items = self.equipment_table.selectedItems()
        row, res = getRow(items)
        if (not res) or (row is None):
            QMessageBox.critical(
                None, 'Warning!', 'Please, select cells in single row')
            return
        else:
            cursor = self.connection.cursor()
            cursor.execute("CALL GET_SHOPS_IDS()")
            data = cursor.fetchall()
            shops_id = [None]
            for value in list(data):
                shops_id.append(str(value[0]))

            dialog = AddEquipmentDlg(shops_id, self)
            dialog.model.setText(self.equipment_table.item(row, 0).text())
            dialog.creation_year.setText(
                self.equipment_table.item(row, 1).text())
            dialog.serial_number.setText(
                self.equipment_table.item(row, 2).text())
            dialog.placement.setCurrentText(self.equipment_table.item(row, 3).text())
            dialog.start_using_date.setText(
                self.equipment_table.item(row, 4).text())
            dialog.comments.setText(self.equipment_table.item(row, 5).text())

            if dialog.exec_() == QDialog.Accepted:
                try:
                    self.session = self.Session()
                    editing_equipment = self.session.query(Equipment).filter_by(
                        serial_number=self.equipment_table.item(row, 2).text()).first()

                    editing_equipment.model = dialog.model.text(
                    ) if dialog.model.text() != "" else None
                    editing_equipment.creation_year = dialog.creation_year.text(
                    ) if dialog.creation_year.text() != "" else None
                    editing_equipment.serial_number = dialog.serial_number.text(
                    ) if dialog.serial_number.text() != "" else None
                    editing_equipment.placement = dialog.placement.currentText(
                    ) if dialog.placement.currentText() != "" else None
                    editing_equipment.start_using_date = dialog.start_using_date.text(
                    ) if dialog.start_using_date.text() != "" else None
                    editing_equipment.comments = dialog.comments.text(
                    ) if dialog.comments.text() != "" else None

                    self.session.commit()
                    self.clearEquipmentFilter()
                except Exception as err:
                    QMessageBox.critical(None, 'Error!', str(err))
                finally:
                    self.session.close()

    def deleteEquipment(self):
        items = self.equipment_table.selectedItems()
        row, res = getRow(items)
        if (not res) or (row is None):
            QMessageBox.critical(
                None, 'Warning!', 'Please, select cells in single row')
            return
        else:
            self.session = self.Session()

            deleting_equipment = self.session.query(Equipment).filter_by(
                serial_number=self.equipment_table.item(row, 2).text()).first()
            dialog = YesNoDlg(
                'Equipment deleting', f'Are you really want to delete equipment:\n{deleting_equipment}?')
            if dialog.exec_() == QDialog.Accepted:
                try:
                    self.session.delete(deleting_equipment)
                    self.session.commit()
                    self.clearEquipmentFilter()
                except Exception as err:
                    QMessageBox.critical(None, 'Error!', str(err))
            self.session.close()

    def showEquipmentByFilter(self):
        col = self.equipmentFilterColumn.currentText()
        cursor = self.connection.cursor()
        cursor.execute("CALL FILTER_EQUIPMENT(%s, %s)",
                       (col, self.equipmentFilterValue.text()))
        data = cursor.fetchall()
        self.equipment_table = createTableFromMYSQLDB(
            data, self.equipment_table_headers, self)
        self.equipment_table.resizeColumnsToContents()
        self.equipment_grid_layout.addWidget(self.equipment_table, 1, 0)
        self.equipmentFilterValue.setText('')
        self.equipmentFilterColumn.setCurrentIndex(0)

    def clearEquipmentFilter(self):
        cursor = self.connection.cursor()
        cursor.execute("CALL SHOW_ALL_EQUIPMENT()")
        data = cursor.fetchall()
        self.equipment_table = createTableFromMYSQLDB(
            data, self.equipment_table_headers, self)
        self.equipment_table.resizeColumnsToContents()
        self.equipment_grid_layout.addWidget(self.equipment_table, 1, 0)
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
        executeFilterBtn.setFixedWidth(FILTERS_BUTTON)
        executeFilterBtn.clicked.connect(lambda: self.showRepairsByFilter())

        clearFilterBtn = QPushButton('Clear filters')
        clearFilterBtn.setFixedWidth(FILTERS_BUTTON)
        clearFilterBtn.clicked.connect(lambda: self.clearRepairsFilter())

        controlls = QVBoxLayout(self)
        addRepairBtn = QPushButton('Add repair', self)
        addRepairBtn.setFixedWidth(BUTTON_WIDTH)
        addRepairBtn.clicked.connect(lambda: self.addRepair())
        controlls.addWidget(addRepairBtn)

        editRepairBtn = QPushButton('Edit repair', self)
        editRepairBtn.setFixedWidth(BUTTON_WIDTH)
        editRepairBtn.clicked.connect(lambda: self.editRepair())
        controlls.addWidget(editRepairBtn)

        delRepairBtn = QPushButton('Delete repair', self)
        delRepairBtn.setFixedWidth(BUTTON_WIDTH)
        delRepairBtn.clicked.connect(lambda: self.deleteRepair())
        controlls.addWidget(delRepairBtn)

        filterLayout.addWidget(self.repairsFilterColumn)
        filterLayout.addWidget(self.repairsFilterValue)
        filterLayout.addWidget(executeFilterBtn)
        filterLayout.addWidget(clearFilterBtn)

        filter_group.setLayout(filterLayout)

        toolbar.addWidget(filter_group)
        toolbar.addLayout(controlls)

        table = createTableFromMYSQLDB(headers=self.equipment_table_headers)

        self.repairs_grid_layout = QGridLayout()
        self.repairs_grid_layout.addLayout(toolbar, 0, 0)
        self.repairs_grid_layout.addWidget(table, 1, 0)
        repairs_widget.setLayout(self.repairs_grid_layout)
        self.clearRepairsFilter()
        return repairs_widget

    def addRepair(self):
        dialog = AddRepairDlg(self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                new_repair = Repair(dialog.repair_name.text() if dialog.repair_name.text() != "" else None,
                                    dialog.is_planned.isChecked(),
                                    dialog.receipt_date.text() if dialog.receipt_date.text() != "" else None,
                                    dialog.start_date.text() if dialog.start_date.text() != "" else None,
                                    dialog.finish_date.text() if dialog.finish_date.text() != "" else None,
                                    dialog.responsible_id.text().split(
                                        ' ')[0] if dialog.responsible_id.text() != "" else None,
                                    dialog.equipment_id.text().split(' ')[0] if dialog.equipment_id.text() != "" else None)
                self.session = self.Session()
                self.session.add(new_repair)
                self.session.commit()
                # TODO: Убедиться, что я могу ввести некорректный id оборудования и БД это сама отловит
                self.clearRepairsFilter()
            except Exception as err:
                QMessageBox.critical(None, 'Error!', str(err))

        else:
            print('Cancelled')
            dialog.deleteLater()

    def editRepair(self):
        # TODO: Написать функцию
        pass

    def deleteRepair(self):
        # TODO: Написать функцию
        pass

    def showRepairsByFilter(self):
        # TODO: Написать функцию
        pass

    def clearRepairsFilter(self):
        cursor = self.connection.cursor()
        cursor.execute("CALL SHOW_ALL_REPAIRS()")
        data = cursor.fetchall()
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
        executeFilterBtn.setFixedWidth(FILTERS_BUTTON)
        executeFilterBtn.clicked.connect(lambda: self.showFixationsByFilter())

        clearFilterBtn = QPushButton('Clear filters')
        clearFilterBtn.setFixedWidth(FILTERS_BUTTON)
        clearFilterBtn.clicked.connect(lambda: self.clearFixationsFilter())

        controlls = QVBoxLayout(self)
        addFixationBtn = QPushButton('Add fixation', self)
        addFixationBtn.setFixedWidth(BUTTON_WIDTH)
        addFixationBtn.clicked.connect(lambda: self.addFixation())
        controlls.addWidget(addFixationBtn)

        editFixationBtn = QPushButton('Edit fixation', self)
        editFixationBtn.setFixedWidth(BUTTON_WIDTH)
        editFixationBtn.clicked.connect(lambda: self.editFixation())
        controlls.addWidget(editFixationBtn)

        delFixationBtn = QPushButton('Delete fixation', self)
        delFixationBtn.setFixedWidth(BUTTON_WIDTH)
        delFixationBtn.clicked.connect(lambda: self.deleteFixation())
        controlls.addWidget(delFixationBtn)

        filterLayout.addWidget(self.fixationsFilterColumn)
        filterLayout.addWidget(self.fixationsFilterValue)
        filterLayout.addWidget(executeFilterBtn)
        filterLayout.addWidget(clearFilterBtn)

        filter_group.setLayout(filterLayout)

        toolbar.addWidget(filter_group)
        toolbar.addLayout(controlls)

        table = createTableFromMYSQLDB(headers=self.fixations_table_headers)

        self.fixations_grid_layout = QGridLayout()
        self.fixations_grid_layout.addLayout(toolbar, 0, 0)
        self.fixations_grid_layout.addWidget(table, 1, 0)
        fixations_widget.setLayout(self.fixations_grid_layout)
        self.clearFixationsFilter()
        return fixations_widget

    def addFixation(self):
        # TODO: Написать функцию
        pass

    def editFixation(self):
        # TODO: Написать функцию
        pass

    def deleteFixation(self):
        # TODO: Написать функцию
        pass

    def showFixationsByFilter(self):
        # TODO: Написать функцию
        pass

    def clearFixationsFilter(self):
        cursor = self.connection.cursor()
        cursor.execute("CALL SHOW_ALL_FIXATIONS()")
        data = cursor.fetchall()
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
        executeFilterBtn.setFixedWidth(FILTERS_BUTTON)
        executeFilterBtn.clicked.connect(lambda: self.showPerformersByFilter())

        clearFilterBtn = QPushButton('Clear filters')
        clearFilterBtn.setFixedWidth(FILTERS_BUTTON)
        clearFilterBtn.clicked.connect(lambda: self.clearPerformersFilter())

        controlls = QVBoxLayout(self)
        addPerformerBtn = QPushButton('Add performer', self)
        addPerformerBtn.setFixedWidth(BUTTON_WIDTH)
        addPerformerBtn.clicked.connect(lambda: self.addPerformer())
        controlls.addWidget(addPerformerBtn)

        editPerformerBtn = QPushButton('Edit performer', self)
        editPerformerBtn.setFixedWidth(BUTTON_WIDTH)
        editPerformerBtn.clicked.connect(lambda: self.editPerformer())
        controlls.addWidget(editPerformerBtn)

        delPerformerBtn = QPushButton('Delete performer', self)
        delPerformerBtn.setFixedWidth(BUTTON_WIDTH)
        delPerformerBtn.clicked.connect(lambda: self.deletePerformer())
        controlls.addWidget(delPerformerBtn)

        filterLayout.addWidget(self.performersFilterColumn)
        filterLayout.addWidget(self.performersFilterValue)
        filterLayout.addWidget(executeFilterBtn)
        filterLayout.addWidget(clearFilterBtn)

        filter_group.setLayout(filterLayout)

        toolbar.addWidget(filter_group)
        toolbar.addLayout(controlls)

        table = createTableFromMYSQLDB(headers=self.performers_table_headers)

        self.performers_grid_layout = QGridLayout()
        self.performers_grid_layout.addLayout(toolbar, 0, 0)
        self.performers_grid_layout.addWidget(table, 1, 0)
        performers_widget.setLayout(self.performers_grid_layout)
        self.clearPerformersFilter()
        return performers_widget

    def addPerformer(self):
        # TODO: Написать функцию
        pass

    def editPerformer(self):
        # TODO: Написать функцию
        pass

    def deletePerformer(self):
        # TODO: Написать функцию
        pass

    def showPerformersByFilter(self):
        # TODO: Написать функцию
        pass

    def clearPerformersFilter(self):
        cursor = self.connection.cursor()
        cursor.execute("CALL SHOW_ALL_PERFORMERS()")
        data = cursor.fetchall()
        table = createTableFromMYSQLDB(
            data, self.performers_table_headers, self)
        table.resizeColumnsToContents()
        self.performers_grid_layout.addWidget(table, 1, 0)
        self.performersFilterValue.setText('')
        self.performersFilterColumn.setCurrentIndex(0)

# endregion

    def getConnection(self):

        # TODO: Инвертировать комментарии перед сдачей
        try:
            connection = MySQLdb.connect(host="localhost",
                                         user='root',
                                         passwd='',
                                         db="rmc",
                                         charset='utf8')
            engine = create_engine(
                f"mysql://root:{''}@localhost:3306/rmc?charset=utf8", echo=False)
            return (connection, engine)
        except Exception as err:
            QMessageBox.critical(None, 'Error!', str(err))
            return (None, None)

        # dialog = AuthorizationDlg(self)
        # if dialog.exec_() == QDialog.Accepted:
        #     print('Login: %s' % dialog.login.text())
        #     print('Password: %s' % dialog.passwd.text())
        #     connection = None
        #     engine = None
        #     try:
        #         connection = MySQLdb.connect(host="localhost",
        #                                      user=dialog.login.text(),
        #                                      passwd=dialog.passwd.text(),
        #                                      db="rmc",
        #                                      charset='utf8')
        #         engine = create_engine(
        #             f"mysql://{dialog.login.text()}:{dialog.passwd.text()}@localhost:3306/rmc?charset=utf8", echo=False)
        #         return (connection, engine)
        #     except Exception as err:
        #         QMessageBox.critical(None, 'Error!', str(err))
        #         return (None, None)

        # else:
        #     print('Cancelled')
        #     dialog.deleteLater()
        #     raise NoneConnectionError


if __name__ == "__main__":
    try:
        import sys
        app = QApplication(sys.argv)
        mw = MainWindow()
        mw.showMaximized()
        sys.exit(app.exec())
    except NoneConnectionError:
        print("Exit")
