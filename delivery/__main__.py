import sys

from PyQt5.QtWidgets import QApplication
from terminal import Terminal

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Terminal()
    ex.show()
    app.exec_()
    exit()
