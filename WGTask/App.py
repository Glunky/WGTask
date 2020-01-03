import sys

from Model import Model
from View import View
from Controller import Controller

from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Архитектура по паттерну MVC 
    model = Model()
    controller = Controller(model)
    view = View(model, controller)

    view.show()

    sys.exit(app.exec_())