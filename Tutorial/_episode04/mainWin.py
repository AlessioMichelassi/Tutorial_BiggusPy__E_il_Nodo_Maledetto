from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from widgets.Canvas import Canvas


class MainWindow(QMainWindow):
    statusMousePosition: QLabel

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(100, 100, 800, 600)
        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)
        self.createStatusBar()

    def createStatusBar(self):
        self.statusBar().showMessage("")
        self.statusMousePosition = QLabel("")
        self.statusBar().addPermanentWidget(self.statusMousePosition)
        self.canvas.view.scenePosChanged.connect(self.onScenePosChanged)

    def onScenePosChanged(self, x, y):
        self.statusMousePosition.setText(f"Scene Pos: {x}:{y}")
