import sys
import requests

from bs4 import BeautifulSoup
from bs4.element import Tag
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction,QContextMenuEvent
from PySide6.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        #region Layout and Widgets
    
        widget = QWidget()
        main_layout = QVBoxLayout()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        #endregion

        self.setWindowTitle("Pip Manadger")
    
        self.listwidget = QListWidget()

        self.listwidget.currentItemChanged.connect(self.index_changed)
        self.lineedit = QLineEdit()
        self.lineedit.editingFinished.connect(self.text_changed)
        main_layout.addWidget(self.lineedit)
        main_layout.addWidget(self.listwidget)
        
    def index_changed(self, index:QListWidgetItem):  # Not an index, index is a QListWidgetItem
        print(index.text()) if index.text() else None

    def text_changed(self):  # text is a str
        s = requests.get(f"https://pypi.org/search/?q={self.lineedit.text()}&o=")
        sp = BeautifulSoup(s.text,"html.parser")
        packages = sp.find_all("ul",class_ = "unstyled")
        self.listwidget.clear()
        for a in packages:
            a:Tag
            for package in a.find_all("li"):
                package:Tag
                for name in package.find("span"):
                    self.listwidget.addItem(name.text)


app = QApplication(sys.argv)


window = MainWindow()
window.show()

app.exec()