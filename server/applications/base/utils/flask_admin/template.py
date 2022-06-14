from flask import Blueprint

class TemplateMixin:

    template_folder = None

    def create_blueprint(self, admin):

        """
            Create Flask blueprint.
        """
        # Store admin instance
        self.admin = admin

        # If the static_url_path is not provided, use the admin's
        if not self.static_url_path:
            self.static_url_path = admin.static_url_path

        # Generate URL
        self.url = self._get_view_url(admin, self.url)

        # If we're working from the root of the site, set prefix to None
        if self.url == '/':
            self.url = None
            # prevent admin static files from conflicting with flask static files
            if not self.static_url_path:
                self.static_folder = 'static'
                self.static_url_path = '/static/admin'

        # If name is not provided, use capitalized endpoint name
        if self.name is None:
            self.name = self._prettify_class_name(self.__class__.__name__)

        # Create blueprint and register rules
        self.blueprint = Blueprint(self.endpoint, __name__,
            url_prefix=self.url,
            subdomain=self.admin.subdomain,
            # 修改了这句代码
            template_folder=self.template_folder, # template_folder, #current_app.template_path, #op.join('templates', self.admin.template_mode),
            static_folder=self.static_folder,
            static_url_path=self.static_url_path)

        for url, name, methods in self._urls:
            self.blueprint.add_url_rule(url,
                name,
                getattr(self, name),
                methods=methods)

        return self.blueprint