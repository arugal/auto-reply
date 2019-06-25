#!/usr/bin/python3

import pymongo
from configparser import ConfigParser

__cfg = ConfigParser()
__cfg.read('config.ini')

__client = pymongo.MongoClient(host=__cfg.get('server', 'mongo.ip'), port=__cfg.getint('server', 'mongo.port'))
__db = __client['auto_reply']
__collection = __db['early_reply']


def insert(tid, pid, topic, nickname):
    """
    回复记录
    :param tid:
    :param pid:
    :param topic:
    :param nickname:
    :return:
    """
    topic = {
        '_id': tid,
        'pid': pid,
        'topic': topic,
        'nickname': nickname,
    }
    __collection.insert(topic)


def get(tid):
    return __collection.find_one({'_id': tid})


def earlyReply(tid):
    return get(tid) != None
