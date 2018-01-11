import time
import datetime

from elasticsearch import Elasticsearch, ElasticsearchException


class ESlog:
    size = 30
    doc_type = 'base_type'
    def __init__(self,ipvec,subname,timezone):
        self.timezone = timezone
        self.subname = subname
        self.logindex = time.strftime(u"log-{subname}-%Y.%W".format(subname = subname))
        self._to = datetime.datetime.now()
        self.ipvec = ipvec
        if ipvec[0] == "localhost":
            self.myes = Elasticsearch(timeout=50, max_retries=10, retry_on_timeout=True)
            self.ip=u'127.0.0.1'
        else:
            self.myes = Elasticsearch(ipvec,
                                      sniff_on_start=True,
                                      sniff_on_connection_fail=True,
                                      sniffer_timeout=60,
                                      timeout=30,
                                      max_retries=10,
                                      retry_on_timeout=True)
        self.info = self.myes.info()

    def linfo(self,m):
        doc = {"event_type":"info",
               "e":m,
               "seat":self.subname,
               "ptimestemp":self._to,
               "timestemp":datetime.datetime.now()}
        try:
            print(doc)
            r = self.myes.index(self.logindex,"log",doc)
        except ElasticsearchException as es1:
            print("could not push info doc to loges {0}".format(es1))
            if 'Unable to sniff hosts.' in es1.args:
                self.reconnect()
                self.linfo(m)
            self.lerror({"message": "could_not_push_info_doc_to_loges_{0}".format(es1.error), "event_code": "401"})

    def lerror(self,m):
        doc = {"event_type":"error",
               "e":m,
               "seat":self.subname,
               "ptimestemp":self._to,
               "timestemp":datetime.datetime.now()}
        try:
            print(doc)
            r = self.myes.index(self.logindex,"log",doc)
        except ElasticsearchException as es1:
            print("could not push error doc to loges {0}".format(es1))
            if 'Unable to sniff hosts.' in es1.args:
                self.reconnect()
                self.lerror(m)
            self.lerror({"message": "could_not_push_error_doc_to_loges_{0}".format(es1.error), "event_code": "400"})

    def lwarning(self,m):
        doc = {"event_type":"warning",
               "e":m,
               "seat":self.subname,
               "ptimestemp":self._to,
               "timestemp":datetime.datetime.now()}
        try:
            print(doc)
            r = self.myes.index(self.logindex,"log",doc)
        except ElasticsearchException as es1:
            if 'Unable to sniff hosts.' in es1.args:
                self.reconnect()
                self.lwarning(m)
            self.lerror({"message": "could_not_push_warning_doc_to_loges_{0}".format(es1.error), "event_code": "402"})

    def ldebug(self,m):
        doc = {"event_type":"debug",
               "e":m,
               "seat":self.subname,
               "ptimestemp":self._to,
               "timestemp":datetime.datetime.now()}
        try:
            print(doc)
            r = self.myes.index(self.logindex,"log",doc)
        except ElasticsearchException as es1:
            print("could not push debugdoc to loges {0}".format(es1.error))
            if es1.error == 'Unable to sniff hosts.':
                self.reconnect()
                self.ldebug(m)

    def reconnect(self):
        if self.ipvec[0] =="0":
            self.myes = Elasticsearch(timeout=50, max_retries=10, retry_on_timeout=True)
            self.ip=u'127.0.0.1'
        else:
            self.myes = Elasticsearch(self.ipvec,
                              sniff_on_start=True,
                              sniff_on_connection_fail=True,
                              sniffer_timeout=60,
                              timeout=30,
                              max_retries=10,
                              retry_on_timeout=True)