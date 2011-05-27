from sarpaminfohub.contactlist.models import Contact
from sarpaminfohub.contactlist.profile_adder import ProfileAdder
from django.http import HttpRequest
from sarpaminfohub.contactlist.tests.contactlist_test_case import ContactListTestCase

class LinkedInTest(ContactListTestCase):
    TEST_OAUTH_TOKEN = '7ccce8fb-83e4-4ab7-b8da-7f8b5c32c4ad'
    TEST_OAUTH_VERIFIER = '75959'
    TEST_URL = "http://www.linkedin.com/pub/joyce-kgatlwane/0/123/456"
    XML_HEADER = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
    
    def setUp(self):
        self.rebuild_search_index()
    
    def test_contact_can_be_created_from_linked_in(self):
        num_contacts_before = len(Contact.objects.all())

        self.request_and_add_profile_and_return_response()        
        num_contacts_after = len(Contact.objects.all())
        self.assertEquals(1, num_contacts_after - num_contacts_before)

    def test_request_profile_redirects_to_auth_page(self):
        xml_encoded = self.get_encoded_profile_data(profile_data="notused")
        response = self.add_profile_and_return_response(xml_encoded)
        
        self.assertRedirectsNoFollow(response, 
            "https://api.linkedin.com/uas/oauth/authenticate?oauth_token=%s" % self.TEST_OAUTH_TOKEN)

    def assertRedirectsNoFollow(self, response, expected_url):
        self.assertEqual(response._headers['location'], 
                         ('Location', expected_url))
        self.assertEqual(response.status_code, 302)

    def test_message_appears_when_token_expires(self):
        request = self.create_and_return_http_request()
        profile_adder = ProfileAdder(request, test_data="notempty", 
                                     token_timeout=0)
        profile_adder.get_authorization()
        response = profile_adder.add_profile()
        self.assertContains(response, "Authorization Token Expired", 2)
    
    def create_and_return_http_request(self):
        request = HttpRequest()
        request.method = 'GET'

        params = {'oauth_verifier': self.TEST_OAUTH_VERIFIER, 
                  'oauth_token': self.TEST_OAUTH_TOKEN}
        
        request.GET = params
        request.META['SERVER_NAME'] = "localhost"
        request.META['SERVER_PORT'] = 8000

        return request

    def test_given_name_stored_in_new_contact(self):
        profile_data = self.get_first_name_xml_for("Joyce")

        self.check_field_stored_in_new_contact(field_name='given_name',
                                               expected_value="Joyce", 
                                               profile_data=profile_data)

    def test_family_name_stored_in_new_contact(self):
        profile_data = \
        "  <last-name>Kgatlwane</last-name>"

        self.check_field_stored_in_new_contact(field_name='family_name', 
                                               expected_value="Kgatlwane",
                                               profile_data=profile_data)

    def test_summary_and_specialities_stored_in_note_field_of_new_contact(self):
        profile_data = self.get_summary_xml_for(
            "A healthcare practitioner, specialising as a Pharmacist, in Gaborone, Botswana") +\
            self.get_specialities_xml()
        
        expected_summary = "A healthcare practitioner, specialising as a Pharmacist, in Gaborone, Botswana"
        expected_specialities = "procurement, supply of medicines"
        
        expected_note = self.get_note_html(expected_summary,
                                           expected_specialities)
        
        self.check_field_stored_in_new_contact(field_name='note',
                                           expected_value=expected_note,
                                           profile_data=profile_data)

    def test_tags_include_capitalised_specialities(self):
        profile_data = self.get_specialities_xml()
        
        self.check_field_stored_in_new_contact(field_name='tags', 
                                               expected_value="Procurement,Supply of medicines",
                                               profile_data=profile_data)

    def test_title_of_first_position_stored_in_role_field_of_new_contact(self):
        profile_data = self.get_position_xml_with_title("Pharmacist")

        self.check_field_stored_in_new_contact(field_name='role', 
                                           expected_value="Pharmacist",
                                           profile_data=profile_data)

    def test_company_of_first_position_stored_in_organization_field_of_new_contact(self):
        profile_data = self.get_position_xml_with_company("Botswana Essential Drugs Action Programme")
        
        self.check_field_stored_in_new_contact(field_name='organization', 
            expected_value="Botswana Essential Drugs Action Programme",
            profile_data=profile_data)

    def test_first_part_of_location_stored_in_address_line_3_field_of_new_contact(self):
        profile_data = self.get_location_xml_for("Gaborone, Botswana")
        
        self.check_field_stored_in_new_contact(field_name='address_line_3', 
                                           expected_value="Gaborone",
                                           profile_data=profile_data)
        
    def test_country_stored_in_country_field_of_new_contact(self):
        profile_data = self.get_location_xml_for("Gaborone, Botswana")

        self.check_field_stored_in_new_contact(field_name='country', 
                                           expected_value="BWA",
                                           profile_data=profile_data)        

    def test_country_stored_in_country_field_of_new_contact_when_no_city_exists(self):
        profile_data = self.get_location_xml_for("Botswana")

        self.check_field_stored_in_new_contact(field_name='country', 
                                           expected_value="BWA",
                                           profile_data=profile_data)        

    def test_linked_in_approval_flag_set_on_new_contact(self):
        self.check_field_stored_in_new_contact(field_name='linked_in_approval', 
                                           expected_value=True,
                                           profile_data="")  

    def test_given_name_can_be_updated_for_contact(self):
        profile_data = self.get_first_name_xml_for("Joyce")
        self.request_and_add_profile_and_return_response(profile_data)

        profile_data = self.get_first_name_xml_for("Rose")
        self.check_field_stored_in_new_contact(field_name='given_name',
                                           expected_value="Rose",
                                           profile_data=profile_data)

    def get_first_name_xml_for(self, first_name):
        return "  <first-name>%s</first-name>" % first_name

    def test_family_name_can_be_updated_for_contact(self):
        profile_data = self.get_last_name_xml_for("Kgatlwane")
        self.request_and_add_profile_and_return_response(profile_data)

        profile_data = self.get_last_name_xml_for("Shija")
        self.check_field_stored_in_new_contact(field_name='family_name', 
                                           expected_value="Shija",
                                           profile_data=profile_data)
        
    def get_last_name_xml_for(self, last_name):
        return "  <last-name>%s</last-name>" % last_name

    def test_public_url_can_be_updated_for_contact(self):
        self.request_and_add_profile_and_return_response()
        
        public_url = "http://www.linkedin.com/pub/rose-shija/0/123/456"
        self.check_field_stored_in_new_contact(field_name='linked_in_url',
                                           expected_value=public_url, 
                                           public_url=public_url)
        
    def test_note_can_be_updated_from_summary_for_contact(self):
        profile_data = self.get_summary_xml_for(
            "A healthcare practitioner, specialising as a Pharmacist, in Gaborone, Botswana") +\
        self.get_specialities_xml()
        
        self.request_and_add_profile_and_return_response(profile_data)
        
        profile_data = self.get_summary_xml_for(
            "A qualified healthcare practitioner, specialising as a Senior Pharmacist, in Gaborone, Botswana") +\
        self.get_specialities_xml()
        
        expected_summary = "A qualified healthcare practitioner, specialising as a Senior Pharmacist, in Gaborone, Botswana"
        expected_specialities = "procurement, supply of medicines"
        
        expected_note = self.get_note_html(expected_summary, 
                                           expected_specialities)
        
        self.check_field_stored_in_new_contact(field_name='note',
                                           expected_value=expected_note,
                                           profile_data=profile_data)
            
    def test_note_can_be_updated_from_specialities_for_contact(self):
        summary_xml = self.get_summary_xml_for(
            "A healthcare practitioner, specialising as a Pharmacist, in Gaborone, Botswana")
        
        profile_data =  summary_xml + self.get_specialities_xml()
        
        self.request_and_add_profile_and_return_response(profile_data)
        
        profile_data = summary_xml + self.get_specialities_xml_for("procurement, capacity building")
        
        expected_summary = "A healthcare practitioner, specialising as a Pharmacist, in Gaborone, Botswana"
        expected_specialities = "procurement, capacity building"
        
        expected_note = self.get_note_html(expected_summary, 
                                           expected_specialities)
        
        self.check_field_stored_in_new_contact(field_name='note',
                                           expected_value=expected_note,
                                           profile_data=profile_data)
                
    def test_tags_can_be_updated_from_specialities_for_contact(self):
        profile_data = self.get_specialities_xml()
        self.request_and_add_profile_and_return_response(profile_data)
        
        profile_data = self.get_specialities_xml_for("procurement, capacity building")
        
        self.check_field_stored_in_new_contact(field_name='tags', 
                                           expected_value="Procurement,Capacity building",
                                           profile_data=profile_data)

    def test_role_can_be_updated_from_title_of_first_position_for_contact(self):
        profile_data = self.get_position_xml_with_title("Pharmacist")
        self.request_and_add_profile_and_return_response(profile_data)

        profile_data = self.get_position_xml_with_title("Senior Pharmacist")

        self.check_field_stored_in_new_contact(field_name='role', 
                                           expected_value="Senior Pharmacist",
                                           profile_data=profile_data)

    def test_organization_can_be_updated_from_company_of_first_position(self):
        profile_data = self.get_position_xml_with_company("Botswana Essential Drugs Action Programme")
        self.request_and_add_profile_and_return_response(profile_data)
        
        profile_data = self.get_position_xml_with_company("World Health Organisation")
        self.check_field_stored_in_new_contact(field_name='organization', 
                                           expected_value="World Health Organisation",
                                           profile_data=profile_data)
        
    def test_address_line_3_can_be_updated_from_first_part_of_location(self):
        profile_data = self.get_location_xml_for("Gaborone, Botswana")
        self.request_and_add_profile_and_return_response(profile_data)
        
        profile_data = self.get_location_xml_for("Harare, Zimbabwe")
        self.check_field_stored_in_new_contact(field_name='address_line_3', 
                                           expected_value="Harare",
                                           profile_data=profile_data) 

    def test_country_can_be_updated_from_country_field(self):
        profile_data = self.get_location_xml_for("Gaborone, Botswana")
        self.request_and_add_profile_and_return_response(profile_data)

        profile_data = self.get_location_xml_for("Harare, Zimbabwe")
        self.check_field_stored_in_new_contact(field_name='country', 
                                           expected_value="ZWE",
                                           profile_data=profile_data)  

    def test_access_token_is_stored_in_contact(self):
        self.request_and_add_profile_and_return_response()
        self.check_field_stored_in_new_contact(field_name='access_token', 
                                           expected_value="b20ecb6c-7706-4d6b-b9b0-8f53672f179d")  

    def test_access_token_secret_is_stored_in_contact(self):
        self.request_and_add_profile_and_return_response()
        self.check_field_stored_in_new_contact(field_name='access_token_secret', 
                                           expected_value="1e41d8e9-acd5-48b1-b1df-de0be9ec01fa")
        
    def test_delete_profile_removes_existing_contact(self):
        self.request_and_add_profile_and_return_response()
        num_contacts_before = len(Contact.objects.all())
        self.delete_profile_and_return_response()

        num_contacts_after = len(Contact.objects.all())
        self.assertEquals(1, num_contacts_before - num_contacts_after)
                
    def test_delete_profile_redirects_to_main_page(self):
        self.request_and_add_profile_and_return_response()
        response = self.delete_profile_and_return_response()
        self.assertTemplateUsed(response, "contactlist/window_closer.html")
        self.assertEquals('/contacts/?deleted=true', response.context['redirect_url'])
                
    def test_delete_non_existent_profile_redirects_to_main_page(self):
        response = self.delete_profile_and_return_response()
        self.assertTemplateUsed(response, "contactlist/window_closer.html")
        self.assertEquals('/contacts/', response.context['redirect_url'])        
                
    def test_add_profile_redirects_to_contact_detail_page(self):
        profile_data = self.get_first_name_xml_for("Joyce")
        response = self.request_and_add_profile_and_return_response(profile_data,
                                                                    self.TEST_URL)
        self.assertTemplateUsed(response, "contactlist/window_closer.html")
        new_contact = Contact.objects.get(given_name="Joyce")
        expected_url = '/contacts/%d/?new_contact=true' % new_contact.id
        self.assertEquals(expected_url, response.context['redirect_url'])

    def test_batch_update_changes_given_name(self):
        profile_data = self.get_first_name_xml_for("Joyce")
        self.request_and_add_profile_and_return_response(profile_data,
                                                         self.TEST_URL)
        
        profile_data = self.get_first_name_xml_for("Rose")
        xml_encoded = self.get_encoded_profile_data(profile_data, self.TEST_URL)
        response = self.do_batch_update_and_return_response(test_data=xml_encoded)
        
        new_contact = Contact.objects.get(linked_in_url=self.TEST_URL)
        self.assertEquals("Rose", new_contact.given_name)
        batch_report = response.context['batch_report']
        self.assertEquals([{"Rose" : "Updated"}], batch_report)

    def test_batch_update_does_not_change_contact_with_no_linked_in_profile(self):
        joyce = Contact(given_name="Joyce", family_name="Kgatlwane")
        joyce.save()
        
        response = self.do_batch_update_and_return_response()
        
        matches = Contact.objects.filter(given_name="Joyce")
        self.assertEquals(1, len(matches))
        
        batch_report = response.context['batch_report']
        self.assertEquals([{"Joyce Kgatlwane" : "No LinkedIn Profile"}],
                          batch_report)

    def test_batch_update_uses_correct_template(self):
        response = self.do_batch_update_and_return_response()
        self.assertTemplateUsed(response, "contactlist/batch_report.html")

    def test_batch_update_deletes_contact_when_access_token_has_expired(self):
        profile_data = self.get_first_name_xml_for("Joyce")
        self.request_and_add_profile_and_return_response(profile_data,
                                                         self.TEST_URL)
        
        error_xml = self.XML_HEADER + \
            "<error>" + \
            "    <status>401</status>" + \
            "    <timestamp>1306499003728</timestamp>" + \
            "    <error-code>0</error-code>" + \
            "<message>[unauthorized]. The token used in the OAuth request is not valid. a418d7d7-59de-40f1-8f66-bc8d3981668e</message>" + \
            "</error>"
            
        xml_encoded = error_xml.encode('hex')
        response = self.do_batch_update_and_return_response(test_data=xml_encoded)
        
        batch_report = response.context['batch_report']
        self.assertEquals([{"Joyce" : "Deleted"}], batch_report)

        matches = Contact.objects.filter(linked_in_url=self.TEST_URL)
        self.assertEquals(0, len(matches))
        
    def do_batch_update_and_return_response(self, test_data=""):
        response = self.client.post('/contacts/batch_update/test/%s' % test_data)
        self.assertEquals(200, response.status_code)

        return response

    def delete_profile_and_return_response(self):
        test_data = str("test").encode('hex')
        response = self.client.get('/contacts/delete_linked_in_profile/test/%s' % test_data)
        self.assertEquals(302, response.status_code)
        
        # Help things along a bit
        xml_encoded = self.get_encoded_profile_data("", self.TEST_URL)
        auth_params = '?oauth_token=%s&oauth_verifier=%s' % (self.TEST_OAUTH_TOKEN, self.TEST_OAUTH_VERIFIER)
        response = self.client.get('/contacts/authorized_delete/test/%s%s' % \
                                   (xml_encoded, auth_params))
        self.assertEquals(200, response.status_code)
        return response
        
    def get_position_xml_with_title(self, title):
        return self.get_position_xml("      <title>" + title + "</title>")
        
    def get_position_xml_with_company(self, company):
        return self.get_position_xml(\
        "      <company>" + \
        "        <name>" + company + "</name>" + \
        "      </company>")

    def get_position_xml(self, child_xml):
        return \
        "  <positions total=\"1\">" + \
        "    <position>" + child_xml + \
        "    </position>" + \
        "  </positions>"

    def get_specialities_xml(self):
        return self.get_specialities_xml_for("procurement, supply of medicines")


    def get_specialities_xml_for(self, specialities):
        return "  <specialties>%s</specialties>" % specialities 

    def get_note_html(self, summary, specialities):
        note_html = "<h4>Summary</h4><p>%s</p><h4>Specialities</h4><p>%s</p>" % \
            (summary, specialities)
            
        return note_html

    def get_summary_xml_for(self, summary):
        return "  <summary>%s</summary>" % summary        
        
    def get_location_xml_for(self, name):
        location_format =  \
        "  <location>" + \
        "    <name>%s</name>" + \
        "    <country>" + \
        "      <code>bw</code>" + \
        "    </country>" + \
        "  </location>"
        
        location_xml = location_format % name 
        
        return location_xml

    def check_field_stored_in_new_contact(self, field_name, expected_value,
                                      profile_data="notused", public_url=None):
        if public_url is None:
            public_url = self.TEST_URL
            
        self.request_and_add_profile_and_return_response(profile_data, public_url)
        new_contact = Contact.objects.get(linked_in_url=public_url)
        self.assertEquals(expected_value, getattr(new_contact, field_name))        

    def request_and_add_profile_and_return_response(self, profile_data="notused", 
                                                    public_url=None):
        xml_encoded = self.get_encoded_profile_data(profile_data, public_url)
        
        self.add_profile_and_return_response(xml_encoded)
        
        # we have to help things along a bit here as we've mocked out the
        # linked in API
        response = self.client.get('/contacts/authorized_add/test/%s?oauth_token=%s&oauth_verifier=%s' % (xml_encoded, self.TEST_OAUTH_TOKEN, self.TEST_OAUTH_VERIFIER))
        self.assertEquals(200, response.status_code)
        return response

    def add_profile_and_return_response(self, xml_encoded):
        response = self.client.get('/contacts/add_linked_in_profile/test/%s' % xml_encoded)
        self.assertEquals(302, response.status_code)
        return response

    def get_encoded_profile_data(self, profile_data, public_url=None):
        if public_url is None:
            public_url = self.TEST_URL
        
        xml = self.XML_HEADER + \
        "<person>" + \
        profile_data + \
        "  <public-profile-url>" + public_url + "</public-profile-url>" + \
        "</person>"
        
        xml_encoded = xml.encode('hex')
        
        return xml_encoded

    # A reminder of a typical record
    def unused_test_profile(self):
        profile_xml = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>" + \
        "<person>" + \
        "  <first-name>Joyce</first-name>" + \
        "  <last-name>Kgatlwane</last-name>" + \
        "  <specialties>procurement, supply of medicines</specialties>" + \
        "  <positions total=\"4\">" + \
        "    <position>" + \
        "      <id>16325633</id>" + \
        "      <title>Pharmacist</title>" + \
        "      <start-date>" + \
        "        <year>2007</year>" + \
        "        <month>7</month>" + \
        "      </start-date>" + \
        "      <is-current>true</is-current>" + \
        "      <company>" + \
        "        <name>Botswana Essential Drugs Action Programme</name>" + \
        "        <size>1-10 employees</size>" + \
        "        <type>Privately Held</type>" + \
        "        <industry>Information Technology and Services</industry>" + \
        "      </company>" + \
        "    </position>" + \
        "    <position>" + \
        "      <id>11387749</id>" + \
        "      <title>Not a Pharmacist</title>" + \
        "      <start-date>" + \
        "        <year>2003</year>" + \
        "        <month>11</month>" + \
        "      </start-date>" + \
        "      <is-current>true</is-current>" + \
        "      <company>" + \
        "        <size>Myself Only</size>" + \
        "        <type>Self-Employed</type>" + \
        "        <industry>Computer Software</industry>" + \
        "      </company>" + \
        "    </position>" + \
        "    <position>" + \
        "      <id>11387819</id>" + \
        "      <title>Not a Pharmacist</title>" + \
        "      <start-date>" + \
        "        <year>2001</year>" + \
        "        <month>7</month>" + \
        "      </start-date>" + \
        "      <end-date>" + \
        "        <year>2003</year>" + \
        "        <month>7</month>" + \
        "      </end-date>" + \
        "      <is-current>false</is-current>" + \
        "      <company>" + \
        "        <name>ANT Limited</name>" + \
        "        <size>11-50 employees</size>" + \
        "        <type>Privately Held</type>" + \
        "        <industry>Computer Software</industry>" + \
        "      </company>" + \
        "    </position>" + \
        "    <position>" + \
        "      <id>11387877</id>" + \
        "      <title>Not a Pharmacist</title>" + \
        "      <start-date>" + \
        "        <year>1995</year>" + \
        "        <month>3</month>" + \
        "      </start-date>" + \
        "      <end-date>" + \
        "        <year>2001</year>" + \
        "        <month>7</month>" + \
        "      </end-date>" + \
        "      <is-current>false</is-current>" + \
        "      <company>" + \
        "        <name>Laser-Scan Limited</name>" + \
        "        <size>51-200 employees</size>" + \
        "        <type>Privately Held</type>" + \
        "        <industry>Computer Software</industry>" + \
        "      </company>" + \
        "    </position>" + \
        "  </positions>" + \
        "  <public-profile-url>http://www.linkedin.com/pub/joyce-kgatlwane/0/123/456</public-profile-url>" + \
        "  <summary>A healthcare practitioner, specialising as a Pharmacist, in Gaborone, Botswana</summary>" + \
        "  <location>" + \
        "    <name>Gaborone, Botswana</name>" + \
        "    <country>" + \
        "      <code>bw</code>" + \
        "    </country>" + \
        "  </location>" + \
        "  <phone-numbers total=\"0\" />" + \
        "</person>"
        
        return profile_xml
