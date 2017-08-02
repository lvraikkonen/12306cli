import re
import requests
# from pprint import pprint
import pickle


url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9020'
response = requests.get(url, verify=False)
stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)

stations = dict(stations)
# pprint(dict(stations), indent=4)

# stations_code_mapping = {station_code: station_name for station_name, station_code in stations.items()}


def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    # find_station_code("北京")
    # print(stations)
    save_obj(stations, 'station_dump')
