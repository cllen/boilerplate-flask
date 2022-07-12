from applications.base.models import (
    BaseUser as BaseUserModel,
)
from utils import constants

test_admin_username = 'admin'
test_admin_password = 'admin'

test_admin = BaseUserModel(
    username=test_admin_username,
    password='admin',
    role=constants.UserRole.ADMIN
)

def insert_test_data(session):
    session.add(test_admin)
    session.commit()