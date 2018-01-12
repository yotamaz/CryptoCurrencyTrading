import pandas as pd
import time
from provider.provider import Provider
from eslog.eslog import ESlog
if __name__ == '__main__':
    p = Provider()
    eslog = ESlog("localhost", "test", "UTC")
    while True:
        start = time.time()
        p.get_data()
        done = time.time()
        took = done - startjn
        eslog.linfo({"took": took, "m": "session end"})
        print("asdasd")
        print("stop", "data")