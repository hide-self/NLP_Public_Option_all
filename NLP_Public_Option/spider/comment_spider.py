"""
    微博评论内容 爬虫代码 把微博评论信息存到csv文件
    # https://weibo.com/ajax/statuses/buildComments?id=5208923479214750&is_show_bulletin=2
"""


import csv
import time
from datetime import datetime

from curl_cffi import requests

from util.stringUtil import clean_string


def init_csv():
    """
    初始化操作，判断csv文件是否存在，不能存在就创建一个
    :return:
    """
    with open('comment_data.csv', 'w', encoding='utf8',
              newline='') as file:  # newline=''参数，参数用于控制换行符的行为 这表示禁用自动换行符转换，即写入文件时使用原始的换行符（例如\r\n或\n）。这对于处理CSV文件时避免不必要的空行特别有用。
        writer = csv.writer(file)
        writer.writerow([
            'id',  # 评论信息id
            'text_raw',  # 评论内容
            'created_at',  # 创建日期
            'source',  # 发布位置 少部分没有这个值
            'like_counts',  # 点赞数
            'articleId',  # 微博id
            'userId',  # 评论用户id
            'userName',  # 评论用户名称
            'gender',  # 性别
            'userHomeUrl'  # 评论用户主页地址
        ])


def getAllArticleList():
    """
    获取所有微博信息
    :return:
    """
    articleList=[]
    with open('article_data.csv','r',encoding='utf8') as file:
        csv_reader=csv.reader(file)
        next(csv_reader)    # 不要头信息
        for article in csv_reader:
            articleList.append(article)
        return articleList


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
    response = requests.get(
        url=url,
        headers=headers,
        params=params,
        impersonate="chrome110"
    )

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
    with open('comment_data.csv', 'a', encoding='utf8',
              newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)

def parseJson(json,articleId):
    """
    解析json数据
    :param json:
    :param articleId:
    :return:
    """
    commentList=json['data']
    for comment in commentList:
        id = comment['id']
        text = clean_string(comment['text'])
        if text==None or text=='':  # 删除空了的话，该帖子不放入统计
            continue
        created_at = datetime.strptime(comment['created_at'], "%a %b %d %H:%M:%S %z %Y").strftime("%Y-%m-%d %H:%M:%S")
        source = comment.get('source', '来自').replace('来自', '').strip()
        like_counts = comment['like_counts']
        userId = comment['user']['id']
        userName = comment['user']['screen_name']
        gender = '男'
        g = comment['user']['gender']
        if g == 'f':
            gender = '女'
        userHomeUrl = 'https://weibo.com/u/%s' % comment['user']['id']

        writeToCsv([
            id,  # 评论信息id
            text,
            created_at,
            source,
            like_counts,
            articleId,
            userId,
            userName,
            gender,
            userHomeUrl
        ])

def start():
    url='https://weibo.com/ajax/statuses/buildComments'
    init_csv()
    articleList=getAllArticleList()

    print("微博内容评论信息爬取开始···")
    for article in articleList:
        print('正在爬取标题为：【%s】的微博评论数据' % article[1])
        time.sleep(0.2)
        params = {
            'id': article[0],
            'is_show_bulletin': 2,
        }
        jsonHtml=getJsonHtml(url, params)
        if jsonHtml:
            parseJson(jsonHtml,article[0])

    print("微博内容评论信息爬取结束")

# https://weibo.com/ajax/statuses/buildComments?id=5208923479214750&is_show_bulletin=2
if __name__=='__main__':
    start()
