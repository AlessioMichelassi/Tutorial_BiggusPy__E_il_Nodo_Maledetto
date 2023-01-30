from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Arrow(QGraphicsItem):

    def __init__(self, startNode, endNode, parent=None):
        super().__init__(parent)
        self.startNode = startNode
        self.endNode = endNode
        self.startNode.addEdge(self)
        self.endNode.addEdge(self)
        startPos = QPointF(self.startNode.pos().x() + self.startNode.width // 2, self.startNode.pos().y() + self.startNode.height // 2)
        self.startPoint = startPos
        endPos = QPointF(self.endNode.pos().x() + self.endNode.width // 2, self.endNode.pos().y() + self.endNode.height // 2)
        self.endPoint = endPos
        self.setZValue(-10)

    def adjust(self):
        # Aggiorniamo la posizione della freccia
        startPos = QPointF(self.startNode.pos().x() + self.startNode.width // 2,
                           self.startNode.pos().y() + self.startNode.height // 2)
        self.startPoint = startPos
        endPos = QPointF(self.endNode.pos().x() + self.endNode.width // 2,
                         self.endNode.pos().y() + self.endNode.height // 2)
        self.endPoint = endPos
        self.update()


    def paint(self, painter, _QStyleOptionGraphicsItem, widget=None):
        # Disegniamo la freccia utilizzando un QPainter
        painter.setPen(QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.DashLine))
        painter.drawLine(self.startPoint, self.endPoint)
