import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
        
    def verify_success_message(self):
        expect = "Your changes have been saved successfully"
        result = self.chrome.find_element(By.XPATH, "//*[@data-alert-type='success']").text
        self.assertEqual(expect, result)
        time.sleep(1)
        
    def verify_edited_post_in_postlist(self):
        self.chrome.find_element(By.XPATH, "//*[@data-list-path='posts']/a").click()
        time.sleep(1)
        self.chrome.find_element(By.XPATH, "//*[@placeholder='Search']").clear()
        time.sleep(1)
        self.chrome.find_element(By.XPATH, "//*[@placeholder='Search']").send_keys("test")
        time.sleep(1)
        title = "test"
        result = self.chrome.find_element(By.XPATH, "//tr[1]/td[2]/a").text
        self.assertEqual(title, result)
        status = "Published"
        result = self.chrome.find_element(By.XPATH, "//tr[1]/td[3]/div").text
        self.assertEqual(status, result)
        author = "Demo User"
        result = self.chrome.find_element(By.XPATH, "//tr[1]/td[4]/a").text
        self.assertEqual(author, result)
        
    def edit_post(self):
        # title
        self.chrome.find_element(By.XPATH, "//*[@placeholder='Name']").clear()
        time.sleep(1)
        self.chrome.find_element(By.XPATH, "//*[@placeholder='Name']").send_keys("test")
        time.sleep(1)
        # state
        self.chrome.find_elements(By.XPATH, "//*[@class='Select-control']")[0].click()
        time.sleep(1)
        self.chrome.find_elements(By.XPATH, "//*[contains(@aria-activedescendant, 'react-select')]")[0].send_keys("Published")
        time.sleep(1)
        self.chrome.find_elements(By.XPATH, "//*[contains(@aria-activedescendant, 'react-select')]")[0].send_keys(Keys.ENTER)
        time.sleep(1)
        # author
        self.chrome.find_elements(By.XPATH, "//*[@class='Select-control']")[1].click()
        time.sleep(1)
        self.chrome.find_elements(By.XPATH, "//*[contains(@aria-activedescendant, 'react-select')]")[1].send_keys("Demo User")
        time.sleep(1)
        self.chrome.find_elements(By.XPATH, "//*[contains(@aria-activedescendant, 'react-select')]")[1].send_keys(Keys.ENTER)
        time.sleep(1)
        # save
        self.chrome.find_element(By.XPATH, "//*[@data-button='update']").click()
        time.sleep(1)
        self.verify_success_message()
        self.verify_edited_post_in_postlist()
        
    def test_verify_TC_02(self):
        self.create_new_post()
        self.chrome.find_element(By.XPATH, "//li[@data-section-label='Posts']").click()
        time.sleep(1)
        self.chrome.find_element(By.XPATH, "//*[@placeholder='Search']").clear()
        time.sleep(1)
        self.chrome.find_element(By.XPATH, "//*[@placeholder='Search']").send_keys("test")
        time.sleep(1)
        self.chrome.find_element(By.XPATH, "//tr[1]/td[2]/a").click()
        time.sleep(1)
        self.edit_post()
        
        
unittest.TestLoader().loadTestsFromTestCase(TestCase)
unittest.main(verbosity=2)