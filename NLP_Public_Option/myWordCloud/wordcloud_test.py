import numpy as np
from PIL import Image
from wordcloud import WordCloud
from matplotlib import pyplot as plt


def genWordCloudPic(str,maskImg,outImg):
    """
    生成词云图
    :param str:词云图内容文本 ,内容用空格隔开
    :param maskImg: 遮罩层图片名称
    :param outImg: 图片名称.类型(例子：test.jpg)
    :return:
    """

    img = Image.open(maskImg)  # 创建图片对象
    img_arr = np.array(img)  # 将图片转成图片数组，赋值到词云图的mask的参数中

    wc = WordCloud(
        width=800,
        height=600,
        background_color='white',
        colormap='Blues',
        font_path='STHUPO.TTF',  # 中文的一个字体文件（自带的）
        mask=img_arr  # 图片形状，传入一个ndarray数组
    )  # 设置词云图的外形

    wc.generate_from_text(str)  # 设置词云图的内容

    # 绘制图片，并展示
    plt.imshow(wc)

    # 不显示坐标轴
    plt.axis('off')

    # 保存图片
    plt.savefig(outImg, dpi=500)


if __name__=='__main__':
    text = "牛掰3 牛逼 大佬 我去 张三 卡卡 嘿嘿 哈哈 生成 商城 气死我了 不去 就不要 好滴 骄傲 好的 大战 发展 求生 共存 火了 刘安 伙计 火鸡 打火机"

    genWordCloudPic(text,'article_mask.jpg','wordcloud_test.jpg')


