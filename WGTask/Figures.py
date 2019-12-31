class Line:
    def __init__(self, lineBody):
        self.lineBody = lineBody

    def createConnectionBetweenRects(self, rect1, rect2):
        self.rect1 = rect1
        self.rect2 = rect2
        self.lineBody.setP1(rect1.rectBody.center())
        self.lineBody.setP2(rect2.rectBody.center())


class Rectangle:
    def __init__(self, rectBody, rectColor):
        self.rectBody = rectBody
        self.rectColor = rectColor
        self.lastPos = self.rectBody.center()
