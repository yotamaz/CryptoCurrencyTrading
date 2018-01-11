from ccxt_wrapper.ccxt_wrapper import CcxtWrapper
from market import Market
from time import sleep


class Exchange:
    def __init__(self,exgid):
        self.wrapper = CcxtWrapper()
        self.exg = self.wrapper.getexchange(exgid)
        self.markets = self.getmarkets()
        self.delay = 2

    def getmarkets(self,reload = False):
        return self.exg.load_markets (reload)

    def fetch_order_book(self,symbols=None):
        order_book = {}
        if symbols==None: symbols = self.markets
        for symbol in symbols:
            order_book[symbol] = self.exg.fetch_order_book(symbol)
            sleep(self.delay)
        return order_book