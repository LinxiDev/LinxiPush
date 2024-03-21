import requests

# 全局请求
ss = requests.session()

# 区域ID
Zone_ID = "xxxxxxx"
# API 令牌
API_Token = "xxxxxxxxx"
# 主域名
Domain = "cdn.xxxxx.gq"


# 需要更新DNS的域名列表(移动,联通,电信)
Domains = [f"cmcc.{Domain}",f"cucc.{Domain}",f"ctcc.{Domain}"]

# 全局请求头
headers={'Authorization': 'Bearer ' + API_Token,'Content-Type': 'application/json'}

# 获取Cloudflare CDN 优选IP(多线路)
def Monitor_CDN_IP():
    CDN_List = ss.get("https://monitor.gacjie.cn/api/client/get_ip_address").json()
    if CDN_List['status']:
        CDN_List =  CDN_List['info']
        IP_Typt = {"CM": "移动", "CU": "联通", "CT": "电信", "AB":"境外", "DEF":"默认"}
        IP_List = []
        for Type in CDN_List:
            # 根据delay进行排序（升序），再根据speed进行排序（降序）
            sorted_ips = sorted(CDN_List[Type], key=lambda x: (x['delay'], -x['speed']))
            # 获取第一个IP，即具有最小delay和最大speed的IP
            selected_ip = sorted_ips[0]
            print(f"[{IP_Typt[Type]}优选IP] {selected_ip['ip']} 延迟:{selected_ip['delay']}ms 峰值:{selected_ip['speed']}KB/s")
            IP_List.append(selected_ip['ip'])
        return IP_List
    else:
        print(f"[获取CDN列表] 获取失败,{CDN_List['msg']}!")
        return None,None,None

# 获取Cloudflare CDN 优选IP(多线路) 现在使用的
def Yes_CDN_IP():
    CDN_List = ss.post("https://api.hostmonit.com/get_optimization_ip",json={"key":"iDetkOys"}).json()
    if CDN_List['code']:
        CDN_List =  CDN_List['info']
        IP_Typt = {"CM": "移动", "CU": "联通", "CT": "电信", "AB":"境外", "DEF":"默认"}
        IP_List = []
        # 根据latency进行排序（升序），再根据speed进行排序（降序）
        CDN_List = sorted(CDN_List, key=lambda x: (x['latency'], -x['speed']))
        for Type in IP_Typt:
            for TIP in CDN_List:
                if TIP['line'] == Type:
                    # 获取第一个IP，即具有最小delay和最大speed的IP
                    print(f"[{IP_Typt[Type]}优选IP] {TIP['ip']} 延迟:{TIP['latency']}ms 峰值:{TIP['speed']}KB/s")
                    IP_List.append(TIP['ip'])
                    break
        return IP_List
    else:
        print(f"[获取CDN列表] 获取失败,{CDN_List['msg']}!")
        return None,None,None

# 获取当前IP
def My_IP():
    ipinfo = ss.get("https://v4.ip.zxinc.org/info.php?type=json").json()
    ipcity = ipinfo['data']['location']
    ip = ipinfo['data']['myip']
    print(f"[当前IP地址] {ipcity} {ip}")

# 更新优选IP
def Cloudflare():
    dns_records = ss.get(f"https://api.cloudflare.com/client/v4/zones/{Zone_ID}/dns_records", headers=headers).json()
    if dns_records['success']:
        # IPS = Monitor_CDN_IP()
        IPS = Yes_CDN_IP()
        Zone_DNS = dns_records["result"]
        for domain in Domains:
            for Zone in Zone_DNS:
                if Zone['name'] == domain:
                    Dns_id = Zone['id']
                    if IPS[Domains.index(Zone['name'])] == Zone['content']:
                        print(f"[更新域名({Zone['name']})] IP相同不更新 {Zone['content']}")
                    else:
                        data = {'type': 'A','name': Zone['name'],'content': IPS[Domains.index(Zone['name'])],'proxied': False}
                        result = ss.put(f'https://api.cloudflare.com/client/v4/zones/{Zone_ID}/dns_records/{Dns_id}',json=data,headers=headers).json()
                        if result['success']:
                            print(f"[更新域名({Zone['name']})] {IPS[Domains.index(Zone['name'])]}")
                        else:
                            print(f"[更新域名({Zone['name']})] 更新失败!")
                    break
            else:
                data = {'type': 'A','name': domain,'content': IPS[Domains.index(domain)],'proxied': False}
                result = ss.post(f'https://api.cloudflare.com/client/v4/zones/{Zone_ID}/dns_records',json=data,headers=headers).json()
                if result['success']:
                    print(f"[新增域名({domain})] {IPS[Domains.index(domain)]}")
                else:
                    print(f"[新增域名({Zone['name']})] 新增失败!")
    else:
        print(f"[获取DNS列表] 获取失败,请检查配置是否正确!")

if __name__ == "__main__":
    print('''
    ██╗     ██╗███╗   ██╗██╗  ██╗██╗       ██████╗███████╗ ██████╗██████╗ ███╗   ██╗
    ██║     ██║████╗  ██║╚██╗██╔╝██║      ██╔════╝██╔════╝██╔════╝██╔══██╗████╗  ██║
    ██║     ██║██╔██╗ ██║ ╚███╔╝ ██║█████╗██║     █████╗  ██║     ██║  ██║██╔██╗ ██║
    ██║     ██║██║╚██╗██║ ██╔██╗ ██║╚════╝██║     ██╔══╝  ██║     ██║  ██║██║╚██╗██║
    ███████╗██║██║ ╚████║██╔╝ ██╗██║      ╚██████╗██║     ╚██████╗██████╔╝██║ ╚████║
    ╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝       ╚═════╝╚═╝      ╚═════╝╚═════╝ ╚═╝  ╚═══╝
        项目: CloudFlare CDN 优选IP 自动更新     BY: 林夕科技      日期: 2024-03-15
    ''')
    My_IP()
    Cloudflare()
