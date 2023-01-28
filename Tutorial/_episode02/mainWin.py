import sys

from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class GraphicSceneOverride(QGraphicsScene):
    colorBackground: QColor = QColor(39, 39, 39, 255)
    colorGrayLighter: QColor = QColor(47, 47, 47, 255)
    colorGrayDarker: QColor = QColor(29, 29, 29, 255)
    lastMousePosition = None
    isMiddleMouseBtnPressed = False

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        # set the color of the scene
        self.setBackgroundBrush(self.colorBackground)

        self._penLighter = QPen(self.colorGrayLighter)
        self._penDarker = QPen(self.colorGrayDarker)

        self._penLighter.setWidth(1)
        self._penDarker.setWidth(2)

        self.smallGridSize = 10
        self.bigGridSize = 50

    def wheelEvent(self, event):
        delta = event.delta()
        # if the delta is positive, zoom in
        if delta > 0:
            factor = 1.25
        else:
            factor = 0.8
        currentScale = self.views()[0].transform().m11()
        if 0.13 < currentScale < 15:
            self.views()[0].scale(factor, factor)
        elif currentScale <= 0.13:
            self.views()[0].scale(1.25, 1.25)
        else:
            self.views()[0].scale(0.8, 0.8)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.lastMousePosition = event.scenePos()
        self.isMiddleMouseBtnPressed = True
        self.views()[0].setCursor(Qt.CursorShape.OpenHandCursor)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.isMiddleMouseBtnPressed:
            self.views()[0].setCursor(Qt.CursorShape.ClosedHandCursor)
            if self.views()[0].transform().m11() != 1:
                self.panTheScene(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.isMiddleMouseBtnPressed = False
        self.views()[0].setCursor(Qt.CursorShape.ArrowCursor)

    def panTheScene(self, event):
        # panning the scene
        currentPosition = event.scenePos()
        hsBarValue = self.views()[0].horizontalScrollBar().value()
        vsBarValue = self.views()[0].verticalScrollBar().value()
        deltaPosition = currentPosition - self.lastMousePosition
        self.lastMousePosition = currentPosition
        self.views()[0].horizontalScrollBar().setValue(int(hsBarValue - deltaPosition.x()))
        self.views()[0].verticalScrollBar().setValue(int(vsBarValue - deltaPosition.y()))
        event.accept()

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

        painter.setPen(self._penDarker)
        painter.drawLines(darkGrayLines)
        painter.setPen(self._penLighter)
        painter.drawLines(lightGreyLines)


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.graphicScene = GraphicSceneOverride(-5000, -5000, 5000, 5000)
        self.graphicView = QGraphicsView(self.graphicScene)
        self.setCentralWidget(self.graphicView)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
