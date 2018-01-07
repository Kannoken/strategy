from abc import ABC, abstractmethod
from collections import namedtuple
"""Паттерн Стратегия. Высчитывает скидку в зависимости от переданного класса"""
Customer = namedtuple('Customer', 'name fidelity')


class LineItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quentity = quantity
        self.price = price

    def total(self):
        return self.price * self.quentity


class Order:

    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = cart
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())


class Promotion(ABC):  # Стратегия: абстрактный базовый класс
    @abstractmethod
    def discount(self, order):
        """Вернуть скидку в виде положительной суммы в долларах"""


class FidelityPromo(Promotion):  # first Concrete Strategy
    """5% скидка для заказчиков, имеющих не менее 1000 баллов лояльности"""

    def discount(self, order):
        return order.total() * .05 if order.customer.fidelity >= 1000 else 0


class BulkItemPromo(Promotion):  # second Concrete Strategy
    """10% скидка для каждой позиции LineItem, в которой заказано не менее 20 единиц"""

    def discount(self, order):
        discount = 0
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * .1
        return discount


class LargeOrderPromo(Promotion):  # third Concrete Strategy
    """7% скидка для заказов, включающих не менее 10 различных позиций"""

    def discount(self, order):
        dictinct_items = {item.product for item in order.cart}
        if len(dictinct_items) >= 10:
            return order.total() * .07
        return 0
