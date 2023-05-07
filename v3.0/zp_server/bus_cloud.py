from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
import jieba
from data.mysqlHelper import get_a_conn


def GetWordCloud(data):
    try:
        print('开始生成词云图')
        path_img = "../zp_web/src/assets/imgs/cloud/cloud.png"
        # path_img = "../zp_web/src/assets/imgs/cloud/cloud.png"

        background_image = np.array(Image.open(path_img))
        # Python join() 方法用于将序列中的元素以指定的字符连接生成一个新的字符串。
        cut_text = " ".join(jieba.cut(data))

        wordcloud = WordCloud(
            # 设置字体，不然会出现口字乱码，文字的路径是电脑的字体一般路径，可以换成别的
            font_path="C:/Windows/Fonts/simfang.ttf",
            background_color="white",
            min_font_size=8,
            # mask参数=图片背景，必须要写上，另外有mask参数再设定宽高是无效的
            mask=background_image).generate(cut_text)
        # 生成颜色值
        image_colors = ImageColorGenerator(background_image)
        # 下面代码表示显示图片
        plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
        plt.axis("off")
        # plt.show()
        # 保存
        # plt.savefig('../zp_web/src/assets/imgs/cloud/fuliColoud.png')
        plt.savefig('../zp_web/src/assets/imgs/cloud/fuliColoud.png')
        plt.close()

        print('成功生成词云图')
        return '1'
    except Exception as e:
        print('失败：')
        print(e)
        return '0'


if __name__ == '__main__':
    short_evals = ""
    mysql = get_a_conn()
    sql3 = "SELECT fuli FROM tbl_job WHERE fuli != ''"
    evals = mysql.fetchall(sql3)
    for item in evals:
        short_evals += item.get('fuli')
    print(GetWordCloud(short_evals))
