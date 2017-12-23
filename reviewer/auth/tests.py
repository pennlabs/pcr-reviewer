from django.test import TestCase, Client


class BasicTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
