import time
from eslog.eslog import ESlog
from ccxt_wrapper.ccxt_wrapper import CcxtWrapper
from multiprocessing.pool import ThreadPool
from DB.elasticsearch.elasticsearch import myElasticSearch
import os
from configobj import ConfigObj

class Provider:
    def __init__(self):
        self.base_path = os.getcwd()
        self.conf = ConfigObj(self.base_path + "{sep}provider{sep}config.ini".format(sep=os.path.sep))

        self.cw = CcxtWrapper()
        self.eslog = ESlog("localhost","test","UTC")
        self.exgs = self.conf['exgs']

    def get_exgs_providers(self,exgs):
        pass

    @staticmethod
    def get_ticker(exchange,exgname,symbol,all=True):
        if all:
            ticker = exchange.fetch_tickers()
            for d in ticker.values():
                d["exchange"] = exgname
                d["doc_type"] = "ticker"
        else:
            ticker = exchange.fetch_ticker(symbol)
            ticker['exchange'] = exgname
            ticker["doc_type"] = "ticker"
        return ticker

    @staticmethod
    def get_orderbook(exchange,exgname,symbol):
        orderbook = exchange.fetch_order_book(symbol)
        docs = []
        for i in ['bids', 'asks']:
            for order in orderbook[i]:
                docs.append({"datetime": orderbook['datetime'], 'timestamp': orderbook['timestamp'], i: order[0],
                     'amount': order[1], 'symbol': symbol, 'exchange': exgname, "doc_type": "order_book"})
        return docs

    @staticmethod
    def get_exchange_data(exgname,ues=True):
        cw = CcxtWrapper()
        exchange = cw.getexchange(exgname)
        if ues:
            es = myElasticSearch("localhost", "yotam", "UTC")
        eslog = ESlog("localhost", "test", "UTC")
        delay = 2
        exg = {"name": exgname, "data": {'orderbook': [], 'ticker': {}}}
        try:
            symbols = exchange.load_markets()
            eslog.linfo({"lib": "provider", "m": "got symbols", "exchange": exgname, "numsymbols": len(symbols)})
        except:
            eslog.lerror({"lib": "provider", "m": "couldnt get symbols", "exchange": exgname})
            return exg
        try:
            exg["data"]['ticker']= Provider.get_ticker(exchange,exgname,None,True)
            ft = False
        except:
            ft = True
        ns = 0
        for symbol in symbols:
            ns += 1
            exg["data"]['ticker'][symbol] = {}
            try:
                exg["data"]['orderbook'].extend(Provider.get_orderbook(exchange,exgname,symbol))
                time.sleep(delay)
            except:
                eslog.lerror({"lib": "provider", "m": "couldnt get orderbook", "exchange": exgname, "symbol": symbol})
            if ft:
                try:
                    exg["data"]['ticker'][symbol] = Provider.get_ticker(exchange,exgname,symbol,False)
                    time.sleep(delay)
                except:
                    eslog.lerror({"lib": "provider", "m": "couldnt get ticker", "exchange": exgname, "symbol": symbol})
            if ns > 15:
                break
        if ues:
            es.push(exg["data"]['orderbook'], time.strftime(u"{0}-{1}-%Y.%W".format("data","yotam")))
            es.push(list(exg["data"]['ticker'].values()), time.strftime(u"{0}-{1}-%Y.%W".format("data","yotam")))
        return exg

    def get_data(self):
        args = []
        for exg in self.exgs:
            self.get_exchange_data(exg)
            args.append((exg))
        pool = ThreadPool()
        mymap = pool.map_async(self.get_exchange_data, args)
        time.sleep(1)
        pool.close()
        mymap.wait()
        pool.join()
