import MySQLdb

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, QObject
from PyQt5 import QtGui, QtWidgets
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QSize

from additional_modules import *
from dialogs import *

from classes_for_alchemy_orm import Base, Worker, Fixation
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


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

        self.connection, self.engine = self.getConnection()
        while not self.connection:
            QMessageBox.critical(
                None, "Error", "Wrong authorization parameters")
            self.connection = self.getConnection()

        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        # for instance in session.query(Worker).order_by(Worker.idworker):
        #     print(instance)

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

        controlls = QVBoxLayout(self)
        addWorkerBtn = QPushButton('Add worker', self)
        addWorkerBtn.setFixedWidth(75)
        addWorkerBtn.clicked.connect(lambda: self.addWorker())
        controlls.addWidget(addWorkerBtn)

        editWorkerBtn = QPushButton('Edit worker', self)
        editWorkerBtn.setFixedWidth(75)
        editWorkerBtn.clicked.connect(lambda: self.editWorker())
        controlls.addWidget(editWorkerBtn)

        delWorkerBtn = QPushButton('Delete worker', self)
        delWorkerBtn.setFixedWidth(75)
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
                # dialog.shop.currentText() if dialog.shop.currentText() != "" else None)
                self.session.add(new_worker)
                self.session.commit()

                if dialog.shop.currentText() != "":
                    new_fixation = Fixation(
                        new_worker.idworker, dialog.shop.currentText())
                    print(new_fixation)
                    self.session.add(new_fixation)
                    self.session.commit()

                # cursor.execute(
                #     "CALL INSERT_WORKER(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", args)
                self.clearWorkersFilter()
            except Exception as err:
                QMessageBox.critical(None, 'Error!', str(err))

        else:
            print('Cancelled')
            dialog.deleteLater()

    def editWorker(self):
        items = self.workers_table.selectedItems()
        row, res = getRow(items)
        if not res:
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

    def deleteWorker(self):
        items = self.workers_table.selectedItems()
        row, res = getRow(items)
        if not res:
            QMessageBox.critical(
                None, 'Warning!', 'Please, select cells in single row')
            return
        else:
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

    def showWorkersByFilter(self):
        col = self.workersFilterColumn.currentText()
        cursor = self.connection.cursor()
        cursor.execute("CALL FILTER_WORKERS(%s, %s)",
                       (col, self.workersFilterValue.text()))
        data = cursor.fetchall()
        # print(data)
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
        # print(data)
        self.workers_table = createTableFromMYSQLDB(
            data, self.workers_table_headers, self)
        self.workers_table.resizeColumnsToContents()
        self.workers_grid_layout.addWidget(self.workers_table, 1, 0)
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
            except Exception as err:
                QMessageBox.critical(None, 'Error!', str(err))

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
        # print(data)
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
        pass

    def showShopsByFilter(self):
        pass

    def clearShopsFilter(self):
        cursor = self.connection.cursor()
        cursor.execute("CALL SHOW_ALL_SHOPS()")
        data = cursor.fetchall()
        # print(data)
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
        pass

    def showEquipmentByFilter(self):
        pass

    def clearEquipmentFilter(self):
        cursor = self.connection.cursor()
        cursor.execute("CALL SHOW_ALL_EQUIPMENT()")
        data = cursor.fetchall()
        # print(data)
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
        pass

    def showRepairsByFilter(self):
        pass

    def clearRepairsFilter(self):
        cursor = self.connection.cursor()
        cursor.execute("CALL SHOW_ALL_REPAIRS()")
        data = cursor.fetchall()
        # print(data)
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
        pass

    def showFixationsByFilter(self):
        pass

    def clearFixationsFilter(self):
        cursor = self.connection.cursor()
        cursor.execute("CALL SHOW_ALL_FIXATIONS()")
        data = cursor.fetchall()
        # print(data)
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
        pass

    def showPerformersByFilter(self):
        pass

    def clearPerformersFilter(self):
        cursor = self.connection.cursor()
        cursor.execute("CALL SHOW_ALL_PERFORMERS()")
        data = cursor.fetchall()
        # print(data)
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
                engine = create_engine(
                    f"mysql://{dialog.login.text()}:{dialog.passwd.text()}@localhost:3306/rmc?charset=utf8", echo=False)

                return (connection, engine)
            except Exception as err:
                QMessageBox.critical(None, 'Error!', str(err))

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
