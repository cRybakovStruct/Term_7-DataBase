from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


def createTableFromPYMYSQL(table_data=None, parent=None):
    table = QTableWidget(parent)
    table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
    try:
        table.setColumnCount(len(table_data.keys()))
        table.setRowCount(len(table_data[list(table_data.keys())[0]]))
        table.setHorizontalHeaderLabels(table_data.keys())
        for col, key in enumerate(table_data.keys()):
            for row, value in enumerate(table_data[key]):
                table.setItem(row, col, QTableWidgetItem(value))
        table.resizeColumnsToContents()
    except:
        table.setColumnCount(1)
        table.setRowCount(1)
        table.setItem(0, 0, QTableWidgetItem("None"))
        table.resizeColumnsToContents()
    finally:
        return table


def createTableFromMYSQLDB(table_data=None, parent=None):
    pass
