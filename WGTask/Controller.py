from PyQt5.QtCore import Qt, QPoint, QLine
from PyQt5.QtWidgets import QWidget

# Класс Controller отрабатывает пользовательский ввод
class Controller(QWidget):

    def __init__(self, model):
        super(Controller, self).__init__()
        self.model = model

    # Событие клика мыши
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # находим прямоугольник для перетаскивания, если координаты клика попали в рамки прямоугольника
            self.model.rectToMove = self.model.findDraggableRect(event.pos())

        elif event.button() == Qt.RightButton:
            self.model.createConnectionLine(event.pos(), event.pos())

        elif event.button() == Qt.MidButton:
            self.model.createRemovalLine(event.pos(), event.pos())

        self.update()


    #Событие двйного клика мыши
    def mouseDoubleClickEvent(self, event):
        rectWidth = self.model.rectWidth
        rectHeight = self.model.rectHeight
        positionToAdd = event.pos()

        if event.button() == Qt.LeftButton and self.model.isEnoughSpaceToCreateRect(positionToAdd, rectWidth, rectHeight):
            self.model.addNewRect(positionToAdd, rectWidth, rectHeight)

        self.update()


    # Событие движения мыши
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.model.rectToMove is not None:
            self.model.dragRect(event.pos())
        # перетаскиваем второй конец отрезка на позицию, куда указывает мышь
        elif event.buttons() == Qt.RightButton:
            self.model.connectionLine.lineBody.setP2(event.pos())
        # аналогично для линии удаления
        elif event.buttons() == Qt.MidButton:
            self.model.removalLine.setP2(event.pos())

        self.update()


    # Событие отжатия кнопки мыши
    def mouseReleaseEvent(self,event):
        if event.button() == Qt.RightButton and self.model.connectionLine is not None:
            # создаём связь, если концы линии попадают в прямоугольники
            firstRect, secondRect = self.model.findRectsToCreateConnection(self.model.connectionLine)
            if firstRect and secondRect:
                self.model.connectionLine.createConnectionBetweenRects(firstRect, secondRect)
                self.model.addNewLine(self.model.connectionLine)

            self.model.connectionLine = None
                    
        # обррезаем линии связи, которые пересекаются с линией удаления
        elif event.button() == Qt.MidButton:
            indexesToRemove = self.model.findIndexesOfDeletedLines()
            if len(indexesToRemove) != 0:
                self.model.cutLines(indexesToRemove)
            self.model.removalLine = None
        self.update()
    