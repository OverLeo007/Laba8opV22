class Order:
    def __init__(self):
        self.dishes = []
        self.cost = 0

    def add_dish(self, dish):
        self.dishes.append(dish)
        self.cost += dish.cost

    def remove_dish(self, dish):
        self.dishes.remove(dish)
        self.cost -= dish.cost

    def __str__(self):
        pass


class Dish:
    def __init__(self, name, weight, cost):
        self.name = name
        self.weight = weight
        self.cost = cost
        self.is_cooked = False
        self.is_packed = False

    def cook(self):
        self.is_cooked = True

    def pack(self):
        self.is_packed = True

    def __str__(self):
        return f'{self.name}, стоимость: {self.cost}руб, вес: {self.weight}г'

    def dish_inf(self):
        return {'name': self.name, 'cost': self.cost,
                'weight': self.weight, 'packed': self.is_packed,
                'cooked': self.is_cooked}

