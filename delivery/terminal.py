import sys

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore, QtWidgets, Qt

from ordering import Dish, Order
from gui.delivery_gui import Ui_deliveryTerminal


class Terminal(QWidget, Ui_deliveryTerminal):
    def __init__(self):
        super(Terminal, self).__init__()
        self.setupUi(self)

        self.order = Order()
        self.menu = []
        self.menu_gui = []
        self.making_dishes_queue = []
        self.made_dishes = []
        self.timer = Qt.QTimer()
        self.timer_interval = 500
        self.timer.setInterval(self.timer_interval)
        with open('dishes.txt', 'r', encoding='utf-8') as dishes_file:
            for dish in dishes_file.readlines():
                dish_name, dish_cost, dish_weight = dish.replace('\n', '').split(' - ')
                self.menu.append(Dish(dish_name, int(dish_weight), int(dish_cost)))

        self.addUi()

    def addUi(self):

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
        self.getOrderButton.setEnabled(False)
        self.getOrderButton.hide()
        self.doNewOrderLabel.hide()
        self.doNewOrderButton.hide()
        self.exitButton.hide()

        self.makeOrderButton.clicked.connect(self.do_order)
        self.backToPickButton.clicked.connect(self.back_to_pick)
        self.doOrderButton.clicked.connect(self.generate_order_ui)
        self.getOrderButton.clicked.connect(self.get_order)
        self.doNewOrderButton.clicked.connect(self.reset)
        self.exitButton.clicked.connect(exit)
        self.timer.timeout.connect(self.recurring_timer)

    def reset(self):
        self.making_dishes_queue = []
        self.made_dishes = []

        self.doNewOrderButton.hide()
        self.exitButton.hide()
        self.doNewOrderLabel.hide()

        self.orderCostLabel.show()
        self.makeOrderButton.show()

        self.getOrderButton.setEnabled(False)

        for dish in self.menu_gui:
            dish.setCheckState(False)
            dish.counter.setValue(1)
            dish.show()
            dish.counter.show()

        self.order = Order()
        self.cost_upd()

    def generate_order_ui(self):
        self.orderTextBrowser.hide()
        self.backToPickButton.hide()
        self.doOrderButton.hide()
        self.getOrderButton.show()

        uniq_dishes = self.order.get_uniq_dishes()
        for i in uniq_dishes.keys():
            dish_name = i
            dish_count = uniq_dishes[i][1]
            dish_label = QtWidgets.QLabel(f'{dish_name} - {dish_count}шт')
            dish_progress_bar = QtWidgets.QProgressBar()
            dish_progress_bar.setValue(0)
            dish_status_label = QtWidgets.QLabel('Ожидает приготовления')

            dish_making_layout = QtWidgets.QHBoxLayout()
            dish_making_layout.addWidget(dish_label)
            dish_making_layout.addWidget(dish_progress_bar)
            dish_making_layout.addWidget(dish_status_label)
            self.making_dishes_queue.append({'dish': dish_label,
                                             'progressBar': dish_progress_bar,
                                             'status': dish_status_label})
            self.doOredrLayout.addLayout(dish_making_layout)

        self.timer.start()

    def recurring_timer(self):
        if self.making_dishes_queue:
            progress_bar = self.making_dishes_queue[0]['progressBar']
            progress_bar.setValue(progress_bar.value() + int(50 * (self.timer_interval / 1000)))
            status = self.making_dishes_queue[0]['status']
            if progress_bar.value() <= 60:
                status.setText('Готовим')
            elif 60 < progress_bar.value() < 100:
                status.setText('Упаковываем')
            else:
                status.setText('Готово!')
                self.made_dishes.append(self.making_dishes_queue[0])
                del self.making_dishes_queue[0]
        else:
            self.timer.stop()
            self.getOrderButton.setEnabled(True)

    def get_order(self):
        for dish in self.made_dishes:
            for widget in dish.values():
                widget.hide()
        self.getOrderButton.hide()
        self.doNewOrderLabel.show()
        self.doNewOrderButton.show()
        self.exitButton.show()

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
            self.orderTextBrowser.setText(self.order.__str__())
            self.orderTextBrowser.show()
            self.backToPickButton.show()
            self.doOrderButton.show()

    def back_to_pick(self):
        for dish in self.menu_gui:
            dish.show()
            dish.counter.show()
        self.orderCostLabel.show()
        self.makeOrderButton.show()

        self.orderTextBrowser.hide()
        self.backToPickButton.hide()
        self.doOrderButton.hide()

    def cost_upd(self):
        self.orderCostLabel.setText(f'Стоимость: {self.order.cost}')

    def get_menu(self):
        res = []
        for i in self.menu:
            res.append(i.dish_inf())
        return res


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Terminal()
    ex.show()
    app.exec_()
    exit()
