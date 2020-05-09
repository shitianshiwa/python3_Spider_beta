##测试用的是这个版本
* https://www.python.org/downloads/release/python-368/
* python3 -m pip install selenium（==2.53.6是最后不警告PhantomJS浏览器的版本，该浏览器从2018年3月4日开始暂停更新） 
* https://github.com/SeleniumHQ/selenium
* python3 -m pip install lxml
* apt-get install firefox
* 1.下载 geckodriver
- wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
* 各个版本的driver下载地址如下(有windows版，可下载放在python根目录里的Scripts文件夹里)
- https://github.com/mozilla/geckodriver/releases
* 2.解压
- tar zxvf geckodriver-v0.22.0-linux64.tar.gz
* 3.转移
* 转移的目的是将解压出来的exe程序放到python的安装目录下
- mv geckodriver /usr/local/bin
* 4.查看版本
- geckodriver --version
* https://blog.csdn.net/qq_34803821/article/details/86653282 linux环境下安装geckodriver
* //PhantomJS（https://github.com/ariya/phantomjs） ，放在python根目录的Scripts文件夹里
##以下可省略，因为目前不使用
# linux上的安装命令
 介绍
 PhantomJS是一种脚本化的无头浏览器，可用于自动执行网页交互。PhantomJS是免费的开放源代码，并根据BSD许可进行分发。PhantomJS基于WebKit，与Safari和    Google Chrome浏览器非常相似。PhantomJS JavaScript API可用于打开网页，执行用户操作和截屏。

在本教程中，我们将学习如何在Ubuntu 16.04服务器上安装PhantomJS。

先决条件
Ubuntu 16.04服务器实例。
一个sudo的用户。
# 步骤1：更新系统
在开始之前，建议使用最新的稳定版本更新系统。您可以使用以下命令执行此操作：(可以跳过)

* sudo apt-get update -y
* sudo apt-get upgrade -y
* sudo shutdown -r now
# 步骤2：安装PhantomJS
在安装PhantomJS之前，您需要在系统上安装一些必需的软件包。您可以使用以下命令安装所有组件：

* sudo apt-get install build-essential chrpath libssl-dev libxft-dev libfreetype6-dev libfreetype6 libfontconfig1-dev libfontconfig1 -y
接下来，您将需要下载PhantomJS。您可以从其官方网站下载PhantomJS的最新稳定版本。运行以下命令以下载PhantomJS：

* sudo wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
下载完成后，将下载的存档文件解压缩到所需的系统位置：

* sudo tar xvjf phantomjs-2.1.1-linux-x86_64.tar.bz2 -C /usr/local/share/
接下来，创建PhantomJS二进制文件到系统bin目录的符号链接：

* sudo ln -s /usr/local/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs   /usr/local/bin/
# 步骤3：验证PhantomJS
* PhantomJS现在已安装在您的系统上。现在，您可以使用以下命令来验证PhantomJS的安装版本：

* phantomjs --version
  您应该看到以下输出：

  2.1.1
  您还可以从PhantomJS提示符下找到PhantomJS的版本，如下所示：

  phantomjs
  您将收到phantomjs提示：

  phantomjs>
  现在，运行以下命令以查找版本详细信息：

  phantomjs> phantom.version
  您应该看到以下输出：

  {
     "major": 2,
     "minor": 1,
     "patch": 1
  }
  而已。您已在Ubuntu 16.04服务器上成功安装了PhantomJS。
  https://www.vultr.com/docs/how-to-install-phantomjs-on-ubuntu-16-04 
