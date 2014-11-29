from elasticsearch import Elasticsearch

ES_INDEX="ctf-submitter"
ES_TYPE_EVENT="event"
ES_HOST="localhost"
ES_PORT=9200

def createConnection():
    return ElasticSearch([{"host": ES_HOST, "port": ES_PORT}])


def addEventEntry(connection, event, flag, additionalData={}):
    additionalData["event"] = event
    additionalData["flag"] = flag
    return _createEvent(connection, additionalData)


def getEvents( event, flag ):
    pass


def _createEvent(connection, data):
    res = connection.index(index=ES_INDEX, doc_type=ES_TYPE_EVENT, body=data)
    return res['_id']
