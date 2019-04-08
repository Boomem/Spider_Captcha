# 爬取点：价格
# 爬取问题：价格为图片格式，每个数字class刷新页面时更新

# 解决方案：
# 1.获取源码，匹配每个数字的class
# 2.读取包含class名的css文件，匹配到背景图及class名对应的background-position的px值
# 3.通过px值截取背景图，宽度为25-30即可
# 4.使用pytesseract识别

import cv2
import requests
from PIL import Image
import pytesseract


# 背景图url
url = "https://images.bthhotels.com/PriceImg/Images/20190407/0d740df3a2bf423b894e1ffd26b50238.png"
res = requests.get(url)
with open("a.png","wb") as f:
    f.write(res.content)

#
img = cv2.imread("a.png")
# 可注释，测试用来看
cv2.imshow("th",img)
# position  px值
y = 35
# 可注释，测试用来看
cv2.imshow("th1",img[6:,y:y+30])
# 识别
res = pytesseract.image_to_string(img[6:,y:y+30],lang='chi_sim', config='--psm 10')
print(res)
# 测试用来阻塞，！！注释掉
cv2.waitKey(0)
