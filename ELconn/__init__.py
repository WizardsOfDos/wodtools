import os

from elasticsearch import Elasticsearch
from flask.config import Config  # reusing flasks config system

from ELconn import config_default

config = Config(os.environ)
config.from_object(config_default)
config.from_envvar('ELconn.config', True)


def create_connection(**kwargs):
    conn_config = {"host": config['ES_HOST'], "port": config['ES_PORT']}
    conn_config.update(kwargs)
    return Elasticsearch([conn_config])


ES_CONNECTION = create_connection()


def create_event(data, connection=ES_CONNECTION):
    res = connection.index(index=config['ES_INDEX'], doc_type=config['ES_TYPE_EVENT'], body=data)
    return res['_id']


def search(body, size=100, page=0, connection=ES_CONNECTION):
    return connection.search(index=config['ES_INDEX'], doc_type=config['ES_TYPE_EVENT'],
                             body=body, size=size, page=page)