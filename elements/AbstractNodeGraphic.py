from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class AbstractNodeGraphic(QGraphicsItem):
    # NodeGraphic parameter
    width: int = 50
    height: int = 100

    # NodeGraphic colors
    borderColorDefault = QColor(10, 120, 10)
    borderColorSelect = QColor(255, 70, 10)
    backGroundColor = QColor(10, 180, 40)

    edges = []

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.boundingRect = QRectF(0, 0, self.width, self.height)
        self.setZValue(-1)

    def addEdge(self, edge):
        self.edges.append(edge)

    def itemChange(self, change, value):

        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            for edge in self.edges:
                edge.adjust()

        return QGraphicsItem.itemChange(self, change, value)

    def boundingRect(self):
        return self.boundingRect.normalized()

    def paint(self, painter, option, widget=None):
        if not self.isSelected():
            painter.setPen(self.borderColorDefault)
        else:
            painter.setPen(self.borderColorSelect)
        painter.setBrush(self.backGroundColor)
        painter.drawRoundedRect(self.boundingRect, 5, 5)
