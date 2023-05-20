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
        
    def delete_category(self):
        self.chrome.find_element(By.XPATH, "//*[@data-list-path='post-categories']/a").click()
        time.sleep(1)
        self.chrome.find_element(By.XPATH, "//*[@placeholder='Search']").clear()
        time.sleep(1)
        self.chrome.find_element(By.XPATH, "//*[@placeholder='Search']").send_keys("test")
        time.sleep(1)
        self.chrome.find_element(By.XPATH, "//tr[1]/td[1]").click()
        self.chrome.find_element(By.XPATH, "//*[@data-button-type='confirm']").click()
        time.sleep(1)

    def tearDown(self):
        self.delete_category()
        self.chrome.quit()
        
    def verify_category_should_be_exist_in_categorylist(self):
        counter = 0
        self.chrome.find_element(By.XPATH, "//*[@data-list-path='post-categories']/a").click()
        time.sleep(1)
        for td in range(1, len(self.chrome.find_elements(By.XPATH, "//tbody/tr/td")), 2):
            title = self.chrome.find_elements(By.XPATH, "//tbody/tr/td")[td].text
            if(title=="test"):
                counter += 1
        self.assertTrue(counter > 0)
        
    def verify_empty_name_waring_message_should_be_visable(self):
        self.chrome.find_element(By.XPATH, "//li[@data-section-label='Posts']").click()
        time.sleep(1)
        self.chrome.find_element(By.XPATH, "//*[@data-list-path='post-categories']/a").click()
        time.sleep(1)
        if(len(self.chrome.find_elements(By.XPATH, "//*[@type='button']"))==1):
            self.chrome.find_element(By.XPATH, "//*[@type='button']").click()
        else:
            self.chrome.find_element(By.XPATH, "//*[@title='Create Category']").click()
        time.sleep(1)
        expect = "Name is required"
        self.chrome.find_element(By.XPATH, "//*[@data-button-type='submit']").click()
        time.sleep(1)
        result = self.chrome.find_element(By.XPATH, "//*[@data-alert-type='danger']/div").text
        self.assertEqual(expect, result)
        
    def create_new_category(self):
        self.chrome.find_elements(By.XPATH, "//*[@class='css-foh633']")[1].send_keys("test")
        time.sleep(1)
        self.chrome.find_element(By.XPATH, "//*[@data-button-type='submit']").click()
        time.sleep(1)
        
    def test_verify_TC_08(self):
        self.verify_empty_name_waring_message_should_be_visable()
        self.create_new_category()
        self.verify_category_should_be_exist_in_categorylist()
        
unittest.TestLoader().loadTestsFromTestCase(TestCase)
unittest.main(verbosity=2)