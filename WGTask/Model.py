from Figures import Rectangle, Line
from PyQt5.QtCore import Qt, QPoint, QRect, QLine, QSize
from PyQt5.QtGui import QColor
class Model:
    def __init__(self,):
        self.rectWidth = 200
        self.rectHeight = self.rectWidth / 2
        self.rectToMove = None
        self.removalLine = None
        self.connectionLine = None
        self.rects = [] 
        self.lines = []

    def isEnoughSpaceToCreateRect(self, rectPos, rectWidth, rectHeight):
        rectCenter = QPoint((rectPos.x() - rectWidth / 2), (rectPos.y() - rectHeight / 2))
        rectToAdd = QRect(rectCenter, QSize(rectWidth, rectHeight))

        for rect in self.rects:
            if rect.rectBody.intersects(rectToAdd):
                return False

        return True

    def addNewRect(self, pos, rectWidth, rectHeight):
        red,green,blue = self.createRandomColor(pos)
        rectColor = QColor(red, green, blue)
        rectCenter = QPoint((pos.x() - rectWidth / 2), (pos.y() - rectHeight / 2))
        rectBody = QRect(rectCenter, QSize(rectWidth, rectHeight))
        addedRect = Rectangle(rectBody, rectColor)
        self.rects.append(addedRect)














    def createRandomColor(self, pos):
        rangeBegin = 0
        rangeEnd = 255
        red = rangeBegin + pos.x() % pos.y() % (rangeEnd - rangeBegin);
        green = rangeBegin + pos.y() % pos.x() % (rangeEnd - rangeBegin);
        blue = rangeBegin + abs(green - red) % (rangeEnd - rangeBegin);
        return red, green, blue

