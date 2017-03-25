# -*- coding: UTF-8 -*-
import requests

def test():
    url = 'wwww.baidu.com'
    fp = open('ipPool.txt', 'r')
    ips = fp.readlines()
    proxys = []
    for p in ips:
        print p
        ip = p.strip('\n').split('\t')
        print ip
        proxy = 'http:\\' + ip[0] + ':' + ip[1]
        proxies = {'proxy': proxy}
        proxys.append(proxies)
    N = 0
    for pro in proxys:
        try:
            s = requests.get(url, proxies=pro)
            print('第{}个ip：{} 状态{}'.format(N,pro,s.status_code))
        except Exception as e:
            print(e)
        N+=1
        
test()