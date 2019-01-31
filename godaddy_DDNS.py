import requests
import urllib.request
import re
import json
import time

url = r'https://api.godaddy.com/v1/domains/xxx/records'  # 替换xxx为你的域名地址
headers = dict()
headers['Accept'] = 'application/json'
headers['Content-Type'] = 'application/json'
headers['Authorization'] = 'sso-key ***********************************:**********************'  # 替换为你的公钥:密钥
wait_time = 30  # 等待时间


def get_local_ip():
    response = requests.get("http://2019.ip138.com/ic.asp")
    ip = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", response.content.decode(errors='ignore')).group(
        0)
    print("当前本机IP为：" + str(ip))
    return ip


def get_remote_ip():
    request = urllib.request.Request(url + r'/A/@', headers=headers, method="GET")
    data = urllib.request.urlopen(request).read().decode('utf-8')
    ip = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", data).group(0)
    print("当前DNS记录为：" + str(ip))
    return ip


def update_ip(ip):
    print("更新DNS记录中...")
    records_a = {
        "data": ip,
        "ttl": 600,
    }
    put_data = [records_a]
    try:
        request = urllib.request.Request(url + r'/A/@', headers=headers, data=json.dumps(put_data).encode(),
                                         method="PUT")
        code = urllib.request.urlopen(request).getcode()
        if code == 200:
            print("DNS记录更新成功！" + str(wait_time) + "秒后将再次检查")
    except urllib.error.HTTPError as e:
        print("错误代码：" + str(e.code))
        if e.code == 400:
            print("请求格式不正确")
        if e.code == 401:
            print("身份验证信息未发送或无效，请检查密钥填写是否正确")
        if e.code == 422:
            print("记录结构不正确，请检查")


if wait_time > 1:
    while True:
        local_ip = get_local_ip()
        remote_ip = get_remote_ip()
        if local_ip == remote_ip:
            print("本机IP与DNS记录相同，" + str(wait_time) + "秒后将再次检查")
        else:
            print("本机IP与DNS记录不同")
            update_ip(local_ip)
        time.sleep(wait_time)
else:
    print("Godaddy只允许每个API每分钟发送60个请求，等待时间最少大于1秒")
    exit()
