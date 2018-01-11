from ccxt_wrapper.ccxt_wrapper import CcxtWrapper
from exchange import Exchange
import pandas as pd
class Manager():
    def __init__(self):
        self.wccxt = CcxtWrapper()

    def getexgsid(self):
        return self.wccxt.getallexchanges()

    def session(self):
        exgs = self.wccxt.getallexchanges()
        df = pd.DataFrame()
        for exg in exgs:
            exchange = Exchange(exg)
            order_book = exchange.fetch_order_book()
            df.append(order_book)
            order_bookdf = pd.DataFrame(order_book)
            print("aa")
