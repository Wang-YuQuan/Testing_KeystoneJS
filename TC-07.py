import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class TestCase(unittest.TestCase):
    def login(self):
        self.chrome.find_elements(By.XPATH, "//*[@class='css-foh633']")[0].send_keys(self.email)
        self.chrome.find_elements(By.XPATH, "//*[@class='css-foh633']")[1].send_keys(self.password)
        self.chrome.find_element(By.XPATH, "//*[@class='css-2960tt']").click()
        
    def delete_post(self):
        self.chrome.find_element(By.XPATH, "//*[@data-list-path='posts']/a").click()
        time.sleep(1)
        self.chrome.find_element(By.XPATH, "//*[@placeholder='Search']").clear()
        time.sleep(1)
        self.chrome.find_element(By.XPATH, "//*[@placeholder='Search']").send_keys("test")
        time.sleep(1)
        self.chrome.find_element(By.XPATH, "//tr[1]/td[1]").click()
        self.chrome.find_element(By.XPATH, "//*[@data-button-type='confirm']").click()
        time.sleep(1)
        
    def delete_comment(self):
        self.chrome.find_element(By.XPATH, "//*[@data-list-path='post-comments']/a").click()
        time.sleep(1)
        for td in range(3, len(self.chrome.find_elements(By.XPATH, "//tbody/tr/td")), 6):
            title = self.chrome.find_elements(By.XPATH, "//tbody/tr/td")[td].text
            if(title=="test"):
                self.chrome.find_elements(By.XPATH, "//tbody/tr/td")[td-3].click()
                self.chrome.find_element(By.XPATH, "//*[@data-button-type='confirm']").click()
                time.sleep(1)
    
    def setUp(self):
        self.login_url = "http://127.0.0.1:3000/keystone/signin"
        self.email = "demo@keystonejs.com"
        self.password = "demo"
        self.chrome = webdriver.Chrome('./chromedriver')
        self.chrome.get(self.login_url)
        self.chrome.maximize_window()
        time.sleep(1)
        self.login()
        time.sleep(1)

    def tearDown(self):
        self.delete_post()
        self.chrome.quit()
        
    def create_new_post(self):
        self.chrome.find_element(By.XPATH, "//li[@data-section-label='Posts']").click()
        time.sleep(1)
        if(len(self.chrome.find_elements(By.XPATH, "//*[@type='button']"))==1):
            self.chrome.find_element(By.XPATH, "//*[@type='button']").click()
        else:
            self.chrome.find_element(By.XPATH, "//*[@title='Create Post']").click()
        time.sleep(1)
        self.chrome.find_element(By.XPATH, "//*[@class='FormField__inner field-size-full']/input").send_keys("test")
        time.sleep(1)
        self.chrome.find_element(By.XPATH, "//*[@data-button-type='submit']").click()
        time.sleep(1)
        self.chrome.find_element(By.XPATH, "//*[@data-list-path='posts']/a").click()
        time.sleep(1)
        
    def create_new_comment(self):
        self.chrome.find_element(By.XPATH, "//li[@data-section-label='Posts']").click()
        time.sleep(1)
        self.chrome.find_element(By.XPATH, "//*[@data-list-path='post-comments']/a").click()
        time.sleep(1)
        if(len(self.chrome.find_elements(By.XPATH, "//*[@type='button']"))==1):
            self.chrome.find_element(By.XPATH, "//*[@type='button']").click()
        else:
            self.chrome.find_element(By.XPATH, "//*[@title='Create Comment']").click()
        time.sleep(1)
        # post
        self.chrome.find_elements(By.XPATH, "//*[@class='Select-control']")[1].click()
        time.sleep(1)
        self.chrome.find_elements(By.XPATH, "//*[contains(@aria-activedescendant, 'react-select')]")[1].send_keys("test")
        time.sleep(1)
        self.chrome.find_elements(By.XPATH, "//*[contains(@aria-activedescendant, 'react-select')]")[1].send_keys(Keys.ENTER)
        time.sleep(1)
        self.chrome.find_element(By.XPATH, "//*[@data-button-type='submit']").click()
        time.sleep(1)
        
    def verify_comment_not_exist_commentlist(self):
        for td in range(3, len(self.chrome.find_elements(By.XPATH, "//tbody/tr/td")), 6):
            title = self.chrome.find_elements(By.XPATH, "//tbody/tr/td")[td].text
            self.assertNotEqual(title, "test")
        
    def test_verify_TC_07(self):
        self.create_new_post()
        self.create_new_comment()
        self.delete_comment()
        self.verify_comment_not_exist_commentlist()
        
unittest.TestLoader().loadTestsFromTestCase(TestCase)
unittest.main(verbosity=2)