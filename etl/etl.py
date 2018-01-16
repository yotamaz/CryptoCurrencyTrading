from DB.elasticsearch.elasticsearch import myElasticSearch
from configobj import ConfigObj
import os


class ETL:
    def __init__(self):
        self.base_path = os.getcwd()
        self.conf = ConfigObj(self.base_path + "{sep}provider{sep}config.ini".format(sep=os.path.sep))
        self.es = myElasticSearch(self.conf['elasticsearch']['host'], "yotam", "UTC")

