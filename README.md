# 12306cli
command line tool for querying tickets from 12306

![12306cli result](http://7xkfga.com1.z0.glb.clouddn.com/12306cli_result.png)

所用到的库：

- `requests`，使用 Python 访问 HTTP 资源的必备库。
- `docopt`，Python3 命令行参数解析工具。
- `prettytable`， 格式化信息打印工具，能让你像 MySQL 那样打印数据。
- `colorama`，命令行着色工具
- `pickle`，持久化对象

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:

    python tickets.py 北京 上海 2017-08-01
    python tickets.py -dg 成都 南京 2017-08-01


从12306获取的JSON源数据如下：

```
/ *0 * /  'FV6hYAQ2H0fvhJ3r0eGxAEcQuU2UXnb%2FvQrnSMVxdCeDeSQBhhCuIrNpt3pmsyyPJOGTTAap8ge5%0A74EWeoeZIULwwokviBtqPwwHs5cRoIBjkCKOoejxx1pTnd%2FRd8LEt2S9SZrkBAjsF0qakfNnLhMZ%0AF6hHXKQ8KhzT8O5wFgaXShrqZ%2F8UVahZXyrh7aeAWNJp3iyIz0VqZwrRxKCfYG8q74hLi15BeSKW%0AuE91tAKgZkds',
/ *1 * /  '预订',
/ *2 * /  '240000G1010C',
/ *3 * /  'G101',
/ *4 * /  'VNP',
/ *5 * /  'AOH',
/ *6 * /  'VNP',
/ *7 * /  'AOH',
/ *8 * /  '06:44',
/ *9 * /  '12:38',
/ *10 * / '05:54',
/ *11 * / 'Y',
/ *12 * / 'gugKt653kjpEc64uHfG51MyDTiGiP674QDaYp8GHqQ2cZOZV',
/ *13 * / '20170805',
/ *14 * / '3',
/ *15 * / 'P2',
/ *16 * / '01',
/ *17 * / '11',
/ *18 * / '1',
/ *19 * / '0',
/ *20 * / '',
/ *21 * / '',
/ *22 * / '',
/ *23 * / '',
/ *24 * / '',
/ *25 * / '',
/ *26 * / '',
/ *27 * / '',
/ *28 * / '',
/ *29 * / '',
/ *30 * / '有',
/ *31 * / '有',
/ *32 * / '16',
/ *33 * / '',
/ *34 * / 'O0M090',
/ *35 * / 'OM9'

其中，

3为车次、8为发车时间、9为到达时间、10为总时间、13为乘车日期
2为列车编号，可以根据这个查询车次中途停靠站信息
30为二等座，31为一等座、32为商务座、33为动卧
23为软卧、24为软座、26为无座、28为硬卧、29为硬座
6、7为实际的始发站和到达站
4、5为列车的始发站和到达站
```
