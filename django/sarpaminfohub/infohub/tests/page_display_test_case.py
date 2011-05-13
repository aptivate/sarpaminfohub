from sarpaminfohub.infohub.tests.sarpam_test_case import SarpamTestCase

class PageDisplayTestCase(SarpamTestCase):
    def check_search_field_visible_on_page(self, url):
        response = self.client.get(url)
        self.assertContains(response,
                            "<input type=\"text\" name=\"search\" id=\"id_search\" />")
        
    def check_search_results_link_visible_on_page(self, response):
        self.check_link_visible_on_page(response, href="/?search=amitrip",
                                        text="Search Results")

    def check_link_visible_on_page(self, response, href, text, count=1):
        self.assertContains(response, text)
        expected_link = "<a href=\"" + href + "\">" + text + "</a>"
        self.assertContains(response, expected_link, count=count)

    def check_tab_is_selected(self, response, text):
        self.assertContains(response, text)
        expected_li = "<li class=\"selected\">" + text + "</li>"
        self.assertContains(response, expected_li, count=1)

    def check_sub_title_is(self, response, expected_title):
        self.check_heading(response, "h2", 'sub_title', expected_title)

    def check_sub_sub_title_is(self, response, expected_title):
        self.check_heading(response, tag_name="h3",
                           context_variable='sub_sub_title', 
                           expected_title=expected_title)

    def check_heading(self, response, tag_name, context_variable,
                      expected_title):
        
        open_tag = "<%s>" % tag_name
        close_tag = "</%s>" % tag_name
        self.assertEquals(expected_title, response.context[context_variable])
        self.assertContains(response, open_tag, count=1)
        self.assertContains(response, close_tag, count=1)
                
        self.assertContains(response, expected_title)
        self.assertContains(response, open_tag + expected_title + close_tag,
                            count=1)
         
