import time

from enum import Enum
class OrderType(Enum):
    LIMIT = 1
    MARKET = 2
    IOC = 3

class OrderSide(Enum):
    BUY = 1
    SELL = 2


class NonPositiveQuantity(Exception):
    pass

class NonPositivePrice(Exception):
    pass

class InvalidSide(Exception):
    pass

class UndefinedOrderType(Exception):
    pass

class UndefinedOrderSide(Exception):
    pass

class NewQuantityNotSmaller(Exception):
    pass

class UndefinedTraderAction(Exception):
    pass

class UndefinedResponse(Exception):
    pass


from abc import ABC


class Order(ABC):
    def __init__(self, id, symbol, quantity, side, time):
        self.id = id
        self.symbol = symbol
        if quantity > 0:
            self.quantity = quantity
        else:
            raise NonPositiveQuantity("Quantity Must Be Positive!")
        if side in [OrderSide.BUY, OrderSide.SELL]:
            self.side = side
        else:
            raise InvalidSide("Side Must Be Either \"Buy\" or \"OrderSide.SELL\"!")
        self.time = time


class LimitOrder(Order):
    def __init__(self, id, symbol, quantity, price, side, time):
        super().__init__(id, symbol, quantity, side, time)
        if price > 0:
            self.price = price
        else:
            raise NonPositivePrice("Price Must Be Positive!")
        self.type = OrderType.LIMIT


class MarketOrder(Order):
    def __init__(self, id, symbol, quantity, side, time):
        super().__init__(id, symbol, quantity, side, time)
        self.type = OrderType.MARKET


class IOCOrder(Order):
    def __init__(self, id, symbol, quantity, price, side, time):
        super().__init__(id, symbol, quantity, side, time)
        if price > 0:
            self.price = price
        else:
            raise NonPositivePrice("Price Must Be Positive!")
        self.type = OrderType.IOC


class FilledOrder(Order):
    def __init__(self, id, symbol, quantity, price, side, time, limit = False):
        super().__init__(id, symbol, quantity, side, time)
        self.price = price
        self.limit = limit




class MatchingEngine():
    def __init__(self):
        self.bid_book = []
        self.ask_book = []
        # These are the order books you are given and expected to use for matching the orders below

    # Note: As you implement the following functions keep in mind that these enums are available:
#     class OrderType(Enum):
#         LIMIT = 1
#         MARKET = 2
#         IOC = 3

#     class OrderSide(Enum):
#         BUY = 1
#         SELL = 2

    def handle_order(self, order):
        # Implement this function
        # In this function you need to call different functions from the matching engine
        # depending on the type of order you are given

        if order.type == OrderType.LIMIT:
            self.handle_limit_order(order)
        elif order.type == OrderType.MARKET:
            self.handle_market_order(order)
        elif order.type == OrderType.IOC:
            self.handle_ioc_order(order)

        else:
        # You need to raise the following error if the type of order is ambiguous
            raise UndefinedOrderType("Undefined Order Type!")


    def handle_limit_order(self, order):
        # Implement this function
        # Keep in mind what happens to the orders in the limit order books when orders get filled
        # or if there are no crosses from this order
        # in other words, handle_limit_order accepts an arbitrary limit order that can either be
        # filled if the limit order price crosses the book, or placed in the book. If the latter,
        # pass the order to insert_limit_order below.
        filled_orders = []
        # The orders that are filled from the market order need to be inserted into the above list

        ask_copy = self.ask_book.copy()
        bid_copy = self.bid_book.copy()

        if order.side == OrderSide.BUY:
            if len(ask_copy) == 0:
                self.insert_limit_order(order)

            for i,a in enumerate(ask_copy):
                if order.price > a.price and order.quantity < a.quantity:
                    self.ask_book[0].quantity = a.quantity - order.quantity
                    filled_orders.append(self.ask_book[0])
                    filled_orders.append(order)
                    break

                elif order.price > a.price and order.quantity > a.quantity:
                    order.quantity = order.quantity - a.quantity

                    filled_orders.append(self.ask_book[0])
                    filled_orders.append(order)

                    self.cancel_order(a.id)

                else:
                    self.insert_limit_order(order)
                    break

        elif order.side == OrderSide.SELL:
            if len(bid_copy) == 0:
                self.insert_limit_order(order)

            for i,a in enumerate(bid_copy):
                if order.price < a.price and order.quantity < a.quantity:
                    self.bid_book[0].quantity = a.quantity - order.quantity
                    filled_orders.append(self.bid_book[0])
                    filled_orders.append(order)
                    break

                elif order.price < a.price and order.quantity > a.quantity:
                    order.quantity = order.quantity - a.quantity

                    filled_orders.append(self.bid_book[0])
                    filled_orders.append(order)

                    self.cancel_order(a.id)

                else:
                    self.insert_limit_order(order)
                    break

        # You need to raise the following error if the side the order is for is ambiguous
        else:
            raise UndefinedOrderSide("Undefined Order Side!")

        self.bid_book = sorted(self.bid_book, key = lambda o: [-o.price, o.time])
        self.ask_book = sorted(self.ask_book, key = lambda o: [o.price, o.time])


        # The filled orders are expected to be the return variable (list)
        return filled_orders


    def handle_market_order(self, order):
        # Implement this function
        filled_orders = []
        # The orders that are filled from the market order need to be inserted into the above list
        ask_copy = self.ask_book.copy()
        bid_copy = self.bid_book.copy()
        # The filled orders are expected to be the return variable (list)
        if order.side == OrderSide.BUY:
            for i,a in enumerate(ask_copy):
                if order.quantity < a.quantity:
                    self.ask_book[i].quantity = a.quantity - order.quantity
                    filled_orders.append(self.ask_book[i])
                    filled_orders.append(order)
                    break

                elif order.quantity > a.quantity:

                    filled_orders.append(self.ask_book[i])
                    filled_orders.append(order)

                    self.cancel_order(a.id)

                    break

        elif order.side == OrderSide.SELL:
            for i,a in enumerate(bid_copy):
                if order.quantity < a.quantity:
                    self.bid_book[i].quantity = a.quantity - order.quantity
                    filled_orders.append(self.bid_book[i])
                    filled_orders.append(order)
                    break

                elif order.quantity > a.quantity:

                    filled_orders.append(self.bid_book[i])
                    filled_orders.append(order)

                    self.cancel_order(a.id)

                    break

        # You need to raise the following error if the side the order is for is ambiguous

        else:
            raise UndefinedOrderSide("Undefined Order Side!")

        self.bid_book = sorted(self.bid_book, key = lambda o: [-o.price, o.time])
        self.ask_book = sorted(self.ask_book, key = lambda o: [o.price, o.time])

        return filled_orders


    def handle_ioc_order(self, order):
        # Implement this function
        filled_orders = []
        # The orders that are filled from the ioc order need to be inserted into the above list
        ask_copy = self.ask_book.copy()
        bid_copy = self.bid_book.copy()

        if order.side == OrderSide.BUY:
            for i,a in enumerate(ask_copy):
                if order.price > a.price and order.quantity < a.quantity:
                    self.ask_book[i].quantity = a.quantity - order.quantity
                    filled_orders.append(self.ask_book[i])
                    filled_orders.append(order)
                    break

                elif order.price > a.price and order.quantity > a.quantity:
                    #order.quantity = order.quantity - a.quantity

                    filled_orders.append(self.ask_book[i])
                    filled_orders.append(order)

                    self.cancel_order(a.id)

                    break

                else:
                    break

        elif order.side == OrderSide.SELL:
            for i,a in enumerate(bid_copy):
                if order.price < a.price and order.quantity < a.quantity:
                    self.bid_book[i].quantity = a.quantity - order.quantity
                    filled_orders.append(self.bid_book[i])
                    filled_orders.append(order)
                    break

                elif order.price < a.price and order.quantity > a.quantity:
                    #order.quantity = order.quantity - a.quantity

                    filled_orders.append(self.bid_book[i])
                    filled_orders.append(order)

                    self.cancel_order(a.id)

                    break

                else:
                    break


        # You need to raise the following error if the side the order is for is ambiguous

        else:
            raise UndefinedOrderSide("Undefined Order Side!")

        self.bid_book = sorted(self.bid_book, key = lambda o: [-o.price, o.time])
        self.ask_book = sorted(self.ask_book, key = lambda o: [o.price, o.time])

        # The filled orders are expected to be the return variable (list)
        return filled_orders

    def insert_limit_order(self, order):
        assert order.type == OrderType.LIMIT
        # Implement this function
        # this function's sole puporse is to place limit orders in the book that are guaranteed
        # to not immediately fill

        if order.side == OrderSide.BUY:
            self.bid_book.append(order)
        elif order.side == OrderSide.SELL:
            self.ask_book.append(order)

        # You need to raise the following error if the side the order is for is ambiguous
        else:
            raise UndefinedOrderSide("Undefined Order Side!")

        self.bid_book = sorted(self.bid_book, key = lambda o: [-o.price, o.time])
        self.ask_book = sorted(self.ask_book, key = lambda o: [o.price, o.time])

    def amend_quantity(self, id, quantity):
        # Implement this function
        # Hint: Remember that there are two order books, one on the bid side and one on the ask side
        for idx, order in enumerate(self.bid_book):
            if order.id == id:
                if self.bid_book[idx].quantity <= quantity:
                    raise NewQuantityNotSmaller("Amendment Must Reduce Quantity!")
                self.bid_book[idx].quantity = quantity
        for idx, order in enumerate(self.ask_book):
            if order.id == id:
                if self.ask_book[idx].quantity <= quantity:
                    raise NewQuantityNotSmaller("Amendment Must Reduce Quantity!")
                self.ask_book[idx].quantity = quantity

        self.bid_book = sorted(self.bid_book, key = lambda o: [-o.price, o.time])
        self.ask_book = sorted(self.ask_book, key = lambda o: [o.price, o.time])



        # You need to raise the following error if the user attempts to modify an order
        # with a quantity that's greater than given in the existing order

        #raise NewQuantityNotSmaller("Amendment Must Reduce Quantity!")
        #return False

    def cancel_order(self, id):
        # Implement this function
        # Think about the changes you need to make in the order book based on the parameters given
        for idx, order in enumerate(self.bid_book):
            if order.id == id:
                self.bid_book.remove(order)
        for idx, order in enumerate(self.ask_book):
            if order.id == id:
                self.ask_book.remove(order)

        self.bid_book = sorted(self.bid_book, key = lambda o: [-o.price, o.time])
        self.ask_book = sorted(self.ask_book, key = lambda o: [o.price, o.time])
