import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon, QPainter, QBrush, QPen, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QPoint, QRect, QLine, QSize
     

class Line:
    def __init__(self, lineBody):
        self.lineBody = lineBody
        self.connectionWasCreated = False

    def createConnectionBetweenRects(self, rect1, rect2):
        self.rect1 = rect1
        self.rect2 = rect2
        self.lineBody.setP1(rect1.rectBody.center())
        self.lineBody.setP2(rect2.rectBody.center())
        self.connectionWasCreated = True


class Rectangle:
    def __init__(self, rectBody, rectColor):
        self.rectBody = rectBody
        self.rectColor = rectColor
        self.lastPos = self.rectBody.center()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()     

        self.setGeometry(0, 0, 1024, 768)
        self.setWindowTitle('WGTask')   
        self.setWindowIcon(QIcon(r"Icons/icon.jpg"))

        self.rectWidth = 200
        self.rectHeight = self.rectWidth / 2
        self.rectToMove = None
        self.removalLine = None
        self.connectionLine = None
        self.rects = [] 
        self.lines = []

        self.show()
 

    '''
    @Событие отрисовки
        Отрисовываем линии и прямоугольники
    '''
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)

        self.drawRectangles(qp)
        self.drawLines(qp)
        self.drawRemovalLine(qp)
        self.drawConnectionLine(qp)

        qp.end()

    '''
    @Событие двойного нажатия мыши
        С помощью левой кнопки создаём новый прямугольник в точке нажатия
    '''
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton and self.isEnoughSpaceToCreateRect(event.pos(), self.rectWidth, self.rectHeight):
            self.addNewRect(event.pos(), self.rectWidth, self.rectHeight)
        self.update()


    '''
    @Событие нажатия мыши
        1) С помощью левой кноки мыши детектируется перетаскиваемый прямоугольник
        2) С помощью правой кнопки начинаем создание новой линии путём добавления в список.
            Дальше уже отрисовка линии в событии движения мыши
        3) C помощью центральной кнопки мыши создаём линию удаления
    '''
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            #self.addNewLine(event.pos(), event.pos())
            self.connectionLine = Line(QLine(event.pos(), event.pos()))

        elif event.button() == Qt.LeftButton:
            self.rectToMove = self.findDraggableRect(event.pos())

        elif event.buttons() == QtCore.Qt.MidButton:
            self.removalLine = QLine(event.pos(), event.pos())
    '''
    @Событие отпускания мыши
        1) Если для линий, то создаём связь
        2) Если рисовали линию удаления, то удаляем связи, которые он пересекла
    '''
    def mouseReleaseEvent(self,event):
        if event.button() == Qt.RightButton:
            try:
                firstRect, secondRect = self.findRectsToCreateConnection(self.connectionLine)
                if firstRect and secondRect:
                    self.connectionLine.createConnectionBetweenRects(firstRect, secondRect)
                    self.addNewLine(self.connectionLine)
                    print(len(self.lines))
                self.connectionLine = None
                    
            except IndexError:
                pass

        elif event.button() == Qt.MidButton:
            indexesToRemove = self.findIndexesOfDeletedLines()
            for i, idx in enumerate(indexesToRemove):
                del self.lines[idx - i]
            self.removalLine = None

        self.update()   

    '''
    @Событие движения мыши
        1) С помощью левой кнопки мыши перетаскиваем прямоугольники и проверяем, пересекались ли они.
            Если пересеклись, то возвращаем перетаскиваемый прямоугольник в предыдущую позицию
        2) С помощью правой кнопки отрисовывем новое значение p2 текущей линии
        3) С помощью центральной кнопки мыши рисуем линию удаления
    '''
    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton and self.rectToMove is not None:
            self.rectToMove.lastPos = self.rectToMove.rectBody.center()
            self.rectToMove.rectBody.moveCenter(event.pos())
            if self.isRectsIntersect():
                self.rectToMove.rectBody.moveCenter(self.rectToMove.lastPos)

        elif event.buttons() == QtCore.Qt.RightButton:
            self.connectionLine.lineBody.setP2(event.pos())

        elif event.buttons() == QtCore.Qt.MidButton:
            self.removalLine.setP2(event.pos())

        self.update()

            


    #!-------- Функции управления линиями --------!#

    def addNewLine(self, line):
        self.lines.append(line)


    def drawLines(self, qp):
        for line in self.lines:
            rect1Center = line.rect1.rectBody.center()
            rect2Center = line.rect2.rectBody.center()
            line.lineBody.setP1(rect1Center)
            line.lineBody.setP2(rect2Center)
            pen = QPen(Qt.black, 2, Qt.SolidLine)
            qp.setPen(pen)
            qp.drawLine(line.lineBody)

    def drawRemovalLine(self, qp): #одинаковые функции!!
        if self.removalLine:
            pen = QPen(Qt.red, 2, Qt.SolidLine)
            qp.setPen(pen)
            qp.drawLine(self.removalLine)

    def drawConnectionLine(self, qp): #одинаковые функции!!
        if self.connectionLine:
            pen = QPen(Qt.black, 2, Qt.SolidLine)
            qp.setPen(pen)
            qp.drawLine(self.connectionLine.lineBody)

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
            if self.isLinesIntersect(line.lineBody, self.removalLine):
                indexesToRemove.append(idx)

        return indexesToRemove


    def isLinesIntersect(self,line1, line2):
        def ccw(A,B,C):
            return (C.y()-A.y()) * (B.x()-A.x()) > (B.y()-A.y()) * (C.x()-A.x())

        A = line1.p1()
        B = line1.p2()
        C = line2.p1()
        D = line2.p2()

        return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

    #!-------- Функции управления прямоугольниками --------!#
    def addNewRect(self, pos, rectWidth, rectHeight):
        red,green,blue = self.createRandomColor(pos)
        rectColor = QColor(red, green, blue)
        rectCenter = QPoint((pos.x() - rectWidth / 2), (pos.y() - rectHeight / 2))
        rectBody = QRect(rectCenter, QSize(rectWidth, rectHeight))
        addedRect = Rectangle(rectBody, rectColor)
        self.rects.append(addedRect)
       

    def isEnoughSpaceToCreateRect(self, rectPos, rectWidth, rectHeight):
        rectCenter = QPoint((rectPos.x() - rectWidth / 2), (rectPos.y() - rectHeight / 2))
        rectToAdd = QRect(rectCenter, QSize(rectWidth, rectHeight))

        for rect in self.rects:
            if rect.rectBody.intersects(rectToAdd):
                return False

        return True


    def isRectsIntersect(self):
        for outerRect in (self.rects):
            for innerRect in (self.rects):

                if innerRect is outerRect: 
                    continue
                if outerRect.rectBody.intersects(innerRect.rectBody):
                    return True

        return False


    def drawRectangles(self, qp):
        for rect in self.rects:
            qp.setBrush(rect.rectColor)
            qp.drawRects(rect.rectBody)


    def findDraggableRect(self, mouseClickCoords):
        xMousePos = mouseClickCoords.x()
        yMousePos = mouseClickCoords.y()

        for rect in (self.rects):
            leftSideOfRect = rect.rectBody.left()
            rightSideOfRect = rect.rectBody.right()
            topSideOfRect = rect.rectBody.top()
            bottomSideOfRect = rect.rectBody.bottom()

            if (leftSideOfRect<= xMousePos <= rightSideOfRect) and  \
                (topSideOfRect<= yMousePos <= bottomSideOfRect):
                return rect

        return None


    #случайный цвет создаётся на основе позиции прямоугольника
    def createRandomColor(self, pos):
        rangeBegin = 0
        rangeEnd = 255
        red = rangeBegin + pos.x() % pos.y() % (rangeEnd - rangeBegin);
        green = rangeBegin + pos.y() % pos.x() % (rangeEnd - rangeBegin);
        blue = rangeBegin + abs(green - red) % (rangeEnd - rangeBegin);
        return red, green, blue


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()