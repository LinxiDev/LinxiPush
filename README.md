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
>    - 环境变量:
>        - 需修改 `Btype = "本地"` 为 `Btype = "青龙"`
>        - 变量名为 `linxivps`
>        - 值为 `{"name":"备注","username":"账号","password":"密码"}`
>          `{"name":"备注","username":"账号","password":"密码"}`
>    - 本地运行:
>      修改代码 `ck_token`:
>      ```python
>      ck_token = [
>          {"name":"备注","username":"123@123.com","password":"123456"},
>          {"name":"备注","username":"123@123.com","password":"123456"}
>      ]
>      ```
>      为自己真实的账号密码

> 3. 运行程序:
>    ```bash
>    Python Freenom.py
>    ```

# 赞赏
![赞赏码](https://github.com/linxi-520/LinxiPush/blob/main/yzsm.png)

# 注意提醒:
本仓库脚本仅用于交流学习，请下载后24之内自行删除
