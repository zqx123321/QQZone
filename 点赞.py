
# _*_ coding: utf-8 _*_ 
from selenium import webdriver
import time
import traceback
class Praise():
    def __init__(self,QQ,password,friendQQ):
        self.QQ=QQ
        self.password=password
        self.friendQQ=friendQQ
        self.n = 0
        self.logs=""
        self.praised_list = []
        if self.friendQQ:
            self.url="https://user.qzone.qq.com/"+self.friendQQ+"/main"
        else:
            self.url="https://user.qzone.qq.com/"+self.QQ

    def run(self):
        print 'Current URL:', self.browser.current_url
        # see more
        try:
            btn_more = self.browser.find_element_by_css_selector(".b-inline.data_btn_more")
            if btn_more:
                btn_more.click()
        except:
            pass
        if self.friendQQ:
            self.praise_someone()
        else:
            self.praise_all()
        self.browser.quit()

    def login_qzone(self):
        self.browser = webdriver.PhantomJS()
        #self.browser.maximize_window()
        self.browser.get(self.url)
        self.browser.switch_to.frame("login_frame")
        self.browser.find_element_by_id("switcher_plogin").click()
        self.browser.find_element_by_id("u").clear()
        self.browser.find_element_by_id("u").send_keys(self.QQ)
        self.browser.find_element_by_id("p").clear()
        self.browser.find_element_by_id("p").send_keys(self.password)
        self.browser.find_element_by_id("login_button").click()
        time.sleep(10)
        print u"登录成功"
        # 解决FireFox的登录成功后，直接访问新页面出现can't access dead object错误的方法链接：
        # http://stackoverflow.com/questions/16396767/firefox-bug-with-selenium-cant-access-dead-object
        # 通过下面这句解决，可能时因为上面switch_to到了login_frame，所以现在它是dead object
        self.browser.switch_to.default_content()

    def praise_someone(self):
        self.log_num=0
        pre_num=0
        while 1:
            self.browser.switch_to.frame("QM_Feeds_Iframe")  # 个人主页才有
            self.log_head = self.browser.find_element_by_id("host_home_feeds")
            self.log_list=self.log_head.find_elements_by_css_selector(".f-single.f-s-s")
            self.start_praising()
            self.browser.switch_to.default_content()
            for i in range(50):
                self.browser.execute_script("window.scrollBy(0,500);")
            time.sleep(2)

    def praise_all(self):
        feed_friend_list = self.browser.find_element_by_id("feed_friend_list")
        self.log_list = feed_friend_list.find_elements_by_css_selector(".f-single.f-s-s")
        # 向下翻动一段距离，为了使feed_page_container那个变化的列表出现
        for i in range(100):
            self.browser.execute_script("window.scrollBy(0,500);")
        time.sleep(60)
        self.start_praising()

        self.log_num = len(self.log_list)
        self.log_list=[]
        container_head = feed_friend_list.find_element_by_class_name("feed_page_container")
        # 个人中心页面，说说是在<li class="feed_page_container">...</li>下动态出现的
        # 该标签下最多有3个<ul data-page="0">...</ul>，每个ul标签下又包含4个说说
        # 这里面的数值12只是估算，因为说说的评论数不同，导致一条说说所占的高度不同
        i=0
        while 1:
            if i % 12 == 0:
                time.sleep(2)
                self.log_list= container_head.find_elements_by_css_selector(".f-single.f-s-s")
                print len(self.log_list)
                self.start_praising()
            self.browser.execute_script("window.scrollBy(0,500)")
            i+=1

    def start_praising(self):
        for log in self.log_list:
            # 赞过的就不赞了
            if log in self.praised_list:
                continue
            try:
                self.n+=1
                # 名字
                print self.n,"【",log.find_element_by_xpath("./div/div[4]/div/a").text,"】 :",
                # 说说内容
                print log.find_element_by_xpath("./div[2]/div/div").text,
                # 点赞图标
                thumb_up_block=log.find_element_by_xpath("./div[3]/div[1]/p/a[3]")
                # 若已赞过，则class属性中会增加一个CSS属性值item-on
                if "item-on" not in thumb_up_block.get_attribute("class"):
                    thumb_up_icon=thumb_up_block.find_element_by_xpath("./i")
                    thumb_up_icon.click()
                    print u"[点赞成功]\n"
                else:
                    print u"[已赞]\n"
                self.praised_list.append(log)
                time.sleep(1)
            except:
                traceback.print_exc()
                continue

def main():
    QQ =raw_input(u"输入QQ号：")
    password =raw_input(u"输入QQ密码：")
    friendQQ =raw_input(u"输入被点赞的好友QQ号(不输入则给空间所有发出来的动态点赞)：")
    praise_spider = Praise(QQ,password,friendQQ)
    praise_spider.login_qzone()
    praise_spider.run()

if __name__ == "__main__":
    main()