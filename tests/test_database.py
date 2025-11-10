import unittest
from app.database import SessionLocal, add_channel, Channel

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.session = SessionLocal()

    def tearDown(self):
        self.session.close()

    def test_add_channel(self):
        add_channel(self.session, "test_id", "Test Channel")
        ch = self.session.query(Channel).filter_by(id="test_id").first()
        self.assertIsNotNone(ch)