"""
微博评论信息分词 词频统计
"""

import re

import jieba
import pandas as pd

from DAO import commentDAO




def getStopWordsList():
    """
    获取停顿词
    :return:
    """
    return [line.strip() for line in open('stopWords.txt', encoding='UTF-8').readlines()]



def cut_comment():
    """
    将评论从数据库中读取，并分词
    :return:
    """

    allComment_Str=' '.join([comment[1].strip() for comment in commentDAO.getAllComment()])
    seg_list_accurate=jieba.cut(allComment_Str)

    return seg_list_accurate


def word_fre_count():
    """
    词频统计 过滤数据，单个字以及停顿词
    :return:
    """
    seg_list = cut_comment()    # 获取分词后的列表
    stopWord_list = getStopWordsList()  # 获取停顿词

    new_seg_list=[] # 新列表中存放 去除数字和停顿次 的分词
    # 用正则来去除数字，之后去掉停顿词
    for s in seg_list:
        number = re.search('\d+', s)
        if not number and s not in stopWord_list and len(s) > 1:
            new_seg_list.append(s)

    # 词频统计
    wfc = {}
    for w in set(new_seg_list):
        wfc[w] = new_seg_list.count(w)

    # 排序
    sorted_wfc_list = sorted(wfc.items(), key=lambda x: x[1], reverse=True)
    return sorted_wfc_list

def outCommentFreToCsv(sorted_wfc_list):
    """
    词频统计后，写入到csv
    :param sorted_wfc_list:
    :return:
    """
    df = pd.DataFrame(sorted_wfc_list, columns=['热词', '数量'])
    df.to_csv('comment_fre.csv', index=False)

if __name__=='__main__':
    outCommentFreToCsv(word_fre_count())

