import unittest
import urllib.request

# Automatically select URL based on environment variable
import os
ENV = os.environ.get("ENVIRONMENT", "dev").lower()
if ENV == "prod":
    BASE_URL = "http://10.48.229.55"  # Production LoadBalancer IP
else:
    BASE_URL = "http://127.0.0.1:5000"  # Dev ClusterIP via port-forward

class HttpLightTests(unittest.TestCase):

    def test_index_page_loads(self):
        """Check that the index page returns 200"""
        with urllib.request.urlopen(BASE_URL) as response:
            self.assertEqual(response.status, 200)

    def test_sample_part_exists(self):
        """Check that a known sample part exists in the HTML"""
        with urllib.request.urlopen(BASE_URL) as response:
            html = response.read().decode('utf-8')
        sample_parts = ["Brake Pad", "Oil Filter", "Tire"]
        found = any(part in html for part in sample_parts)
        self.assertTrue(found, "No sample parts found in the page source")

if __name__ == "__main__":
    unittest.main()
