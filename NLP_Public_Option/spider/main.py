"""
    调用爬取的函数，将爬取的数据持久化存储到MySQL中
"""


import pandas as pd
from sqlalchemy import create_engine

from arcType_spider import start as arcTypeSpiderStart
from article_spider import start as articleSpiderStart
from comment_spider import start as commentSpiderStart

engine = create_engine('mysql+pymysql://root:123456@localhost:3306/db_blog?charset=utf8mb4')

def dataClean():
    """
    数据清洗，对csv文件进行清洗，使用pandas库
    :return:
    """
    pass

def saveToDb():
    """
    将数据存储到数据库
    :return:
    """
    try:

        # 对文章数据的操作
        oldArticleDb = pd.read_sql('select * from t_article', engine)   # 读旧数据
        newArticleCsv = pd.read_csv('article_data.csv') # 读新数据
        concatArticlePd = pd.concat([newArticleCsv, oldArticleDb])  # 合并新旧数据
        resultArticlePd = concatArticlePd.drop_duplicates(subset='id', keep='last') # 对合并后数据去重
        resultArticlePd.to_sql('t_article', con=engine, if_exists='replace', index=False)   # 重新保存回sql

        # 对评论数据的操作和上述过程一直
        oldCommentDb = pd.read_sql('select * from t_comment', engine)
        newCommentCsv = pd.read_csv('comment_data.csv')
        concatCommentPd = pd.concat([newCommentCsv, oldCommentDb])
        resultCommentPd = concatCommentPd.drop_duplicates(subset='id', keep='last')
        resultCommentPd.to_sql('t_comment', con=engine, if_exists='replace', index=False)


    except Exception as e:
        print('异常:',e)

        newArticleCsv=pd.read_csv("article_data.csv")
        newCommentCsv=pd.read_csv("comment_data.csv")

        # to_sql()方法
        # 第一个参数传入数据表名字（未检测到会自动创建）
        # con传入数据库引擎
        # if_exists的三个值：replace表存在时替换，fall表存在时报错，append表存在时追加
        # index表示是否将dataframe的index当作列传入，False表示不传入
        newArticleCsv.to_sql('t_article', con=engine, if_exists='replace', index=False)
        newCommentCsv.to_sql('t_comment', con=engine, if_exists='replace', index=False)




if __name__=='__main__':
    # 爬取内容类型
    print("微博内容类型爬取开始···")
    # arcTypeSpiderStart()  # 若要重新爬取，就解开对他的注释
    print("微博内容类型爬取结束···")

    # 爬取内容
    print("微博内容爬取开始···")
    articleSpiderStart()  # 若要重新爬取，就解开对他的注释
    print("微博内容爬取结束···")


    # 爬取评论
    print("微博评论爬取开始···")
    commentSpiderStart()  # 若要重新爬取，就解开对他的注释
    print("微博评论爬取结束···")

    # 数据清洗
    print("数据清洗开始...")
    dataClean()
    print("数据清洗结束...")

    # 数据持久化存储到MySQL
    print("微博内容和评论信息持久化到数据库开始...")
    saveToDb()
    print("微博内容和评论信息持久化到数据库结束...")



