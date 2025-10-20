import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from snownlp import SnowNLP

from util import wordcloudUtil, mapUtil
from util.dbUtil import getCon, closeCon


# Create your views here.

# 测试视图
def index(request):
    return render(request, 'hello3.html')


# 下面的是数据库查询函数
def getArticleCount() -> int:
    """
    数据库查询函数，获取总文章数
    :return:
    """
    conn = getCon()  # 启动数据库连接
    cursor = conn.cursor()  # 创建光标对象

    cursor.execute("select count(id) from t_article")
    data = cursor.fetchall()
    # print(data) # ((1119,),)

    cursor.close()  # 关闭光标对象
    closeCon(conn)  # 关闭数据库链接对象

    return data[0][0]


def get_maxAttitude_AutherName() -> int:
    """
    数据库查询函数，获取获得最多点赞的博客的作者名
    :return:
    """
    conn = getCon()  # 启动数据库连接
    cursor = conn.cursor()  # 创建光标对象

    cursor.execute("SELECT authorName,attitudes_count FROM t_article ORDER BY attitudes_count DESC LIMIT 1;")
    data = cursor.fetchall()
    # print(data) # (('微博音乐盛典', 1000000),)

    cursor.close()  # 关闭光标对象
    closeCon(conn)  # 关闭数据库链接对象

    return data[0][0]


def get_maxAttitude_RegionName() -> int:
    """
    数据库查询函数，获取获得最多点赞的城市
    :return:
    """
    conn = getCon()  # 启动数据库连接
    cursor = conn.cursor()  # 创建光标对象

    cursor.execute(
        "SELECT region_name,SUM(attitudes_count) as atc FROM t_article GROUP BY region_name ORDER BY atc DESC LIMIT 1;")
    data = cursor.fetchall()
    # print(data)  # (('北京', Decimal('32807046')),)

    cursor.close()  # 关闭光标对象
    closeCon(conn)  # 关闭数据库链接对象

    return data[0][0]


def get_Top6_Article():
    """
        数据库查询函数，点赞量前6的帖子
        :return:
    """
    conn = getCon()  # 启动数据库连接
    cursor = conn.cursor()  # 创建光标对象

    cursor.execute("select text_raw,attitudes_count from t_article order by attitudes_count DESC LIMIT 0,6")
    data = cursor.fetchall()
    # print(data)
    # (('镜头给到自己串串花少花儿与少年', 1000000),
    # ('美酒献给空余位', 1000000),
    # ('这个七老童心不基础那姐不基础那小大买菜更不基础花儿与少年', 1000000),
    # ('预判了哥哥们的预判又拿到心仪的歌曲咯披荆斩棘', 1000000),
    # ('一人一个王牌养生方式我宣誓我再也不熬夜了跟发炎肿痛说不快来跟我一起加入养生队伍吧王牌对王牌', 1000000),
    # ('以CT夏洛特蒂铂丽磨法师打开磨皮底妆新思路全新升级CT超磨瓶粉底液开启无瑕时刻', 1000000))

    cursor.close()  # 关闭光标对象
    closeCon(conn)  # 关闭数据库链接对象

    return data


def get_7Day_ArticleCount():
    """
        数据库查询函数，获取数据库中收录的最近7日的微博帖子（若要更新，重新爬取）
        :return:
    """
    conn = getCon()  # 启动数据库连接
    cursor = conn.cursor()  # 创建光标对象

    cursor.execute(
        "select DATE_FORMAT(created_at,'%Y-%m-%d') as articleDate,COUNT(id) from t_article GROUP BY articleDate ORDER BY articleDate DESC LIMIT 0,7;")
    data = cursor.fetchall()
    # print(data) # (('2025-09-16', 173), ('2025-09-15', 158), ('2025-09-14', 72), ('2025-09-13', 68), ('2025-09-12', 59), ('2025-09-11', 51), ('2025-09-10', 284))

    cursor.close()  # 关闭光标对象
    closeCon(conn)  # 关闭数据库链接对象

    return data


def getArticleTypeAmount():
    """
        数据库查询函数，获取帖子类别数量
        :return:
    """
    conn = getCon()  # 启动数据库连接
    cursor = conn.cursor()  # 创建光标对象

    cursor.execute("select articleType,count(articleType) from t_article group by articleType")
    data = cursor.fetchall()
    # print(data) # (('热门', 2), ('明星', 8), ('情感', 37), ('短剧', 19), ('印像', 22), ('周末', 19), ('电影', 28), ('社会', 11), ('电视剧', 7), ('国际', 10), ('深度', 29), ('财经', 28), ('读书', 9), ('汽车', 21), ('颜值', 36), ('体育', 20), ('综艺', 28), ('股市', 36), ('家居', 35), ('萌宠', 11), ('科技', 19), ('科普', 17), ('动漫', 37), ('运动健身', 35), ('瘦身', 37), ('好物', 28), ('历史', 30), ('艺术', 20), ('美妆', 20), ('法律', 28), ('设计', 27), ('健康', 30), ('音乐', 39), ('新时代', 35), ('校园', 29), ('收藏', 36), ('政务', 37), ('育儿', 39), ('教育', 40), ('婚恋', 31), ('舞蹈', 38), ('辟谣', 40), ('公益', 39), ('三农', 36), ('搞笑', 10), ('美食', 11), ('摄影', 17), ('数码', 17), ('时尚', 11), ('星座', 10), ('军事', 11), ('旅游', 11))

    cursor.close()  # 关闭光标对象
    closeCon(conn)  # 关闭数据库链接对象

    return data


def getTopCommentUser():
    """
        数据库查询函数，获取评论次数前50名的用户名
        :return:
    """
    conn = getCon()  # 启动数据库连接
    cursor = conn.cursor()  # 创建光标对象

    cursor.execute(
        "SELECT username,COUNT(username) AS userCount FROM t_comment GROUP BY username ORDER BY userCount DESC LIMIT 0,50;")
    data = cursor.fetchall()
    # print(data)

    cursor.close()  # 关闭光标对象
    closeCon(conn)  # 关闭数据库链接对象

    return data


def getCommentAmount():
    """
        数据库查询函数，获取评论数量(最近7天)
        :return:
    """
    conn = getCon()  # 启动数据库连接
    cursor = conn.cursor()  # 创建光标对象

    cursor.execute(
        "select DATE_FORMAT(created_at, '%Y-%m-%d') as commentDate,count(text_raw) as commentTotal from t_comment group by DATE_FORMAT(created_at, '%Y-%m-%d')  order by commentDate desc limit 0,7")
    data = cursor.fetchall()
    # print(data)

    cursor.close()  # 关闭光标对象
    closeCon(conn)  # 关闭数据库链接对象

    return data


def getCommentHotWordAmount(hotWord):
    """
        数据库查询函数，统计所选择热词语近7日的数目
        :return:
    """
    conn = getCon()  # 启动数据库连接
    cursor = conn.cursor()  # 创建光标对象

    cursor.execute(
        f"SELECT DATE_FORMAT(created_at, '%Y-%m-%d') AS commentDate,COUNT(text_raw) AS commentTotal FROM t_comment WHERE LOCATE('{hotWord}',text_raw)>0 GROUP BY DATE_FORMAT(created_at, '%Y-%m-%d')  ORDER BY commentDate DESC")
    data = cursor.fetchall()
    # print(data)

    cursor.close()  # 关闭光标对象
    closeCon(conn)  # 关闭数据库链接对象

    return data


def getCommentByHotWord(hotWord):
    """
        数据库查询函数，查询所有包含该热词的评论
        :return:
    """
    conn = getCon()  # 启动数据库连接
    cursor = conn.cursor()  # 创建光标对象

    cursor.execute(f"select * from t_comment where locate('{hotWord}',text_raw)>0")
    data = cursor.fetchall()
    # print(data)

    cursor.close()  # 关闭光标对象
    closeCon(conn)  # 关闭数据库链接对象

    return data


def getAllArticle():
    """
    获取所有帖子信息
    :return:
    """
    conn = getCon()  # 启动数据库连接
    cursor = conn.cursor()  # 创建光标对象

    cursor.execute("select * from t_article")
    data = cursor.fetchall()
    # print(data)

    cursor.close()  # 关闭光标对象
    closeCon(conn)  # 关闭数据库链接对象

    return data


def getAllComment():
    """
        获取所有评论信息
        :return:
    """
    conn = getCon()  # 启动数据库连接
    cursor = conn.cursor()  # 创建光标对象

    cursor.execute("select * from t_comment")
    data = cursor.fetchall()
    # print(data)

    cursor.close()  # 关闭光标对象
    closeCon(conn)  # 关闭数据库链接对象

    return data


def getArticleByArcType(defaultArcType):
    """
        获取对应类型的所有贴子
        :return:
        """
    conn = getCon()  # 启动数据库连接
    cursor = conn.cursor()  # 创建光标对象

    cursor.execute(f"select * from t_article where articleType='{defaultArcType}';")
    data = cursor.fetchall()
    # print(data)

    cursor.close()  # 关闭光标对象
    closeCon(conn)  # 关闭数据库链接对象

    return data


def getRandComment():
    """
        随机获取1000评论信息
        :return:
    """
    conn = getCon()  # 启动数据库连接
    cursor = conn.cursor()  # 创建光标对象

    cursor.execute("SELECT * FROM t_comment ORDER BY RAND() LIMIT 1000;")
    data = cursor.fetchall()
    # print(data)

    cursor.close()  # 关闭光标对象
    closeCon(conn)  # 关闭数据库链接对象

    return data

def getRandArticle():
    """
        随机获取300博客文章信息
        :return:
    """
    conn = getCon()  # 启动数据库连接
    cursor = conn.cursor()  # 创建光标对象

    cursor.execute("SELECT * FROM t_article ORDER BY RAND() LIMIT 300;")
    data = cursor.fetchall()
    # print(data)

    cursor.close()  # 关闭光标对象
    closeCon(conn)  # 关闭数据库链接对象

    return data


# 下面的都是页面视图

def getHomePageData(request):
    """
    获取主页数据 ajax异步交互 前端每隔10分钟请求一次 实时数据
    :return:
    """

    return JsonResponse({
        'totalArticle': getArticleCount(),
        'topAuthor': get_maxAttitude_AutherName(),
        'topRegion': get_maxAttitude_RegionName(),
        'topArticles': get_Top6_Article()
    })


def home(request):
    # 7日微博每日的帖子总量
    articleData_7Days = get_7Day_ArticleCount()
    xAxis7ArticleData = []
    yAxis7ArticleData = []
    for article in articleData_7Days:
        xAxis7ArticleData.append(article[0])
        yAxis7ArticleData.append(article[1])

    # 获取帖子类别数量，作为饼图数据
    arcTypeData = []
    articleTypeAmountList = getArticleTypeAmount()
    for arcType in articleTypeAmountList:
        arcTypeData.append({'value': arcType[1], 'name': arcType[0]})

    # 获取top50评论用户名
    top50CommentUserList = getTopCommentUser()
    top50CommentUserNameList = [cu[0] for cu in top50CommentUserList]
    str = ' '.join(top50CommentUserNameList)
    # 生成评论用户名词云图
    wordcloudUtil.genWordCloudPic(str, 'comment_mask.jpg', 'comment_user_cloud.jpg')

    commentData = []
    commentAmountList = getCommentAmount()
    for comment in commentAmountList:
        commentData.append({'value': comment[1], 'name': comment[0]})

    return render(request, 'index.html',
                  context={
                      'username': request.session['username'],
                      'xAxis7ArticleData': xAxis7ArticleData,
                      'yAxis7ArticleData': yAxis7ArticleData,
                      'arcTypeData': arcTypeData,
                      'commentData': commentData
                  })


def hotWord(request):
    """
    热词分析统计
    :return:
    """
    hotWordList = []
    # 只读取前100条
    df = pd.read_csv('./cut_scentence/comment_fre.csv', nrows=100)
    for value in df.values:
        hotWordList.append(value[0])
    # 获取请求参数，如果没有获取到，给个默认值 第一个列表数据
    defaultHotWord = request.GET.get('word', default=hotWordList[0])
    hotWordNum = 0  # 出现次数
    for value in df.values:
        if defaultHotWord == value[0]:
            hotWordNum = value[1]
    # 情感分析
    sentiments = ''
    stc = SnowNLP(defaultHotWord).sentiments
    if stc > 0.6:
        sentiments = '正面'
    elif stc < 0.2:
        sentiments = '负面'
    else:
        sentiments = '中性'

    # 生成热词近几天的统计图
    commentHotWordData = getCommentHotWordAmount(defaultHotWord)
    xAxisHotWordData = []
    yAxisHotWordData = []
    for comment in commentHotWordData:
        xAxisHotWordData.append(comment[0])
        yAxisHotWordData.append(comment[1])

    # 根据热词查询评论信息
    commentList = getCommentByHotWord(defaultHotWord)

    return render(
        request,
        'hotWord.html',
        context={
            'username': request.session['username'],
            'defaultHotWord': defaultHotWord,
            'hotWordList': hotWordList,
            'hotWordNum': hotWordNum,
            'sentiments': sentiments,
            'xAxisHotWordData': xAxisHotWordData,
            'yAxisHotWordData': yAxisHotWordData,
            'commentList': commentList
        }
    )


def articleData(request):
    """
    微博舆情分析
    :return:
    """
    articleOldList = getAllArticle()
    articleNewList = []
    for article in articleOldList:
        article = list(article)
        # 情感分析
        sentiments = ''
        try:
            stc = SnowNLP(article[1]).sentiments
            if stc > 0.6:
                sentiments = '正面'
            elif stc < 0.2:
                sentiments = '负面'
            else:
                sentiments = '中性'
        except Exception as e:
            print(article[1])
            sentiments = '中性'
        article.append(sentiments)
        articleNewList.append(article)
    return render(request, 'articleData.html',
                  context={'username': request.session['username'], 'articleList': articleNewList})


def articleDataAnalysis(request):
    """
    文章数据分析
    :return:
    """
    arcTypeList = []
    df = pd.read_csv('./spider/arcType_data.csv')
    for value in df.values:
        arcTypeList.append(value[0])
    # 获取请求参数，如果没获取到，给个默认值 第一个列表数据。
    defaultArcType = request.GET.get('arcType', default=arcTypeList[0])

    articleList = getArticleByArcType(defaultArcType)
    xDzData = []  # 点赞x轴数据
    xPlData = []  # 评论x轴数据
    xZfData = []  # 转发x轴数据
    rangeNum = 1000
    rangeNum2 = 100
    for item in range(0, 10):
        xDzData.append(str(rangeNum * item) + '-' + str(rangeNum * (item + 1)))
        xPlData.append(str(rangeNum * item) + '-' + str(rangeNum * (item + 1)))
    for item in range(0, 20):
        xZfData.append(str(rangeNum2 * item) + '-' + str(rangeNum2 * (item + 1)))
    xDzData.append('1万+')
    xPlData.append('1万+')
    xZfData.append('2千+')
    yDzData = [0 for x in range(len(xDzData))]  # 点赞y轴数据
    yPlData = [0 for x in range(len(xPlData))]  # 评论y轴数据
    yZfData = [0 for x in range(len(xZfData))]  # 转发y轴数据
    for article in articleList:
        for item in range(len(xDzData)):
            if int(article[4]) < rangeNum * (item + 1):
                yDzData[item] += 1
                break
            elif int(article[4]) > 10000:
                yDzData[len(xDzData) - 1] += 1
                break
        for item in range(len(xPlData)):
            if int(article[3]) < rangeNum * (item + 1):
                yPlData[item] += 1
                break
            elif int(article[3]) > 10000:
                yPlData[len(xPlData) - 1] += 1
                break
    for article in articleList:
        for item in range(len(xZfData)):
            if int(article[2]) < rangeNum2 * (item + 1):
                yZfData[item] += 1
                break
            elif int(article[2]) > 2000:
                yZfData[len(xZfData) - 1] += 1
                break
    return render(request, 'articleDataAnalysis.html', context={
        'username': request.session['username'],
        'arcTypeList': arcTypeList,
        'defaultArcType': defaultArcType,
        'xDzData': xDzData,
        'yDzData': yDzData,
        'xPlData': xPlData,
        'yPlData': yPlData,
        'xZfData': xZfData,
        'yZfData': yZfData
    })


def ipDataAnalysis(request):
    """
    IP地址数据分析
    :return:
    """

    cityDic = {}  # 微博文章作者IP
    cityList = mapUtil.cityList
    articleList = getAllArticle()
    for article in articleList:
        if article[5]:
            for city in cityList:
                if city['province'].find(article[5]) != -1:
                    if cityDic.get(city['province'], -1) == -1:
                        cityDic[city['province']] = 1
                    else:
                        cityDic[city['province']] += 1
    articleCityDicList = [{
        'name': x[0],
        'value': x[1]
    } for x in cityDic.items()]

    cityDic2 = {}  # 微博评论作者IP
    commentList = getAllComment()
    for comment in commentList:
        if comment[3]:
            for city in cityList:
                if city['province'].find(comment[3]) != -1:
                    if cityDic2.get(city['province'], -1) == -1:
                        cityDic2[city['province']] = 1
                    else:
                        cityDic2[city['province']] += 1
    commentCityDicList = [{
        'name': x[0],
        'value': x[1]
    } for x in cityDic2.items()]

    return render(request, 'ipDataAnalysis.html', context={
        'username': request.session['username'],
        'articleCityDicList': articleCityDicList,
        'commentCityDicList': commentCityDicList
    })


def commentDataAnalysis(request):
    """
    微博评论数据分析
    :return:
    """
    commentList = getAllComment()
    xDzData = []  # 点赞x轴数据
    rangeNum = 5
    for item in range(0, 20):
        xDzData.append(str(rangeNum * item) + '-' + str(rangeNum * (item + 1)))
    xDzData.append('1百+')
    genderDic = {'男': 0, '女': 0}
    yDzData = [0 for x in range(len(xDzData))]  # 点赞y数据
    for comment in commentList:
        for item in range(len(xDzData)):
            if int(comment[4] < rangeNum * (item + 1)):
                yDzData[item] += 1
                break
            elif int(comment[4]) > 100:
                yDzData[len(xDzData) - 1] += 1
        if genderDic.get(comment[8], -1) != -1:
            genderDic[comment[8]] += 1
    genderData = [{
        'name': x[0],
        'value': x[1]
    } for x in genderDic.items()]

    # 只读取前50条
    df = pd.read_csv('./cut_scentence/comment_fre.csv', nrows=50)
    hotCommentWordList = [x[0] for x in df.values]
    str2 = ' '.join(hotCommentWordList)
    wordcloudUtil.genWordCloudPic(str2, 'comment_mask.jpg', 'comment_cloud.jpg')

    return render(request, 'commentDataAnalysis.html', context={
        'username': request.session['username'],
        'xDzData': xDzData,
        'yDzData': yDzData,
        'genderData': genderData
    })


def sentimentAnalysis(request):
    """
    舆情数据分析
    :return:
    """
    xHotBarData = ['正面', '中性', '负面']
    yHotBarData = [0, 0, 0]
    # 只读取前100条
    df = pd.read_csv('./cut_scentence/comment_fre.csv', nrows=100)
    for value in df.values:
        # 情感分析
        stc = SnowNLP(value[0]).sentiments
        if stc > 0.6:
            yHotBarData[0] += 1
        elif stc < 0.2:
            yHotBarData[2] += 1
        else:
            yHotBarData[1] += 1

    hotTreeMapData = [{
        'name': xHotBarData[0],
        'value': yHotBarData[0]
    }, {
        'name': xHotBarData[1],
        'value': yHotBarData[1]
    }, {
        'name': xHotBarData[2],
        'value': yHotBarData[2]
    }]

    commentPieData = [{
        'name': '正面',
        'value': 0
    }, {
        'name': '中性',
        'value': 0
    }, {
        'name': '负面',
        'value': 0
    }]
    articlePieData = [{
        'name': '正面',
        'value': 0
    }, {
        'name': '中性',
        'value': 0
    }, {
        'name': '负面',
        'value': 0
    }]

    commentList = getRandComment()
    for comment in commentList:
        # 情感分析
        stc = SnowNLP(comment[1]).sentiments
        if stc > 0.6:
            commentPieData[0]['value'] += 1
        elif stc < 0.2:
            commentPieData[2]['value'] += 1
        else:
            commentPieData[1]['value'] += 1

    articleList = getRandArticle()
    for article in articleList:
        # 情感分析
        stc = SnowNLP(article[1]).sentiments
        if stc > 0.6:
            articlePieData[0]['value'] += 1
        elif stc < 0.2:
            articlePieData[2]['value'] += 1
        else:
            articlePieData[1]['value'] += 1

    # 只读取前15条
    df2 = pd.read_csv('./cut_scentence/comment_fre.csv', nrows=15)
    xhotData15 = [x[0] for x in df2.values][::-1]
    yhotData15 = [x[1] for x in df2.values][::-1]

    return render(request, 'sentimentAnalysis.html', context={
        'username': request.session['username'],
        'xHotBarData': xHotBarData,
        'yHotBarData': yHotBarData,
        'hotTreeMapData': hotTreeMapData,
        'commentPieData': commentPieData,
        'articlePieData': articlePieData,
        'xhotData15':xhotData15,
        'yhotData15':yhotData15
    })


def articleCloud(request):
    """
    微博内容词云图
    :return:
    """
    # 只读取前50条
    df = pd.read_csv('./cut_scentence/article_fre.csv', nrows=50)
    hotArticleWordList = [x[0] for x in df.values]
    str2 = ' '.join(hotArticleWordList)
    wordcloudUtil.genWordCloudPic(str2, 'article_mask.jpg', 'article_cloud.jpg')
    return render(request,'articleCloud.html',context={
        'username':request.session['username']
    })


def commentUserCloud(request):
    """
    微博评论用户词云图
    :return:
    """
    # 获取top50评论用户名
    top50CommentUserList = getTopCommentUser()
    top50CommentUserNameList = [cu[0] for cu in top50CommentUserList]
    str = ' '.join(top50CommentUserNameList)
    # 生成评论用户名词云图
    wordcloudUtil.genWordCloudPic(str, 'comment_mask.jpg', 'comment_user_cloud.jpg')
    return render(request,'commentUserCloud.html',context={
        'username':request.session['username']
    })


def commentCloud(request):
    """
    微博评论词云图
    :return:
    """
    # 只读取前50条
    df = pd.read_csv('./cut_scentence/comment_fre.csv', nrows=50)
    hotCommentWordList = [x[0] for x in df.values]
    str2 = ' '.join(hotCommentWordList)
    wordcloudUtil.genWordCloudPic(str2, 'comment_mask.jpg', 'comment_cloud.jpg')
    return render(request,'commentCloud.html',context={
        'username':request.session['username']
    })

if __name__ == '__main__':
    # getArticleCount()
    # get_maxAttitude_AutherName()
    # get_maxAttitude_RegionName()
    # get_Top6_Article()
    # get_7Day_ArticleCount()
    getArticleTypeAmount()
