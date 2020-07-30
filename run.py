import sys
import time
import datetime
from getpass import getpass
import json
import argparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from post import Post, Reply

def save_html(driver, file_name='index.html'):
    html= driver.page_source
    fobj = open(file_name, 'w', encoding='utf-8')
    fobj.write(html)
    fobj.close()

def convert_posts_to_json(posts, file_name='output.json'):
    print('Saving into json...')
    output = []
    for post in posts:
        output.append({
            'id': post.id,
            'content': post.content,
            'time': str(post.time),
            'replies': [
                {
                    'id': reply.id,
                    'name': reply.name,
                    'content': reply.content,
                    'time': str(reply.time)
                }
                for reply in post.replies
            ]
        })
    json.dump(output, open(file_name, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

def login(driver, user_token):
    driver.get("https://pkuhelper.pku.edu.cn/hole/")
    
    # 点击“登录”按钮
    login = driver.find_elements_by_xpath("//a[@class='no-underline control-btn']")[1]
    login.click()
    time.sleep(0.1)

    # 点击“登录”按钮
    login2 = driver.find_element_by_xpath("//button")
    login2.click()
    time.sleep(0.1)

    # 输入user token
    input_user_token = driver.find_element_by_xpath("//input[@placeholder='User Token']")
    input_user_token.send_keys(user_token)
    time.sleep(0.1)

    # 点击“导入”按钮
    load = driver.find_element_by_xpath("//button[contains(text(), '导入')]")
    load.click()
    time.sleep(0.1)

    print("Log in successfully ")

    driver.refresh()
    time.sleep(0.5)

    
def extract_post(post_tree, crawled_pids):
    pid = post_tree.find_element_by_xpath(".//div[@class='flow-item']//code[@class='box-id']").text
    if pid in crawled_pids:
        return None
    else:
        crawled_pids.add(pid)
    pcontent = post_tree.find_element_by_xpath(".//div[@class='flow-item']//div[@class='box-content']").text
    ptime = post_tree.find_element_by_xpath(".//div[@class='flow-item']//time").get_attribute('datetime')[:19]
    ptime = datetime.datetime.strptime(ptime,'%Y-%m-%dT%H:%M:%S')
    
    new_post = Post(pid, pcontent, ptime)

    for reply_tree in post_tree.find_elements_by_xpath(".//div[@class='flow-reply box']"):
        rid = reply_tree.find_element_by_xpath(".//code[@class='box-id']").text
        
        rtime = reply_tree.find_element_by_xpath(".//time").get_attribute('datetime')[:19]
        rtime = datetime.datetime.strptime(rtime,'%Y-%m-%dT%H:%M:%S')

        rcontent = reply_tree.find_element_by_xpath(".//div[@class='box-content']").text 
        left_paren_pos = rcontent.find('[')
        right_paren_pos = rcontent.find(']')
        name = rcontent[left_paren_pos+1:right_paren_pos]
        rcontent = rcontent[right_paren_pos+2:]
        new_post.add_reply(rid, name, rcontent, rtime)

    return new_post

def get_posts(driver, crawled_pids):
    posts = []
    post_trees = driver.find_elements_by_xpath("//div[@style='']")
    for post_tree in post_trees:
        new_post = extract_post(post_tree, crawled_pids)
        if new_post != None:
            posts.append(new_post)
    return posts


if __name__ == '__main__':
    parse = argparse.ArgumentParser()

    parse.add_argument('--crawl_size', type=int, default=50)
    parse.add_argument('--show_browser', action='store_true')
    parse.add_argument('--output_json_name', type=str, default='output.json')

    args_ret = parse.parse_args()
    print(args_ret)

    args = vars(args_ret)
    user_token = getpass("User token:")

    chrome_options = Options()
    if args['show_browser'] == False:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    driver= webdriver.Chrome(options=chrome_options)
    try:
        login(driver, user_token)

        save_html(driver)

        posts = []
        crawled_pids = set([])
        while(len(posts) < args['crawl_size']):
            post_cnt = len(driver.find_elements_by_xpath("//div[@style='']"))
            new_posts = get_posts(driver, crawled_pids)
            posts += new_posts
            print("%s~%s" % (new_posts[0].id, new_posts[-1].id))

            # 滚轮
            driver.execute_script("arguments[0].scrollIntoView(false);", driver.find_elements_by_xpath("//div[@style='']")[-1])
            time.sleep(0.05)
        posts = posts[:args['crawl_size']]
        
        print('Crawling done')
        convert_posts_to_json(posts, file_name=args['output_json_name'])
        
    except Exception as err:
        print(err)

    input("Press any key to finish...")
    driver.close()
