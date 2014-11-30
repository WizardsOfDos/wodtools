from elasticsearch import Elasticsearch
from flag import Flag

ES_INDEX="ctf-submitter"
ES_TYPE_EVENT="event"
ES_HOST="localhost"
ES_PORT=9200

def createConnection():
    return ElasticSearch([{"host": ES_HOST, "port": ES_PORT}])


def addEventEntry(connection, flag, additionalData={}):
    for key in flag.__dict__.keys():
        additionalData[key] = flag.__dict__[key]
    return _createEvent(connection, additionalData)


def getFlagsByEvent(connection, event, size=100, page=0 ):
    data = getDataByEvent(connection, event, size, page)
    return map(Flag.fromDict, data)


def numberOfEntries(connection, event, flag):
    body = {"query": { "bool": { "must": [ {"term": { "flag": flag}}, {"term": { "event": event}}]}}}
    data = _search(connection, body, size=0)
    return data["hits"]["total"]


def getDataByEvent(connection, event, size=100, page=0):
    body = {"query":{ "term": { "event": event }}}
    res = _search(connection, body, size, page)
    return map(lambda hit: hit['_source'], res['hits']['hits'])


def getDataByFlag(connection, flag, size=100, page=0):
    body={"query":{ "term": { "flag": flag }}}
    res = _search(connection, body, size, page)
    return map(lambda hit: hit['_source'], res['hits']['hits'])


def getDataByFlagAndEvent(connection, flag, event, size=100, page=0):
    body= {"query": { "bool": { "must": [ {"term": { "flag": flag}}, {"term": { "event": event}}]}}}
    res = _search(connection, body, size, page)
    return map(lambda hit: hit['_source'], res['hits']['hits'])


def _createEvent(connection, data):
    res = connection.index(index=ES_INDEX, doc_type=ES_TYPE_EVENT, body=data)
    return res['_id']


def _search(connection, body, size=100, page=0):
    return connection.search( index=ES_INDEX, doc_type=ES_TYPE_EVENT, body=body, size=size, page=page)
