from pymysql import Connection


def getCon():
    """
    获取数据连接
    :return: 数据库连接
    """
    con = Connection(
        host="localhost",  # 主机名
        port=3306,  # 端口
        user="root",  # 账户
        password="123456",  # 密码
        database="db_blog",  # 数据库
        autocommit=True  # 设置自动提交，可以去掉每次增删改后的con.commit()操作
    )
    return con


def closeCon(con: Connection):
    """
    关闭数据库连接
    :param con: 数据库连接
    :return:
    """
    if con:
        con.close()