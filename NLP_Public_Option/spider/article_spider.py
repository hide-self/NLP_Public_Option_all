"""
    微博内容爬取，以及存储csv文件
    https://weibo.com/ajax/feed/hottimeline?since_id=0&refresh=0&group_id=102803&containerid=102803&extparam=discover%7Cnew_feed&max_id=0&count=10
"""
import csv
import time
from datetime import datetime

from curl_cffi import requests
from util.stringUtil import clean_string    # 之后会讲其中内容


def init_csv():
    """
    初始化操作，每次执行后初始化csv中的所有内容，值写入第一行的列名
    :return:
    """
    with open('article_data.csv', 'w', encoding='utf8',
              newline='') as file:  # newline=''参数，参数用于控制换行符的行为 这表示禁用自动换行符转换，即写入文件时使用原始的换行符（例如\r\n或\n）。这对于处理CSV文件时避免不必要的空行特别有用。
        writer = csv.writer(file)
        writer.writerow([
            'id',  # 帖子id
            'text_raw',  # 内容
            'reposts_count',  # 转发总数
            'comments_count',  # 评论总数
            'attitudes_count',  # 点赞总数
            'region_name',  # 发布位置 少部分没有这个值
            'created_at',  # 创建日期
            'articleType',  # 帖子类型
            'articleUrl',  # 帖子地址   https://weibo.com/userid/mblogid
            'authorId',  # 用户id
            'authorName',  # 用户名称
            'authorHomeUrl'  # 用户主页地址
        ])


def getAllTypeList():
    """
    获取所有微博类别信息，读取arcType_data.csv
    :return:
    """
    allTypeList = []

    with open('arcType_data.csv', 'r', encoding='utf8', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # 从第二行开始读取
        for articleType in reader:
            allTypeList.append(articleType)
        return allTypeList


def getJsonHtml(url, params):
    """
    请求获取Html内容 json数据
    :param url:
    :param params:
    :return:
    """
    headers = {
        'referer': 'https://weibo.com/newlogin?tabtype=weibo&gid=102803&openLoginLayer=0&url=https%3A%2F%2Fweibo.com%2F',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        'cookie': 'SCF=AtuyUqXBFVnetuJXSD1Uu4jkcksrMHsmqArTmcQ0Vvz7KwvLqcjDdLSr_SoW7IjiB6IjauIByLBK5k3s0GcaaaA.; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WF7OroSG-H_98HyIRMcopgF5JpVF02NS0-pShMpeK.p; SUB=_2AkMfnIjndcPxrARYnvERz2_nbYVH-jysSeERAn7uJhMyAxh87moQqSVutBF-XBUzOL4y3hqAzeDgkEa0wtsr4A6m; XSRF-TOKEN=lIuo6_yHzZRw71WS8W4HOeYG; WBPSESS=Dt2hbAUaXfkVprjyrAZT_JZ417LJEQncKUMDm21mjP4lVD5WsQe-8tUmQ6sDlx_6Y9lzRQiE7cmVQrFnq_JcqpEY5cA3rGQXNQXf5T6HNzPG6knB6viXVTTJHLeV9pXLqepmHIAgzI2M7dZN914nHw=='
    }
    response = requests.get(url, headers=headers, params=params, impersonate="chrome110")
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
    with open('article_data.csv', 'a', encoding='utf8',
              newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)


def parseJson(json,articleType):
    """
    解析Json数据,传入爬取的json数据json 和 articleType类别名称
    :param json
    :param articleType
    :return:
    """
    articleList=json['statuses']
    for article in articleList:
        id=article['id']    # 帖子id
        text_raw=clean_string(article['text_raw'])# 帖子内容  # 调用util.stringUtil的clean_string函数来清洗掉某些表情字符等不能存入数据库的字符
        if text_raw==None or text_raw=='':    # 删除空了的话，该帖子不放入统计
            continue
        reposts_count = article['reposts_count']    # 转发总数
        comments_count = article['comments_count']  # 评论总数
        attitudes_count = article['reposts_count']  # 点赞总数
        # 部分微博没有这个地区名称，所以需要用get方法来访问字典避免报错
        region_name = article.get('region_name', '发布于').replace('发布于', '').strip()  # 地区名称，去掉“发布于”和两侧空格
        # 发布时间的格式修改
        created_at = datetime.strptime(article['created_at'], "%a %b %d %H:%M:%S %z %Y").strftime("%Y-%m-%d %H:%M:%S")
        articleUrl = 'https://weibo.com/%s/%s' % (article['user']['id'], article['mblogid'])    # 博客的具体地址
        authorId = article['user']['id']    # 作者id
        authorName = article['user']['screen_name'] # 作者名字
        authorHomeUrl = 'https://weibo.com/u/%s' % article['user']['id']    # 作者主页地址

        writeToCsv([
            id,
            text_raw,
            reposts_count,
            comments_count,
            attitudes_count,
            region_name,
            created_at,
            articleType,
            articleUrl,
            authorId,
            authorName,
            authorHomeUrl
        ])

def start():
    url = 'https://weibo.com/ajax/feed/hottimeline'
    init_csv()
    allTypeList = getAllTypeList()
    # print(allTypeList)

    print('微博内容爬取开始···')
    for articleType in allTypeList:
        print('正在爬取"{0}"类别的微博文章···'.format(articleType[0]))
        time.sleep(1)
        params = {
            'since_id': '0',
            'refresh': '0',
            'group_id': '102803',
            'containerid': '102803',
            'extparam': 'discover|new_feed',  # %7C 的实际含义为： |
            'max_id': '0',
            'count': '10',
        }
        jsonHtml = getJsonHtml(url, params)
        parseJson(jsonHtml,articleType[0])



    print('微博内容爬取结束。')


if __name__ == '__main__':
    """
    https://weibo.com/ajax/feed/hottimeline?group_id=102803600169&containerid=102803_ctg1_600169_-_ctg1_600169&extparam=discover%7Cnew_feed
    """
    start()
