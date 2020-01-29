# python3_Spider_beta
[github](https://github.com/shitianshiwa/python3_Spider_beta)

# python3.7.3
## 需要下载 https://www.python.org/downloads/
https://www.python.org/ftp/python/3.7.3/

# 可以用openoffice打开csv文件或转换文件
* http://www.openoffice.org/

## 全部都需要安装的依赖模块
* python3 -m pip install BeautifulSoup4
* python3 -m pip install requests
## 可选（更新pip用）
* python3 -m pip install --upgrade pip(推荐)
* pip3 install --upgrade pip
# 安装模块失败的解决方法
* https://github.com/Tsuk1ko/CQ-picfinder-robot/issues/42#issuecomment-572051285
## 1
* https://npm.taobao.org/
* npm config set registry https://registry.npm.taobao.org
* npm config get registry
## 2
单纯挂的系统代理是没用的，因为命令行并不走系统代理，你需要用 sstap 之类的工具代理，或者尝试按下面的方法为 npm 设置代理
以本地端口为1080的小飞机为例
* npm config set proxy http://127.0.0.1:1080
* npm config set https-proxy http://127.0.0.1:1080
# 如果要取消
* npm config delete proxy
* npm config delete https-proxy


# 注意
* 可能存在无法访问到链接的错误，暂时没有方法解决

# 参考
* [爬虫入门教程 —— 1](https://blog.csdn.net/redpintings/article/details/79916679)
* [【Python】Python处理csv文件](https://www.cnblogs.com/yanglang/p/7126660.html)
* [Python 日期和时间](https://www.runoob.com/python/python-date-time.html)
* [python 网络爬虫入门（一）———第一个python爬虫实例](https://blog.csdn.net/Bo_wen_/article/details/50868339)
* [python常用命令](https://blog.csdn.net/weixin_39875181/article/details/78695264)
* [Python对于CSV文件的读取与写入](https://www.cnblogs.com/unnameable/p/7366437.html )

# 备忘录（这个项目还没在这个系统上试过且所需的依赖库不一定能装到）
* python3最后支持的windows xp系统的版本是3.4.4
* https://www.python.org/ftp/python/3.4.4/python-3.4.4.msi

# Linux 定时循环执行(安装python3的方法自行用搜索引擎解决吧！ubuntu-18-04自带有（Linux某个发行版，Linux超多其它版本）)
* 后台运行 nohup python3 /root/test/XXXXX.py &
* 显示所有进程 ps aux
* 杀死进程 PID（数字）
Linux系统 nohup python3 /root/test/XXXXX.py(文件路径每个人都不一样,用filezilla把文件传上linux服务器)

Linux 定时循环执行 python 脚本 - sherlockChen - 博客园

https://www.cnblogs.com/sherlockChen/p/8196590.html

每天一个linux命令（50）：crontab命令 - peida - 博客园

https://www.cnblogs.com/peida/archive/2013/01/08/2850483.html

# 其它
crond简介

crond是linux下用来周期性的执行某种任务或等待处理某些事件的一个守护进程，与windows下的计划任务类似，当安装完成操作系统后，默认会安装此服务工具，并且会自动启动crond进程，crond进程每分钟会定期检查是否有要执行的任务，如果有要执行的任务，则自动执行该任务。

# 个人记录
因意外丢失了2019年10月10日至10月18日的记录数据


