import sys

import pandas as pd
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from wordcloud import WordCloud

sys.path.append('fenci')


def genWordCloudPic(str, maskImg, outImg):
    """
    生成云图
    :param str: 词云 空格隔开
    :param maskImg: 遮罩图片
    :param outImg: 输出的词云图文件名
    :return:
    """
    img = Image.open('./static/' + maskImg)  # 打开遮罩图片
    img_arr = np.array(img)  # 将图片转化为列表
    wc = WordCloud(
        width=800, height=600,
        background_color='white',
        colormap='Blues',
        font_path='STHUPO.TTF',
        mask=img_arr,
    )
    wc.generate_from_text(str)

    # 绘制图片
    plt.imshow(wc)
    plt.axis('off')  # 不显示坐标轴

    # 输入词语图片到文件
    plt.savefig('./static/' + outImg, dpi=500)
