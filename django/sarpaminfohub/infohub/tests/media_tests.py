from django.test import TestCase

class MediaTest(TestCase):
    def test_favicon_exists(self):
        response = self.client.get('/site_media/favicon.ico')
        self.assertEquals(response.status_code, 200)
