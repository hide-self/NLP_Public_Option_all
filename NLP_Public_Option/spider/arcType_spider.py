"""
    https://weibo.com/ajax/feed/allGroups?is_new_segment=1&fetch_hot=1
    微博类别 爬虫代码 以及存到csv文件中
"""
import csv

import numpy as np
from curl_cffi import requests


def init_csv():
    """
    初始化操作，每次执行后初始化csv中的所有内容，值写入第一行的列名
    :return:
    """
    with open('arcType_data.csv', 'w', encoding='utf8',
              newline='') as file:  # newline=''参数，参数用于控制换行符的行为 这表示禁用自动换行符转换，即写入文件时使用原始的换行符（例如\r\n或\n）。这对于处理CSV文件时避免不必要的空行特别有用。
        writer = csv.writer(file)
        writer.writerow([
            '类别标题(title)',
            '分组id(gid)',
            '分类id(containerid)'
        ])

def getJsonHtml(url, params):
    """
    请求获取Html内容 json数据
    :param url:
    :param params:
    :return:
    """
    headers = {
        'referer': 'https://weibo.com/newlogin?tabtype=weibo&gid=1028034288&openLoginLayer=0&url=https%3A%2F%2Fweibo.com%2Fhot%2Fweibo%2F102803',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        'cookie': 'SCF=AtuyUqXBFVnetuJXSD1Uu4jkcksrMHsmqArTmcQ0Vvz7KwvLqcjDdLSr_SoW7IjiB6IjauIByLBK5k3s0GcaaaA.; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WF7OroSG-H_98HyIRMcopgF5JpVF02NS0-pShMpeK.p; SUB=_2AkMfnIjndcPxrARYnvERz2_nbYVH-jysSeERAn7uJhMyAxh87moQqSVutBF-XBUzOL4y3hqAzeDgkEa0wtsr4A6m; XSRF-TOKEN=3kupyyrVNskqyxHyW839xMVy; WBPSESS=Dt2hbAUaXfkVprjyrAZT_JZ417LJEQncKUMDm21mjP4lVD5WsQe-8tUmQ6sDlx_6Y9lzRQiE7cmVQrFnq_JcqhFwAv4avMbR-9-DzCEt9HH5-2U8mhZIH1kCN-6Yx1rFkgVB6bfqsHpyk5769Lfbyw=='
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def writeToCsv(row):
    """
    写入csv操作 a操作 尾部追加 写入操作
    :param row:
    :return:
    """
    with open('arcType_data.csv', 'a', encoding='utf8',
              newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)


def parseJson(json):
    """
    解析Json数据
    :param json:
    :return:
    """
    arcTypeList = np.append(json['groups'][3]['group'], json['groups'][4]['group'])

    print(type(arcTypeList))
    print(arcTypeList)

    for arcType in arcTypeList:
        arcType_title = arcType['title']
        gid = arcType['gid']
        containerid = arcType['containerid']
        writeToCsv([arcType_title, gid, containerid])


def start():
    init_csv()
    url = 'https://weibo.com/ajax/feed/allGroups?is_new_segment=1&fetch_hot=1'
    jsonHtml = getJsonHtml(url, {})
    print(jsonHtml)
    parseJson(jsonHtml)


if __name__ == '__main__':
    start()
