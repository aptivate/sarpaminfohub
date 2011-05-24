from HTMLParser import HTMLParser
from sarpaminfohub.infohub.tests.sarpam_test_case import SarpamTestCase

class SearchTest(SarpamTestCase):
    class TableParser(HTMLParser):
        FINDING_RESULTS_HEADING = 0
        PARSING_RESULTS_HEADING = 10
        FINDING_TABLE = 20
        FINDING_TABLE_HEADINGS = 30
        PARSING_TABLE_HEADINGS = 40
        FINDING_ROWS = 50
        PARSING_CELL = 60
        FINISHED = 70

        DEBUG_PARSER = False

        def __init__(self):        
            self.state = self.FINDING_RESULTS_HEADING
            self.rows = []
            self.cells = []
            self.hrefs = []
            self.headings = []
            self.cell_classes = []
            HTMLParser.__init__(self)
            self.results_heading = None
            self.input_field_value = None
        
        def get_attribute(self, attributes, name):
            for name_value_pair in attributes:
                if name in name_value_pair:
                    return name_value_pair[1]
            return None
            
        def handle_starttag(self, tag, attributes):
            if self.DEBUG_PARSER:
                print "handle_starttag %s" % tag
                print "state = %d" % self.state

            if tag == "input" and ('name', 'search') in attributes:
                self.input_field_value = self.get_attribute(attributes, 'value')
            
            if tag == "td":
                self.cell_classes.append(self.get_attribute(attributes, 'class'))
            
            if tag == "a" and self.state == self.PARSING_CELL:
                self.hrefs.append(self.get_attribute(attributes, 'href'))
            
            if self.state == self.FINDING_RESULTS_HEADING and tag == "li":
                self.state = self.PARSING_RESULTS_HEADING
            
            if self.state == self.FINDING_TABLE and tag == "table":
                self.state = self.FINDING_TABLE_HEADINGS
            elif self.state == self.FINDING_TABLE_HEADINGS and tag == "th":
                self.state = self.PARSING_TABLE_HEADINGS
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
            if self.state == self.FINDING_TABLE_HEADINGS and tag == "tr":
                self.state = self.FINDING_ROWS
            if self.state == self.PARSING_TABLE_HEADINGS and tag == "th":
                self.state = self.FINDING_TABLE_HEADINGS
            elif self.state == self.PARSING_CELL and tag == "td":
                self.state = self.FINDING_ROWS
            elif self.state == self.FINDING_ROWS and tag == "table":
                self.state = self.FINISHED
        
        def handle_data(self, data):
            if self.DEBUG_PARSER:
                print "handle_data %s" % data
                print "state = %d" % self.state
            if self.state == self.PARSING_RESULTS_HEADING:
                self.results_heading = data
                self.state = self.FINDING_TABLE
            if self.state == self.PARSING_TABLE_HEADINGS:
                self.headings.append(data)
            if self.state == self.PARSING_CELL:
                self.cells.append(data)
          
    def test_search_page_is_based_on_search_template(self):
        response = self.client.get('/search/')
        self.assertTemplateUsed(response, 'search.html')

    def test_search_page_has_no_results_initially(self):
        response = self.client.get('/search')
        parser = self.parse_table_content(response)
        self.assertEquals(parser.FINDING_RESULTS_HEADING, parser.state)

    def search_for(self, search_term, backend):
        url = "/search/?search=%s" % search_term
        
        if backend is not None:
            url += '&backend=%s' % backend
        
        return self.client.get(url)
        

    def search_for_ciprofloxacin(self, backend):
        return self.search_for("ciprofloxacin", backend)

    def parse_table_content(self, response):
        parser = self.TableParser()
        parser.feed(response.content)
        parser.close()
        return parser

    def parse_search_results_for(self, search_term, backend=None):
        response = self.search_for(search_term, backend=backend)
        parser = self.parse_table_content(response)
        return parser
    
    def get_rows_for_ciprofloxacin(self, backend=None):
        parser = self.parse_search_results_for("ciprofloxacin", backend=backend)
        self.assertEquals(parser.FINISHED, parser.state)
        
        return parser.rows
    
    def test_search_for_ciprofloxacin_returns_south_africa_prices(self):
        self.set_up_exchange_rate_for_zar()
        rows = self.get_rows_for_ciprofloxacin('test')
        expected_rows = [["ciprofloxacin 500mg tablet",
                          "0.044", "0.044", "0.033"]]
        self.assertEquals(expected_rows, rows)
        
    def test_search_term_displayed_in_heading(self):
        parser = self.parse_search_results_for("ciprofloxacin")
        self.assertEquals("Search Results", 
                          parser.results_heading)
        
    def test_search_term_displayed_in_input_field(self):
        parser = self.parse_search_results_for("ciprofloxacin")
        self.assertEquals("ciprofloxacin", 
                          parser.input_field_value)
        
    def test_by_default_search_field_is_empty(self):
        response = self.client.get('/search')
        parser = self.parse_table_content(response)
        self.assertEquals(None, parser.input_field_value)

    def test_search_result_headings_are_as_expected(self):
        parser = self.parse_search_results_for("ciprofloxacin")
        self.assertEquals(parser.FINISHED, parser.state)
        self.assertEquals(["Formulation",
                           "Median FOB Price (USD)",
                           "Median Landed Price (USD)",
                           "MSH International Median (USD)"],
                          parser.headings)

    def test_search_for_ciprofloxacin_with_django_backend_returns_drc_prices(self):
        self.set_up_and_return_drc_ciprofloxacin()
        self.set_up_msh_for_ciprofloxacin()
        self.set_up_exchange_rate_for_eur()
        parser = self.parse_search_results_for("ciprofloxacin")
        
        expected_rows = [["ciprofloxacin 500mg tablet",
                          "0.025", 
                          "0.029",
                          "0.033"]]
        self.assertEquals(expected_rows, parser.rows)
        
    def test_null_prices_displayed_as_double_dash(self):
        self.set_up_and_return_drc_ciprofloxacin(fob_price=None, landed_price=None)
        self.set_up_exchange_rate_for_eur()
        
        rows = self.get_rows_for_ciprofloxacin()
        
        expected_rows = [["ciprofloxacin 500mg tablet",
                          "--", "--", "--"]]
        self.assertEquals(expected_rows, rows)

    def test_price_cells_are_in_number_class(self):
        self.set_up_exchange_rate_for_zar()
        parser = self.parse_search_results_for("ciprofloxacin", backend='test')
        self.assertEquals(['first', 'second number', 'third number', 'fourth number'], 
                          parser.cell_classes)
        
    def test_search_results_link_to_formulation_page(self):
        self.set_up_exchange_rate_for_usd()
        self.set_up_exchange_rate_for_eur()
        self.set_up_exchange_rate_for_nad()
        parser = self.parse_search_results_for("amox", backend='test')
        self.assertEquals(3, len(parser.hrefs))
        amoxycillin125_href = "/formulation/9/"
        amoxycillin500_href = "/formulation/10/"
        tamoxifen_href = "/formulation/49/"
        
        expected_hrefs = [amoxycillin125_href, amoxycillin500_href, 
                          tamoxifen_href] 
        self.assertEquals(expected_hrefs, parser.hrefs)
