# LinxiPush (林夕脚本)

基于Python的各种脚本仓库，欢迎投稿!

> ## Freenom域名续费:
> `Freenom域名续费`，用于`Freenom`的域名（.tk、.gq 等）自动续期，支持`AWS-WAF验证`Token。

> ### 使用方法
> 1. 安装依赖:
>    ```bash
>    pip install requests
>    ```

> 2. 修改配置
>    - 推送支持 `wxpusher`、`Telegram`、`Bark` 支持同时推送多个平台
>    - 青龙运行:
>        - 新增变量`Btype` 值为`青龙`
>        - 新增变量 `linxivps`
>        - 值为 `{"name":"备注","username":"账号","password":"密码"}`
>          `{"name":"备注","username":"账号","password":"密码"}` 换行分割!
>        - 推送默认关闭 新增变量 `freenom_push` 值为 `true` 开启
>    - 青龙推送:
>        - `wxpusher` 新增变量 `wxpusher_uid` 值为 https://wxpusher.zjiecode.com/demo/ 扫码获得（例如UID_xxx）的 uid
>        - `Telegram` 直接修改青龙配置文件（暂不支持代理）
>        - `Bark` 直接修改青龙配置文件
>    - 本地运行:
>        - 修改代码 `ck_token`:
>      ```python
>      ck_token = [
>          {"name":"备注","username":"123@123.com","password":"123456"},
>          {"name":"备注","username":"123@123.com","password":"123456"}
>      ]
>      ```
>      为自己真实的账号密码
>        - 推送默认关闭 修改代码 `push` 值为 `true` 开启
>    - 本地推送:
>        - `wxpusher` 填写 `WxUID` 值为 https://wxpusher.zjiecode.com/demo/ 扫码获得（例如UID_xxx）的 uid
>        - `Telegram` 填写`telegram_token`和`chat_id`（暂不支持代理）
>        - `Bark` 填写 `bark_token`


> 3. 运行程序:
>    ```bash
>    Python Freenom.py
>    ```

# 赞赏
![赞赏码](https://github.com/linxi-520/LinxiPush/blob/main/yzsm.png)

# 注意提醒:
本仓库脚本仅用于交流学习，请下载后24之内自行删除
