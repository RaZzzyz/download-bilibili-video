import re
from requests import get
import os
import aiohttp
import asyncio
import aiofiles
from tqdm import tqdm
from concurrent.futures.thread import ThreadPoolExecutor


def get_cid(bid):
    url = 'https://api.bilibili.com/x/player/pagelist?bvid='+bid+'&jsonp=jsonp'
    res = get(url).json()
    cid = [i['cid'] for i in res['data']]
    name = [i['part'] for i in res['data']]
    return cid, name


def get_list(bid, cid, cookie):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'cookie': cookie
    }
    u_l = []
    for c in cid:
        url = 'http://api.bilibili.com/x/player/playurl?'+'&cid=' + \
            str(c)+'&bvid='+bid+'&qn=80&fnval=0&fnver=0&fourk=1'
        # 6	240P 极速	仅mp4方式支持
        # 16	360P 流畅
        # 32	480P 清晰
        # 64	720P 高清	web端默认值
        # B站前端需要登录才能选择，但是直接发送请求可以不登录就拿到720P的取流地址
        # 无720P时则为720P60
        # 74	720P60 高帧率	需要认证登录账号
        # 80	1080P 高清	TV端与APP端默认值
        # 需要认证登录账号
        # 112	1080P+ 高码率	大多情况需求认证大会员账号
        # 116	1080P60 高帧率	大多情况需求认证大会员账号
        # 120	4K 超清	需要fnver&128=128且fourk=1
        # 大多情况需求认证大会员账号
        # 125	HDR 真彩色	仅支持dash方式
        # 需要fnver&64=64
        # 大多情况需求认证大会员账号
        res = get(url, headers=headers).json()
        if res['code'] != 0:
            print("请求错误")
            return 0
        else:
            for i in res['data']['durl']:
                u_l.append(i['url'])
    return u_l


def run(url, name, dist):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'referer': 'http://player.bilibili.com/',
    }
    req = get(url, headers=headers, stream=True,verify=False)
    file_size = int(req.headers['content-length'])
    print(f"获取视频总长度:{file_size}")
    first_byte = os.path.getsize(dist)
    pbar = tqdm(
        total=file_size, initial=first_byte,
        unit='B', unit_scale=True, desc=name)
    with open(f'{dist}\{name}.flv', 'wb')as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    print(f'{name}done')


if __name__ == '__main__':
    url = 'https://www.bilibili.com/video/BV1eT4y1o7LB?spm_id_from=333.999.0.0'
    cookie = ""
    bv = re.compile('BV..........').search(url).group()
    cid, name = get_cid(bv)
    u_l = get_list(bv, cid, cookie)
    dist = "C:/project/python/download-bilibili-video/"
    with ThreadPoolExecutor(10) as t:
        for i in range(len(u_l)):
            t.submit(run,url=u_l[i],name=name[i],dist=dist)
