from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtGui import QIcon, QPainter

class View(QMainWindow):

    def __init__(self, model, controller):
        super(View, self).__init__()


        self.setFixedSize(1024,720)
        controller.setFixedSize(1024,720)
        self.setWindowTitle('WGTask')   
        self.setWindowIcon(QIcon(r"Icons/icon.jpg"))

        self.model = model
        self.layout().addWidget(controller)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)

        self.drawRectangles(qp)
        #self.drawLines(qp)
        #self.drawRemovalLine(qp)
        #self.drawConnectionLine(qp)

        qp.end()
 
    def drawRectangles(self, qp):
        for rect in self.model.rects:
            qp.setBrush(rect.rectColor)
            qp.drawRects(rect.rectBody)



