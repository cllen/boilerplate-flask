from flask import current_app
from utils.login import (
    current_user,
)

class CurrentUserMixin:

    def render(self, *args, **kwargs):
        return super().render(*args, 
            current_view=self, 
            current_user=current_user, 
            current_app=current_app, 
        **kwargs)
