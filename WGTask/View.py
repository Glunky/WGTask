from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtGui import QIcon, QPainter, QPen
from PyQt5.QtCore import Qt

# Класс View отвечает за настройку главного окна и отображение пользовательского ввода
class View(QMainWindow):

    def __init__(self, model, controller):
        super(View, self).__init__()

        self.setFixedSize(1024,720)
        controller.setFixedSize(1024,720)
        self.setWindowTitle('WGTask')   
        self.setWindowIcon(QIcon(r"Icons/icon.jpg"))

        self.model = model
        self.layout().addWidget(controller)

    # Событие отрисовки
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)

        self.drawRectangles(qp)
        self.drawLines(qp)
        if self.model.removalLine:
            self.drawRemovalLine(qp)
        if self.model.connectionLine:
            self.drawConnectionLine(qp)

        qp.end()
 

    #!----- Функции отрисовки фигур -----!#
    def drawRectangles(self, qp):
        for rect in self.model.rects:
            qp.setBrush(rect.rectColor)
            qp.drawRects(rect.rectBody)


    def drawLines(self, qp):
        for line in self.model.lines:
            rect1Center = line.rect1.rectBody.center()
            rect2Center = line.rect2.rectBody.center()
            line.lineBody.setP1(rect1Center)
            line.lineBody.setP2(rect2Center)
            pen = QPen(Qt.black, 2, Qt.SolidLine)
            qp.setPen(pen)
            qp.drawLine(line.lineBody)


    def drawRemovalLine(self, qp):
        pen = QPen(Qt.red, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(self.model.removalLine)


    def drawConnectionLine(self, qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(self.model.connectionLine.lineBody)


