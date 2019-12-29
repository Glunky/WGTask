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
        self.rectToMove = None
        self.removalLine = None
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
        if self.removalLine:
            self.drawRemovalLine(qp)

        qp.end()

    '''
    @Событие двойного нажатия мыши
        С помощью левой кнопки создаём новый прямугольник в точке нажатия
    '''
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.addNewRect(event.pos())
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
            self.addNewLine(event.pos(), event.pos())

        elif event.button() == Qt.LeftButton:
            self.rectToMove = self.findDraggableRect(event.pos())

        elif event.buttons() == QtCore.Qt.MidButton:
            self.removalLine = QLine(event.pos(), event.pos())
    '''
    @Событие отпускания мыши
        1) Если мы перетаскивали прямоугольник, то при отжатии устанавливаем текущую позицию как последнюю стабильную,
        чтобы, если случится пересечение, вернуться в неё
        2) Если для линий, то создаём связь
        3) Если рисовали линию удаления, то удаляем связи, которые он пересекла
    '''
    def mouseReleaseEvent(self,event):
        if event.button() == Qt.RightButton:
            try:
                lastLine = self.lines[len(self.lines) - 1]
                firstRect, secondRect = self.findRectsToCreateConnection(lastLine)
                if firstRect and secondRect:
                    lastLine.createConnectionBetweenRects(firstRect, secondRect)
            except IndexError:
                pass
            self.update()

        elif event.button() == Qt.LeftButton:
            if self.rectToMove is not None:
                self.rectToMove.lastPos = self.rectToMove.rectBody.center()

        elif event.button() == Qt.MidButton:
            indexesToRemove = self.findIndexesOfDeletedLines()
            for i, idx in enumerate(indexesToRemove):
                del self.lines[idx - i]
            self.removalLine.setPoints(QPoint(0,0), QPoint(0,0))
            self.update()

    '''
    @Событие движения мыши
        1) С помощью левой кнопки мыши перетаскиваем прямоугольники и проверяем, пересекались ли они.
            Если пересеклись, то возвращаем перетаскиваемый прямоугольник в предыдущую позицию
        2) С помощью правой кнопки отрисовывем новое значение p2 текущей линии
        3) С помощью центральной кнопки мыши рисуем линию удаления
    '''
    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            if self.rectToMove is not None:
                self.rectToMove.rectBody.moveCenter(event.pos())
                if self.isRectsIntersect():
                    self.rectToMove.rectBody.moveCenter(self.rectToMove.lastPos)
                    self.rectToMove = None
                self.update()

        elif event.buttons() == QtCore.Qt.RightButton:
            lastLine = self.lines[len(self.lines) - 1]
            lastLine.lineBody.setP2(event.pos())
            self.update()

        elif event.buttons() == QtCore.Qt.MidButton:
            self.removalLine.setP2(event.pos())
            self.update()

            


    #!-------- Функции управления линиями --------!#

    def addNewLine(self, P1, P2):
        addedLine = Line(QLine(P1, P2))
        self.lines.append(addedLine)


    def drawLines(self, qp):
        for line in self.lines:
            if line.connectionWasCreated:
                line.lineBody.setP1(line.rect1.rectBody.center())
                line.lineBody.setP2(line.rect2.rectBody.center())
            pen = QPen(Qt.black, 2, Qt.SolidLine)
            qp.setPen(pen)
            qp.drawLine(line.lineBody)

    def drawRemovalLine(self, qp):
        pen = QPen(Qt.red, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(self.removalLine)


    def findRectsToCreateConnection(self, line):
        lastLineP1 = line.lineBody.p1()
        lastLineP2 = line.lineBody.p2()
        firstRect = None
        secondRect = None
            
        for rect in (self.rects):
            xLeftPosOfRect = rect.rectBody.left()
            xRightPosOfRect = rect.rectBody.right()
            yTopPosOfRect = rect.rectBody.top()
            yBottomPosOfRect = rect.rectBody.bottom()
            if (xLeftPosOfRect <= lastLineP1.x() <= xRightPosOfRect) and (yTopPosOfRect <= lastLineP1.y() <= yBottomPosOfRect):
                firstRect = rect;
            if (xLeftPosOfRect <= lastLineP2.x() <= xRightPosOfRect) and (yTopPosOfRect <= lastLineP2.y() <= yBottomPosOfRect):
                secondRect = rect;

        if firstRect is not None and secondRect is not None and firstRect is not secondRect:
            return firstRect, secondRect
        else:
            del self.lines[len(self.lines) - 1]
            return None, None

    def findIndexesOfDeletedLines(self):
        indexesToRemove = []
        for idx, line in enumerate(self.lines):
            if self.isLinesIntersect(line.lineBody, self.removalLine):
                indexesToRemove.append(idx)
        return indexesToRemove


    def isLinesIntersect(self,line1, line2):
        dir1 = line1.p2() - line1.p1();
        dir2 = line2.p2() - line2.p1();

        a1 = -dir1.y();
        b1 = abs(dir1.x());
        d1 = -(a1 * line1.p1().x() + b1 * line1.p1().y());

        a2 = -dir2.y();
        b2 = abs(dir2.x());
        d2 = -(a2 * line2.p1().x() + b2 * line2.p1().y());

        seg1_line2_start = a2 * line1.p1().x() + b2 * line1.p1().y() + d2;
        seg1_line2_end = a2 * line1.p2().x() + b2 * line1.p2().y() + d2;

        seg2_line1_start = a1 * line2.p1().x() + b1 * line2.p1().y() + d1;
        seg2_line1_end = a1 * line2.p2().x() + b1 * line2.p2().y() + d1;

        if (seg1_line2_start * seg1_line2_end >= 0 or seg2_line1_start * seg2_line1_end >= 0): 
            return False
        return True

    #!-------- Функции управления прямоугольниками --------!#
    def addNewRect(self, pos):
        red,green,blue = self.createRandomColor(pos)
        rectColor = QColor(red, green, blue)
        rectWidth = self.rectWidth;
        rectHeight = self.rectWidth / 2
        rectCenter = QPoint(pos.x() - self.rectWidth / 2, pos.y() - rectHeight / 2)
        addedRect = Rectangle(QRect(rectCenter, QSize(rectWidth, rectHeight)), rectColor)
        self.rects.append(addedRect)
        
        # если при создании не хватает места для добавления прямоугольника, то удаляем его
        if self.isRectsIntersect():
            del self.rects[len(self.rects) - 1]

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
        for rect in (self.rects):
            if (rect.rectBody.left() <= mouseClickCoords.x() <= rect.rectBody.right()) and (rect.rectBody.top() <= mouseClickCoords.y() <= rect.rectBody.bottom()):
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