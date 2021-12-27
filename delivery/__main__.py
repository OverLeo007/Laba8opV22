import sys

from PyQt5.QtWidgets import QApplication
from delivery.terminal import Terminal

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Terminal('dishes.txt')
    ex.show()
    app.exec_()
    exit()
