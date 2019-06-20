# 链家网(lianjia.com)和贝壳网(ke.com)爬虫
- 爬取链家网、贝壳网的各类房价数据（小区数据，挂牌二手房, 出租房，新房）。
- **如果好用，请点星支持 ！**
- 支持北京上海广州深圳等国内21个主要城市；支持Python2和Python3; 基于页面的数据爬取，稳定可靠; 丰富的代码注释，帮助理解代码并且方便扩展功能。
- 数据含义：城市-city, 区县-district, 板块-area, 小区-xiaoqu, 二手房-ershou, 租房-zufang， 新房-loupan。
- 每个版块存储为一个csv文件，该文件可以作为原始数据进行进一步的处理和分析。
- 支持图表展示。
![alt text](https://github.com/jumper2014/lianjia-spider/blob/master/pic/xiaoqu_top.png)
![alt text](https://github.com/jumper2014/lianjia-spider/blob/master/pic/district_top.png)
- 如果链家和贝壳页面结构有调整，欢迎反馈，我将尽力保持更新。
- 此代码仅供学习与交流，请勿用于商业用途，后果自负。

## 安装依赖
- pip install -r requirements.txt
- 运行前，请将当前目录加入到系统环境变量PYTHONPATH中。
- 运行前，请指定要爬取的网站，见lib/spider/base_spider.py里面的SPIDER_NAME变量。
- 清理数据，运行 python tool/clean.py

## 快速问答
- Q: 如何降低爬取速度，避免被封IP？A:见base_spider.py里面的RANDOM_DELAY
- Q: 如何减少并发的爬虫数？ A: 见见base_spider.py的thread_pool_size
- Q: 为何无法使用xiaoqu_to_chart.py? A: 该脚本现仅支持mac系统
- Q: 有其他问题反馈途径么？ A: 问题反馈QQ群号635276285。

## 小区房价数据爬取
- 内容格式：采集日期,所属区县,板块名,小区名,挂牌均价,挂牌数
- 内容如下：20180221,浦东,川沙,恒纬家苑,32176元/m2,3套在售二手房
- 数据可以存入MySQL/MongoDB数据库，用于进一步数据分析，比如排序，计算区县和版块均价。
- MySQL数据库结构可以通过导入tool/lianjia_xiaoqu.sql建立。
- MySQL数据格式: 城市 日期 所属区县 版块名 小区名 挂牌均价 挂牌数
- MySQL数据内容：上海 20180331 徐汇 衡山路 永嘉路621号 333333 0
- MongoDB数据内容: { "_id" : ObjectId("5ac0309332e3885598b3b751"), "city" : "上海", "district" : "黄浦", "area" : "五里桥", "date" : "20180331", "price" : 81805, "sale" : 11, "xiaoqu" : "桥一小区" }
- Excel数据内容：上海 20180331 徐汇 衡山路 永嘉路621号 333333 0
- 运行, python xiaoqu.py 根据提示输入城市代码，回车确认，开始采集数据到csv文件
- 运行, python xiaoqu.py city, 自动开始采集数据到csv文件
```
hz: 杭州, sz: 深圳, dl: 大连, fs: 佛山
xm: 厦门, dg: 东莞, gz: 广州, bj: 北京
cd: 成都, sy: 沈阳, jn: 济南, sh: 上海
tj: 天津, qd: 青岛, cs: 长沙, su: 苏州
cq: 重庆, wh: 武汉, hf: 合肥, yt: 烟台
nj: 南京, 
```
- 修改 xiaoqu_to_db.py 中的database变量，设置数据最终存入mysql/mongodb/Excel/json
- python xiaoqu_to_db.py 根据提示将今天采集到的csv数据存入数据库。(默认导出为单一csv文件)
- python xiaoqu_to_chart.py 将单一csv文件数据通过图表展示。

## 挂牌二手房数据爬取
- 获取链家网挂牌二手房价数据，数据格式如下：
- 20180405,浦东,万祥镇,祥安菊苑 3室2厅 258万,258万,祥安菊苑  | 3室2厅 | 126.58平米 | 南 | 毛坯
- 运行，python ershou.py 根据提示输入城市代码，回车确认，开始采集数据到csv文件
- 运行，python ershou.py city，自动开始采集数据到csv文件


## 出租房数据爬取
- 获取链家网挂牌出租房数据，数据格式如下：
- 20180407,浦东,御桥,仁和都市花园  ,3室2厅,100平米,8000
- 运行，python zufang.py 根据提示输入城市代码，回车确认，开始采集数据到csv文件
- 运行，python zufang.py city，自动开始采集数据到csv文件

## 新房数据爬取
- 获取链家网新房数据，数据格式如下：
- 20180407,上海星河湾,76000,1672万
- 运行，python loupan.py 根据提示输入城市代码，回车确认，开始采集数据到csv文件
- 运行，python loupan.py city，自动开始采集数据到csv文件

## 结果存储
- 根目录下建立data目录存放结果数据文件
- 小区房价数据存储目录为 data/site/xiaoqu/city/date
- 二手房房价数据存储目录为 data/site/ershou/city/date
- 出租房房价数据存储目录为 data/site/zufang/city/date
- 新房房价数据存储目录为 data/site/loupan/city/date

## 性能
- 300秒爬取上海市207个版块的2.7万条小区数据，平均每秒90条数据。
```
Total crawl 207 areas.
Total cost 294.048109055 second to crawl 27256 data items.
```
- 1000秒爬取上海215个版块的7.5万条挂牌二手房数据，平均每秒75条数据。
```
Total crawl 215 areas.
Total cost 1028.3090899 second to crawl 75448 data items.
```
- 300秒爬取上海215个版块的3.2万条出租房数据, 平均每秒150条数据。
```
Total crawl 215 areas.
Total cost 299.7534770965576 second to crawl 32735 data items.
```
- 30秒爬取上海400个新盘数据。
```
Total crawl 400 loupan.
Total cost 29.757128953933716 second
```



### 更新记录
- 2019/06/21 去除requirements.txt中的webbrower
- 2018/11/05 增加工具下载二手房缩略图tool/download_ershou_image.py
- 2018/11/01 增加二手房缩略图地址
- 2018/10/28 xiaoqu_to_db.py改造成支持命令行参数自动运行。
- 2018/10/25 将主要爬取代码抽取到spider类中。
- 2018/10/22 文件名，目录，代码重构。
- 2018/10/20 增加中间文件清理功能，能够爬取贝壳网的小区，新房，二手房和租房数据。
- 2018/10/19 支持贝壳网小区数据爬取
- 2018/10/15 增加Spider类，优化异常处理，功能无变动
- 2018/10/14 允许用户通过命令行指定要爬取的城市，而不仅仅通过交互模式选择，用于支持自动爬取。
- 2018/10/11 增加初步log功能。
- 2018/10/09 图表展示区县均价排名。
- 2018/10/07 小区房价导出到json文件, csv文件。图表展示最贵的小区。
- 2018/10/05 增加Referer。增加透明代理服务器获取(未使用)
- 2018/06/01 支持User-Agent
- 2018/04/07 支持采集新房的基本房价信息
- 2018/04/07 支持采集出租房的相关信息
- 2018/04/05 支持采集挂牌二手房信息
- 2018/04/02 支持将采集到的csv数据导入Excel
- 2018/04/01 同时支持Python2和Python3
- 2018/04/01 支持将采集到的csv数据导入MongoDB数据库
- 2018/03/31 支持将采集到的csv数据导入MySQL数据库
- 2018/03/27 修复bug: 版块下只有一页小区数据时未能正确爬取 
- 2018/03/27 增加5个城市，现在支持21个城市的小区数据爬取
- 2018/03/10 自动获取城市的区县列表，现在支持16个城市小区数据爬取
- 2018/03/06 支持北京二手房小区数据采集
- 2018/02/21 应对链家前端页面更新，使用内置urllib2代替第三方requests库,提升性能，减少依赖
- 2018/02/01 支持上海二手房小区数据采集