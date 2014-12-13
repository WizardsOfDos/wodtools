from enum import Enum
from datetime import datetime
import os

import ELconn
from ELconn import ES_CONNECTION

config = ELconn.Config(os.path.dirname(os.path.abspath(__file__)), defaults=ELconn.config)
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


def add_event_DUPLICATE(flag, result, **kwargs):
    return add_event(flag, event_type=EventTypes.DUPLICATE, result=result, **kwargs)


def get_events_count(flag, event_type, **kwargs):
    event_type = event_type.name if isinstance(event_type, EventTypes) else event_type
    body = {"query": { "bool": { "must": [ {"term": { "flag": flag}}, {"term": { "event": event_type}}]}}}
    data = ELconn.search(body, size=0, **kwargs)
    return data["hits"]["total"]


def get_events_count_ENTRY(flag, **kwargs):
    return get_events_count(flag, event_type=EventTypes.ENTRY)

# not so much cleaned up below here; also: NOT TESTED!

def getFlagsByEvent(event, size=100, skip=0):
    return getDataByEvent(event, size, skip)


def getDataByEvent(event, size=100, skip=0):
    body = {"query":{ "term": { "event": event }}}
    res = ELconn.search(body, size, skip, connection=ES_CONNECTION)
    return map(lambda hit: hit['_source'], res['hits']['hits'])


def getDataByFlag(flag, size=100, skip=0):
    body={"query":{ "term": { "flag": flag }}}
    res = ELconn.search(body, size, skip, connection=ES_CONNECTION)
    return map(lambda hit: hit['_source'], res['hits']['hits'])


def getDataByFlagAndEvent(flag, event, size=100, skip=0):
    body= {"query": { "bool": { "must": [ {"term": { "flag": flag}}, {"term": { "event": event}}]}}}
    res = ELconn.search(body, size, skip, connection=ES_CONNECTION)
    return map(lambda hit: hit['_source'], res['hits']['hits'])