# -*- coding:utf-8 -*-
import random, requests, time, re
import utiltools.constant as constant


# http://www.ip168.com/json.do?view=myipaddress
# nn是高匿，nt是普通透明代理
class Proxyutil(object):
    def __init__(self):
        print("构造对象完成")


    def get_random_header(self):
        """
        随机生成一个header头
        :return:
        """
        headers = {'User-Agent': random.choice(constant.user_agent_list),
                   'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                   'Accept-Encoding': 'gzip'}
        return headers

    def scraw_proxies(self,page_num,iptype="HTTP",scraw_url="http://www.xicidaili.com/nn/"):
        """
        从代理ip网站获取一些免费的代理ip
        :param page_num: 从代理ip网站获取几页的代理ip
        :param iptype: ip类型“HTTP”或者“HTTPS”
        :param scraw_url: 代理ip网址
        :return: 返回获得的所有的代理IP
        """
        scraw_ip = list()
        all_proxy_list=list()
        for page in range(1, page_num):
            print("抓取第%d页代理IP" % page)
            url = scraw_url + str(page)
            r = requests.get(url, headers=self.get_random_header())
            r.encoding = 'utf-8'
            pattern = re.compile('<td class="country">.*?alt="Cn" />.*?</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td class="country">(.*?)</td>.*?<td>(.*?)</td>', re.S)
            scraw_ip = re.findall(pattern, r.text)
            # 循环爬取回来的所有ip
            for ip in scraw_ip:
                if (ip[3].upper()==iptype.upper()):
                    all_proxy_list.append(ip)
                    print(ip)
            print("代理爬虫暂停10s")
            time.sleep(10)
            print("爬虫重启")
        print('抓取代理IP结束')
        return all_proxy_list


    def check_ip(self,ip, test_url='http://2018.ip138.com/ic.asp', time_out=5):
        """验证指定代理ip是否有效
        :param ip: 待验证的ip，ip[0]是ip，ip[1]是端口
        :param test_url:验证ip使用的网站，这里是ip138
        :param time_out:超时时间，默认5秒没有连接成功，则放弃该代理ip
        :return:
        """
        proxies = {'http': ip[0] + ':' + ip[1]}
        try_ip = ip[0]
        try:
            r = requests.get(test_url, headers=self.get_random_header(), proxies=proxies, timeout=time_out)
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
        except:
            print('%s:%s 请求过程错误' % (ip[0], ip[1]))
            return False

    def get_available_iplist(self, page_num, iptype="HTTP"):
        all_proxy_list = proxyutil.scraw_proxies(page_num, iptype)
        available_ip = list(filter(self.check_ip, all_proxy_list))
        print("available_ip :", available_ip)
        return available_ip



if __name__ == "__main__":
    proxyutil=Proxyutil()
    proxyutil.get_available_iplist(2)

