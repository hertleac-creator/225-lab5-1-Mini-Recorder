from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import unittest

class TestParts(unittest.TestCase):
    def setUp(self):
        # Setup Firefox options
        firefox_options = Options()
        firefox_options.add_argument("--headless")  # Ensures the browser window does not open
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Firefox(options=firefox_options)

    def test_parts(self):
        driver = self.driver
        driver.get("http://10.48.229.148")  # Replace with your cluster/dev site
        
        # Check for the presence of all 10 test parts
        for i in range(10):
            test_name = f'Test Part {i}'
            assert test_name in driver.page_source, f"Test part {test_name} not found in page source"
        print("Test completed successfully. All 10 test parts were verified.")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
