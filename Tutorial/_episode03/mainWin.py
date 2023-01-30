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

        painter.setPen(self._penDarker)
        painter.drawLines(darkGrayLines)
        painter.setPen(self._penLighter)
        painter.drawLines(lightGreyLines)


class GraphicViewOverride(QGraphicsView):
    scenePosChanged = pyqtSignal(int, int)

    isMiddleMouseButtonPressed: bool = False
    lastMiddleMousePosition = QPointF(0, 0)

    def __init__(self, graphicScene, parent=None):
        super().__init__()
        self.scene = graphicScene
        self.setScene(self.scene)

        self.setRenderProperties()
        self.centerOn(0, 0)
        self.scaleScene(2)

    def setRenderProperties(self):
        self.setRenderHints(QPainter.RenderHint.Antialiasing
                            | QPainter.RenderHint.TextAntialiasing | QPainter.RenderHint.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

    def wheelEvent(self, event):
        # sourcery skip: assign-if-exp
        """
        Override the wheel event to zoom in and out the scene
        :param event:
        :return:
        """
        scaleFactor = round(1.5 ** (-event.angleDelta().y() / 240.0), 2)
        self.scaleScene(scaleFactor)

    def scaleScene(self, scaleFactor):
        """
        Scale the scene
        :param scaleFactor:
        :return:
        """
        # get the current scale
        currentScale = self.transform().m11()
        factor = 1
        if scaleFactor < 1:
            factor *= 0.8
        else:
            factor *= 1.25
        if 0.13 < currentScale < 10:
            self.scale(factor, factor)
        elif currentScale <= 0.13:
            self.scale(0.4 / currentScale, 0.4 / currentScale)
        else:
            self.scale(0.8, 0.8)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.MiddleButton:
            self.middleMouseButtonPress(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.MouseButton.MiddleButton:
            self.middleMouseButtonRelease(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        mousePosition = self.mapToScene(event.pos())
        self.scenePosChanged.emit(int(mousePosition.x()), int(mousePosition.y()))
        if self.isMiddleMouseButtonPressed:
            # panning the scene!
            self.panTheScene(event)

    def middleMouseButtonPress(self, event):
        self.isMiddleMouseButtonPressed = True
        self.lastMiddleMousePosition = event.pos()
        self.setCursor(Qt.CursorShape.ClosedHandCursor)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)

    def middleMouseButtonRelease(self, event):
        self.isMiddleMouseButtonPressed = False
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

    def panTheScene(self, event):
        # panning the scene!
        currentPosition = event.pos()
        deltaPosition = currentPosition - self.lastMiddleMousePosition
        self.lastMiddleMousePosition = currentPosition
        hsBarValue = self.horizontalScrollBar().value()
        self.horizontalScrollBar().setValue(int(hsBarValue - (deltaPosition.x())))
        vsBarValue = self.verticalScrollBar().value()
        self.verticalScrollBar().setValue(int(vsBarValue - (deltaPosition.y())))
        event.accept()


class Canvas(QWidget):
    mainLayout: QVBoxLayout
    scene: GraphicSceneOverride
    view: QGraphicsView
    width: int = 5000
    height: int = 5000

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.mainLayout = QVBoxLayout()
        self.scene = GraphicSceneOverride()
        self.scene.setGraphicSceneSize(self.width, self.height)
        self.view = GraphicViewOverride(self.scene)
        self.mainLayout.addWidget(self.view)
        self.setLayout(self.mainLayout)

        obj = QGraphicsRectItem(0, 0, 100, 100)
        obj.setBrush(QBrush(QColor(255, 0, 0)))
        obj.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.scene.addItem(obj)
        obj.setPos(100, 100)


class MainWindow(QMainWindow):
    statusMousePosition: QLabel

    def __init__(self, parent=None):
        super().__init__(parent)

        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Tutorial - Episode 3 - Il mistero del lago di Garda")
        self.createStatusBar()

    def createStatusBar(self):
        self.statusBar().showMessage("")
        self.statusMousePosition = QLabel("")
        self.statusBar().addPermanentWidget(self.statusMousePosition)
        self.canvas.view.scenePosChanged.connect(self.onScenePosChanged)

    def onScenePosChanged(self, x, y):
        self.statusMousePosition.setText(f"Scene Pos: {x}:{y}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
