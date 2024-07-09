# Author: LinGPT
# Update:2023-10-10
# 多线程示例脚本模板
# 添加账号说明(青龙/本地)二选一
#   青龙: 青龙变量cstoken 值{"ck":"xxxxxxxx"} 一行一个(回车分割)
#   本地: 脚本内置ck方法ck_token = [{"ck":"xxxxxxxx"},{"ck":"xxxxxxxx"}]
# 推送消息:
#   青龙变量linxi_push 值为WxPusher UID
# 脚本声明: 仅供学习交流，如用于违法违规操作与本作者无关,请勿用于非法用途,请在24小时内删除该文件!
# 软件版本
version = "0.0.1"
name = "多线程示例脚本模板"
linxi_token = "cstoken"
linxi_tips = '{"ck":"xxxxxxxx"}'

import os
import re
import json
import time
import requests
from urllib.parse import quote
from multiprocessing import Pool
# 变量类型(本地/青龙)
Btype = "本地"
# 域名(无法使用时请更换)
domain = 'http://www.example.com'
# 保持连接,重复利用
ss = requests.session()
# 全局基础请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.39 (0x18002733) NetType/WIFI Language/zh_CN',
    'Referer': '',
    'Origin': '',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
}


def user_info(i,ck):
    print(f"账号【{i+1}】✅ {ck}")
    pass


def do_read(i,ck):
    print(f"账号【{i+1}】✴️  {ck}")
    pass


def get_money(i,ck):
    print(f"账号【{i+1}】❌ {ck}")
    pass

# 微信Wxpusher 推送 UID扫码获取: https://wxpusher.zjiecode.com/demo/
def Wxpusher(name,key,message,ipinfo=""):
    # 通知标题,Wxpusher UID,通知消息内容
    code = f'''{name}
        <body style="font-family: 'Arial', sans-serif; background-color: #f2f2f2; margin: 0; padding: 20px;">
            <div class="notification" style="background-color: #ffffff; border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 20px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                <h2 style="color: #333; text-align: center;"> 任务执行结束 </h2>
                <h3 style="color: #666; text-align: center;"> {name} </h3>
                <div class="code-block" style="background-color: #f9f9f9; border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-top: 15px; overflow: auto;">
                    <pre style="color: #333;">{message}</pre></div>
                <div class="ip-address" style="margin-top: 15px; text-align: center; font-weight: bold; color: #007bff;">推送IP: {ipinfo}</div></div>
            <div class="separator" style="margin: 20px 0; border-top: 1px solid #ddd;"></div>
            <div class="end-message" style="text-align: center; color: #28a745; font-weight: bold;">任务已完成</div>
        </body>
    '''
    result = ss.get(f"https://wxpusher.zjiecode.com/demo/send/custom/{key}?content={quote(code)}").json()
    if result['code'] == 1000:
        return True, f"微信Wxpusher 通知: 推送成功!"
    else:
        return False, f"微信Wxpusher 通知: 推送失败!"

def handle_exception(e,i):
    print(f"账号【{i+1}】🆘 程序出现异常: {e}")
    if os.getenv("linxi_push") == None:
        print(f"账号【{i+1}】✴️ 未配置Wxpusher推送!")
    else:
        ipinfo = ss.get("https://v4.ip.zxinc.org/info.php?type=json").json()
        ipcity = ipinfo['data']['location']
        ip = ipinfo['data']['myip']
        Wxpusher(name,os.getenv("linxi_push"),f"账号【{i+1}】🆘 程序出现异常: {e}",f"{ipcity} [{ip}]")

def process_wrapper(func, args):
    try:
        func(*args)
    except Exception as e:
        handle_exception(e,args[0])


if __name__ == "__main__":
    print(f"""██╗     ██╗███╗   ██╗██╗  ██╗██╗      ██████╗ ███████╗███╗   ███╗ ██████╗ 
██║     ██║████╗  ██║╚██╗██╔╝██║      ██╔══██╗██╔════╝████╗ ████║██╔═══██╗
██║     ██║██╔██╗ ██║ ╚███╔╝ ██║█████╗██║  ██║█████╗  ██╔████╔██║██║   ██║
██║     ██║██║╚██╗██║ ██╔██╗ ██║╚════╝██║  ██║██╔══╝  ██║╚██╔╝██║██║   ██║
███████╗██║██║ ╚████║██╔╝ ██╗██║      ██████╔╝███████╗██║ ╚═╝ ██║╚██████╔╝
╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚══════╝╚═╝     ╚═╝ ╚═════╝ 
    项目:{name}           BY-LinGPT          Verion: {version}(并发)
    提示:脚本仅供技术交流学习使用，严禁用于任何商业用途或非法活动!
    Github仓库地址: https://github.com/LinxiDev/LinxiPush
""")
    if Btype == "青龙":
        if os.getenv(linxi_token) == None:
            print(f'⛔ 青龙变量异常: 请添加{linxi_token}变量示例:{linxi_tips} 确保一行一个')
            exit()
        # 变量CK列表
        #ck_token = [json.loads(line) for line in os.getenv(linxi_token).splitlines()]
        ck_token = [json.loads(li) if "&" in line else json.loads(line) for line in os.getenv(linxi_token).splitlines() for li in re.findall(r'{.*?}', line)]
    else:
        # 本地CK列表
        ck_token = [
            # 这里填写本地变量
            {"ck":"xxx"}
        ]
        if ck_token == []:
            print(f'⛔ 本地变量异常: 请添加本地ck_token示例:{linxi_tips}')
            exit()
    # 创建进程池
    with Pool() as pool:
        print("==================👻获取账号信息👻=================")
        pool.starmap(process_wrapper, [(user_info, (i, ck)) for i, ck in enumerate(ck_token)])
        print("==================💫开始执行任务💫=================")
        pool.starmap(process_wrapper, [(do_read, (i, ck)) for i, ck in enumerate(ck_token)])
        print("==================🐣获取账号信息🐣=================")
        pool.starmap(process_wrapper, [(user_info, (i, ck)) for i, ck in enumerate(ck_token)])
        print("==================🐋开始账号提现🐋=================")
        pool.starmap(process_wrapper, [(get_money, (i, ck)) for i, ck in enumerate(ck_token)])


        # 关闭进程池
        pool.close()
        # 等待所有子进程执行完毕
        pool.join()

        # 关闭连接
        ss.close
        # 输出结果
        print(f"================[{name}V{version}]===============")