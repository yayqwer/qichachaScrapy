### 使用说明
- 需要python3环境,安装scrapy框架
- 企查查有一个频繁访问出现滑动验证界面，还没有解决，现在使用time防止频繁访问
- 启动文件 main.py
- 如果cookie失效  需要重新从浏览器获取(可以使用spcookie.py将获取到的改变为对应的格式)。
- proxiesip/proxies.py 在西刺网获取可用的代理ip
