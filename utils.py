#!/usr/bin/python3

import requests
import re
import hashlib
import time


def get_tbs(bduss):
    # 获取tbs
    headers = {
        'Host': 'tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'Cookie': 'BDUSS=' + bduss,
    }
    url = 'http://tieba.baidu.com/dc/common/tbs'
    return requests.get(url=url, headers=headers).json()['tbs']


def get_name(bduss):
    # 网页版获取贴吧用户名
    headers = {
        'Host': 'tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'Cookie': 'BDUSS=' + bduss,
    }
    url = 'https://tieba.baidu.com/mo/q-'
    try:
        r = requests.get(url=url, headers=headers).text
        name = re.search(r">([\u4e00-\u9fa5a-zA-Z0-9]+)的i贴吧<", r).group(1)
    except Exception:
        name = None
    finally:
        return name


def get_at(bduss):
    data = {
        'BDUSS': bduss,
        '_client_type': '2',
        '_client_id': 'wappc_1534235498291_488',
        '_client_version': '9.7.8.0',
        '_phone_imei': '000000000000000',
        'from': '1008621y',
        'page_size': '3000',
        'model': 'MI+5',
        'net_type': '1',
        'timestamp': str(int(time.time())),
        'vcode_tag': '11',
    }
    data = encodeData(data)
    url = 'http://c.tieba.baidu.com/c/u/feed/atme'
    res = requests.post(url=url, data=data).json()
    return res


def get_favorite(bduss):
    # 客户端关注的贴吧
    returnData = {}
    i = 1
    data = {
        'BDUSS': bduss,
        '_client_type': '2',
        '_client_id': 'wappc_1534235498291_488',
        '_client_version': '9.7.8.0',
        '_phone_imei': '000000000000000',
        'from': '1008621y',
        'page_no': '1',
        'page_size': '200',
        'model': 'MI+5',
        'net_type': '1',
        'timestamp': str(int(time.time())),
        'vcode_tag': '11',
    }
    data = encodeData(data)
    url = 'http://c.tieba.baidu.com/c/f/forum/like'
    res = requests.post(url=url, data=data, timeout=2).json()
    returnData = res
    if 'forum_list' not in returnData:
        returnData['forum_list'] = []
    if res['forum_list'] == []:
        return {'gconforum': [], 'non-gconforum': []}
    if 'non-gconforum' not in returnData['forum_list']:
        returnData['forum_list']['non-gconforum'] = []
    if 'gconforum' not in returnData['forum_list']:
        returnData['forum_list']['gconforum'] = []
    while 'has_more' in res and res['has_more'] == '1':
        i = i + 1
        data = {
            'BDUSS': bduss,
            '_client_type': '2',
            '_client_id': 'wappc_1534235498291_488',
            '_client_version': '9.7.8.0',
            '_phone_imei': '000000000000000',
            'from': '1008621y',
            'page_no': str(i),
            'page_size': '200',
            'model': 'MI+5',
            'net_type': '1',
            'timestamp': str(int(time.time())),
            'vcode_tag': '11',
        }
        data = encodeData(data)
        url = 'http://c.tieba.baidu.com/c/f/forum/like'
        res = requests.post(url=url, data=data, timeout=2).json()
        if 'non-gconforum' in res['forum_list']:
            returnData['forum_list']['non-gconforum'].append(res['forum_list']['non-gconforum'])
        if 'gconforum' in res['forum_list']:
            returnData['forum_list']['gconforum'].append(res['forum_list']['gconforum'])
    return returnData


def get_fid(bdname):
    # 获取贴吧对用的fourm id
    url = 'http://tieba.baidu.com/f/commit/share/fnameShareApi?ie=utf-8&fname=' + str(bdname)
    fid = requests.get(url, timeout=2).json()['data']['fid']
    return fid


def Post(bduss, content, tid, fid, tbname):
    # 网页版回帖
    tbs = get_tbs(bduss)
    headers = {
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        'Connection': "keep-alive",
        'Content-Type': "application/x-www-form-urlencoded;charset=UTF-8",
        'Cookie': 'BDUSS=' + bduss,
        'DNT': '1',
        'Host': 'tieba.baidu.com',
        'Origin': 'https://tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data = {
        'ie': 'utf-8',
        'kw': tbname,
        'fid': fid,
        'tid': tid,
        'tbs': tbs,
        '__type__': 'reply',
        'content': content,
    }
    url = 'https://tieba.baidu.com/f/commit/post/add'
    r = requests.post(url=url, data=data, headers=headers, timeout=2).json()
    return r


def get_qid(tid, floor):
    # 获取楼中楼的qid参数
    floor = int(floor)
    headers = {
        'Host': 'tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    }
    page = floor // 20 + 1
    url = 'https://tieba.baidu.com/p/' + str(tid) + '?pn=' + str(page)
    res = requests.get(url=url, headers=headers, timeout=2).text
    qid = re.findall(r"post_content_(\d+)", res)
    try:
        return qid[floor - 1]
    except Exception:
        return qid[len(qid) - 1]


def get_kw(tid):
    # 通过tid获取贴吧名字
    headers = {
        'Host': 'tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    }
    url = 'https://tieba.baidu.com/p/' + str(tid)
    res = requests.get(url=url, headers=headers, timeout=2).text
    kw = re.search("fname=\"([^\"]+)\"", res).group(1)
    return kw


def LZL(bduss, content, kw, fid, tid, qid, floor):
    # 网页端楼中楼
    tbs = get_tbs(bduss)
    headers = {
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        'Connection': "keep-alive",
        'Content-Type': "application/x-www-form-urlencoded;charset=UTF-8",
        'Cookie': 'BDUSS=' + bduss,
        'DNT': '1',
        'Host': 'tieba.baidu.com',
        'Origin': 'https://tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data = {
        'ie': 'utf-8',
        'kw': kw,
        'fid': fid,
        'tid': tid,
        'tbs': tbs,
        'quote_id': qid,
        'floor_num': floor,
        'content': content,
    }
    url = 'https://tieba.baidu.com/f/commit/post/add'
    r = requests.post(url=url, data=data, headers=headers, timeout=2).json()
    return r


def client_LZL(bduss, kw, fid, content, quote_id, tid):
    # 客户端楼中楼
    tbs = get_tbs(bduss)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'ka=open',
        'User-Agent': 'bdtb for Android 9.7.8.0',
        'Connection': 'close',
        'Accept-Encoding': 'gzip',
        'Host': 'c.tieba.baidu.com',
    }

    data = {
        'BDUSS': bduss,
        '_client_type': '2',
        '_client_id': 'wappc_1534235498291_488',
        '_client_version': '9.7.8.0',
        '_phone_imei': '000000000000000',
        'anonymous': '1',
        'content': content,
        'fid': fid,
        'kw': kw,
        'model': 'MI+5',
        'net_type': '1',
        'new_vcode': '1',
        'post_from': '3',
        'quote_id': quote_id,
        'tbs': tbs,
        'tid': tid,
        'timestamp': str(int(time.time())),
        'vcode_tag': '12',
    }
    data = encodeData(data)
    url = 'http://c.tieba.baidu.com/c/c/post/add'
    res = requests.post(url=url, data=data, headers=headers, timeout=2).json()
    return res


def encodeData(data):
    SIGN_KEY = 'tiebaclient!!!'
    s = ''
    keys = data.keys()
    for i in sorted(keys):
        s += i + '=' + str(data[i])
    sign = hashlib.md5((s + SIGN_KEY).encode('utf-8')).hexdigest().upper()
    data.update({'sign': str(sign)})
    return data


def client_Post(bduss, kw, tid, fid, content):
    # 客户端回帖模式
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'ka=open',
        'User-Agent': 'bdtb for Android 9.7.8.0',
        'Connection': 'close',
        'Accept-Encoding': 'gzip',
        'Host': 'c.tieba.baidu.com',
    }

    data = {
        'BDUSS': bduss,
        '_client_type': '2',
        '_client_version': '9.7.8.0',
        '_phone_imei': '000000000000000',
        'anonymous': '1',
        'content': content,
        'fid': fid,
        'from': '1008621x',
        'is_ad': '0',
        'kw': kw,
        'model': 'MI+5',
        'net_type': '1',
        'new_vcode': '1',
        'tbs': get_tbs(bduss),
        'tid': tid,
        'timestamp': str(int(time.time())),
        'vcode_tag': '11',
    }
    data = encodeData(data)
    url = 'http://c.tieba.baidu.com/c/c/post/add'
    a = requests.post(url=url, data=data, headers=headers, timeout=2).json()
    return a


def client_Sign(bduss, kw, fid, tbs):
    # 客户端签到
    url = "http://c.tieba.baidu.com/c/c/forum/sign"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'ka=open',
        'User-Agent': 'bdtb for Android 9.7.8.0',
        'Connection': 'close',
        'Accept-Encoding': 'gzip',
        'Host': 'c.tieba.baidu.com',
    }
    data = {
        "BDUSS": bduss,
        '_client_type': '2',
        '_client_version': '9.7.8.0',
        '_phone_imei': '000000000000000',
        "fid": fid,
        'kw': kw,
        'model': 'MI+5',
        "net_type": "1",
        'tbs': tbs,
        'timestamp': str(int(time.time())),
    }
    data = encodeData(data)
    url = 'http://c.tieba.baidu.com/c/c/forum/sign'
    res = requests.post(url=url, data=data, timeout=1).json()
    return res


def check(bduss):
    # 检查bduss是否失效
    headers = {
        'Host': 'tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'Cookie': 'BDUSS=' + bduss,
    }
    url = 'http://tieba.baidu.com/dc/common/tbs'
    return requests.get(url=url, headers=headers).json()['is_login']


def get_thread_list(aim_tieba: str, pn=0):
    try:
        threads = []
        payload = {'pn': pn, 'ie': 'utf-8'}
        headers = {
            'Host': 'tieba.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        }
        content = requests.get('http://tieba.baidu.com/f?kw=' + aim_tieba, params=payload, headers=headers).text
        raws = re.findall('thread_list clearfix([\s\S]*?)创建时间"', content)
        for raw in raws:
            tid = re.findall('href="/p/(\d*)', raw)
            pid = re.findall('&quot;first_post_id&quot;:(.*?),', raw)
            topic = re.findall('href="/p/.*?" title="([\s\S]*?)"', raw)
            nickname = re.findall('title="主题作者: (.*?)"', raw)
            reply_num = re.findall('&quot;reply_num&quot;:(.*?),', raw)
            username = re.findall(
                '''frs-author-name-wrap"><a rel="noreferrer"  data-field='{&quot;un&quot;:&quot;(.*?)&quot;}''', raw)
            if len(tid) == len(pid) == len(topic) == len(username) == len(reply_num):
                dic = {"tid": tid[0], "pid": pid[0], "topic": topic[0],
                       "author": username[0].encode('utf-8').decode('unicode_escape'), "reply_num": reply_num[0],
                       "nickname": nickname[0]}
                threads.append(dic)
        if threads == []:
            print('获取首页失败')
    except Exception:
        print('Exception Logged')
        return []
    return threads


if __name__ == '__main__':
    bduss = 'nJXVEVPfm5aU1JZOG9NaVRFNHVEeEFKSUVLUEJNUXlHYkxEWnRpQX5pfnMwalpkSVFBQUFBJCQAAAAAAAAAAAEAAADzPEUpybW1xNPQu-7BpgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOxFD13sRQ9dV'
    list = get_thread_list(aim_tieba='湖南工业职业技术学院')
    for topic in list:
        # client_Post(bduss=bduss, kw='湖南工业职业技术学院', fid='195965', tid=topic['tid'], content='嗨咯')
        # time.sleep(2)
        print(topic)
