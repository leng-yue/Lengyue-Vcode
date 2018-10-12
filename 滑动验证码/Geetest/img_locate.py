"""
此文件代码来自 https://github.com/OSinoooO/bilibili_geetest/blob/master/bilibili_geetest_crack.py
"""

from PIL import Image


class ImgProcess:
    location_list = [
        {'y': -58, 'x': -157},
        {'y': -58, 'x': -145},
        {'y': -58, 'x': -265},
        {'y': -58, 'x': -277},
        {'y': -58, 'x': -181},
        {'y': -58, 'x': -169},
        {'y': -58, 'x': -241},
        {'y': -58, 'x': -253},
        {'y': -58, 'x': -109},
        {'y': -58, 'x': -97},
        {'y': -58, 'x': -289},
        {'y': -58, 'x': -301},
        {'y': -58, 'x': -85},
        {'y': -58, 'x': -73},
        {'y': -58, 'x': -25},
        {'y': -58, 'x': -37},
        {'y': -58, 'x': -13},
        {'y': -58, 'x': -1},
        {'y': -58, 'x': -121},
        {'y': -58, 'x': -133},
        {'y': -58, 'x': -61},
        {'y': -58, 'x': -49},
        {'y': -58, 'x': -217},
        {'y': -58, 'x': -229},
        {'y': -58, 'x': -205},
        {'y': -58, 'x': -193},
        {'y': 0, 'x': -145},
        {'y': 0, 'x': -157},
        {'y': 0, 'x': -277},
        {'y': 0, 'x': -265},
        {'y': 0, 'x': -169},
        {'y': 0, 'x': -181},
        {'y': 0, 'x': -253},
        {'y': 0, 'x': -241},
        {'y': 0, 'x': -97},
        {'y': 0, 'x': -109},
        {'y': 0, 'x': -301},
        {'y': 0, 'x': -289},
        {'y': 0, 'x': -73},
        {'y': 0, 'x': -85},
        {'y': 0, 'x': -37},
        {'y': 0, 'x': -25},
        {'y': 0, 'x': -1},
        {'y': 0, 'x': -13},
        {'y': 0, 'x': -133},
        {'y': 0, 'x': -121},
        {'y': 0, 'x': -49},
        {'y': 0, 'x': -61},
        {'y': 0, 'x': -229},
        {'y': 0, 'x': -217},
        {'y': 0, 'x': -193},
        {'y': 0, 'x': -205}
    ]

    def get_merge_image(self, filename):
        """
        根据图片位置合并还原
        :param filename: 图片
        :param location: 位置
        :return:合并后的图片对象
        """
        im = Image.open(filename)

        new_im = Image.new('RGB', (260, 116))
        im_list_upper = []
        im_list_lower = []

        for location in self.location_list:
            if location['y'] == -58:
                im_list_upper.append(im.crop((abs(location['x']), 58, abs(location['x']) + 10, 116)))
            if location['y'] == 0:
                im_list_lower.append(im.crop((abs(location['x']), 0, abs(location['x']) + 10, 58)))

        x_offset = 0
        for img in im_list_upper:
            new_im.paste(img, (x_offset, 0))
            x_offset += img.size[0]

        x_offset = 0
        for img in im_list_lower:
            new_im.paste(img, (x_offset, 58))
            x_offset += img.size[0]
        return new_im

    def is_px_equal(self, img1, img2, x, y):
        """
        判断两个像素是否相同
        :param img1: 图片1
        :param img2:图片2
        :param x:位置1
        :param y:位置2
        :return:像素是否相同
        """
        pix1 = img1.load()[x, y]
        pix2 = img2.load()[x, y]
        threshold = 60

        if abs(pix1[0] - pix2[0]) < threshold and abs(pix1[1] - pix2[1]) < threshold and abs(pix1[2] - pix2[2]) < threshold:
            return True
        else:
            return False

    def get_gap(self, img1, img2):
        """
        获取缺口偏移量
        :param img1: 不带缺口图片
        :param img2: 带缺口图片
        :return:
        """
        left = 0
        for i in range(left, img1.size[0]):
            for j in range(img1.size[1]):
                if not self.is_px_equal(img1, img2, i, j):
                    left = i
                    return left
        return left