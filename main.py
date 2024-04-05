import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


# login to your instagram account
def login(driver, username, password):
    driver.get("https://www.instagram.com")
    time.sleep(10)
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_name("password").send_keys(Keys.RETURN)
    time.sleep(5)

# get the list of followers
def get_followers(driver, username):
    driver.get("https://www.instagram.com/" + username)
    time.sleep(5)
    followers = driver.find_element_by_partial_link_text("followers")
    followers.click()
    time.sleep(2)
    # scroll down to load more followers
    for i in range(1, 3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.randint(2, 4))
    # get the list of followers
    follower_elems = driver.find_elements_by_css_selector("li button")
    follower_elems = [elem for elem in follower_elems if elem.text == "Follow"]
    return follower_elems

# get the list of following
def get_following(driver, username):
    driver.get("https://www.instagram.com/" + username)
    time.sleep(5)
    following = driver.find_element_by_partial_link_text("following")
    following.click()
    time.sleep(2)
    # scroll down to load more following
    for i in range(1, 3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.randint(2, 4))
    # get the list of following
    following_elems = driver.find_elements_by_css_selector("li button")
    following_elems = [elem for elem in following_elems if elem.text == "Following"]
    return following_elems

# remove fake followers
def remove_followers(driver, username, followers, following):
    driver.get("https://www.google.com/" + username)
    time.sleep(5)
    # get the list of fake followers
    fake_followers = [elem for elem in following if elem not in followers]
    # remove fake followers
    for elem in fake_followers:
        elem.click()
        time.sleep(2)
        driver.find_element_by_xpath("//button[contains(text(), 'Unfollow')]").click()
        time.sleep(2)

# main function
def main():
    # enter your username and password
    username = "your_username"
    password = "your_password"
    # create a new Firefox session
    service =  ChromeService("./chromedriver")
    driver = webdriver.Chrome("./chromedriver")
    driver.maximize_window()
    # login to your instagram account
    login(driver, username, password)
    # get the list of followers
    followers = get_followers(driver, username)
    # # get the list of following
    following = get_following(driver, username)
    # # remove fake followers
    remove_followers(driver, username, followers, following)
    # close the browser window
    driver.quit()

if __name__ == "__main__":
    main()

