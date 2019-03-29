from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from PIL import Image
import time
import base64


def get_image(driver, n):
    canvas = driver.find_element_by_xpath('//canvas[@class="geetest_canvas_slice geetest_absolute"]')
    left = canvas.location['x']
    top = canvas.location['y']
    print(left,top)
    print(canvas.size['width'])
    print(canvas.size['height'])
    # time.sleep(100)
    elementWidth = left + canvas.size['width']
    elementHeight = top + canvas.size['height']
    driver.save_screenshot(n + '.png')
    picture = Image.open(n + '.png')
    picture = picture.crop((left*1.25, top, elementWidth*1.25, elementHeight))   # 电脑缩放比例为125%
    picture = picture.resize((canvas.size['width'],canvas.size['height']))
    picture.save('photo' + n + '.png')
    return picture

    # JS = 'return document.getElementsByClassName("geetest_canvas_bg geetest_absolute")[0].toDataURL("image/png");'
    # # 执行 JS 代码并拿到图片 base64 数据
    # im_info = driver.execute_script(JS)  # 执行js文件得到带图片信息的图片数据
    # im_base64 = im_info.split(',')[1]  # 拿到base64编码的图片信息
    # im_bytes = base64.b64decode(im_base64)  # 转为bytes类型
    # with open('photo' + n + '.png', 'wb') as f:  # 保存图片到本地
    #     f.write(im_bytes)
    # return Image.open('photo' + n + '.png')


def get_space(picture1, picture2):
    start = 70
    threhold = 70

    for i in range(start, picture1.size[0]):
        for j in range(picture1.size[1]):
            rgb1 = picture1.load()[i, j]
            rgb2 = picture2.load()[i, j]
            res1 = abs(rgb1[0] - rgb2[0])
            res2 = abs(rgb1[1] - rgb2[1])
            res3 = abs(rgb1[2] - rgb2[2])
            if not (res1 < threhold and res2 < threhold and res3 < threhold):
                print("i",i-8)
                return i-8
    print(i-8)
    return i-8


def get_tracks(space):
    # 模拟人工滑动，避免被识别为机器
    space += 30  # 先滑过一点，最后再反着滑动回来
    v = 0
    t = 0.2
    forward_tracks = []
    current = 0
    mid = space * 3 / 5
    while current < space:
        if current < mid:
            a = 2
        else:
            a = -3
        s = v * t + 0.5 * a * (t ** 2)
        v = v + a * t
        current += s
        forward_tracks.append(round(s))
    # 反着滑动到准确位置
    back_tracks = [-3,-3,-3,-3,-3,-2,-2,-2,-2,-2,-1,-1,-1,-1,-1]
    return {'forward_tracks': forward_tracks, 'back_tracks': back_tracks}


def main():
    driver = webdriver.Chrome()
    # driver.maximize_window()
    driver.get('http://www.geetest.com/type/')
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="app"]/section/div/ul/li[2]/h2').click()  # 选择滑动行为验证
    # driver.find_element_by_xpath('//div[@class="geetest_slider_button"]').click()  ????why
    time.sleep(1.5)
    # 1、出现滑块验证，获取有缺口的图片
    # driver.find_element_by_xpath('//*[@id="captcha"]/div[2]/div[2]/div[1]/div[3]/span[1]').click()
    driver.find_element_by_xpath('//span[@class="geetest_wait_dot geetest_dot_2"]').click()
    time.sleep(1.5)
    picture1 = get_image(driver, '1')
    # 2、执行js改变css样式，显示背景图！！！！！重点是这一步！
    # driver.execute_script('document.querySelectorAll("canvas")[1].style=""')  # 不是1
    driver.execute_script('document.querySelectorAll("canvas")[2].style=""')
    time.sleep(1.5)
    # 3、获取没有缺口的图片
    picture2 = get_image(driver, '2')
    # exit(0)
    # 4、对比两种图片的像素点，找出位移
    space = get_space(picture1, picture2)
    tracks = get_tracks(space)
    print(tracks)
    button = driver.find_element_by_class_name('geetest_slider_button')
    ActionChains(driver).click_and_hold(button).perform()
    for track in tracks['forward_tracks']:
        ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()
    time.sleep(0.5)
    for back_track in tracks['back_tracks']:
        ActionChains(driver).move_by_offset(xoffset=back_track, yoffset=0).perform()
    ActionChains(driver).move_by_offset(xoffset=-3, yoffset=0).perform()
    ActionChains(driver).move_by_offset(xoffset=3, yoffset=0).perform()
    time.sleep(0.5)
    ActionChains(driver).release().perform()
    time.sleep(2)
    # driver.close()
    # driver.quit()


if __name__ == '__main__':
    main()

