from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import json

service = Service(executable_path=r"D:\BaiduNetdiskDownload\chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://weibo.com/hot/weibo/102803")

input("按回车键继续···")

cookies = driver.get_cookies()

cookies_str = json.dumps(cookies)

with open("blog_cookies.txt", "w", encoding="utf-8") as file:
    file.write(cookies_str)

input("按回车键继续···")

driver.quit()
