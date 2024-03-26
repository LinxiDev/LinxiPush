# Author: lindaye
# Update:2024-01-24
# 使用说明: 自行查看文档 https://github.com/linxi-520/LinxiPush 
# 软件版本
version = "1.0.1"
name = "Freenom 域名续期"
linxi_token = "linxivps"
linxi_tips = '{"name":"备注","username":"账号","password":"密码"}'

import os
import re
import json
import time
import requests
from urllib.parse import quote
from multiprocessing import Pool

# 变量类型(本地/青龙)
Btype = "青龙"
# 消息通知配置信息
push = os.getenv("linxipush")
# 保持连接,重复利用
ss = requests.session()
# 全局域名
domain = "https://my.freenom.com"
# 全局基础请求头
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'referer': 'https://my.freenom.com/clientarea.php',
    'authority': 'my.freenom.com',
}

def freenom(i, ck, token):
    username = ck['username']
    data = {"username": username, "password": ck['password']}
    if token:
        result = ss.post(f"{domain}/dologin.php", headers=headers, cookies={'aws-waf-token': token}, data=data)
    else:
        result = ss.post(f"{domain}/dologin.php", headers=headers, data=data)
    for count in range(3):
        if result.status_code == 200:
            result = ss.get(f"{domain}/domains.php?a=renewals", headers=headers).text
            if "logout.php" in result:
                token = re.findall('name="token" value="(.*?)"', result)
                if token:
                    print(f"账号【{i+1}】[{ck['name']}] ✅ [Freenom] 账号:{username} 获取账号Token成功!")
                    domains = re.findall(r'<tr><td>(.*?)</td><td>[^<]+</td><td>[^<]+<span class="[^<]+>(\d+?).Days</span>[^&]+&domain=(\d+?)">.*?</tr>', result)
                    if domains:
                        print(f"账号【{i+1}】[{ck['name']}] ✅ [Freenom] 账号:{username} 获取域名成功!")
                        tips = "\n"
                        for do, days, renewal_id in domains:
                            if int(days) < 14:
                                headers["referer"] =  f"https://my.freenom.com/domains.php?a=renewdomain&domain={renewal_id}"
                                data = {"token": token, "renewalid": renewal_id, f"renewalperiod[{renewal_id}]": "12M", "paymentmethod": "credit"}
                                result = ss.post(f"{domain}/domains.php?submitrenewals=true", data=data).text
                                if "Order Confirmation" in result:
                                    tips += f" 域名:{do}续期成功!\n"
                                else:
                                    tips += f" 域名:{do}续期失败!\n"
                            else:
                                tips += f" 域名:{do} 剩余:{days} 天续期!\n"
                        print(f"账号【{i+1}】[{ck['name']}] ✴️ [Freenom] 账号:{username} 续期结果: {tips}")
                        send_msg(i,f"FreeNom 续期查询: \n 账号:{username} \n✴️ 续期结果: {tips}")
                else:
                    print(f"账号【{i+1}】[{ck['name']}] ❌ [Freenom] 账号:{username} 获取账号Token失败!")
                    send_msg(i,f"FreeNom 续期异常: \n 账号:{username} \n❌ 获取账号Token失败!")
            else:
                print(f"账号【{i+1}】[{ck['name']}] ❌ [Freenom] 账号:{username} 登陆状态验证失败,请检查账号密码!")
                send_msg(i,f"FreeNom 续期异常: \n 账号:{username} \n❌ 登陆状态验证失败,请检查账号密码!")
            break
        else:
            print(f"账号【{i+1}】[{ck['name']}] 🆘 [Freenom] 账号:{username} 未知异常:{result}!")
            send_msg(i,f"FreeNom 续期异常: \n 账号:{username} \n🆘 未知异常:{result}!")
        time.sleep(3)

def process_wrapper(func, args):
    try:
        func(*args)
    except Exception as e:
        handle_exception(e,args[0])

def handle_exception(e,i):
    print(f"账号【{i+1}】🆘 程序出现异常:", e)
    send_msg(i,f"FreeNom 续期错误: \n {e}")
    
def send_msg(i,body):
    if push:
        try:
            pushs = json.loads(push)
            if len(pushs['types']) != len(pushs['keys']):
                print(f"账号【{i+1}】推送通知: ❌ 错误填写通知配置信息,不执行消息推送!")
                return
            ipinfo = ss.get("https://v4.ip.zxinc.org/info.php?type=json").json()
            ipname = ipinfo['data']['location']
            ip = ipinfo['data']['myip']
            data = {
                "name":name, "message":body, "ipinfo":f"[{ipname}]({ip})",
                "types":pushs['types'],
                "keys":pushs['keys']
            }
            result = ss.post(f"https://api.linxi.tk/api/push/message",json=data).json()
            if result['code'] == 200:
                for ts in pushs['types']:
                    print(f"账号【{i+1}】{result[ts]['tips']}!")
            else:
                print(f"账号【{i+1}】推送通知: ❌ 推送失败!")
        except json.JSONDecodeError:
            print(f"账号【{i+1}】推送通知: 通知配置信息不是合法的 JSON 格式")
    else:
        print(f"账号【{i+1}】推送通知: ❌ 未填写通知配置信息,不执行消息推送!")
    
if __name__ == "__main__":
    print(f"""
███████╗██████╗ ███████╗███████╗    ███╗   ██╗ ██████╗ ███╗   ███╗
██╔════╝██╔══██╗██╔════╝██╔════╝    ████╗  ██║██╔═══██╗████╗ ████║
█████╗  ██████╔╝█████╗  █████╗█████╗██╔██╗ ██║██║   ██║██╔████╔██║
██╔══╝  ██╔══██╗██╔══╝  ██╔══╝╚════╝██║╚██╗██║██║   ██║██║╚██╔╝██║
██║     ██║  ██║███████╗███████╗    ██║ ╚████║╚██████╔╝██║ ╚═╝ ██║
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝    ╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝
    项目:{name}           BY-林夕          Verion: {version}(并发)
    Github仓库地址: https://github.com/linxi-520/LinxiPush
""")
    if Btype == "青龙":
        if os.getenv(linxi_token) == None:
            print(f'⛔ 青龙变量异常: 请添加{linxi_token}变量示例:{linxi_tips} 确保一行一个')
            exit()
        # 变量CK列表
        ck_token = [json.loads(line) for line in os.getenv(linxi_token).splitlines()]
    else:
        # 本地CK列表
        ck_token = [
            {"name":"测试","username":"123@123.com","password":"123456"}
        ]
        if ck_token == []:
            print(f'⛔ 本地变量异常: 请添加本地ck_token示例:{linxi_tips}')
            exit()
    print("=================♻️Freenom 域名♻️================")
    token = False
    try:
        result = ss.get("https://my.freenom.com/clientarea.php",headers=headers)
        if result.status_code != 200:
            print(f"[Freenom] 官网访问失败 状态码: {result.status_code} 开始获取AWS-WAF-Token!")
            token = ss.get("http://dt.lieren.link/token").json()['token']
    except Exception as e:
        print(f'⛔ 获取AWS-WAF-Token失败: {e}')
        exit()
    # 创建进程池
    with Pool() as pool:
        pool.starmap(process_wrapper, [(freenom, (i, ck,token)) for i, ck in enumerate(ck_token)])

        # 关闭进程池
        pool.close()
        # 等待所有子进程执行完毕
        pool.join()

        # 关闭连接
        ss.close
        # 输出结果
        print(f"================[{name}V{version}]===============")
