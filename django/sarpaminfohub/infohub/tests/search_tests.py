from django.test import TestCase

from sarpaminfohub.infohub.forms import SearchForm
from HTMLParser import HTMLParser

class SearchTest(TestCase):
    class TableParser(HTMLParser):
        FINDING_TABLE = 0
        FINDING_HEADINGS = 1
        PARSING_HEADING = 2
        FINDING_ROWS = 3
        PARSING_CELL = 4
        FINISHED = 5

        DEBUG_PARSER = False

        def __init__(self):        
            self.state = self.FINDING_TABLE
            self.rows = []
            self.cells = []
            self.headings = []
            HTMLParser.__init__(self)
        
        def handle_starttag(self, tag, attrs):
            if self.DEBUG_PARSER:
                print "handle_starttag %s" % tag
                print "state = %d" % self.state
            
            if self.state == self.FINDING_TABLE and tag == "table":
                self.state = self.FINDING_HEADINGS
            elif self.state == self.FINDING_HEADINGS and tag == "th":
                self.state = self.PARSING_HEADING
            elif self.state == self.FINDING_ROWS:
                if tag == "tr":
                    self.cells = []
                    self.rows.append(self.cells)
                elif tag == "td":
                    self.state = self.PARSING_CELL 
                
        def handle_endtag(self, tag):
            if self.DEBUG_PARSER:
                print "handle_endtag %s" % tag
                print "state = %d" % self.state
            if self.state == self.FINDING_HEADINGS and tag == "tr":
                self.state = self.FINDING_ROWS
            if self.state == self.PARSING_HEADING and tag == "th":
                self.state = self.FINDING_HEADINGS
            elif self.state == self.PARSING_CELL and tag == "td":
                self.state = self.FINDING_ROWS
            elif self.state == self.FINDING_ROWS and tag == "table":
                self.state = self.FINISHED
        
        def handle_data(self, data):
            if self.DEBUG_PARSER:
                print "handle_data %s" % data
                print "state = %d" % self.state
            if self.state == self.PARSING_HEADING:
                self.headings.append(data)
            if self.state == self.PARSING_CELL:
                self.cells.append(data)
          
    def test_search_page_is_based_on_search_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'search.html')

    def test_search_form_can_be_created(self):
        search_form = SearchForm()
        self.assertTrue(isinstance(search_form, SearchForm))

    def test_search_form_has_search_field(self):
        search_form = SearchForm()
        self.assertTrue(search_form.fields.has_key('search'))

    def test_search_page_has_no_results_initially(self):
        response = self.client.get('/')
        parser = self.TableParser()
        parser.feed(response.content)
        parser.close()
        self.assertEquals(parser.FINDING_TABLE, parser.state)

    def test_search_result_headings_are_as_expected(self):
        response = self.client.get('/?search=ciprofloxacin')
        parser = self.TableParser()
        parser.feed(response.content)
        parser.close()
        self.assertEquals(parser.FINISHED, parser.state)
        self.assertEquals(["Molecule", "Product", "Formulation", "Price", "Country"], 
                          parser.headings)

    def test_search_for_ciprofloxacin_returns_ciprobay(self):
        response = self.client.get('/?search=ciprofloxacin')
        parser = self.TableParser()
        parser.feed(response.content)
        parser.close()
        self.assertEquals(parser.FINISHED, parser.state)
        
        expected_rows = [["ciprofloxacin", "Ciprobay 500",
                          "500mg tablet", "0.54", "South Africa"]]
        self.assertEquals(expected_rows, parser.rows)
        
        