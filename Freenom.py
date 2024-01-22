# Author: lindaye
# Update:2023-09-26
# 使用说明: 
#     1.青龙面板(环境变量)： 需修改Btype = "本地"为Btype = "青龙",环境变量(变量名为linxivps 值为{"name":"备注","username":"账号","password":"密码"}) 多号换行[一行一个]
#     2.本地/直接运行: 需修改代码ck_token = [{"name":"测试","username":"123@123.com","password":"123456"}] 即可多号[{},{}]
# 软件版本
version = "0.0.2"
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
if os.getenv("Btype") is None:
    Btype = "本地"
else:
    Btype = "青龙"
# Wxpusher 通知UID
# https://wxpusher.zjiecode.com/demo/ 扫码获得 例如UID_xxx
WxUID = ""
# Telegram
# 机器人Token
telegram_token = ""
# 接收人
chat_id = ""
# Bark
bark_token = ""
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
    cookies = {'aws-waf-token': token}
    result = ss.post(f"{domain}/dologin.php", headers=headers, cookies=cookies, data=data)
    for count in range(3):
        if result.status_code == 200:
            print(f"账号【{i+1}】[{ck['name']}] ✅ [Freenom] 账号:{username} AWS-WAF验证成功!")
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
    # Wxpusher
    if WxUID == "" or WxUID is None:
        print(f"账号【{i + 1}】Wxpusher 通知: ❌ 未填写 Wxpusher UID 不推送消息!")
    else:
        ipinfo = ss.get("https://v4.ip.zxinc.org/info.php?type=json").json()
        ipname = ipinfo['data']['location']
        ip = ipinfo['data']['myip']
        code = f'''{name}通知
                <body style="font-family: 'Arial', sans-serif; background-color: #f2f2f2; margin: 0; padding: 20px;">

                    <div class="notification" style="background-color: #ffffff; border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 20px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                        <h2 style="color: #333; text-align: center;">🔭 任务执行结束 🔭</h2>
                        <h3 style="color: #666; text-align: center;">🏁 {name} 🏁</h3>
                        <div class="code-block" style="background-color: #f9f9f9; border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-top: 15px; overflow: auto;">
                            <pre style="color: #333;">{body}</pre>
                        </div>
                        <div class="ip-address" style="margin-top: 15px; text-align: center; font-weight: bold; color: #007bff;">
                            推送IP: {ipname}({ip})
                        </div>
                    </div>

                    <div class="separator" style="margin: 20px 0; border-top: 1px solid #ddd;"></div>

                    <div class="end-message" style="text-align: center; color: #28a745; font-weight: bold;">
                        任务已完成
                    </div>

                </body>
            '''
        result = ss.get(f"https://wxpusher.zjiecode.com/demo/send/custom/{WxUID}?content={quote(code)}").json()
        if result['code'] == 1000:
            print(f"账号【{i + 1}】Wxpusher 通知: ✅ 推送成功!")
        else:
            print(f"账号【{i + 1}】Wxpusher 通知: ❌ 推送失败!")
    # Telegram
    if telegram_token == "" or chat_id == "" or telegram_token is None or chat_id is None:
        print(f"账号【{i + 1}】Telegram 通知: ❌ 未填写 telegram_token 或 chat_id 不推送消息!")
    else:
        url = f'https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={chat_id}&text={body}'
        result = ss.get(url).json()
        if result['ok']:
            print(f"账号【{i + 1}】Telegram 通知: ✅ 推送成功!")
        else:
            print(f"账号【{i + 1}】Telegram 通知: ❌ 推送失败!")
    # Bark
    if bark_token == "" or bark_token is None:
        print(f"账号【{i + 1}】Bark 通知: ❌ 未填写 bark_token 不推送消息!")
    else:
        bark_api = f'https://api.day.app/{bark_token}/Freenom通知/{body}'
        result = ss.get(bark_api).json()
        if result['code'] == 200:
            print(f"账号【{i + 1}】Bark 通知: ✅ 推送成功!")
        else:
            print(f"账号【{i + 1}】Bark 通知: ❌ 推送失败!")


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
        # 青龙推送
        WxUID = os.getenv("wxpusher_uid")
        telegram_token = os.getenv("TG_BOT_TOKEN")
        chat_id = os.getenv("TG_USER_ID")
        bark_token = os.getenv("BARK_PUSH")
        if not (WxUID or telegram_token or chat_id or bark_token):
            print('⛔ 青龙变量异常: 未配置推送')
            exit()
    else:
        # 本地CK列表
        ck_token = [
            {"name":"测试","username":"123@123.com","password":"123456"}
        ]
    if ck_token == []:
        print(f'⛔ 本地变量异常: 请添加本地ck_token示例:{linxi_tips}')
        exit()
    # 创建进程池
    with Pool() as pool:
        print("=================♻️Freenom 域名♻️================")

        token = requests.get("https://dt.lieren.link/token").json()['token']
        pool.starmap(process_wrapper, [(freenom, (i, ck,token)) for i, ck in enumerate(ck_token)])

        # 关闭进程池
        pool.close()
        # 等待所有子进程执行完毕
        pool.join()

        # 关闭连接
        ss.close
        # 输出结果
        print(f"================[{name}V{version}]===============")
