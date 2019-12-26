from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QMainWindow, QMessageBox, QTabWidget, QWidget
from PyQt5.QtCore import QSize
import sys
from additional_modules import AuthorizationDlg, NoneConnectionError

from classes_for_alchemy_orm import Base, Worker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.connection = self.getConnection()
        while not self.connection:
            QMessageBox.critical(
                None, "Error", "Wrong authorization parameters")
            self.connection = self.getConnection()

        # self.connection.autocommit(True)
        self.createWindow()

    def createWindow(self):
        self.setMinimumSize(QSize(480, 80))
        self.setWindowTitle("others")
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.grid_layout = QGridLayout()
        self.tab_widget = self.createMainTabWidget()
        self.grid_layout.addWidget(self.tab_widget, 0, 0)
        central_widget.setLayout(self.grid_layout)

    def createMainTabWidget(self):
        tab_widget = QTabWidget(self)
        # TODO: Придумать, что сюда добавить
        return tab_widget

    def getConnection(self):

        dialog = AuthorizationDlg(self)
        if dialog.exec_() == QDialog.Accepted:
            print('Login: %s' % dialog.login.text())
            print('Password: %s' % dialog.passwd.text())
            try:
                engine = create_engine(
                    f"mysql://{dialog.login.text()}:{dialog.passwd.text()}@localhost:3306/rmc", echo=False)
                Base.metadata.create_all(engine)
                Session = sessionmaker(bind=engine)
                session = Session()
                for instance in session.query(Worker).order_by(Worker.idworker):
                    print(instance)
                return engine
            except Exception as err:
                print(err)
                return

        else:
            print('Cancelled')
            dialog.deleteLater()
            raise NoneConnectionError


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        mw = MainWindow()
        mw.showMaximized()
        sys.exit(app.exec())
    except NoneConnectionError:
        print("Exit")
