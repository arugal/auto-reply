#!/usr/bin/python3
import time

from mongo import insert, earlyReply
from utils import get_thread_list, client_Post, compare
from configparser import ConfigParser

__cfg = ConfigParser()
__cfg.read('config.ini')

bduss = __cfg.get('topic', 'bduss')
kw = __cfg.get('topic', 'kw')
fid = __cfg.get('topic', 'fid')
interval = __cfg.getint('server', 'scan.interval')

if __name__ == '__main__':
    while True:
        list = get_thread_list(aim_tieba=kw)
        for topic in list:
            if not earlyReply(topic['tid']):
                if compare(topic['tid']):
                    print(topic)
                    insert(tid=topic['tid'], pid=topic['pid'], topic=topic['topic'], nickname=topic['nickname'])
                    client_Post(bduss=bduss, kw=kw, fid=fid, tid=topic['tid'], content='微笑了吗今天')
        # 间隔
        time.sleep(interval)
