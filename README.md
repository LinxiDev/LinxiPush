# LinxiPush (林夕脚本)

基于Python的各种脚本仓库，欢迎投稿！

## Freenom域名续费

`Freenom域名续费`，用于`Freenom`的域名（.tk、.gq 等）自动续期，支持`AWS-WAF验证`Token。

### 使用方法

1. 安装依赖:

    ```bash
    pip install requests
    ```

2. 修改配置
   - **环境变量:**
       - 账号配置`变量名`为 `linxivps`
       - 账号配置`值`为 一行一个`回车`分割
         ```json
         {"name":"备注","username":"账号","password":"密码"}
         {"name":"备注","username":"账号","password":"密码"}
         ```
        ![示例](https://github.com/linxi-520/LinxiPush/blob/main/yzsm.png)
       - 推送配置`变量名`为 `linxipush`
       - 推送配置`值`为 
         ```json
         {
             "types":["telegram","wxpusher","pushplus","bark","serverj","wecompush","wechatpush"],
             "keys":["telegram_id","wxpusher_UID","pushplus_key","bark_key","serverj_key","wecompush_key","wechatpush_openid"]
         }
         ```
         ![示例](https://github.com/linxi-520/LinxiPush/blob/main/yzsm.png)
       - 消息推送说明: `types` 与 `keys` 一一对应,且可单选和多选。
            | 类型 | 对应的 key 值 | 备注 |
            | --- | --- | --- |
            | telegram | telegram_id | 这是 Telegram 的用户 ID |
            | wxpusher | wxpusher_UID | 这是 wxpusher 的用户 UID |
            | pushplus | pushplus_key | 这是 PushPlus 的推送密钥 |
            | bark | bark_key | 这是 Bark 的推送密钥 |
            | serverj | serverj_key | 这是 Server酱 的推送密钥 |
            | wecompush | wecompush_key | 这是 企业微信推送 的密钥 |
            | wechatpush | wechatpush_openid | 这是 自建微信公众推送 的 OpenID |

   - **本地运行:**
       修改代码`Btype` `ck_token` 位置自查:
       ```python
       # 修改 Btype = "青龙"为 Btype = "本地"
       Btype = "本地"
       ck_token = [
           {"name":"备注","username":"123@123.com","password":"123456"},
           {"name":"备注","username":"123@123.com","password":"123456"}
       ]
       #  为自己真实的账号密码
       ```
3. 运行程序:

    ```bash
    python Freenom.py
    ```

# 赞赏
![赞赏码](https://github.com/linxi-520/LinxiPush/blob/main/yzsm.png)

# 注意提醒
本仓库脚本仅用于交流学习，请下载后24小时内自行删除。
