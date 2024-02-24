# 🚀 版本更新记录

## 📦 v1.0.2 (2024-02-02)

### ✨ 新增
- 🔍 新增了Action运行配置文件`Freenom.yml`
- 👤 新增WARP for fscarmen

### 🐞 修复
- 🔑 修复了请求被AWF拦截才执行获取AWS-WAF-Token问题
- 🖼️ 修复了网络加载失败的问题

## 📦 v1.0.1 (2024-02-22)

### ✨ 新增
- 💬 新增了多平台通知服务

### 🐞 修复
- 📐 修复了获取TOKEN时失败的问题

## 📦 v1.0.0 (2024-01-20)

### ✨ 新增
- 🎉 发布了第一个版本
- 🔑 新增了自动获取验证AWS-WAF-TOKEN功能

### 📘 使用方法

1. **安装依赖:**

    ```bash
    pip install requests
    ```

2. **修改配置**
   - **环境变量:**
       - 账号配置`变量名`为 `linxivps`
       - 账号配置`值`为 一行一个`回车`分割
         ```json
         {"name":"备注","username":"账号","password":"密码"}
         {"name":"备注","username":"账号","password":"密码"}
         ```
       - ![示例](https://github.com/linxi-520/LinxiPush/blob/main/img/user.png)
       - 推送配置`变量名`为 `linxipush`
       - 推送配置`值`为 
         ```json
         {
             "types":["telegram","wxpusher","pushplus","bark","serverj","wecompush","wechatpush"],
             "keys":["telegram_id","wxpusher_UID","pushplus_key","bark_key","serverj_key","wecompush_key","wechatpush_openid"]
         }
         ```
       - ![示例](https://github.com/linxi-520/LinxiPush/blob/main/img/push.png)
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
    - **Github Action:**
        | 变量名 | 描述 | 提示 |
        | --- | --- | --- |
        | linxipush | 推送配置 | 根据上述内容查看 |
        | linxivps | 账号密码 | 根据上述内容查看 |
3. **运行程序:**

    ```bash
    python Freenom.py
    ```

