from sqlalchemy import select
from migrate.tests import fixture

class TestConnect(fixture.DB):
    level=fixture.DB.TXN

    @fixture.usedb()
    def test_connect(self):
        """Connect to the database successfully"""
        # Connection is done in fixture.DB setup; make sure we can do stuff
        select(['42'], bind=self.engine).execute()
