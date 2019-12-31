import sys

from Model import Model
from View import View
from Controller import Controller

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":

    app = QApplication(sys.argv)
    model = Model()
    controller = Controller(model)
    main_window = View(model, controller)
    main_window.show()
    sys.exit(app.exec_())