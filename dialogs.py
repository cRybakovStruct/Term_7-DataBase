from PyQt5.QtWidgets import QCalendarWidget, QCheckBox, QComboBox, QDialog, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout
from additional_modules import createTableFromMYSQLDB, getRow
# from PyQt5 import Qt

HEADERS_FOR_WORKER_SELECTION = ['idworker', 'surname', 'name', 'fathername']
HEADERS_FOR_EQUIPMENT_SELECTION = ['serial_number', 'model', 'placement']
HEADERS_FOR_MACHINE_SELECTION = ['model', 'eq_type', 'firm']
BUTTON_FOR_ADDITIONAL_SELECTION_WIDTH = 25


class GetDateDlg(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle('Выбрать дату')
        self.layout = QVBoxLayout(self)
        self.hbox_layout = QHBoxLayout()
        self.ok_button = QPushButton('Ok', self)
        self.ok_button.clicked.connect(self.accept)
        self.hbox_layout.addWidget(self.ok_button)
        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
        self.hbox_layout.addWidget(self.cancel_button)
        self.date = QCalendarWidget()
        self.layout.addWidget(self.date)
        self.layout.addLayout(self.hbox_layout)


class AuthorizationDlg(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle('Авторизация')
        self.layout = QVBoxLayout(self)

        self.hbox_layout = QHBoxLayout()
        self.ok_button = QPushButton('Ok', self)
        self.ok_button.clicked.connect(self.accept)
        self.hbox_layout.addWidget(self.ok_button)
        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
        self.hbox_layout.addWidget(self.cancel_button)

        self.layout.addWidget(QLabel("Логин*"))
        self.login = QLineEdit(self)
        self.layout.addWidget(self.login)
        self.layout.addWidget(QLabel("Пароль"))
        self.passwd = QLineEdit(self)
        self.layout.addWidget(self.passwd)
        self.layout.addLayout(self.hbox_layout)


class AddWorkerDlg(QDialog):
    def __init__(self, shops=None, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle('Добавить работника')
        self.shops = shops
        self.layout = QVBoxLayout(self)

        self.hbox_layout = QHBoxLayout()
        self.ok_button = QPushButton('Ok', self)
        self.ok_button.clicked.connect(self.accept)
        self.hbox_layout.addWidget(self.ok_button)
        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
        self.hbox_layout.addWidget(self.cancel_button)

        self.surname = QLineEdit(self)
        self.__createInputField__('Фамилия*', self.surname)

        self.name = QLineEdit(self)
        self.__createInputField__('Имя*', self.name)

        self.fathername = QLineEdit(self)
        self.__createInputField__('Отчество', self.fathername)

        self.education = QLineEdit(self)
        self.__createInputField__('Образование', self.education)

        self.town = QLineEdit(self)
        self.__createInputField__('Город', self.town)

        self.address = QLineEdit(self)
        self.__createInputField__('Адрес', self.address)

        self.phonenumber = QLineEdit(self)
        self.__createInputField__('Номер телефона', self.phonenumber)

        self.birthday = QLineEdit(self)
        self.birth_btn = QPushButton('•••', self)
        self.birth_btn.setFixedWidth(BUTTON_FOR_ADDITIONAL_SELECTION_WIDTH)
        self.birth_btn.clicked.connect(lambda: self.addBirthDate())
        tmp_layout = QHBoxLayout(self)
        tmp_layout.addWidget(self.__createLabel__('Дата рождения*'))
        tmp_layout.addWidget(self.birthday)
        tmp_layout.addWidget(self.birth_btn)
        self.layout.addLayout(tmp_layout)

        self.employ_date = QLineEdit(self)
        self.employ_btn = QPushButton('•••', self)
        self.employ_btn.setFixedWidth(BUTTON_FOR_ADDITIONAL_SELECTION_WIDTH)
        self.employ_btn.clicked.connect(lambda: self.addEmployDate())
        tmp_layout = QHBoxLayout(self)
        tmp_layout.addWidget(self.__createLabel__('Дата приёма на работу*'))
        tmp_layout.addWidget(self.employ_date)
        tmp_layout.addWidget(self.employ_btn)
        self.layout.addLayout(tmp_layout)

        self.salary = QLineEdit(self)
        self.__createInputField__('Зар. плата*', self.salary)

        self.position = QLineEdit(self)
        self.__createInputField__('Должность*', self.position)

        self.category = QLineEdit(self)
        self.__createInputField__('Разряд*', self.category)

        self.shop = QComboBox(self)
        self.shop.addItems(self.shops)
        self.__createInputField__('Цех', self.shop)

        self.unemploy_date = QLineEdit(self)
        self.unemploy_btn = QPushButton('•••', self)
        self.unemploy_btn.setFixedWidth(BUTTON_FOR_ADDITIONAL_SELECTION_WIDTH)
        self.unemploy_btn.clicked.connect(lambda: self.addUnemployDate())
        tmp_layout = QHBoxLayout(self)
        tmp_layout.addWidget(self.__createLabel__('Дата увольнения'))
        tmp_layout.addWidget(self.unemploy_date)
        tmp_layout.addWidget(self.unemploy_btn)
        self.layout.addLayout(tmp_layout)

        self.layout.addLayout(self.hbox_layout)

    # Qt.AlignVCenter | Qt.AlignRight):
    def __createLabel__(self, text, alignment=None):
        label = QLabel(text)
        label.setFixedSize(150, 20)
        # label.setAlignment(alignment)
        return label

    def __createInputField__(self, label_text, line_edit):
        tmp_layout = QHBoxLayout(self)
        tmp_layout.addWidget(self.__createLabel__(label_text))
        tmp_layout.addWidget(line_edit)
        self.layout.addLayout(tmp_layout)

    def addBirthDate(self):
        dialog = GetDateDlg(self)
        if dialog.exec_() == QDialog.Accepted:
            tmp = dialog.date.selectedDate().toString("yyyy.MM.dd")
            self.birthday.setText(str(tmp))

    def addEmployDate(self):
        dialog = GetDateDlg(self)
        if dialog.exec_() == QDialog.Accepted:
            tmp = dialog.date.selectedDate().toString("yyyy.MM.dd")
            self.employ_date.setText(str(tmp))

    def addUnemployDate(self):
        dialog = GetDateDlg(self)
        if dialog.exec_() == QDialog.Accepted:
            tmp = dialog.date.selectedDate().toString("yyyy.MM.dd")
            self.unemploy_date.setText(str(tmp))


class EditWorkerDlg(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle('Отредактировать работника')
        self.layout = QVBoxLayout(self)

        self.hbox_layout = QHBoxLayout()
        self.ok_button = QPushButton('Ok', self)
        self.ok_button.clicked.connect(self.accept)
        self.hbox_layout.addWidget(self.ok_button)
        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
        self.hbox_layout.addWidget(self.cancel_button)

        self.surname = QLineEdit(self)
        self.__createInputField__('Фамилия*', self.surname)

        self.name = QLineEdit(self)
        self.__createInputField__('Имя*', self.name)

        self.fathername = QLineEdit(self)
        self.__createInputField__('Отчество', self.fathername)

        self.education = QLineEdit(self)
        self.__createInputField__('Образование', self.education)

        self.town = QLineEdit(self)
        self.__createInputField__('Город', self.town)

        self.address = QLineEdit(self)
        self.__createInputField__('Адрес', self.address)

        self.phonenumber = QLineEdit(self)
        self.__createInputField__('Номер телефона', self.phonenumber)

        self.birthday = QLineEdit(self)
        self.birth_btn = QPushButton('•••', self)
        self.birth_btn.setFixedWidth(BUTTON_FOR_ADDITIONAL_SELECTION_WIDTH)
        self.birth_btn.clicked.connect(lambda: self.addBirthDate())
        tmp_layout = QHBoxLayout(self)
        tmp_layout.addWidget(self.__createLabel__('Дата рождения'))
        tmp_layout.addWidget(self.birthday)
        tmp_layout.addWidget(self.birth_btn)
        self.layout.addLayout(tmp_layout)

        self.employ_date = QLineEdit(self)
        self.employ_btn = QPushButton('•••', self)
        self.employ_btn.setFixedWidth(BUTTON_FOR_ADDITIONAL_SELECTION_WIDTH)
        self.employ_btn.clicked.connect(lambda: self.addEmployDate())
        tmp_layout = QHBoxLayout(self)
        tmp_layout.addWidget(self.__createLabel__('Дата приёма на работу*'))
        tmp_layout.addWidget(self.employ_date)
        tmp_layout.addWidget(self.employ_btn)
        self.layout.addLayout(tmp_layout)

        self.salary = QLineEdit(self)
        self.__createInputField__('Зар. плата*', self.salary)

        self.position = QLineEdit(self)
        self.__createInputField__('Должность*', self.position)

        self.category = QLineEdit(self)
        self.__createInputField__('Разряд*', self.category)

        self.unemploy_date = QLineEdit(self)
        self.unemploy_btn = QPushButton('•••', self)
        self.unemploy_btn.setFixedWidth(BUTTON_FOR_ADDITIONAL_SELECTION_WIDTH)
        self.unemploy_btn.clicked.connect(lambda: self.addUnemployDate())
        tmp_layout = QHBoxLayout(self)
        tmp_layout.addWidget(self.__createLabel__('Дата увольнения'))
        tmp_layout.addWidget(self.unemploy_date)
        tmp_layout.addWidget(self.unemploy_btn)
        self.layout.addLayout(tmp_layout)

        self.layout.addLayout(self.hbox_layout)

    # Qt.AlignVCenter | Qt.AlignRight):
    def __createLabel__(self, text, alignment=None):
        label = QLabel(text)
        label.setFixedSize(150, 20)
        # label.setAlignment(alignment)
        return label

    def __createInputField__(self, label_text, line_edit):
        tmp_layout = QHBoxLayout(self)
        tmp_layout.addWidget(self.__createLabel__(label_text))
        tmp_layout.addWidget(line_edit)
        self.layout.addLayout(tmp_layout)

    def addBirthDate(self):
        dialog = GetDateDlg(self)
        if dialog.exec_() == QDialog.Accepted:
            tmp = dialog.date.selectedDate().toString("yyyy.MM.dd")
            self.birthday.setText(str(tmp))

    def addEmployDate(self):
        dialog = GetDateDlg(self)
        if dialog.exec_() == QDialog.Accepted:
            tmp = dialog.date.selectedDate().toString("yyyy.MM.dd")
            self.employ_date.setText(str(tmp))

    def addUnemployDate(self):
        dialog = GetDateDlg(self)
        if dialog.exec_() == QDialog.Accepted:
            tmp = dialog.date.selectedDate().toString("yyyy.MM.dd")
            self.unemploy_date.setText(str(tmp))


class AddMachineDlg(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle('Добавить станок')
        self.layout = QVBoxLayout(self)

        self.hbox_layout = QHBoxLayout()

        self.ok_button = QPushButton('Ok', self)
        self.ok_button.clicked.connect(self.accept)
        self.hbox_layout.addWidget(self.ok_button)

        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
        self.hbox_layout.addWidget(self.cancel_button)

        self.model = QLineEdit(self)
        self.__createInputField__('Модель*', self.model)

        self.type = QLineEdit(self)
        self.__createInputField__('Тип*', self.type)

        self.length = QLineEdit(self)
        self.__createInputField__('Длина*', self.length)

        self.width = QLineEdit(self)
        self.__createInputField__('Ширина*', self.width)

        self.height = QLineEdit(self)
        self.__createInputField__('Высота*', self.height)

        self.weight = QLineEdit(self)
        self.__createInputField__('Вес*', self.weight)

        self.power = QLineEdit(self)
        self.__createInputField__('Мощность*', self.power)

        self.detail_length = QLineEdit(self)
        self.__createInputField__('Макс. длина заготовки', self.detail_length)

        self.detail_width = QLineEdit(self)
        self.__createInputField__(
            'Ширина/диаметр заготовки', self.detail_width)

        self.detail_thickness = QLineEdit(self)
        self.__createInputField__('Толщина заготовки', self.detail_thickness)

        self.tools = QLineEdit(self)
        self.__createInputField__('Инструмент', self.tools)

        self.manufacturer = QLineEdit(self)
        self.__createInputField__('Страна-производитель', self.manufacturer)

        self.firm = QLineEdit(self)
        self.__createInputField__('Фирма-производитель', self.firm)

        self.contact = QLineEdit(self)
        self.__createInputField__('Контакт фирмы', self.contact)

        self.comments = QLineEdit(self)
        self.__createInputField__('Комментарий', self.comments)

        self.layout.addLayout(self.hbox_layout)

    # Qt.AlignVCenter | Qt.AlignRight):
    def __createLabel__(self, text, alignment=None):
        label = QLabel(text)
        label.setFixedSize(150, 20)
        # label.setAlignment(alignment)
        return label

    def __createInputField__(self, label_text, line_edit):
        tmp_layout = QHBoxLayout(self)
        tmp_layout.addWidget(self.__createLabel__(label_text))
        tmp_layout.addWidget(line_edit)
        self.layout.addLayout(tmp_layout)


class AddShopDlg(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.parent = parent
        self.setWindowTitle('Добавить цех')
        self.layout = QVBoxLayout(self)

        self.hbox_layout = QHBoxLayout()

        self.ok_button = QPushButton('Ok', self)
        self.ok_button.clicked.connect(self.accept)
        self.hbox_layout.addWidget(self.ok_button)

        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
        self.hbox_layout.addWidget(self.cancel_button)

        self.idshop = QLineEdit(self)
        self.__createInputField__(
            'Наименование цеха (Именит. падеж)*', self.idshop)

        self.chief_IP = QLineEdit(self)
        self.__createInputField__(
            'Фамилия начальника цеха (Именит. падеж)*', self.chief_IP)

        self.chief_RP = QLineEdit(self)
        self.__createInputField__(
            'Фамилия начальника цеха (Родит. падеж)*', self.chief_RP)

        self.chief_DP = QLineEdit(self)
        self.__createInputField__(
            'Фамилия начальника цеха (Дат. падеж)*', self.chief_DP)

        self.chief_VP = QLineEdit(self)
        self.__createInputField__(
            'Фамилия начальника цеха (Винит. падеж)*', self.chief_VP)

        self.chief_TP = QLineEdit(self)
        self.__createInputField__(
            'Фамилия начальника цеха (Творит. падеж)*', self.chief_TP)

        self.chief_PP = QLineEdit(self)
        self.__createInputField__(
            'Фамилия начальника цеха (Предл. падеж)*', self.chief_PP)

        self.idshop_RP = QLineEdit(self)
        self.__createInputField__(
            'Наименование цеха (Родит. падеж)*', self.idshop_RP)

        self.layout.addLayout(self.hbox_layout)

    def __createLabel__(self, text, alignment=None):
        label = QLabel(text)
        label.setFixedSize(230, 20)
        return label

    def __createInputField__(self, label_text, line_edit):
        tmp_layout = QHBoxLayout(self)
        tmp_layout.addWidget(self.__createLabel__(label_text))
        tmp_layout.addWidget(line_edit)
        self.layout.addLayout(tmp_layout)


class AddEquipmentDlg(QDialog):
    def __init__(self, shops=None, parent=None):
        QDialog.__init__(self, parent)
        self.parent = parent
        self.setWindowTitle('Добавить станок')
        self.shops = shops
        self.layout = QVBoxLayout(self)

        self.hbox_layout = QHBoxLayout()
        self.ok_button = QPushButton('Ok', self)
        self.ok_button.clicked.connect(self.accept)
        self.hbox_layout.addWidget(self.ok_button)
        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
        self.hbox_layout.addWidget(self.cancel_button)

        self.model = QLineEdit(self)
        self.model_btn = QPushButton('•••', self)
        self.model_btn.setFixedWidth(BUTTON_FOR_ADDITIONAL_SELECTION_WIDTH)
        self.model_btn.clicked.connect(lambda: self.add_machine_id())
        tmp_layout = QHBoxLayout(self)
        tmp_layout.addWidget(self.__createLabel__('Модель*'))
        tmp_layout.addWidget(self.model)
        tmp_layout.addWidget(self.model_btn)
        self.layout.addLayout(tmp_layout)

        self.creation_year = QLineEdit(self)
        self.__createInputField__('Год выпуска*', self.creation_year)

        self.serial_number = QLineEdit(self)
        self.__createInputField__('Серийный номер*', self.serial_number)

        self.placement = QComboBox(self)
        self.placement.addItems(self.shops)
        self.__createInputField__('Расположение*', self.placement)

        self.start_using_date = QLineEdit(self)
        self.start_using_date_btn = QPushButton('•••', self)
        self.start_using_date_btn.setFixedWidth(
            BUTTON_FOR_ADDITIONAL_SELECTION_WIDTH)
        self.start_using_date_btn.clicked.connect(
            lambda: self.addStartUsingDate())
        tmp_layout = QHBoxLayout(self)
        tmp_layout.addWidget(self.__createLabel__('Дата ввода в эксплуатацию'))
        tmp_layout.addWidget(self.start_using_date)
        tmp_layout.addWidget(self.start_using_date_btn)
        self.layout.addLayout(tmp_layout)

        self.comments = QLineEdit(self)
        self.__createInputField__('Комментарии', self.comments)

        self.layout.addLayout(self.hbox_layout)

    # Qt.AlignVCenter | Qt.AlignRight):
    def __createLabel__(self, text, alignment=None):
        label = QLabel(text)
        label.setFixedSize(150, 20)
        # label.setAlignment(alignment)
        return label

    def __createInputField__(self, label_text, line_edit):
        tmp_layout = QHBoxLayout(self)
        tmp_layout.addWidget(self.__createLabel__(label_text))
        tmp_layout.addWidget(line_edit)
        self.layout.addLayout(tmp_layout)

    def addStartUsingDate(self):
        dialog = GetDateDlg(self)
        if dialog.exec_() == QDialog.Accepted:
            tmp = dialog.date.selectedDate().toString("yyyy.MM.dd")
            self.start_using_date.setText(str(tmp))

    def add_machine_id(self):
        dialog = SelectMachineDlg(self.parent)
        if dialog.exec_() == QDialog.Accepted:
            try:
                items = dialog.table.selectedItems()
                row, res = getRow(items)
                if (not res) or (row is None):
                    QMessageBox.critical(
                        None, 'Warning!', 'Please, select cells in single row')
                    return
                else:
                    self.model.setText(dialog.table.item(row, 0).text())
            except Exception as err:
                QMessageBox.critical(None, 'Error!', str(err))


class AddRepairDlg(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.parent = parent
        self.setWindowTitle('Добавить ремонт')
        self.layout = QVBoxLayout(self)

        self.hbox_layout = QHBoxLayout()

        self.ok_button = QPushButton('Ok', self)
        self.ok_button.clicked.connect(self.accept)
        self.hbox_layout.addWidget(self.ok_button)

        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
        self.hbox_layout.addWidget(self.cancel_button)

        self.repair_name = QLineEdit(self)
        self.__createInputField__('Наименование ремонта*', self.repair_name)

        self.is_planned = QCheckBox('(Да/Нет)')
        self.__createInputField__('Запланированный ремонт*', self.is_planned)

        self.receipt_date = QLineEdit(self)
        self.receipt_btn = QPushButton('•••', self)
        self.receipt_btn.setFixedWidth(BUTTON_FOR_ADDITIONAL_SELECTION_WIDTH)
        self.receipt_btn.clicked.connect(lambda: self.add_receipt_date())
        tmp_layout = QHBoxLayout(self)
        tmp_layout.addWidget(self.__createLabel__(
            'Дата поступления в ремонт*'))
        tmp_layout.addWidget(self.receipt_date)
        tmp_layout.addWidget(self.receipt_btn)
        self.layout.addLayout(tmp_layout)

        self.start_date = QLineEdit(self)
        self.start_btn = QPushButton('•••', self)
        self.start_btn.setFixedWidth(BUTTON_FOR_ADDITIONAL_SELECTION_WIDTH)
        self.start_btn.clicked.connect(lambda: self.add_start_date())
        tmp_layout = QHBoxLayout(self)
        tmp_layout.addWidget(self.__createLabel__('Дата начала ремонта*'))
        tmp_layout.addWidget(self.start_date)
        tmp_layout.addWidget(self.start_btn)
        self.layout.addLayout(tmp_layout)

        self.finish_date = QLineEdit(self)
        self.finish_btn = QPushButton('•••', self)
        self.finish_btn.setFixedWidth(BUTTON_FOR_ADDITIONAL_SELECTION_WIDTH)
        self.finish_btn.clicked.connect(lambda: self.add_finish_date())
        tmp_layout = QHBoxLayout(self)
        tmp_layout.addWidget(self.__createLabel__('Дата окончания ремонта'))
        tmp_layout.addWidget(self.finish_date)
        tmp_layout.addWidget(self.finish_btn)
        self.layout.addLayout(tmp_layout)

        self.responsible_id = QLineEdit(self)
        self.responsible_btn = QPushButton('•••', self)
        self.responsible_btn.setFixedWidth(
            BUTTON_FOR_ADDITIONAL_SELECTION_WIDTH)
        self.responsible_btn.clicked.connect(lambda: self.add_responsible_id())
        tmp_layout = QHBoxLayout(self)
        tmp_layout.addWidget(self.__createLabel__('Ответственный за ремонт*'))
        tmp_layout.addWidget(self.responsible_id)
        tmp_layout.addWidget(self.responsible_btn)
        self.layout.addLayout(tmp_layout)

        self.equipment_id = QLineEdit(self)
        self.equipment_btn = QPushButton('•••', self)
        self.equipment_btn.setFixedWidth(BUTTON_FOR_ADDITIONAL_SELECTION_WIDTH)
        self.equipment_btn.clicked.connect(lambda: self.add_equipment_id())
        tmp_layout = QHBoxLayout(self)
        tmp_layout.addWidget(self.__createLabel__('Ремонтируемый станок*'))
        tmp_layout.addWidget(self.equipment_id)
        tmp_layout.addWidget(self.equipment_btn)
        self.layout.addLayout(tmp_layout)

        self.layout.addLayout(self.hbox_layout)

    def __createLabel__(self, text, alignment=None):
        label = QLabel(text)
        label.setFixedSize(150, 20)
        return label

    def __createInputField__(self, label_text, line_edit):
        tmp_layout = QHBoxLayout(self)
        tmp_layout.addWidget(self.__createLabel__(label_text))
        tmp_layout.addWidget(line_edit)
        self.layout.addLayout(tmp_layout)

    def add_receipt_date(self):
        dialog = GetDateDlg(self)
        if dialog.exec_() == QDialog.Accepted:
            tmp = dialog.date.selectedDate().toString("yyyy.MM.dd")
            self.receipt_date.setText(str(tmp))

    def add_start_date(self):
        dialog = GetDateDlg(self)
        if dialog.exec_() == QDialog.Accepted:
            tmp = dialog.date.selectedDate().toString("yyyy.MM.dd")
            self.start_date.setText(str(tmp))

    def add_finish_date(self):
        dialog = GetDateDlg(self)
        if dialog.exec_() == QDialog.Accepted:
            tmp = dialog.date.selectedDate().toString("yyyy.MM.dd")
            self.finish_date.setText(str(tmp))

    def add_responsible_id(self):
        dialog = SelectWorkerDlg(self.parent)
        if dialog.exec_() == QDialog.Accepted:
            try:
                items = dialog.table.selectedItems()
                row, res = getRow(items)
                if (not res) or (row is None):
                    QMessageBox.critical(
                        None, 'Warning!', 'Please, select cells in single row')
                    return
                else:
                    self.responsible_id.setText(
                        f'{dialog.table.item(row, 0).text()} {dialog.table.item(row, 1).text()} {dialog.table.item(row, 2).text()}')
            except Exception as err:
                QMessageBox.critical(None, 'Error!', str(err))

    def add_equipment_id(self):
        dialog = SelectEquipmentDlg(self.parent)
        if dialog.exec_() == QDialog.Accepted:
            try:
                items = dialog.table.selectedItems()
                row, res = getRow(items)
                if (not res) or (row is None):
                    QMessageBox.critical(
                        None, 'Warning!', 'Please, select cells in single row')
                    return
                else:
                    self.equipment_id.setText(
                        f'{dialog.table.item(row, 0).text()} {dialog.table.item(row, 1).text()} {dialog.table.item(row, 2).text()}')
            except Exception as err:
                QMessageBox.critical(None, 'Error!', str(err))

# TODO: Добавить диалог на создание закрепления


class AddFixationDlg(QDialog):
    def __init__(self, shops=None, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle('Добавить закрепление')
        self.parent = parent
        self.shops = shops
        self.layout = QVBoxLayout(self)

        self.hbox_layout = QHBoxLayout()
        self.ok_button = QPushButton('Ok', self)
        self.ok_button.clicked.connect(self.accept)
        self.hbox_layout.addWidget(self.ok_button)
        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
        self.hbox_layout.addWidget(self.cancel_button)

        self.worker_id = QLineEdit(self)
        self.worker_btn = QPushButton('•••', self)
        self.worker_btn.setFixedWidth(
            BUTTON_FOR_ADDITIONAL_SELECTION_WIDTH)
        self.worker_btn.clicked.connect(lambda: self.add_worker_id())
        tmp_layout = QHBoxLayout(self)
        tmp_layout.addWidget(self.__createLabel__('Сотрудник*'))
        tmp_layout.addWidget(self.worker_id)
        tmp_layout.addWidget(self.worker_btn)
        self.layout.addLayout(tmp_layout)

        self.shop = QComboBox(self)
        self.shop.addItems(self.shops)
        self.__createInputField__('Цех*', self.shop)

        self.layout.addLayout(self.hbox_layout)

    # Qt.AlignVCenter | Qt.AlignRight):
    def __createLabel__(self, text, alignment=None):
        label = QLabel(text)
        label.setFixedSize(150, 20)
        # label.setAlignment(alignment)
        return label

    def __createInputField__(self, label_text, line_edit):
        tmp_layout = QHBoxLayout(self)
        tmp_layout.addWidget(self.__createLabel__(label_text))
        tmp_layout.addWidget(line_edit)
        self.layout.addLayout(tmp_layout)

    def add_worker_id(self):
        dialog = SelectWorkerDlg(self.parent)
        if dialog.exec_() == QDialog.Accepted:
            try:
                items = dialog.table.selectedItems()
                row, res = getRow(items)
                if (not res) or (row is None):
                    QMessageBox.critical(
                        None, 'Warning!', 'Please, select cells in single row')
                    return
                else:
                    self.worker_id.setText(
                        f'{dialog.table.item(row, 0).text()} {dialog.table.item(row, 1).text()} {dialog.table.item(row, 2).text()}')
            except Exception as err:
                QMessageBox.critical(None, 'Error!', str(err))

# TODO: Добавить диалог на создание исполнителя


class YesNoDlg(QDialog):
    def __init__(self, title, message, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle(title)
        self.layout = QVBoxLayout(self)

        msg = QLabel(message)
        msg.setWordWrap(True)
        self.layout.addWidget(msg)

        self.hbox_layout = QHBoxLayout()
        self.ok_button = QPushButton('Да', self)
        self.ok_button.clicked.connect(self.accept)
        self.hbox_layout.addWidget(self.ok_button)
        self.cancel_button = QPushButton('Нет', self)
        self.cancel_button.clicked.connect(self.reject)
        self.hbox_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.hbox_layout)


class SelectWorkerDlg(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.setWindowTitle('Выберите работника')
        self.layout = QVBoxLayout(self)

        cursor = parent.connection.cursor()
        cursor.execute("CALL GET_WORKERS_FOR_SELECTION()")
        data = cursor.fetchall()

        self.table = createTableFromMYSQLDB(
            data, HEADERS_FOR_WORKER_SELECTION, self)
        self.table.resizeColumnsToContents()
        self.layout.addWidget(self.table)

        self.hbox_layout = QHBoxLayout()
        self.ok_button = QPushButton('Ок', self)
        self.ok_button.clicked.connect(self.accept)
        self.hbox_layout.addWidget(self.ok_button)
        self.cancel_button = QPushButton('Отмена', self)
        self.cancel_button.clicked.connect(self.reject)
        self.hbox_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.hbox_layout)


class SelectEquipmentDlg(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.setWindowTitle('Выберите станок')
        self.layout = QVBoxLayout(self)

        cursor = parent.connection.cursor()
        cursor.execute("CALL GET_EQUIPMENT_FOR_SELECTION()")
        data = cursor.fetchall()

        self.table = createTableFromMYSQLDB(
            data, HEADERS_FOR_EQUIPMENT_SELECTION, self)
        self.table.resizeColumnsToContents()
        self.layout.addWidget(self.table)

        self.hbox_layout = QHBoxLayout()
        self.ok_button = QPushButton('Ок', self)
        self.ok_button.clicked.connect(self.accept)
        self.hbox_layout.addWidget(self.ok_button)
        self.cancel_button = QPushButton('Отмена', self)
        self.cancel_button.clicked.connect(self.reject)
        self.hbox_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.hbox_layout)


class SelectMachineDlg(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.setWindowTitle('Выберите станок')
        self.layout = QVBoxLayout(self)

        cursor = parent.connection.cursor()
        cursor.execute("CALL GET_MACHINE_FOR_SELECTION()")
        data = cursor.fetchall()

        self.table = createTableFromMYSQLDB(
            data, HEADERS_FOR_MACHINE_SELECTION, self)
        self.table.resizeColumnsToContents()
        self.layout.addWidget(self.table)

        self.hbox_layout = QHBoxLayout()
        self.ok_button = QPushButton('Ок', self)
        self.ok_button.clicked.connect(self.accept)
        self.hbox_layout.addWidget(self.ok_button)
        self.cancel_button = QPushButton('Отмена', self)
        self.cancel_button.clicked.connect(self.reject)
        self.hbox_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.hbox_layout)
