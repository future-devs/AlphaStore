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
        driver.find_element_by_id("details-section-switch").click()
        driver.find_element_by_id("owner-name").click()
        driver.find_element_by_id("owner-name").clear()
        driver.find_element_by_id("owner-name").send_keys("Alpha Store Warehouse test")
        driver.find_element_by_id("owner-number").click()
        driver.find_element_by_id("owner-number").clear()
        driver.find_element_by_id("owner-number").send_keys("7894612231")
        driver.find_element_by_id("owner-address").click()
        driver.find_element_by_id("owner-address").clear()
        driver.find_element_by_id("owner-address").send_keys("Mumbai test")
        driver.find_element_by_xpath("//button[@onclick='saveDetails()']").click()
    
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
