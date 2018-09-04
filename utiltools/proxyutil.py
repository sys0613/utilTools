# -*- coding:utf-8 -*-
import random, requests, time, re
import utiltools.constant as constant

class Proxyutil(object):
    def __init__(self):
        pass

# http://www.ip168.com/json.do?view=myipaddress
    #nn是高匿，nt是普通透明代理

    def scraw_proxies(self,page_num,iptype="HTTP",scraw_url="http://www.xicidaili.com/nn/"):
        scraw_ip = list()
        available_ip = list()
        for page in range(1, page_num):
            print("抓取第%d页代理IP" % page)
            url = scraw_url + str(page)
            r = requests.get(url, headers=get_random_header())
            r.encoding = 'utf-8'
            # <td class="country">.*?alt="Cn">.*?</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td class="country">(.*?)</td>.*?<td>(.*?)</td>
            pattern = re.compile('<td class="country">.*?alt="Cn" />.*?</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td class="country">(.*?)</td>.*?<td>(.*?)</td>', re.S)
            scraw_ip = re.findall(pattern, r.text)
            # 循环爬取回来的所有ip
            for ip in scraw_ip:
                print(ip)
                # if (test_ip(ip) == True):
                #     print('%s:%s通过测试，添加进可用代理列表' % (ip[0], ip[1]))
                #     available_ip.append(ip)
                # else:
                #     pass
            print("代理爬虫暂停10s")
            time.sleep(10)
            print("爬虫重启")
        print('抓取结束')
        return available_ip


def get_random_header():
    headers = {'User-Agent': random.choice(constant.user_agent_list),
               'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
               'Accept-Encoding': 'gzip'}
    return headers


#'http://2017.ip138.com/ic.asp'http://2018.ip138.com/ic.asp'
def test_ip(ip, test_url='http://www.ip138.com/', time_out=0.1):
    """验证指定代理ip是否有效
    :param ip: 待验证的ip，ip[0]是ip，ip[1]是端口
    :param test_url:验证ip使用的网站，这里是ip138
    :param time_out:
    :return:
    """
    proxies = {'http': ip[0] + ':' + ip[1]}
    try_ip = ip[0]
    # print(try_ip)
    try:
        r = requests.get(test_url, headers=get_random_header(), proxies=proxies, timeout=time_out)
        print('r.text:',r.text,'code:',r.status_code)
        if r.status_code == 200:
            r.encoding = 'gb2312'
            result = re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', r.text)
            result = result.group()
            if result[:9] == try_ip[:9]:
                print(r.text)
                print('测试通过')
                return True
            else:
                print('%s:%s 携带代理失败,使用了本地IP' % (ip[0], ip[1]))
                return False
        else:
            print('%s:%s 请求码不是200' % (ip[0], ip[1]))
            return False
    except :
        print('%s:%s 请求过程错误' % (ip[0], ip[1]))
        return False

def scraw_proxies(page_num,scraw_url="http://www.xicidaili.com/nt/"):
    """从西祠代理获取代理ip，并对其进行测试
    :param page_num:获取几页的ip
    :param scraw_url:爬取的网址
    :return:
    """
    scraw_ip = list()
    available_ip = list()
    for page in range(1, page_num):
        print("抓取第%d页代理IP" % page)
        url = scraw_url + str(page)
        r = requests.get(url, headers=get_random_header())
        r.encoding = 'utf-8'
        pattern = re.compile('<td class="country">.*?alt="Cn" />.*?</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>', re.S)
        scraw_ip = re.findall(pattern, r.text)
        #循环爬取回来的所有ip
        for ip in scraw_ip:
            if (test_ip(ip) == True):
                print('%s:%s通过测试，添加进可用代理列表' % (ip[0], ip[1]))
                available_ip.append(ip)
            else:
                pass
        print("代理爬虫暂停10s")
        time.sleep(10)
        print("爬虫重启")
    print('抓取结束')
    return available_ip


if __name__ == "__main__":
    proxyutil=Proxyutil()
    proxyutil.scraw_proxies(3)
    # available_ip = scraw_proxies(2)
