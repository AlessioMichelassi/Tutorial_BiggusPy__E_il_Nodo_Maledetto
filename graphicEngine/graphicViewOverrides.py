
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from elements.AbstractNodeGraphic import AbstractNodeGraphic
from elements.arrow import Arrow


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

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        node = AbstractNodeGraphic()
        self.scene.addItem(node)
        node.setPos(self.mapToScene(event.pos()))

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.MiddleButton:
            self.middleMouseButtonPress(event)
        if event.button() == Qt.RightButton:
            if len(self.scene.selectedItems()) == 2:
                edge = Arrow(self.scene.selectedItems()[0], self.scene.selectedItems()[1])
                self.scene.addItem(edge)

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
