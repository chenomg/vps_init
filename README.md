# vps_init
update the ip setting in Configuration file and the IP A record in he.net after updated the server location in bandwagon

**本例适合搬瓦工及其他VPS用户(可以更换主机)**

1.  在data.json中填好相关信息

2.  把data.json，he_change_ip.py，vps_init.py三个文件放到`/root/init/`文件夹下  

3.  将vps_init.py添加到rc.local中

    >   开机后自动检测IP地址，*若VPS更换IP后不必手动变更ss-libev中的设置*，并且自动更新he.net中的DNS记录**

4.  重启生效