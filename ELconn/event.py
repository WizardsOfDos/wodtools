from enum import Enum
from datetime import datetime

import ELconn
from ELconn import ES_CONNECTION

config = ELconn.Config(ELconn.config)
config.update(ES_INDEX='flag_event')
config.from_envvar('ELconn.event.config', True)


class EventTypes(Enum):
    UNKNOWN = None,
    ENTRY = 0,
    DUPLICATE = -1,
    SUBMIT = 10,


def add_event(flag, event_type=EventTypes.UNKNOWN, **additional_data):
    additional_data.update(flag=flag,
                           event_type=event_type.name if isinstance(event_type, EventTypes) else event_type)
    return ELconn.add(additional_data, timestamp=datetime.now(),
                      connection=ES_CONNECTION, index=config['ES_INDEX'])


def add_event_ENTRY(flag, team=None, service=None, **kwargs):
    return add_event(flag, event_type=EventTypes.ENTRY, team=team, service=service, **kwargs)


def add_event_SUBMIT(flag, result, **kwargs):
    return add_event(flag, event_type=EventTypes.SUBMIT, result=result, **kwargs)

# not so much cleaned up below here; also: NOT TESTED!

def getFlagsByEvent(event, size=100, page=0):
    return getDataByEvent(event, size, page)


def numberOfEntries(event, flag):
    body = {"query": { "bool": { "must": [ {"term": { "flag": flag}}, {"term": { "event": event}}]}}}
    data = ELconn.search(body, size=0, connection=ES_CONNECTION)
    return data["hits"]["total"]


def getDataByEvent(event, size=100, page=0):
    body = {"query":{ "term": { "event": event }}}
    res = ELconn.search(body, size, page, connection=ES_CONNECTION)
    return map(lambda hit: hit['_source'], res['hits']['hits'])


def getDataByFlag(flag, size=100, page=0):
    body={"query":{ "term": { "flag": flag }}}
    res = ELconn.search(body, size, page, connection=ES_CONNECTION)
    return map(lambda hit: hit['_source'], res['hits']['hits'])


def getDataByFlagAndEvent(flag, event, size=100, page=0):
    body= {"query": { "bool": { "must": [ {"term": { "flag": flag}}, {"term": { "event": event}}]}}}
    res = ELconn.search(body, size, page, connection=ES_CONNECTION)
    return map(lambda hit: hit['_source'], res['hits']['hits'])