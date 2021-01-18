# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        # AppDynamics will automatically override this web driver
        # as documented in https://docs.appdynamics.com/display/PRO44/Write+Your+First+Script
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_app_dynamics_job(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/warehouse/")
        driver.find_element_by_id("addProductBtn").click()
        driver.find_element_by_id("add-pid").click()
        driver.find_element_by_id("add-pid").click()
        driver.find_element_by_id("add-name").click()
        driver.find_element_by_id("add-name").clear()
        driver.find_element_by_id("add-name").send_keys("Sample")
        driver.find_element_by_id("add-category").click()
        Select(driver.find_element_by_id("add-category")).select_by_visible_text("Products")
        driver.find_element_by_id("Products").click()
        driver.find_element_by_id("add-specifications").click()
        driver.find_element_by_id("add-specifications").clear()
        driver.find_element_by_id("add-specifications").send_keys("This is a specification")
        driver.find_element_by_id("add-tags").click()
        driver.find_element_by_id("add-tags").clear()
        driver.find_element_by_id("add-tags").send_keys("New, Sample")
        driver.find_element_by_id("add-price").click()
        driver.find_element_by_id("add-price").clear()
        driver.find_element_by_id("add-price").send_keys("100")
        driver.find_element_by_id("add-quantity").click()
        driver.find_element_by_id("add-quantity").clear()
        driver.find_element_by_id("add-quantity").send_keys("2")
        driver.find_element_by_xpath("//div[@id='modal-body']/div[17]/div").click()
        driver.find_element_by_xpath("//div[@id='modal-body']/div[17]/div").click()
        driver.find_element_by_id("available").click()
        driver.find_element_by_xpath("//button[@onclick='addProduct()']").click()
        driver.find_element_by_id("main-modal").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        # To know more about the difference between verify and assert,
        # visit https://www.seleniumhq.org/docs/06_test_design_considerations.jsp#validating-results
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
