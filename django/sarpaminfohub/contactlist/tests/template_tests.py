from django.test.testcases import TestCase
class TemplateTest(TestCase):
    def test_iframe_template_used(self):
        response = self.client.get('/contacts/iframe/')
        self.assertTemplateUsed(response, "iframe/index.html")

