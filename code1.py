# %% [markdown]
# copyright: Shatong Zhu, Tongji Uni

# %%
import requests
from prettytable import PrettyTable
import pandas as pd
import re
import datetime

import requests
from prettytable import PrettyTable  # 美化库，PrettyTable模块可以将输出内容如表格方式整齐地输出
import re
from pprint import pprint  # 用于打印 Python 数据结构,输入格式整齐便于阅读
from time import sleep
# 一个python专门用来在控制台、命令行输出彩色文字的模块,Fore是针对字体颜色，Back是针对字体背景颜色，Style是针对字体格式
from colorama import Fore, Back, Style

import datetime

# %%
def getStationName():
    # 爬取12306网站所有车站名称信息
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9050'  # 车站信息控件
    r = requests.get(url)
    pattern = '([\u4e00-\u9fa5]+)\|([A-Z]+)'  # 正则匹配规则
    result = re.findall(pattern, r.text)
    stationName = dict(result)  # 所有车站信息，转换为字典
    # print(stationName)
    return stationName


def get_name_by_code(text, name):
    for station_name, code in text.items():
        if code == name:
            return station_name
    return "未找到"


text = getStationName()
print(text)
# 查看大小
print(len(text))

# %%
def get_visit_url(text, date, from_station, to_station):
    # 构建用于查询列车车次信息的url
    # 参数：日期，出发地，到达地
    # key为车站名称， value为车站代号

    date = date
    from_station = from_station+","+text[from_station]
    to_station = to_station+","+text[to_station]    # 新的url
    url = ("https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&"
           "fs={}"
           "&ts={}"
           "&date={}"
           "&flag=N,N,Y"
           ).format(from_station, to_station, date)
    print(url)
    
get_visit_url(text, '2024-08-08', '上海', '北京')

# %%
def get_query_url(text, date, from_station, to_station):
    # 构建用于查询列车车次信息的url
    # 参数：日期，出发地，到达地
    # key为车站名称， value为车站代号

    date = date
    from_station = text[from_station]
    to_station = text[to_station]    # 新的url
    url = ("https://kyfw.12306.cn/otn/leftTicket/queryE?leftTicketDTO.train_date={}"
           "&leftTicketDTO.from_station={}"
           "&leftTicketDTO.to_station={}"
           "&purpose_codes=ADULT"
           ).format(date, from_station, to_station)
    return url

get_query_url(text, '2024-08-08', '上海','北京')

# %%
def get_price_url(text, date, from_station, to_station):
    # 构建用于查询列车车次信息的url
    # 参数：日期，出发地，到达地
    # key为车站名称， value为车站代号

    date = date
    from_station = text[from_station]
    to_station = text[to_station]    # 新的url
    
    url = ("https://kyfw.12306.cn/otn/leftTicketPrice/query?leftTicketDTO.train_date={}"
           "&leftTicketDTO.from_station={}"
           "&leftTicketDTO.to_station={}"
           ).format(date, from_station, to_station)
    return url


get_price_url(text, '2024-08-08', '上海', '北京')

# %%
def get_price(text, date, from_station, to_station, show=False):
    try:

        url = get_price_url(text, date, from_station, to_station)

        headers = {
            'Cookie': f'_jc_save_toStation={text[from_station]}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76',
        }

        r = requests.get(url=url, headers=headers)

        results = r.json()['data']

        tb = PrettyTable()
        tb.field_names = ['车次',  "起点站", "起点站代号", "终点站", "终点站代号",   "出发站", "出发站代号", "到站", "到站代号",'持续时间','二等座 ' ]

        acc = []
        
        
        for i in results:
            traindata = i["queryLeftNewDTO"]
            #print(traindata)
            
            tb.add_row([ 
                traindata["station_train_code"],
                traindata["start_station_name"],
                traindata["start_station_telecode"],
                traindata["end_station_name"],
                traindata["end_station_telecode"],
                traindata["from_station_name"],
                traindata["from_station_telecode"],
                traindata["to_station_name"],
                traindata["to_station_telecode"],
                
             
                traindata["lishi"],
                
                
                traindata["ze_price"], # 二等座
                
   

                        ])
            
            acc.append(
                [ 
                date, 
                traindata["station_train_code"],
                traindata["start_station_name"],
                traindata["start_station_telecode"],
                traindata["end_station_name"],
                traindata["end_station_telecode"],
                traindata["from_station_name"],
                traindata["from_station_telecode"],
                traindata["to_station_name"],
                traindata["to_station_telecode"],
                
               
                traindata["lishi"],
                

                traindata["ze_price"], # 二等座
  
                        ]
                )
            
        if show:
            print(tb)
        return acc

    except Exception as e:
        return e


get_price(text, '2024-08-08', '上海', '如皋', show=True)


