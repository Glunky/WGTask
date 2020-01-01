from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt, QPoint, QLine
from PyQt5.QtWidgets import QWidget

class Controller(QWidget):

    handleLeftMouseDoubleClick = pyqtSignal(QPoint, int, int)
    handleLeftMouseDrag = pyqtSignal(QPoint)


    def __init__(self, model):
        super(Controller, self).__init__()
        self.model = model

        self.handleLeftMouseDoubleClick.connect(model.addNewRect)
        self.handleLeftMouseDrag.connect(model.dragRect)
        


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.model.rectToMove = self.model.findDraggableRect(event.pos())

        elif event.button() == Qt.RightButton:
            self.model.createConnectionLine(event.pos(), event.pos())

        elif event.button() == Qt.MidButton:
            self.model.createRemovalLine(event.pos(), event.pos())

        self.update()


    def mouseDoubleClickEvent(self, event):
        rectWidth = self.model.rectWidth
        rectHeight = self.model.rectHeight
        positionToAdd = event.pos()

        if event.button() == Qt.LeftButton and self.model.isEnoughSpaceToCreateRect(positionToAdd, rectWidth, rectHeight):
            self.handleLeftMouseDoubleClick.emit(positionToAdd, rectWidth, rectHeight)

        self.update()




    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.model.rectToMove is not None:
            self.handleLeftMouseDrag.emit(event.pos())

        elif event.buttons() == Qt.RightButton:
            self.model.connectionLine.lineBody.setP2(event.pos())

        elif event.buttons() == Qt.MidButton:
            self.model.removalLine.setP2(event.pos())

        self.update()



    def mouseReleaseEvent(self,event):
        if event.button() == Qt.RightButton:
            try:
                firstRect, secondRect = self.model.findRectsToCreateConnection(self.model.connectionLine)
                if firstRect and secondRect:
                    self.model.connectionLine.createConnectionBetweenRects(firstRect, secondRect)
                    self.model.addNewLine(self.model.connectionLine)
                self.model.connectionLine = None
                    
            except IndexError:
                pass

        elif event.button() == Qt.MidButton:
            indexesToRemove = self.model.findIndexesOfDeletedLines()
            for i, idx in enumerate(indexesToRemove):
                del self.model.lines[idx - i]
            self.model.removalLine = None

        self.update()
    