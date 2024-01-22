# Author: lindaye
# Update:2023-09-26
# 使用说明: 
#     1.青龙面板(环境变量)： 需修改Btype = "本地"为Btype = "青龙",环境变量(变量名为linxivps 值为{"name":"备注","username":"账号","password":"密码"}) 多号换行[一行一个]
#     2.本地/直接运行: 需修改代码ck_token = [{"name":"测试","username":"123@123.com","password":"123456"}] 即可多号[{},{}]
# 软件版本
version = "0.0.1"
name = "Freenom 域名续期"
linxi_token = "linxivps"
linxi_tips = '{"name":"备注","username":"账号","password":"密码"}'

import os
import re
import json
import time
import requests
from multiprocessing import Pool

# 变量类型(本地/青龙)
Btype = "本地"
# 保持连接,重复利用
ss = requests.session()
# 全局基础请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.39 (0x18002733) NetType/WIFI Language/zh_CN',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
}

def freenom(i,ck):
    domain = "https://my.freenom.com"
    headers["referer"] = "https://my.freenom.com/clientarea.php"
    # 重试次数
    check_count = 32
    # 等待时间
    sleep_time = 30
    def renew(user):
        result = ss.get(domain+"/domains.php?a=renewals",headers=headers).text
        if "logout.php" in result:
            print(f"账号【{i+1}】[{ck['name']}] ✅ [Freenom] 账号:{user['username']} 登陆状态验证成功!")
            token = re.findall('name="token" value="(.*?)"',result)
            if token != []:
                print(f"账号【{i+1}】[{ck['name']}] ✅ [Freenom] 账号:{user['username']} 获取账号Token成功!")
                domains = re.findall(r'<tr><td>(.*?)</td><td>[^<]+</td><td>[^<]+<span class="[^<]+>(\d+?).Days</span>[^&]+&domain=(\d+?)">.*?</tr>', result)
                if domains != []:
                    print(f"账号【{i+1}】[{ck['name']}] ✅ [Freenom] 账号:{user['username']} 获取域名成功!")
                    tips = "\n"
                    for do, days, renewal_id in domains:
                        if int(days) < 14:
                            headers["referer"] =  f"https://my.freenom.com/domains.php?a=renewdomain&domain={renewal_id}"
                            data={"token": token, "renewalid": renewal_id, f"renewalperiod[{renewal_id}]": "12M", "paymentmethod": "credit" }
                            result = ss.post(domain + "/domains.php?submitrenewals=true",data=data).text
                            if result.find("Order Confirmation") != -1:
                                tips += f"\t域名:{do}续期成功!\n"
                            else:
                                tips += f"\t域名:{do}续期失败!\n"
                        else:
                            tips += f"\t域名:{do} 剩余:{days} 天续期!\n"
                    print(f"账号【{i+1}】[{ck['name']}] ✴️ [Freenom] 账号:{user['username']} 续期结果: {tips}")

            else:
                print(f"账号【{i+1}】[{ck['name']}] ❌ [Freenom] 账号:{user['username']} 获取账号Token失败!")
            return True
        else:
            print(f"账号【{i+1}】[{ck['name']}] ❌ [Freenom] 账号:{user['username']} 登陆状态验证失败!")
            return False
    data = {"username": ck['username'], "password": ck['password']}
    token = requests.get("http://dt.lieren.link/token").json()['token']
    cookies = {'aws-waf-token': token}
    theaders = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'referer': 'https://my.freenom.com/clientarea.php',
        'authority': 'my.freenom.com',
    }
    result = ss.get("https://my.freenom.com/clientarea.php",headers=theaders,cookies=cookies)
    result = ss.post(domain+"/dologin.php",headers=headers ,cookies=cookies,data=data)
    for count in range(check_count):
        if result.status_code == 405:
            print(f"账号【{i+1}】[{ck['name']}] ❌ [Freenom] 账号:{ck['username']} 人机验证拦截,30秒后开始重新尝试! 当前[{count+1}/{check_count}]")
        elif result.status_code == 200:
            print(f"账号【{i+1}】[{ck['name']}] ✅ [Freenom] 账号:{ck['username']} 登陆成功!")
            renew(ck)
            break
        else:
            print(f"账号【{i+1}】[{ck['name']}] 🆘 [Freenom] 账号:{ck['username']} 未知异常:{result}!")
        time.sleep(sleep_time)

def process_wrapper(func, args):
    try:
        func(*args)
    except Exception as e:
        handle_exception(e,args[0])

def handle_exception(e,i):
    print(f"账号【{i+1}】🆘 程序出现异常:", e)
    
    
if __name__ == "__main__":
    print(f"""██╗     ██╗███╗   ██╗██╗  ██╗██╗      ██╗   ██╗██████╗ ███████╗
██║     ██║████╗  ██║╚██╗██╔╝██║      ██║   ██║██╔══██╗██╔════╝
██║     ██║██╔██╗ ██║ ╚███╔╝ ██║█████╗██║   ██║██████╔╝███████╗
██║     ██║██║╚██╗██║ ██╔██╗ ██║╚════╝╚██╗ ██╔╝██╔═══╝ ╚════██║
███████╗██║██║ ╚████║██╔╝ ██╗██║       ╚████╔╝ ██║     ███████║
╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝        ╚═══╝  ╚═╝     ╚══════╝
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
            #{"name":"测试","username":"123@123.com","password":"123456"}
        ]

        if freenom_token == []:
            print(f'⛔ 本地变量异常: 请添加本地ck_token示例:{linxi_tips}')
            exit()
    # 创建进程池
    with Pool() as pool:
        if freenom_token != []:
            print("=================♻️Freenom 域名♻️================") 
            pool.starmap(process_wrapper, [(freenom, (i, ck)) for i, ck in enumerate(ck_token)])
        # 关闭进程池
        pool.close()
        # 等待所有子进程执行完毕
        pool.join()

        # 关闭连接
        ss.close
        # 输出结果
        print(f"================[{name}V{version}]===============")
