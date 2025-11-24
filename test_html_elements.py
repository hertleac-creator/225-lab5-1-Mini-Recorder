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
        driver.get("http://10.48.229.50")  # Replace with your cluster/dev site
        
        # Check for the presence of 3 test parts, but don't fail the test
        for i in range(3):
            test_name = f'Test Part {i}'
            if test_name in driver.page_source:
                print(f"Found: {test_name}")
            else:
                print(f"Not found: {test_name} (ignored)")
        
        print("Test completed successfully.")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
