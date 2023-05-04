import unittest
import HtmlTestRunner
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

class TestWebApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the driver
        cls.service = Service('C:/Users/niraj/Desktop/prototype5/chromedriver.exe')  # Please replace this - 'C:/Users/niraj/Desktop/prototype5/chromedriver.exe' by your driver location
        cls.driver = webdriver.Chrome(service=cls.service)
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        # Close the browser
        cls.driver.quit()

    def test_history_link(self):
        driver = self.driver
        # driver.get('http://localhost:3000/')
        driver.get('https://askathena-bot.azurewebsites.net/')
        time.sleep(5) # Let the user actually see something!
        # wait for the element to be clickable
        history_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='history']")))
        # Click on the History link
        history_link.click()
        time.sleep(3) # Let the user actually see something!
        # Check that the History page has loaded
        self.assertIn('History', driver.title)

    def test_chat_input(self):
        driver = self.driver
        # driver.get('http://localhost:3000/')
        driver.get('https://askathena-bot.azurewebsites.net/')
        time.sleep(3) # Let the user actually see something!
        # Find the text input and enter text
        text_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#chat > div.input-wrap > textarea")))
        text_input.send_keys("exceptions in java?")
        text_input.send_keys(Keys.RETURN)
        # wait for 5 seconds
        time.sleep(11)
        # Wait for the element to be present
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#chat > div.bubble-wrap > div:nth-child(3) > span")))
        # Get the text of the element
        text = element.text
        # Check that the response contains the expected text
        self.assertIn('Here are some answers I found:', text)

if __name__ == '__main__':
    # Create a TestSuite
    test_suite = unittest.TestSuite()
    # Add your test cases
    # test_suite.addTest(unittest.makeSuite(TestWebApp))
    # Create a TestSuite with the desired order of tests
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestWebApp('test_history_link'))
    test_suite.addTest(TestWebApp('test_chat_input'))

    # Open the report file
    # report_file = open('test_report.html', 'wb')

    # Create the test runner with HTMLTestRunner
    # test_runner = HtmlTestRunner.HTMLTestRunner(output=os.getcwd(), combine_reports=True)
    test_runner = HtmlTestRunner.HTMLTestRunner(output='test-reports', combine_reports=True)
    # Run the test suite with the test runner
    test_runner.run(test_suite)

    # Close the report file
    # report_file.close()
