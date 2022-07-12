from applications.base.models import (
    BaseUser as BaseUserModel,
)
from utils import constants

dev_admin_username = 'admin'
dev_admin_password = 'admin'

dev_admin = BaseUserModel(
    username=dev_admin_username,
    password='admin',
    role=constants.UserRole.ADMIN
)

def insert_dev_data(session):
    session.add(dev_admin)
    session.commit()