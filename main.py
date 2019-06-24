#!/usr/bin/python3
import time

from mongo import insert, earlyReply
from utils import get_thread_list, client_Post

bduss = ''
kw = ''
fid = ''

if __name__ == '__main__':

    while True:
        list = get_thread_list(aim_tieba=kw)
        for topic in list:
            if not earlyReply(topic['tid']):
                print(topic)
                insert(tid=topic['tid'], pid=topic['pid'], topic=topic['topic'], nickname=topic['nickname'])
                client_Post(bduss=bduss, kw=kw, fid=fid, tid=topic['tid'], content=topic['nickname'] + "，很高兴见到你!")
        # 间隔
        time.sleep(120)
