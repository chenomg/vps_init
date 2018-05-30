#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# =============================================================================
#      FileName: vps_init.py
#      Desc: update the ip setting in Configuration file
#            after updated the server location in bandwagon
#            使用前请先将信息补全
#        Author: Jase Chen
#         Email: xxmm@live.cn
#      HomePage: https://jase.im/
#       Version: 0.0.1
#       License: GPLv2
#    LastChange: 2018-05-29 22:52:10
#       History:
# =============================================================================
'''

import socket
import re
import he_change_ip


# 获取当前主机的IP地址
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

# 获取当前主机中的ss-libev的配置文件，用以检查当前IP有没有变更
def get_config():
    config_file = '/etc/shadowsocks-libev/config.json'
    with open(config_file,'r') as cfg:
        content = cfg.read()
    return content

# 初始化当前主机ss-libev配置文件中的IP
def init_IP_shadowsocks_libev():
    config_file = '/etc/shadowsocks-libev/config.json'
    ip = get_host_ip()
    with open(config_file, 'w') as f:
        f.write('{')
        f.write('\n    "server":"{}",'.format(ip))
        f.write('''
    "server_port":此处为端口号,
    "local_port":1080,
    "password":"此处为密码",
    "timeout":60,
    "method":"chacha20-ietf-poly1305"
}''')


def main():
    # 检查当前VPS的IP是否有变化,若有变化则更新本地ss配置文件以及HE.NET中的IP地址
    if re.findall(r"(?:%s)"%(get_host_ip()), get_config()):
        pass
    else:
        init_IP_shadowsocks_libev()
        he_change_ip.update_DNS_IP(get_host_ip())


if __name__ == "__main__":
    main()
