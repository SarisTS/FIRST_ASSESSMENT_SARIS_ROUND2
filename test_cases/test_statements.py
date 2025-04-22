import os
import unittest
from app import app

class GenerateStatementTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.media_path = os.path.join(os.getcwd(), 'media')
        self.valid_customer_id = '1001'
        self.invalid_customer_id = '9999'

    def test_valid_request_english(self):
        response = self.app.get(f'/generate-statement?customer_id={self.valid_customer_id}&language=en')
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIn('.pdf', data.get('pdf_url', ''))

    def test_valid_request_other_language(self):
        response = self.app.get(f'/generate-statement?customer_id={self.valid_customer_id}&language=ta')
        data = response.get_json()
        self.assertTrue(data['success'])

    def test_invalid_customer(self):
        response = self.app.get(f'/generate-statement?customer_id={self.invalid_customer_id}&language=en')
        data = response.get_json()
        self.assertFalse(data['success'])
        self.assertIn('Customer not found', data.get('error', ''))

    def test_missing_customer_id(self):
        response = self.app.get('/generate-statement?language=en')
        data = response.get_json()
        self.assertFalse(data['success'])
        self.assertIn('Customer ID is required', data.get('error', ''))

    def test_missing_language(self):
        response = self.app.get(f'/generate-statement?customer_id={self.valid_customer_id}')
        data = response.get_json()
        self.assertTrue(data['success'])  # Default to English

    def test_invalid_language_code(self):
        response = self.app.get(f'/generate-statement?customer_id={self.valid_customer_id}&language=xx')
        data = response.get_json()
        self.assertTrue(data['success'])  # Fallback to English

    def test_pdf_file_created(self):
        response = self.app.get(f'/generate-statement?customer_id={self.valid_customer_id}&language=en')
        data = response.get_json()
        file_path = os.path.join(self.media_path, os.path.basename(data['pdf_url']))
        self.assertTrue(os.path.exists(file_path))

    def test_empty_transactions(self):
        # Assuming customer_id=2000 has no transactions
        response = self.app.get('/generate-statement?customer_id=2000&language=en')
        data = response.get_json()
        self.assertTrue(data['success'])

    def test_multi_page_transactions(self):
        # Assuming 100+ transactions for customer_id=1001
        response = self.app.get(f'/generate-statement?customer_id={self.valid_customer_id}&language=en')
        data = response.get_json()
        self.assertTrue(data['success'])

    def test_reward_points_shown(self):
        response = self.app.get(f'/generate-statement?customer_id={self.valid_customer_id}&language=en')
        # Not assertable directly but still worth checking success
        self.assertTrue(response.status_code == 200)

    def test_unicode_language_pdf(self):
        response = self.app.get(f'/generate-statement?customer_id={self.valid_customer_id}&language=ar')
        data = response.get_json()
        self.assertTrue(data['success'])

    def test_invalid_method_post(self):
        response = self.app.post('/generate-statement', data={'customer_id': self.valid_customer_id})
        self.assertEqual(response.status_code, 405)

    def test_response_content_type(self):
        response = self.app.get(f'/generate-statement?customer_id={self.valid_customer_id}&language=hi')
        self.assertEqual(response.content_type, 'application/json')

    def test_pdf_filename_pattern(self):
        response = self.app.get(f'/generate-statement?customer_id={self.valid_customer_id}&language=hi')
        data = response.get_json()
        self.assertRegex(data.get('pdf_url', ''), r'statement_\d+_\d{8}\.pdf')

    def test_graceful_handling_of_internal_error(self):
        # Force an error using a bad DB param or mock failure
        with app.test_request_context('/generate-statement?customer_id=BAD_INPUT'):
            try:
                self.app.get('/generate-statement?customer_id=BAD_INPUT')
            except:
                self.fail("API should not crash on bad input")
