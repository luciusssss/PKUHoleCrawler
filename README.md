# PKUHoleCrawler
北大树洞爬虫 (In progress)
使用Selenium动态爬取网页内容。


## 环境配置
安装selenium
```
pip3 install selenium
```
安装Chrome浏览器，并从 https://chromedriver.chromium.org/downloads 下载对应当前系统和Chrome版本的chromedrive，然后执行以下操作
* Windows: 把解压后的chromedrive复制到Python的`Scripts`目录下。
* Mac& Linux: 把解压后的chromedrive放到`/usr/local/bin/`中，并运行命令`sudo chmod u+x,o+x  /usr/local/bin/chromedriver`添加运行权限。


## 运行
从树洞网页版“账户-复制User Token”获得你的User Token。
运行以下命令（可设置爬取最新树洞条数），并输入你的User Token：
```
python3 run.py --crawl_size 100
```
爬取结果默认存储在`output.json`中。

**注意：**
* 代码采用模拟浏览行为动态爬取树洞，所以爬取速度较慢，建议爬取条数不要太多。
* 对于每条树洞，目前只是爬取了首页可见的少量回复，并非爬取所有回复。

## To-do
- [ ] 以调用树洞API的方式进行爬取，而非使用Selenium模拟浏览器操作。
- [ ] 实现多线程
- [ ] 支持爬取所有回复（目前只可以爬取首页可见的少量回复）
- [ ] 支持爬取搜索内容
- [ ] 支持爬取图片
