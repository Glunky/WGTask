from Figures import Rectangle, Line
from PyQt5.QtCore import Qt, QPoint, QRect, QLine, QSize
from PyQt5.QtGui import QColor

# Класс Model содержит информацию о моделе и функции манипулирования ей
class Model:
    def __init__(self,):
        self.rectWidth = 200
        self.rectHeight = self.rectWidth / 2
        self.rectToMove = None
        self.removalLine = None
        self.connectionLine = None
        self.rects = [] 
        self.lines = []

    # функция создания цвета зависит от координат добавляемого прямоугольника
    def createRandomColor(self, pos):
        rangeBegin = 0
        rangeEnd = 255
        red = rangeBegin + pos.x() % pos.y() % (rangeEnd - rangeBegin);
        green = rangeBegin + pos.y() % pos.x() % (rangeEnd - rangeBegin);
        blue = rangeBegin + abs(green - red) % (rangeEnd - rangeBegin);
        return red, green, blue


        #!----- Функции для прямоугольников -----!#
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


    def dragRect(self, dragPos):
        self.rectToMove.lastPos = self.rectToMove.rectBody.center()
        self.rectToMove.rectBody.moveCenter(dragPos)
        if self.areRectsIntersect():
            self.rectToMove.rectBody.moveCenter(self.rectToMove.lastPos)


    def findDraggableRect(self, mouseClickCoords):
        xMousePos = mouseClickCoords.x()
        yMousePos = mouseClickCoords.y()

        for rect in (self.rects):
            leftSideOfRect = rect.rectBody.left()
            rightSideOfRect = rect.rectBody.right()
            topSideOfRect = rect.rectBody.top()
            bottomSideOfRect = rect.rectBody.bottom()

            if (leftSideOfRect<= xMousePos <= rightSideOfRect) and (topSideOfRect<= yMousePos <= bottomSideOfRect):
                return rect

        return None


    def areRectsIntersect(self):
        for rect in (self.rects):

            if rect is self.rectToMove: 
                continue
            if self.rectToMove.rectBody.intersects(rect.rectBody):
                return True

        return False

       

    #!----- Функции для линий -----!#
    def addNewLine(self, line):
        self.lines.append(line)


    def createConnectionLine(self, xPos, yPos):
        self.connectionLine = Line(QLine(xPos, yPos))


    def createRemovalLine(self, xPos, yPos):
        self.removalLine = QLine(xPos, yPos)


    def findRectsToCreateConnection(self, line):
        lineP1 = line.lineBody.p1()
        lineP2 = line.lineBody.p2()
        firstRect = None
        secondRect = None
            
        for rect in (self.rects):
            leftSideOfRect = rect.rectBody.left()
            rightSideOfRect = rect.rectBody.right()
            topSideOfRect = rect.rectBody.top()
            bottomSideOfRect = rect.rectBody.bottom()

            if (leftSideOfRect <= lineP1.x() <= rightSideOfRect) and (topSideOfRect <= lineP1.y() <= bottomSideOfRect):
                firstRect = rect;
            if (leftSideOfRect <= lineP2.x() <= rightSideOfRect) and (topSideOfRect <= lineP2.y() <= bottomSideOfRect):
                secondRect = rect;

        if firstRect is not None and secondRect is not None and firstRect is not secondRect:
            return firstRect, secondRect

        return None, None


    def findIndexesOfDeletedLines(self):
        indexesToRemove = []

        for idx, line in enumerate(self.lines):
            if self.areLinesIntersect(line.lineBody, self.removalLine):
                indexesToRemove.append(idx)

        return indexesToRemove


    def areLinesIntersect(self,line1, line2):
        def ccw(A,B,C):
            return (C.y()-A.y()) * (B.x()-A.x()) > (B.y()-A.y()) * (C.x()-A.x())

        A = line1.p1()
        B = line1.p2()
        C = line2.p1()
        D = line2.p2()

        return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


    def cutLines(self, indexesToRemove):
        for i, idx in enumerate(indexesToRemove):
            del self.lines[idx - i]
        self.removalLine = None

