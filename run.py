import sys
import time
from getpass import getpass

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from post import Post, Reply


def login(driver, user_token):
    driver.get("https://pkuhelper.pku.edu.cn/hole/")
    
    login = driver.find_elements_by_xpath("//*/a[@class='no-underline control-btn']")[1]
    login.click()
    time.sleep(0.2)

    login2 = driver.find_element_by_xpath("//*/button")
    login2.click()
    time.sleep(0.2)

    input_user_token = driver.find_element_by_xpath("//*/input[@placeholder='User Token']")
    input_user_token.send_keys(user_token)
    time.sleep(0.2)

    load = driver.find_element_by_xpath("//*/button[contains(text(), '导入')]")
    load.click()
    time.sleep(0.2)

    driver.refresh()
    time.sleep(0.2)

    print("Successfully login")

def extract_post(post_tree):
    pass

def get_posts(driver):
    fout = open('output.txt', 'w', encoding='utf-8')
    post_trees = driver.find_elements_by_xpath("//*/div[@style='']")
    for post_tree in post_trees:
        fout.write(post_tree.text + '\n')


user_token = getpass("User token:")

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

driver= webdriver.Chrome(chrome_options=chrome_options)
try:
    login(driver, user_token)

    # 滚轮
    # driver.execute_script("window.scrollBy(0,3000)")
    # time.sleep(1)
    get_posts(driver)

    html= driver.page_source
    fobj = open('index.html', 'w')
    fobj.write(html)
    fobj.close()
except Exception as err:
    print(err)

input("Press any key to finish...")
driver.close()
