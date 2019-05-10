#coding:utf-8
import requests
import time
import datetime
import smtplib
from email.mime.text import MIMEText
import socks
import socket
from retrying import retry
from base.operation_excel import OperationExcel

base_socket = socket.socket
socks.set_default_proxy(socks.HTTP, addr='proxy1.bj.petrochina', port=8080)
socket.socket = socks.socksocket

class Run_Test():
    def __init__(self):
        self.data = OperationExcel()

    @retry(stop_max_attempt_number=5)#请求失败重试5次
    def request_url(self,url):
        code = None
        re = requests.get(url, timeout=5)
        return re.status_code

    #监测url返回值，返回报错信息
    def get_url(self):
        error_url = []
        socket.socket = base_socket
        lines = self.data.get_lines()
        for i in range(1,lines):
            url = self.data.get_url_value(i)
            url_explain = self.data.get_url_explain(i)
            try:
                code = self.request_url(url)
            except (requests.exceptions.ConnectionError,requests.exceptions.ReadTimeout) as e:
                print('请求超时:',e)
                code = str(e)

            if code != 200:
                # 获取当前时间
                nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                error_news = str(i)+'--访问失败--：'+str(code)+' '+url+' '+nowTime +' 所属项目：'+url_explain
                error_url.append(error_news)
            else:
                nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(str(i)+'访问正常：%s '% code,url,nowTime,url_explain)
            time.sleep(0.1)
        print(error_url)
        return error_url





if __name__ == '__main__':
    while True:
        list = Run_Test().get_url()
        content = '\n'.join(list)
        print(content)

        # 邮件发送报错url
        def send_mail(content):
            # 设置代理
            socks.set_default_proxy(socks.HTTP, addr='proxy1.bj.petrochina', port=8080)
            socket.socket = socks.socksocket
            msg_from = 'guoyanzero@163.com'  # 发送方邮箱
            passwd = 'guoyan123'  # 填入发送方邮箱的授权码
            # 收件人邮箱
            msg_to = ['531073687@qq.com', 'guoyanzero@163.com']
            subject = '门户异常警告'  # 主题
            # content = '错误页面地址'  # 正文
            msg = MIMEText(content)
            msg['Subject'] = subject
            msg['From'] = msg_from
            msg['To'] = ','.join(msg_to)
            try:
                #s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
                s = smtplib.SMTP_SSL("smtp.163.com", 465)
                s.login(msg_from, passwd)
                s.sendmail(msg_from, msg_to, msg.as_string())
                print("发送成功")
            except smtplib.SMTPException as e:
                print("发送失败:", e)
        if content:
            sendmail = send_mail(content)
        else:
            pass




