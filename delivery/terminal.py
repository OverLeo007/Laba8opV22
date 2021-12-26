import sys

from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets

from ordering import Dish, Order
from gui.delivery_gui import Ui_deliveryTerminal


class Terminal(QWidget, Ui_deliveryTerminal):
    def __init__(self):
        super(Terminal, self).__init__()
        self.setupUi(self)

        self.order = Order()
        self.menu = []
        self.menu_gui = []
        with open('dishes.txt', 'r', encoding='utf-8') as dishes_file:
            for dish in dishes_file.readlines():
                dish_name, dish_cost, dish_weight = dish.replace('\n', '').split(' - ')
                self.menu.append(Dish(dish_name, int(dish_weight), int(dish_cost)))

        self.addUI()

    def addUI(self):

        for n, i in enumerate(self.menu):
            layout_dish = QtWidgets.QHBoxLayout()

            dish = QtWidgets.QCheckBox(i.__str__())
            dish.dish_name = i
            dish.stateChanged.connect(self.add_to_order)

            count_dish = QtWidgets.QSpinBox()
            count_dish.setEnabled(False)
            count_dish.setMinimum(1)
            dish.counter = count_dish

            count_dish.dish_to_count = dish
            count_dish.valueChanged.connect(self.counter_value_changed)
            self.menu_gui.append(dish)
            layout_dish.addWidget(dish)
            layout_dish.addWidget(count_dish)

            self.dishesLayout.addLayout(layout_dish, n, 1, 1, 1)

        self.orderCostLabel.setText(f'Стоимость: 0')

        self.backToPickButton.hide()
        self.doOrderButton.hide()
        self.orderTextBrowser.hide()
        self.makeOrderButton.clicked.connect(self.do_order)

    def add_to_order(self, state):
        dish = self.sender()
        if state == QtCore.Qt.Checked:
            dish.counter.setEnabled(True)
            for _ in range(dish.counter.value()):
                self.order.add_dish(dish.dish_name)

        else:
            dish.counter.setEnabled(False)
            for _ in range(self.order.dishes.count(dish.dish_name)):
                self.order.remove_dish(dish.dish_name)
        self.cost_upd()

    def counter_value_changed(self, value):
        counter = self.sender()
        if value > self.order.dishes.count(counter.dish_to_count.dish_name):
            self.order.add_dish(counter.dish_to_count.dish_name)
        else:
            self.order.remove_dish(counter.dish_to_count.dish_name)
        self.cost_upd()

    def do_order(self):
        if self.order.cost > 0:
            for dish in self.menu_gui:
                dish.hide()
                dish.counter.hide()

            self.orderCostLabel.hide()
            self.makeOrderButton.hide()

            self.orderTextBrowser.show()
            self.backToPickButton.show()
            self.doOrderButton.show()

    def cost_upd(self):
        self.orderCostLabel.setText(f'Стоимость: {self.order.cost}')

    def get_menu(self):
        res = []
        for i in self.menu:
            res.append(i.dish_inf())
        return res

    def make_order(self):
        for i in self.order.dishes:
            i.cook()
            i.pack()


def main():
    terminal = Terminal()
    terminal.show()
    print(terminal.get_menu())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Terminal()
    ex.show()
    app.exec_()
    exit()
