# trade_matching_engine



You will create the class MatchingEngine capable of handling incoming orders and matching orders.
You will need to handle 3 types of orders:
- Limit order
- Market order
- Immediate or Cancel

def handle_order(order), function in charge of handling any types of orders in the matching engine
def handle_limit_order(order), def handle_market_order(order), def handle_ioc_order(order)

This class will have a container of your choice for bids and offers.

Please consider that a limit order A of a quantity QA can be matched with another order B of a quantity QB:
- if QA<QB, B will be partially filled, and the amount left for A will be QB-QA
- if QA>QB, comparable to prior case
- if QA=QB, A and B will be fully-filled

To succeed this part, you will need to show evidence that the different orders and different cases work. For that you are required to use unit testing.
Coming from this library:

https://docs.python.org/3.6/library/unittest.html
