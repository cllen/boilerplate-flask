

class QueryMixin:

    def get_query(self):
        self.session.flush()
        self.session.commit()
        return super().get_query()
