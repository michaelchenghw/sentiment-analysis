from bs4 import BeautifulSoup as soup
from selenium import webdriver
from time import sleep 
import os, time
from datetime import timedelta, datetime

"""
Comment data obtained in the format of:

[[time,text], [time,text], [time,text]]

In US time

"""

os.environ['TZ'] = 'America/Los_Angeles'
time.tzset()


PATH = "/Users/yaushingjonathancheung/Desktop/chromedriver"

driver = webdriver.Chrome(PATH)
driver.get("https://finance.yahoo.com/quote/AAPL/community/")


link = driver.find_element_by_xpath("//div[@class='sorting-tabs-container Pos(r) Mt(5px)']//*[@class='sort-filter-button O(n):h O(n):a Fw(b) M(0) P(0) Ff(i) C(#000) Fz(16px)']")
link.click()

link = driver.find_element_by_xpath("//div[@class='sorting-tabs-container Pos(r) Mt(5px)']//*[@class='sorting-tabs Pos(a) Bd Bdc($c-fuji-grey-c) Bdrs(3px) Bgc(#fff) Bxsh(boxShadow) Mt(8px) O(n) Z(1)']//*[@class='H(44px)']")
link.click()

sleep(5)

#click show more button
link = driver.find_element_by_xpath("//button[@class='Fz(16px) Fw(b) Bdw(2px) Ta(c) Cur(p) Va(m) Bdrs(4px) O(n)! Lh(n) Bgc(#fff) C($c-fuji-blue-1-a) Bdc($c-fuji-blue-1-a) Bd C(#fff):h Bgc($c-fuji-blue-1-a):h Mt(20px) Mb(20px) Px(30px) Py(10px) showNext D(b) Mx(a) Pos(r)']")

click_times = 151 #Click the show more button x times 

for i in range (click_times):
    print(i)
    link.click()
    sleep(5)

sleep(5)
page_html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")



page_soup = soup(page_html, "lxml")

results = []

for element in page_soup.findAll(class_="comments-list List(n) Ovs(touch) Pos(r) Mt(10px) Mstart(-12px) Pt(5px)"):
    contents = element.find_all('li')
    for content in contents:
        result = []
        comment = content.find(class_="C($c-fuji-grey-l) Mb(2px) Fz(14px) Lh(20px) Pend(8px)")
        if comment:
            result.append(comment.text)
        else:
            continue #Skip if the slot doesnt contain text (i.e gif images)
        time = content.find(class_="Fz(12px) C(#828c93)") 
        if time:
            dateofpost = ""
            if (len(time.text.split(" ")) == 1): #yesterday
                dateofpost = datetime.today() - timedelta(days=1)
                dateofpost = dateofpost.strftime("%Y-%m-%d")
            else:
                commentlist = time.text.split(" ")
                if (commentlist[1] == "hours" or commentlist[1] == "hour"):  # x hours ago
                    timebefore = int(commentlist[0])
                    dateofpost = datetime.today() - timedelta(hours=timebefore)
                    dateofpost = dateofpost.strftime("%Y-%m-%d")
                elif (commentlist[1] == "minutes" or commentlist[1] == "minute"): # x minutes ago
                    timebefore = int(commentlist[0])
                    dateofpost = datetime.today() - timedelta(minutes=timebefore)
                    dateofpost = dateofpost.strftime("%Y-%m-%d")
                elif(commentlist[1] == "days" or commentlist[1] == "day"): # x days ago
                    timebefore = int(commentlist[0])
                    dateofpost = datetime.today() - timedelta(days=timebefore)
                    dateofpost = dateofpost.strftime("%Y-%m-%d")

            result.append(dateofpost)

        else:
            continue 
        results.append(result)


file = open("comments.txt","w")
for i in results:
    commentstring = i[1] + ":" + i[0] + "\n" 
    print(commentstring)
    file.write(commentstring)

file.close()











