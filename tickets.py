# coding: utf-8

"""命令行火车票查看器

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
    tickets 北京 上海 2017-08-01
    tickets -dg 成都 南京 2017-08-01
"""
import os
import pickle
from docopt import docopt
from prettytable import PrettyTable
from colorama import init, Fore

# from parse_station_code import stations, stations_code_mapping
import requests


class TrainsCollections(object):

    """train_raw data item
    [
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
    ]
    3为车次、8为发车时间、9为到达时间、10为总时间、13为乘车日期
    2为列车编号，可以根据这个查询车次中途停靠站信息
    30为二等座，31为一等座、32为商务座、33为动卧
    23为软卧、24为软座、26为无座、28为硬卧、29为硬座
    6、7为实际的始发站和到达站
    4、5为列车的始发站和到达站
    """

    header = '车次 车站 时间 历时 一等 二等 软卧 硬卧 硬座 无座'.split()

    def __init__(self, available_trains, options):
        """查询到的火车班次集合

        : param available_trains: 一个列表，包含可获得的火车班次
        : param options: 查询选项
        """
        self.available_trains = available_trains
        self.options = options

    def _get_duration(self, raw_train):
        duration = raw_train[10].replace(':', '小时') + '分'
        if duration.startswith('00'): # less than 1 hour
            return duration[4:]
        if duration.startswith('0'):
            return duration[1:]
        return duration

    @property
    def trains(self):
        for raw_train in self.available_trains:
            train_info_lst = raw_train.split('|')
            train_no = train_info_lst[3]
            initial = train_no[0].lower()
            if not self.options or initial in self.options:
                train = [
                    train_no,
                    '\n'.join([Fore.GREEN + stations_code_mapping[train_info_lst[6]] + Fore.RESET,  # 始发站
                               Fore.RED + stations_code_mapping[train_info_lst[7]] + Fore.RESET]), # 到达站
                    '\n'.join([Fore.GREEN + train_info_lst[8] + Fore.RESET,  # 发车时间
                               Fore.RED + train_info_lst[9] + Fore.RESET]),# 到达时间
                    self._get_duration(train_info_lst),
                    train_info_lst[31], # 一等座
                    train_info_lst[30], # 二等座
                    train_info_lst[23], # 软卧
                    train_info_lst[28], # 硬卧
                    train_info_lst[29], # 硬座
                    train_info_lst[26], # 无座
                ]
                yield train

    def pretty_print(self):
        pt = PrettyTable()
        pt.field_names = self.header
        for train in self.trains:
            pt.add_row(train)
        print(pt)


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def _load_stations():
    filepath = os.path.join(os.path.dirname(__file__), 'station_dump.pkl')
    stations = {}
    with open(filepath, 'rb') as f:
        for line in f.readlines():
            name, code = line.split()
            stations[name] = code
    return stations


stations = load_obj('station_dump')
stations_code_mapping = {station_code: station_name for station_name, station_code in stations.items()}
QUERY_URL = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'



def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    print(arguments)
#     arguments = {'-d': True,
#      '-g': True,
#      '-k': False,
#      '-t': False,
#      '-z': False,
#      '<date>': '2017-08-05',
#      '<from>': '北京',
#      '<to>': '大连'}

    # params getting
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    url = QUERY_URL.format(date, from_station, to_station)

    options = ''.join([
        key for key, value in arguments.items() if value is True
    ])

    req = requests.get(url, verify=False)
    # print(req.json())
    available_trains = req.json()['data']['result']
    TrainsCollections(available_trains, options).pretty_print()
    # print(available_trains)



if __name__ == '__main__':
    cli()
