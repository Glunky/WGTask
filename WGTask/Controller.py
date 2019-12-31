from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget

class Controller(QWidget):

    createRectangle = pyqtSignal(QPoint, int, int)
    def __init__(self, model):
        super(Controller, self).__init__()
        self.model = model


        self.createRectangle.connect(model.addNewRect)

    #def mouseMoveEvent(self, e):
        #self.dragRect.emit(e.pos().x(), e.pos().y())
        #super(Controller, self).mousePressEvent(e)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton and \
            self.model.isEnoughSpaceToCreateRect(event.pos(), self.model.rectWidth, self.model.rectHeight):

            self.createRectangle.emit(event.pos(), self.model.rectWidth, self.model.rectHeight)
            #self.model.addNewRect(event.pos(), self.model.rectWidth, self.model.rectHeight)

        self.update()


