from PyQt5 import uic, QtWidgets #works for pyqt5

import sys

app = QtWidgets.QApplication([])

win = uic.loadUi("climbing_ui.ui")  # specify the location of your .ui file

win.show()

sys.exit(app.exec())
