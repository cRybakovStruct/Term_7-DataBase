from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


def createTableFromPYMYSQL(table_data=None, parent=None):
    table = QTableWidget(parent)
    table.setEditTriggers(QTableWidget.NoEditTriggers)
    try:
        table.setColumnCount(len(table_data.keys()))
        table.setRowCount(len(table_data[list(table_data.keys())[0]]))
        table.setHorizontalHeaderLabels(table_data.keys())
        for col, key in enumerate(table_data.keys()):
            for row, value in enumerate(table_data[key]):
                table.setItem(row, col, QTableWidgetItem(str(value)))
        table.resizeColumnsToContents()
    except:
        table.setColumnCount(1)
        table.setRowCount(1)
        table.setItem(0, 0, QTableWidgetItem("None"))
        table.resizeColumnsToContents()
    finally:
        return table


def createTableFromMYSQLDB(table_data=None, headers=None, parent=None):
    table = QTableWidget(parent)
    table.setEditTriggers(QTableWidget.NoEditTriggers)
    try:
        table.setColumnCount(len(headers))
        table.setRowCount(len(table_data))
        table.setHorizontalHeaderLabels(headers)
        for row, record in enumerate(table_data):
            for col, value in enumerate(record):
                table.setItem(row, col, QTableWidgetItem(str(value)))
        table.resizeColumnsToContents()
    except:
        table.setColumnCount(1)
        table.setRowCount(1)
        table.setItem(0, 0, QTableWidgetItem("None"))
        table.resizeColumnsToContents()
    finally:
        return table


class NoneConnectionError(AttributeError):
    ''''''
