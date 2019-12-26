from PyQt5.QtWidgets import QCalendarWidget, QComboBox, QDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout


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

        self.layout.addWidget(QLabel("Логин"))
        self.login = QLineEdit(self)
        self.layout.addWidget(self.login)
        self.layout.addWidget(QLabel("Пароль (можно без пароля)"))
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
        self.__createInputField__('Фамилия', self.surname)

        self.name = QLineEdit(self)
        self.__createInputField__('Имя', self.name)

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
        self.birth_btn.setFixedWidth(25)
        self.birth_btn.clicked.connect(lambda: self.add_birth_date())
        tmp_layout = QHBoxLayout(self)
        tmp_layout.addWidget(self.__createLabel__('Дата рождения'))
        tmp_layout.addWidget(self.birthday)
        tmp_layout.addWidget(self.birth_btn)
        self.layout.addLayout(tmp_layout)

        self.employ_date = QLineEdit(self)
        self.empl_btn = QPushButton('•••', self)
        self.empl_btn.setFixedWidth(25)
        self.empl_btn.clicked.connect(lambda: self.add_empl_date())
        tmp_layout = QHBoxLayout(self)
        tmp_layout.addWidget(self.__createLabel__('Дата приёма на работу'))
        tmp_layout.addWidget(self.employ_date)
        tmp_layout.addWidget(self.empl_btn)
        self.layout.addLayout(tmp_layout)

        self.salary = QLineEdit(self)
        self.__createInputField__('Зар. плата', self.salary)

        self.position = QLineEdit(self)
        self.__createInputField__('Должность', self.position)

        self.category = QLineEdit(self)
        self.__createInputField__('Разряд', self.category)

        self.shop = QComboBox(self)
        self.shop.addItems(self.shops)
        self.__createInputField__('Цех', self.shop)

        self.unemploy_date = QLineEdit(self)
        self.unempl_btn = QPushButton('•••', self)
        self.unempl_btn.setFixedWidth(25)
        self.unempl_btn.clicked.connect(lambda: self.add_unempl_date())
        tmp_layout = QHBoxLayout(self)
        tmp_layout.addWidget(self.__createLabel__('Дата увольнения'))
        tmp_layout.addWidget(self.unemploy_date)
        tmp_layout.addWidget(self.unempl_btn)
        self.layout.addLayout(tmp_layout)

        self.layout.addLayout(self.hbox_layout)

    def __createLabel__(self, text, alignment=Qt.AlignVCenter | Qt.AlignRight):
        label = QLabel(text)
        label.setFixedSize(150, 20)
        label.setAlignment(alignment)
        return label

    def __createInputField__(self, label_text, line_edit):
        tmp_layout = QHBoxLayout(self)
        tmp_layout.addWidget(self.__createLabel__(label_text))
        tmp_layout.addWidget(line_edit)
        self.layout.addLayout(tmp_layout)

    def add_birth_date(self):
        dialog = GetDateDlg(self)
        if dialog.exec_() == QDialog.Accepted:
            tmp = dialog.date.selectedDate().toString("yyyy.MM.dd")
            self.birthday.setText(str(tmp))

    def add_empl_date(self):
        dialog = GetDateDlg(self)
        if dialog.exec_() == QDialog.Accepted:
            tmp = dialog.date.selectedDate().toString("yyyy.MM.dd")
            self.employ_date.setText(str(tmp))

    def add_unempl_date(self):
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
        self.__createInputField__('Модель', self.model)

        self.type = QLineEdit(self)
        self.__createInputField__('Тип', self.type)

        self.lenght = QLineEdit(self)
        self.__createInputField__('Длина', self.lenght)

        self.width = QLineEdit(self)
        self.__createInputField__('Ширина', self.width)

        self.height = QLineEdit(self)
        self.__createInputField__('Высота', self.height)

        self.weight = QLineEdit(self)
        self.__createInputField__('Вес', self.weight)

        self.power = QLineEdit(self)
        self.__createInputField__('Мощность', self.power)

        self.detail_lenght = QLineEdit(self)
        self.__createInputField__('Макс. длина заготовки', self.detail_lenght)

        self.detail_width = QLineEdit(self)
        self.__createInputField__(
            'Ширина/диаметр заготовки', self.detail_width)

        self.detail_thickness = QLineEdit(self)
        self.__createInputField__('Толщина заготовки', self.detail_thickness)

        self.tools = QLineEdit(self)
        self.__createInputField__('Инструмент', self.tools)

        self.manufactorer = QLineEdit(self)
        self.__createInputField__('Страна-производитель', self.manufactorer)

        self.firm = QLineEdit(self)
        self.__createInputField__('Фирма-производитель', self.firm)

        self.contact = QLineEdit(self)
        self.__createInputField__('Контакт фирмы', self.contact)

        self.comments = QLineEdit(self)
        self.__createInputField__('Комментарий', self.comments)

        self.layout.addLayout(self.hbox_layout)

    def __createLabel__(self, text, alignment=Qt.AlignVCenter | Qt.AlignRight):
        label = QLabel(text)
        label.setFixedSize(150, 20)
        label.setAlignment(alignment)
        return label

    def __createInputField__(self, label_text, line_edit):
        tmp_layout = QHBoxLayout(self)
        tmp_layout.addWidget(self.__createLabel__(label_text))
        tmp_layout.addWidget(line_edit)
        self.layout.addLayout(tmp_layout)
