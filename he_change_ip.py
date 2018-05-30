#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# =============================================================================
#      FileName: he_change_ip.py
#          Desc: change dns server ip in he.net. 使用时请先将缺少的信息补全
#        Author: Jase Chen
#         Email: xxmm@live.cn
#      HomePage: https://jase.im/
#       Version: 0.0.1
#       License: GPLv2
#    LastChange: 2018-05-30 08:33:41
#       History:
# =============================================================================
'''

import requests

def update_DNS_IP(ip):
    # 此处为登陆HE.NET用的账号信息
    Login_data = {'email': '此处为username', 'pass': '此处为password', 'submit': 'Login!'}
    # 更新IP用的表单
    update_IP = {
        'account': '',
        'menu': 'edit_zone',
        'Type': 'a',
        'hosted_dns_zoneid': '此处省略',
        'hosted_dns_recordid': '此处省略',
        'hosted_dns_editzone': '1',
        'Priority': '-',
        'Name': '此处省略',
        'TTL': '300',
        'hosted_dns_editrecord': 'Update',
    }
    # 更新的IP
    update_IP['Content'] = ip
    header = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }
    # 登录用URL
    url = 'https://dns.he.net/'
    # 更新IP信息页URL
    url_changeIP = 'https://dns.he.net/?hosted_dns_zoneid=此处省略'
    with requests.Session() as s:
        s.get(url)
        # 添加请求头
        s.headers.update(header)
        # 登陆
        s.post(url, data=Login_data)
        # 提交更新IP表单
        s.post(url_changeIP, data=update_IP)

def main():
    update_DNS_IP('5.5.5.5')

if __name__ == "__main__":
    main()
