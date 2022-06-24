from applications.base.models import (
    BaseUser as BaseUserModel,
)
from utils import constants

def insert_dev_data(session):
    admin = BaseUserModel(
        username='admin',
        password='admin',
        role=constants.UserRole.ADMIN
    )
    session.add(admin)
    session.commit()