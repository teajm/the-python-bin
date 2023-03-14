from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSignal

import sys
import time

DM_COM_PORT = 'COM8'
SERIAL_BAUD = 115200

app = QtWidgets.QApplication(sys.argv)
window = Ui(DM_COM_PORT,SERIAL_BAUD)
app.exec()