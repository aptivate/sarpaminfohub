from django.test import TestCase

class templateTest(TestCase):
    def test_404_template_exists(self):
        response = self.client.get('/gubbins')
        self.assertTemplateUsed(response, '404.html')
