# 需要安装
* pip3 install BeautifulSoup4
* pip3 install selenium==2.53.6
* PhantomJS 
1. 更新当前系统环境
sudo apt-get update -y
sudo apt-get upgrade -y
2. 安装相应的依赖
sudo apt-get install build-essential chrpath libssl-dev libxft-dev libfreetype6-dev libfreetype6 libfontconfig1-dev libfontconfig1 -y
3. 下载PhantomJS
sudo wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
4. 解压并安装
sudo tar xvjf phantomjs-2.1.1-linux-x86_64.tar.bz2 -C /usr/local/share/
系统环境配置
sudo ln -s /usr/local/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin/
5. 检验
phantomjs --version
6. 测试
phantomjs
phantomjs> phantom.version

来源：https://blog.csdn.net/yin__ren/article/details/79410393 

参考：https://www.vultr.com/docs/how-to-install-phantomjs-on-ubuntu-16-04

PhantomJS：https://bitbucket.org/ariya/phantomjs/downloads/

