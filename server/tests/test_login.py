import unittest
from applications import create_app
from base64 import b64encode

class TestLoginTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)
    
    def tearDown(self):
        self.app_context.pop()

    def get_api_headers(self, username, password):
        return {
            'Authorization': 'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            # 'Accept': 'application/json',
            # 'Content-Type': 'application/json'
        }
    
    def test_admin_login_confirmed(self):
        log_url = "{}/base/login".format(self.app.config['PROJECT_NAME'])
        response = self.client.get(
            log_url,
            headers=self.get_api_headers(
                self.app.config['flask_admin_username'], 
                self.app.config['flask_admin_password']
            ),
        )
        self.assertEqual(response.status_code, 200)
    
    def test_admin_login_unconfirmed(self):
        log_url = "{}/base/login".format(self.app.config['PROJECT_NAME'])
        response = self.client.get(
            log_url,
            headers=self.get_api_headers(
                'wrong-username', 
                'wrong-password', 
            ),
        )
        self.assertEqual(response.status_code, 403)