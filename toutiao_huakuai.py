import cv2
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import requests


class Toutiao():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def __del__(self):
        time.sleep(3)
        self.driver.close()

    def save_img(self,src,name):
        res = requests.get(src)
        with open(name+".png","wb") as f:
            f.write(res.content)

    def get_border(self,img):
        ret, th1 = cv2.threshold(img, 180, 255, cv2.THRESH_BINARY)
        cv2.imwrite("small_th.png", th1)
        h, w = th1.shape[:2]
        border = []
        for i in range(2,w - 30):
            for j in range(2,h):
                if th1[j, i] == 255:
                    border.append([j, i])
        return border

    def get_space(self):
        img1 = cv2.imread("big.png",0)[50:110,55:]
        img2 = cv2.imread("small.png",0)
        border = self.get_border(img2)
        print(border)
        ret2, th2 = cv2.threshold(img1, 120, 255, cv2.THRESH_BINARY)
        cv2.imwrite("big_th.png", th2)
        h2, w2 = th2.shape[:2]
        same = 0
        diff = 0
        y = 0
        y_val = [0,0,0]
        for i in range(h2 - 55):
            for j in range(w2 - 31):
                for x, y in border:
                    if th2[x + i, y + j] == 255:
                        same += 1
                    if th2[x+i, y+j+1] == 0:
                        diff += 1
                    # else:
                        # diff += 1

                if same+diff > y_val[0]+y_val[1]:
                    y_val = [same, diff, j]
                same = 0
                diff = 0
        cv2.imwrite("result.png",th2[:,y_val[2]:])
        cv2.waitKey(10)
        return y_val[2]

    def get_tracks(self,space):
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
        back_tracks = [-3, -3, -3, -3, -3, -2, -2, -2, -2, -2, -1, -1, -1, -1, -1]
        return {'forward_tracks': forward_tracks, 'back_tracks': back_tracks}

    def start(self,url):
        self.driver.get(url)
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="login-type-account"]/img').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="user-name"]').send_keys("2307551610@qq.com")
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys("admin123")
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="bytedance-login-submit"]').click()
        time.sleep(2)
        img1 = self.driver.find_element_by_xpath('//img[@id="validate-big"]').get_attribute("src")
        img2 = self.driver.find_element_by_xpath('//*[@id="verify-bar-box"]/div[2]/img[2]').get_attribute("src")
        self.save_img(img1,"big")
        self.save_img(img2,"small")
        space = self.get_space()
        print(space)
        tracks = self.get_tracks(space+50)
        button = self.driver.find_element_by_xpath('//*[@id="validate-drag-wrapper"]/div[2]/img')
        ActionChains(self.driver).click_and_hold(button).perform()
        for track in tracks['forward_tracks']:
            ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()
        time.sleep(0.5)
        for back_track in tracks['back_tracks']:
            ActionChains(self.driver).move_by_offset(xoffset=back_track, yoffset=0).perform()
        ActionChains(self.driver).move_by_offset(xoffset=-3, yoffset=0).perform()
        ActionChains(self.driver).move_by_offset(xoffset=3, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.driver).release().perform()
        time.sleep(2)


if __name__ == '__main__':
    toutiao = Toutiao()
    toutiao.start("https://sso.toutiao.com/")










