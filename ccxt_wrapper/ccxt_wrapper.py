import ccxt

class CcxtWrapper:
    def __init__(self):
        pass

    def getallexchanges(self):
        return ccxt.exchanges

    def getexchange(self,exgid):
        try:
            exg = getattr(ccxt,exgid)()
            return exg
        except :
            print("getexchanfe failed %s"%exgid)

    def getmarket(self,exg):
        pass

