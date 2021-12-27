class Order:
    """
    Класс заказа, содержит информацию
    о блюдах и их общей цене
    """
    def __init__(self):
        self.dishes = []
        self.cost = 0

    def add_dish(self, dish):
        """
        Метод добавления блюда в заказ,
        также обновляет его стоимость
        """
        self.dishes.append(dish)
        self.cost += dish.cost

    def remove_dish(self, dish):
        """
        Метод удаления блюда из заказа,
        также обновляет его стоимость
        """
        self.dishes.remove(dish)
        self.cost -= dish.cost

    def get_uniq_dishes(self):
        """
        Метод, возвращающий словарь
        ключами которого являются названия блюд,
        а значениями объект блюда и его количество в заказе
        """
        return {dish.name: (dish, self.dishes.count(dish)) for dish in set(self.dishes)}

    def __str__(self):
        uniq_dishes = self.get_uniq_dishes()
        res = ['Ваш заказ:']
        for dish in uniq_dishes.keys():
            count = uniq_dishes[dish][1]
            cost = count * uniq_dishes[dish][0].cost
            res.append(f'{dish} - {count}шт - {cost}руб')
        maxl = len(max(res, key=len))
        res.insert(1, '#' * maxl)
        res.append('#' * maxl)
        res.append(f'ИТОГО: {self.cost}руб')
        return '\n'.join(res)


class Dish:
    def __init__(self, name, weight, cost):
        self.name = name
        self.weight = weight
        self.cost = cost

    def __str__(self):
        return f'{self.name}, стоимость: {self.cost}руб, вес: {self.weight}г'

    def dish_inf(self):
        """
        Метод получения информации о блюде в виде словаря
        """
        return {'name': self.name, 'cost': self.cost,
                'weight': self.weight}
