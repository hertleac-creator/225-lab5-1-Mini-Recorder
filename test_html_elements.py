import unittest
import urllib.request
import os
import sys

ENV = os.environ.get("ENVIRONMENT", "dev").lower()
if len(sys.argv) > 1 and sys.argv[1].startswith("--base-url="):
    BASE_URL = sys.argv[1].split("=",1)[1]
else:
    if ENV == "prod":
        BASE_URL = "http://10.48.229.50"
    else:
        BASE_URL = "http://127.0.0.1:5000"

class HttpLightTests(unittest.TestCase):

    def test_index_page_loads(self):
        with urllib.request.urlopen(BASE_URL) as response:
            self.assertEqual(response.status, 200)

    def test_sample_warhammer_units_exist(self):
        with urllib.request.urlopen(BASE_URL) as response:
            html = response.read().decode('utf-8')

        expected_units = [f"Test Model {i}" for i in range(10)]
        found = any(unit in html for unit in expected_units)
        self.assertTrue(found, "No Test Model entries found in the page source")

if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]] + sys.argv[1:])
