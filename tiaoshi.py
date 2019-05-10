#coding:utf-8
import requests
import socks
import socket
socks.set_default_proxy(socks.HTTP, addr='proxy1.bj.petrochina', port=8080)
socket.socket = socks.socksocket
qq = "http://hse.cnpcint.com/oversea/APP/Portal/HealthHomepage.aspx"
url = "http://210.12.209.231/oversea/Cnpcintl.aspx"

r = requests.get(url)
print(r.status_code)