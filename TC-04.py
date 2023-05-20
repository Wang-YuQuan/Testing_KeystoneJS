import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class TestCase(unittest.TestCase):
    def login(self):
        self.chrome.find_elements(By.XPATH, "//*[@class='css-foh633']")[0].send_keys(self.email)
        self.chrome.find_elements(By.XPATH, "//*[@class='css-foh633']")[1].send_keys(self.password)
        self.chrome.find_element(By.XPATH, "//*[@class='css-2960tt']").click()
    
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
        self.chrome.find_element(By.XPATH, "//*[@data-list-path='posts']/a").click()
        time.sleep(1)
        self.chrome.find_element(By.XPATH, "//*[@placeholder='Search']").clear()
        time.sleep(1)
        self.chrome.find_element(By.XPATH, "//*[@placeholder='Search']").send_keys("test")
        time.sleep(1)
        self.chrome.find_element(By.XPATH, "//tr[1]/td[1]").click()
        self.chrome.find_element(By.XPATH, "//*[@data-button-type='confirm']").click()
        time.sleep(1)
        self.chrome.quit()
        
    def verify_postlist_filter(self):
        self.chrome.find_element(By.XPATH, "//*[@placeholder='Search']").clear()
        time.sleep(1)
        self.chrome.find_element(By.XPATH, "//*[@placeholder='Search']").send_keys("test")
        time.sleep(1)
        for td in range(1, len(self.chrome.find_elements(By.XPATH, "//tbody/tr/td")), 5):
            title = self.chrome.find_elements(By.XPATH, "//tbody/tr/td")[td].text
            self.assertTrue("test" in title)
        
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
        
    def test_verify_TC_04(self):
        self.create_new_post()
        self.verify_postlist_filter()
        
unittest.TestLoader().loadTestsFromTestCase(TestCase)
unittest.main(verbosity=2)