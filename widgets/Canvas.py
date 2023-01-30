from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from graphicEngine.GraphicSceneOverride import GraphicSceneOverride
from graphicEngine.graphicViewOverrides import GraphicViewOverride
from elements.AbstractNodeGraphic import AbstractNodeGraphic


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
        obj.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.scene.addItem(obj)
        obj.setPos(100, 100)

        obj2 = AbstractNodeGraphic()

        self.scene.addItem(obj2)
        obj2.setPos(200, 200)



