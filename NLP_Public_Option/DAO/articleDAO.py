"""
    文章信息 数据访问对象
"""

from util import dbUtil


def getAllArticle():
    """
    获取所有评论
    :return:
    """

    con=None

    try:
        con=dbUtil.getCon()
        cursor=con.cursor()
        sql = "SELECT * from t_article"
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        con.rollback()
        return None
    finally:
        dbUtil.closeCon(con)

