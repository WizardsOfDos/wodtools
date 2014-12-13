import os

from elasticsearch import Elasticsearch
from flask.config import Config  # reusing flasks config system

from ELconn import config_default

config = Config(os.path.dirname(os.path.abspath(__file__)))
config.from_object(config_default)
config.from_envvar('ELconn.config', True)


def create_connection(**kwargs):
    conn_config = {"host": config['ES_HOST'], "port": config['ES_PORT']}
    conn_config.update(kwargs)
    return Elasticsearch([conn_config])


ES_CONNECTION = create_connection()


def add(data, connection=ES_CONNECTION, index=config['ES_INDEX'], **kwargs):
    res = connection.index(index=index, body=data, doc_type=config['ES_TYPE_EVENT'], **kwargs)
    return res['_id']


def search(body, size=100, skip=0, connection=ES_CONNECTION, index=config['ES_INDEX'], **kwargs):
    return connection.search(index=index, body=body, size=size, from_=skip,
                             doc_type=config['ES_TYPE_EVENT'], **kwargs)