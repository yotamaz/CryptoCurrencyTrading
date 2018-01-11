from elasticsearch import Elasticsearch,ElasticsearchException
import sys
from datetime import datetime



class myElasticSearch:
    size = 30
    doc_type = 'base_type'
    lastruning = "last_runing"
    redis_tracker_type="redis_tracker"
    tag_doc_type = "tag_doc"
    def __init__(self,ipvec,subname,timezone):
        self.timezone = timezone
        self.subname = subname
        self._to = datetime.now()
        self.ipvec = ipvec
        if ipvec[0] == "localhost":
            print(ipvec)
            self.myes = Elasticsearch(timeout=50, max_retries=10, retry_on_timeout=True)
            self.ip = u'127.0.0.1'
        else:
            self.myes = Elasticsearch(ipvec,sniff_on_start=True,sniff_on_connection_fail=True,sniffer_timeout=60,timeout=60,max_retries=15,retry_on_timeout=True)

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

    def ExistsDoc(self,id,_doc_type,_index):
        try:
            e= self.myes.exists(index=_index,doc_type=_doc_type,id=id)
        except ElasticsearchException as es1:
            sys.exit("ExistsDoc_field_m_{0}".format(es1.error))
        return e

    def setindexes(self,docs,_index,_type):
        _docs = []
        for doc in docs:
            ESind = {"index": {"_index": _index, "_type": _type}}
            empty_keys = [k for k, v in doc.items() if not v!=None]
            for k in empty_keys:
                del doc[k]
            _docs.extend([ESind,doc])
        return _docs

    def push(self,bulk_data,_index,_type="basic"):
        try:
            docs = self.setindexes(bulk_data,_index,_type)
            res = self.myes.bulk(index = _index, body = docs, refresh = True)
            ervec = []
            if res["errors"]:
                for doc in res["items"]:
                    if doc[u'index'][u'status'] != 201:
                        ervec.append("_push:{0} - {1}".format(doc[u'index'][u'error'][u'reason'],
                                                              doc[u'index'][u'error'][u'type']))
        except ElasticsearchException as es1:
            sys.exit("Push-{0}".format(es1.error))
        return ervec

