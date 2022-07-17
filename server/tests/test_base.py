import unittest
from applications import create_app
from base64 import b64encode

from applications.base.services import (
    login as login_service
)

from data.test import test_admin_username,test_admin_password

import logging
logging.disable(logging.CRITICAL)

class TestBaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing','testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)
    
    def tearDown(self):
        self.app_context.pop()

    def test_service_login_success(self):
        logined_user = login_service(test_admin_username,test_admin_password)
        self.assertEqual(logined_user.username, test_admin_username)
        self.assertEqual(logined_user.password, test_admin_password)
    
    def test_service_login_fail(self):
        logined_user = login_service(test_admin_username,'123')
        self.assertEqual(logined_user, False)

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
                test_admin_username, 
                test_admin_password
            ),
        )
        # 重定向
        self.assertEqual(response.status_code, 302)
    
    def test_admin_login_confirm_failed(self):

        self.test_admin_login_confirmed()

        log_url = "{}/base/login".format(self.app.config['PROJECT_NAME'])
        response = self.client.get(
            log_url,
            headers=self.get_api_headers(
                'wrong-username', 
                'wrong-password', 
            ),
        )
        # 认证失败
        self.assertEqual(response.status_code, 401)

    def test_base_settings(self):

        from applications.base import settings
        from applications.base.models import BaseConfiguration as BaseConfigurationModel

        test_redis_host = 'boilerplate.flask.com'

        configuration = BaseConfigurationModel.query.first()

        configuration_redis_host = configuration.redis_host if configuration else None

        self.assertNotEqual(configuration_redis_host, test_redis_host)
        
        settings.redis_host = test_redis_host

        configuration = BaseConfigurationModel.query.first()

        self.assertEqual(configuration.redis_host, test_redis_host)