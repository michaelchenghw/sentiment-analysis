"""
To scrape comments from yahoo finance

"""

from bs4 import BeautifulSoup as soup
from selenium import webdriver
from time import sleep 


"""
Comment data obtained in the format of:

[[time,text], [time,text], [time,text]]

"""


PATH = "/Users/yaushingjonathancheung/Desktop/chromedriver"

driver = webdriver.Chrome(PATH)
driver.get("https://finance.yahoo.com/quote/AAPL/community/") #URL


link = driver.find_element_by_xpath("//div[@class='sorting-tabs-container Pos(r) Mt(5px)']//*[@class='sort-filter-button O(n):h O(n):a Fw(b) M(0) P(0) Ff(i) C(#000) Fz(16px)']")
link.click()

link = driver.find_element_by_xpath("//div[@class='sorting-tabs-container Pos(r) Mt(5px)']//*[@class='sorting-tabs Pos(a) Bd Bdc($c-fuji-grey-c) Bdrs(3px) Bgc(#fff) Bxsh(boxShadow) Mt(8px) O(n) Z(1)']//*[@class='H(44px)']")
link.click()

sleep(5)

#click show more button
link = driver.find_element_by_xpath("//button[@class='Fz(16px) Fw(b) Bdw(2px) Ta(c) Cur(p) Va(m) Bdrs(4px) O(n)! Lh(n) Bgc(#fff) C($c-fuji-blue-1-a) Bdc($c-fuji-blue-1-a) Bd C(#fff):h Bgc($c-fuji-blue-1-a):h Mt(20px) Mb(20px) Px(30px) Py(10px) showNext D(b) Mx(a) Pos(r)']")

click_times = 5  #Click the show more button x times 

for i in range (click_times):
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
            result.append(time.text)
        else:
            continue 
        results.append(result)


for i in results:
    print(i[0])
    print(i[1])
