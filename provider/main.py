from provider.provider import Provider
from eslog.eslog import ESlog
import  time
if __name__ == '__main__':
    p = Provider()
    eslog = ESlog("localhost", "test", "UTC")
    while True:
        start = time.time()
        data = p.get_data()
        done = time.time()
        took = done - start
        eslog.linfo({"took":took,"m":"session end"})
        time.sleep(10*60)
        print("stop","data")