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
#    LastChange: 2018-06-07 01:15:54
#       History:
# =============================================================================
'''

import socket
import re
import he_change_ip
from os import system
from time import sleep
import json


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
    with open(config_file, 'r') as cfg:
        content = cfg.read()
    return content


# 从data.json文件中获取服务器端口和密码
def data_json_to_dict():
    # return:dict{'server_port': 1234, 'password': 1234}
    file_name = 'data.json'
    with open(file_name, 'r') as f:
        dic = json.load(fp=f)
    return dic


# 初始化当前主机ss-libev配置文件中的IP
def init_IP_shadowsocks_libev():
    config_file = '/etc/shadowsocks-libev/config.json'
    ip = get_host_ip()
    port_passwd_dict = data_json_to_dict()['port_passwd'][0]
    with open(config_file, 'w') as f:
        f.write('{')
        f.write('\n    "server": "{}",'.format(ip))
        f.write('\n    "server_port": {},'.format(
            port_passwd_dict['server_port']))
        f.write('\n    "local_port": 1080,')
        f.write('\n    "password": {},'.format(port_passwd_dict['password']))
        f.write('\n    "timeout": 60,')
        f.write('\n    "method": "chacha20-ietf-poly1305"')
        f.write('\n}')


# 定期重启ss服务（每3小时）
def restart_ss_for_some_time():
    cmd_start_ss = 'sudo /etc/init.d/shadowsocks-libev start'
    cmd_restart_ss = 'sudo /etc/init.d/shadowsocks-libev restart'
    system(cmd_start_ss)
    while True:
        system(cmd_restart_ss)
        sleep(10000)


# 更新he.net信息
def update_he():
    he_info_dict = data_json_to_dict()['he_info'][0]
    he_username = he_info_dict['username']
    he_password = he_info_dict['password']
    he_zoneid = he_info_dict['zoneid']
    he_recordid = he_info_dict['recordid']
    he_name = he_info_dict['name']
    he_change_ip.update_DNS_IP(get_host_ip(), he_username, he_password,
                               he_zoneid, he_recordid, he_name)


def mkdir():
    init_dir = '~/init/'
    if not os.path.exists(init_dir):
        try:
            os.makedir(init_dir)
            os.chdir(init_dir)
        except Exception:
            pass


def upadte_cert():
    """
    定期更新ssl证书
    """
    pass


def main():
    # 检查当前VPS的IP是否有变化,若有变化则更新本地ss配置文件以及HE.NET中的IP地址
    if re.findall(r"(?:%s)" % (get_host_ip()), get_config()):
        pass
    else:
        init_IP_shadowsocks_libev()
        update_he()
    restart_ss_for_some_time()


if __name__ == "__main__":
    main()
