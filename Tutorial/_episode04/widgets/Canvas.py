from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Tutorial._episode04.graphicEngine.GraphicSceneOverride import GraphicSceneOverride
from Tutorial._episode04.graphicEngine.graphicViewOverrides import GraphicViewOverride


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

