# utilTools
开发、整理常用工具模块

## 一、获取可用的代理IP列表（proxyutil.py）
#### 进行爬虫操作时，使用代理IP可以规避反爬首手段
1、从代理IP网站获取代理ip列表<br>
2、过滤代理IP：用代理IP访问IP138网站，判断当前代理IP是否生效<br>
3、将可用的代理IP保存到列表中返回<br>
4、进行其他爬虫操作时，可以使用列表中的代理IP<br>
#### 使用方法：<br>
   （n为从多少页代理ip中进行筛选，每页100个IP）：<br>
    proxyutil=Proxyutil()<br>
    available_ip=proxyutil.get_available_iplist(n)<br>
