from ELconn import ES_CONNECTION, create_event, search


def addEventEntry(flag, additionalData={}, connection=ES_CONNECTION):
    for key in flag.__dict__.keys():
        additionalData[key] = flag.__dict__[key]
    return create_event(additionalData, connection=connection)


def getFlagsByEvent(event, size=100, page=0, connection=ES_CONNECTION):
    return getDataByEvent(event, size, page, connection=connection)


def numberOfEntries(event, flag, connection=ES_CONNECTION):
    body = {"query": { "bool": { "must": [ {"term": { "flag": flag}}, {"term": { "event": event}}]}}}
    data = search(body, size=0, connection=connection)
    return data["hits"]["total"]


def getDataByEvent(event, size=100, page=0, connection=ES_CONNECTION):
    body = {"query":{ "term": { "event": event }}}
    res = search(body, size, page, connection=connection)
    return map(lambda hit: hit['_source'], res['hits']['hits'])


def getDataByFlag(flag, size=100, page=0, connection=ES_CONNECTION):
    body={"query":{ "term": { "flag": flag }}}
    res = search(body, size, page, connection=connection)
    return map(lambda hit: hit['_source'], res['hits']['hits'])


def getDataByFlagAndEvent(flag, event, size=100, page=0, connection=ES_CONNECTION):
    body= {"query": { "bool": { "must": [ {"term": { "flag": flag}}, {"term": { "event": event}}]}}}
    res = search(body, size, page, connection=connection)
    return map(lambda hit: hit['_source'], res['hits']['hits'])