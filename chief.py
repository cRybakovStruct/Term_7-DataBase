import MySQLdb

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt, QObject
from PyQt5 import QtGui, QtWidgets
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QSize, Qt
import authorization
from additional_modules import *

db = MySQLdb.connect("localhost", "root", "", "rmc")
cursor = db.cursor()
cursor.execute("show tables")
data = cursor.fetchall()
print(data)
db.close()
