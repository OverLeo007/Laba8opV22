class Order:
    def __init__(self):
        self.dishes = []
        self.cost = 0

    def add_dish(self, dish):
        self.dishes.append(dish)

    def __str(self):
        pass


class Dish:
    def __init__(self, name, weight, cost):
        self.name = name
        self.weight = weight
        self.cost = cost
        self.is_ready = False
        self.is_packed = False

    def cook(self):
        self.is_ready = True

    def pack(self):
        self.is_packed = True


