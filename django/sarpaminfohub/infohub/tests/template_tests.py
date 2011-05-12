from django.test import TestCase

class TemplateTest(TestCase):
    def test_404_template_exists(self):
        response = self.client.get('/gubbins')
        self.assertTemplateUsed(response, '404.html')

    def test_iframe_src_set_correctly(self):
        response = self.load_iframe_and_return_response()
        self.assertContains(response, "<iframe src=\"/\"")

    def test_iframe_link_set_correctly(self):
        response = self.load_iframe_and_return_response()
        self.assertContains(response, "<a href=\"/\"")

    def test_iframe_page_contains_title(self):
        response = self.load_iframe_and_return_response()
        self.assertContains(response, "Drug Price Database")

    def test_iframe_pricing_template_used(self):
        response = self.load_iframe_and_return_response()
        self.assertTemplateUsed(response, "iframe/pricing.html")
        
    def load_iframe_and_return_response(self):
        response = self.client.get('/iframe/')
        return response
