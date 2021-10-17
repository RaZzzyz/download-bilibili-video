import re
from requests import get
import os
from tqdm import tqdm
def get_cid(bid):
    url='https://api.bilibili.com/x/player/pagelist?bvid='+bid+'&jsonp=jsonp'
    res=get(url).json()
    cid=[i['cid'] for i in res['data']]
    name=[i['part'] for i in res['data']]
    return cid,name
def get_list(bid,cid,cookie):
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'cookie':cookie
    }
    u_l=[]
    for c in cid:
        url='http://api.bilibili.com/x/player/playurl?'+'&cid='+str(c)+'&bvid='+bid+'&qn=80&fnval=0&fnver=0&fourk=1'
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
        res=get(url,headers=headers).json()
        if res['code']!=0 :
            print("请求错误")
            return 0
        else:
            for i in res['data']['durl']:
                u_l.append(i['url'])
    return u_l
def run(url_list,name):
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'referer': 'http://player.bilibili.com/',
    }
    for i in range(len(url_list)):
        print(f'{name[i]}start')
        res=get(url_list[i],headers=headers,stream=True,verify=False)
        file_size=int(res.headers['content-length'])
        first_byte=os.path.getsize('C:/project/python/download-bilibili-video')
        print(first_byte-file_size)
        pbar = tqdm(
        total=file_size, initial=first_byte,
        unit='B', unit_scale=True, desc='C:/project/python/download-bilibili-video')
        with open(f'C:/project/python/download-bilibili-video/{name[i]}.flv','wb')as f:
            for chunk in res.iter_content(chunk_size=512):
                if chunk:       
                    f.write(chunk)
                    pbar.update(512)
            pbar.close()
        print(f'{name[i]}done')
if __name__ == '__main__':
    # url='https://www.bilibili.com/video/BV1Jq4y1578j?spm_id_from=333.851.b_7265636f6d6d656e64.7'
    # cookie="b_ut=-1; _uuid=F48A4784-416C-413B-150F-336299E3BE0115321infoc; buvid3=456E3E85-9070-4F60-82AA-59A624D5804C148806infoc; CURRENT_BLACKGAP=0; fingerprint=5c79d66de68a6783450b1b5542696bce; buvid_fp=456E3E85-9070-4F60-82AA-59A624D5804C148806infoc; buvid_fp_plain=456E3E85-9070-4F60-82AA-59A624D5804C148806infoc; SESSDATA=adefcd9d%2C1649928729%2Caf6cc%2Aa1; bili_jct=80035fcc3760d4b02126929b79fa7b05; DedeUserID=8319923; DedeUserID__ckMd5=ed85c15e5de363e9; sid=i488bmh2; i-wanna-go-back=-1; blackside_state=1; rpdid=|(k|)lJlmRR~0J'uYJRJ~Y~mY; LIVE_BUVID=AUTO1716343772037931; bsource=search_baidu; CURRENT_QUALITY=80; PVID=1; CURRENT_FNVAL=976; bp_video_offset_8319923=582336035644325544; innersign=1"
    # bv=re.compile('BV..........').search(url).group()
    # cid,name=get_cid(bv)
    # u_l=get_list(bv,cid,cookie)
    # print(u_l)
    u_l=['https://upos-sz-mirrorkodoo1.bilivideo.com/upgcxcode/05/53/423615305/423615305_nb2-1-80.flv?e=ig8euxZM2rNcNbR3hwdVhwdlhW4VhwdVhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1634464969&gen=playurlv2&os=kodoo1bv&oi=2085359954&trid=bfe471becd794410bfbb7720742660ceu&platform=pc&upsig=e5e1b6fac717b9fe1af6f6bda5f5cb6d&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mid=8319923&bvc=vod&nettype=0&orderid=0,3&agrr=1&logo=80000000']
    run(u_l,"a")