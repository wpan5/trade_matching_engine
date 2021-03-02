import unittest

class TestOrderBook(unittest.TestCase):

    def test_insert_limit_order(self):
        matching_engine = MatchingEngine()
        order = LimitOrder(1, "S", 10, 10, OrderSide.BUY, time.time())
        matching_engine.insert_limit_order(order)

        self.assertEqual(matching_engine.bid_book[0].quantity, 10)
        self.assertEqual(matching_engine.bid_book[0].price, 10)

    def test_handle_limit_order(self):
        matching_engine = MatchingEngine()
        order = LimitOrder(1, "S", 10, 10, OrderSide.BUY, time.time())
        matching_engine.insert_limit_order(order)

        order_1 = LimitOrder(2, "S", 5, 10, OrderSide.BUY, time.time())
        order_2 = LimitOrder(3, "S", 10, 15, OrderSide.BUY, time.time())
        matching_engine.handle_limit_order(order_1)
        matching_engine.handle_limit_order(order_2)

        self.assertEqual(matching_engine.bid_book[0].price, 15)
        self.assertEqual(matching_engine.bid_book[1].quantity, 10)

        order_sell = LimitOrder(4, "S", 14, 8, OrderSide.SELL, time.time())
        filled_orders = matching_engine.handle_limit_order(order_sell)

        self.assertEqual(matching_engine.bid_book[0].quantity, 6)
        self.assertEqual(filled_orders[0].id, 3)
        self.assertEqual(filled_orders[0].price, 15)
        self.assertEqual(filled_orders[2].id, 1)
        self.assertEqual(filled_orders[2].price, 10)

    def test_handle_market_order(self):
        matching_engine = MatchingEngine()
        order_1 = LimitOrder(1, "S", 6, 10, OrderSide.BUY, time.time())
        order_2 = LimitOrder(2, "S", 5, 10, OrderSide.BUY, time.time())
        matching_engine.handle_limit_order(order_1)
        matching_engine.handle_limit_order(order_2)

        order = MarketOrder(5, "S", 5, OrderSide.SELL, time.time())
        filled_orders = matching_engine.handle_market_order(order)
        self.assertEqual(matching_engine.bid_book[0].quantity, 1)
        self.assertEqual(filled_orders[0].price, 10)

    def test_handle_ioc_order(self):
        matching_engine = MatchingEngine()
        order_1 = LimitOrder(1, "S", 1, 10, OrderSide.BUY, time.time())
        order_2 = LimitOrder(2, "S", 5, 10, OrderSide.BUY, time.time())
        matching_engine.handle_limit_order(order_1)
        matching_engine.handle_limit_order(order_2)

        order = IOCOrder(6, "S", 5, 12, OrderSide.SELL, time.time())
        filled_orders = matching_engine.handle_ioc_order(order)
        self.assertEqual(matching_engine.bid_book[0].quantity, 1)
        self.assertEqual(len(filled_orders), 0)

    def test_amend_quantity(self):
        matching_engine = MatchingEngine()
        order_1 = LimitOrder(1, "S", 5, 10, OrderSide.BUY, time.time())
        order_2 = LimitOrder(2, "S", 10, 15, OrderSide.BUY, time.time())
        matching_engine.handle_limit_order(order_1)
        matching_engine.handle_limit_order(order_2)

        matching_engine.amend_quantity(2, 8)
        self.assertEqual(matching_engine.bid_book[0].quantity, 8)

    def test_cancel_order(self):
        matching_engine = MatchingEngine()
        order_1 = LimitOrder(1, "S", 5, 10, OrderSide.BUY, time.time())
        order_2 = LimitOrder(2, "S", 10, 15, OrderSide.BUY, time.time())
        matching_engine.handle_limit_order(order_1)
        matching_engine.handle_limit_order(order_2)

        matching_engine.cancel_order(1)
        self.assertEqual(matching_engine.bid_book[0].id, 2)
