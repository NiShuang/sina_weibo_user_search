#-*- coding: UTF-8 -*-
import socket, sys
import sys
import xlwt
reload(sys)
sys.setdefaultencoding("utf-8")
timeout = 99999999
socket.setdefaulttimeout(timeout)
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import time
import re

from User import User


class WeiboCrawler:
        def __init__(self):
            self.username = '#########'
            self.password = '########'
            self.keyword = '驴友'   ## 这个关键词没有什么意义， 关键词列表在main()中
            self.url = "http://s.weibo.com/user/" + self.keyword
            self.userList = []
            self.totalPage = 0
            self.driver = webdriver.Chrome()
            self.login()
            self.main()
            self.driver.quit()
            # self.write_excel( self.keyword.decode('utf-8')+'.xls',self.userList)

        def main(self):
            key_list = ['360全景', '全景相机', 'VR游戏']
            for key in key_list:
                self.keyword = key
                self.url = "http://s.weibo.com/user/" + key
                self.userList = []
                self.start()
                self.write_excel(self.keyword.decode('utf-8') + '.xls', self.userList)

        def login(self):
            self.driver.get("http://weibo.com/")
            self.driver.maximize_window()
            wait = WebDriverWait(self.driver, 20)
            element = wait.until(lambda x: x.find_element_by_id("loginname"))
            element.clear()
            element.send_keys(self.username)

            element = self.driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input')
            element.clear()
            element.send_keys(self.password)

            wait = WebDriverWait(self.driver, 10)
            element = wait.until(
                lambda x: x.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a'))
            element.click()

        def start(self):
            self.driver.get(self.url + "&page=1")
            # time.sleep(20)
            # element = self.driver.find_element_by_xpath('//*[@id="pl_user_feedList"]/div[2]/div[1]/span/div/ul/li[last()]/a')
            # print element
            # print element.text
            # exit()
            first_uuid = ''
            wait = WebDriverWait(self.driver, 20)
            try:
                # temp = wait.until(lambda x: x.find_element_by_xpath('//*[@id="pl_user_feedList"]/div[2]/div[1]/span/div/ul/li[last()]/a').text)
                temp = wait.until(lambda x: x.find_element_by_xpath('//*[@id="pl_user_feedList"]/div[2]/div[2]/span').text)
                print temp
                pattern = re.compile('\d+', re.S)
                items = re.findall(pattern, temp)
                temp = items[0]
                print temp
                total = int(temp)
                totalPage = total / 20 + (0 if total % 20 == 0 else 1)
                if totalPage > 50:
                    totalPage = 50
                self.totalPage = totalPage
                # self.totalPage = int(temp)
                print 'total page:',self.totalPage
            except TimeoutException:
                self.totalPage = 50
            for i in range(1, self.totalPage + 1):
                print "page ", i, ":"
                if i != 1:
                    self.driver.get(self.url + "&page=" + str(i))
                warp = wait.until(lambda x: x.find_elements_by_class_name("pl_personlist"))[0]
                elements = warp.find_elements_by_class_name('list_person')
                for element in elements:
                    name = element.find_element_by_xpath('div[@class="person_detail"]/p[@class="person_name"]/a[1]').text
                    uid = element.find_element_by_xpath('div[@class="person_detail"]/p[@class="person_name"]/a[1]').get_attribute("uid")
                    link = element.find_element_by_xpath('div[@class="person_detail"]/p[@class="person_addr"]/a[1]').text
                    follow = element.find_element_by_xpath('div[@class="person_detail"]/p[@class="person_num"]/span[1]/a').text
                    follower = element.find_element_by_xpath('div[@class="person_detail"]/p[@class="person_num"]/span[2]/a').text
                    weibo = element.find_element_by_xpath('div[@class="person_detail"]/p[@class="person_num"]/span[3]/a').text
                    follow = self.format_number(follow)
                    follower = self.format_number(follower)
                    weibo = self.format_number(weibo)
                    try:
                        brief = element.find_element_by_xpath('div[@class="person_detail"]/div[@class="person_info"]/p').text
                    except:
                        brief = ''
                    try:
                        element.find_element_by_xpath('div[@class="person_detail"]/p[@class="person_name"]/a[@href="http://verified.weibo.com/verify"]')
                        verify = '认证'
                    except:
                        verify = '未认证'
                    try:
                        card = element.find_element_by_xpath('div[@class="person_detail"]/p[@class="person_card"]').text
                    except:
                        card = ''
                    try:
                        tag = element.find_element_by_xpath('div[@class="person_detail"]/p[@class="person_label"]').text
                    except:
                        tag = ''
                    user = User(name, uid, brief, link, follow, follower, weibo, card, tag, verify)
                    self.userList.append(user)
                    user.show()
                time.sleep(1)

        def format_number(self, number):
            if '万' in number:
                number = number[:-1]
                result = int(number)
                result *= 10000
            else:
                result = int(number)
            return result

        def write_excel(self, excel_file, userList):
            wb = xlwt.Workbook(encoding = 'utf-8')
            ws = wb.add_sheet(u'工作表1')
            row = 0
            ws.write(row, 0, u'用户名')
            ws.write(row, 1, u'uid')
            ws.write(row, 2, u'名片')
            ws.write(row, 3, u'认证')
            ws.write(row, 4, u'链接')
            ws.write(row, 5, u'简介')
            ws.write(row, 6, u'关注')
            ws.write(row, 7, u'粉丝')
            ws.write(row, 8, u'微博数')
            ws.write(row, 9, u'标签')
            row = 1
            for item in userList:
                ws.write(row, 0, item.name)
                ws.write(row, 1, item.uid)
                ws.write(row, 2, item.card)
                ws.write(row, 3, item.verify)
                ws.write(row, 4, item.link)
                ws.write(row, 5, item.brief)
                ws.write(row, 6, item.follow)
                ws.write(row, 7, item.follower)
                ws.write(row, 8, item.weibo)
                ws.write(row, 9, item.tag)
                row += 1
            wb.save(excel_file)

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    jd = WeiboCrawler()