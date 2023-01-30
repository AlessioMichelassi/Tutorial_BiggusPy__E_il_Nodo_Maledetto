
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class GraphicSceneOverride(QGraphicsScene):
    colorBackground: QColor = QColor(39, 39, 39, 255)
    colorGrayLighter: QColor = QColor(47, 47, 47, 255)
    colorGrayDarker: QColor = QColor(29, 29, 29, 255)
    lastMousePosition = None
    isMiddleMouseBtnPressed = False

    def __init__(self):
        super().__init__()
        # set the color of the scene
        self.setBackgroundBrush(self.colorBackground)

        self._penLighter = QPen(self.colorGrayLighter)
        self._penDarker = QPen(self.colorGrayDarker)

        self._penLighter.setWidth(1)
        self._penDarker.setWidth(2)

        self.smallGridSize = 10
        self.bigGridSize = 50

    def setGraphicSceneSize(self, width, height):
        self.setSceneRect(-width // 2, -height // 2, width, height)

    def drawBackground(self, painter: QPainter, rectF: QRectF) -> None:
        super().drawBackground(painter, rectF)

        _left = int(rectF.left())
        _right = int(rectF.right())
        _top = int(rectF.top())
        _bottom = int(rectF.bottom())

        firstHorizontalLine = _left - (_left % self.smallGridSize)
        firstVerticalLine = _top - (_top % self.smallGridSize)

        lightGreyLines, darkGrayLines = [], []
        for x in range(firstHorizontalLine, _right, self.smallGridSize):
            if x % self.bigGridSize == 0:
                darkGrayLines.append(QLine(x, _top, x, _bottom))
            else:
                lightGreyLines.append(QLine(x, _top, x, _bottom))

        for y in range(firstVerticalLine, _bottom, self.smallGridSize):
            if y % self.bigGridSize == 0:
                darkGrayLines.append(QLine(_left, y, _right, y))
            else:
                lightGreyLines.append(QLine(_left, y, _right, y))

        painter.setPen(self._penLighter)
        painter.drawLines(*lightGreyLines)
        painter.setPen(self._penDarker)
        if darkGrayLines:
            painter.drawLines(*darkGrayLines)







