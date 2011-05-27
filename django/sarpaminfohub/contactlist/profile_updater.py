from django.core.cache import cache
from django.shortcuts import redirect
from django.conf import settings
from sarpaminfohub.contactlist.test_linked_in_api import TestLinkedInApi
from linkedin import linkedin
from sarpaminfohub.contactlist.custom_fields import COUNTRY_DICT
from django.core.exceptions import ObjectDoesNotExist
from sarpaminfohub.contactlist.models import Contact

class ProfileUpdater(object):
    ONE_MINUTE = 60

    def __init__(self, request, post_authorize_url=None, test_data=None,
                 token_timeout=None):
        self.request = request
        
        if token_timeout is None:
            self.token_timeout = self.ONE_MINUTE
        else:
            self.token_timeout = token_timeout

        api_key = settings.LINKED_IN_API_KEY
        secret_key = settings.LINKED_IN_SECRET_KEY
    
        if test_data is not None:
            api = TestLinkedInApi(api_key, secret_key, post_authorize_url, 
                                  test_data)
        else:
            api = linkedin.LinkedIn(api_key, secret_key, post_authorize_url)

        self.api = api
        self.api.REDIRECT_URL = "/uas/oauth/authenticate"
    
    
    def get_authorization(self):
        self.api.requestToken()
        
        auth_url = self.api.getAuthorizeURL()    

        cache.set(self.api.request_token, self.api.request_token_secret, 
                  self.token_timeout)
        
        return redirect(auth_url)
    
    def update_contact_from_profile(self, contact):
        profile = self.get_profile_for_contact_fields()
        
        if profile is not None:
            contact_data = self.get_contact_data_from_profile(profile)

            self.update_contact_from_contact_data(contact, contact_data)
            
            return contact
        else:
            return None
    
    def create_or_update_contact_from_profile(self):
        profile = self.get_profile_for_contact_fields()
        
        contact_data = self.get_contact_data_from_profile(profile)
        
        try:
            contact = Contact.objects.get(linked_in_url=profile.public_url)
            self.update_contact_from_contact_data(contact, contact_data)
        except ObjectDoesNotExist:
            contact = Contact.objects.create(**contact_data)

        contact.access_token = self.api.access_token
        contact.access_token_secret = self.api.access_token_secret
        contact.save()
    
        return contact
    
    def update_contact_from_contact_data(self, contact, contact_data):
        contact.given_name = contact_data['given_name']
        contact.family_name = contact_data['family_name']
        contact.linked_in_url = contact_data['linked_in_url']
        contact.note = contact_data['note']
        contact.tags = contact_data['tags']
        contact.role = contact_data['role']
        contact.organization = contact_data['organization']
        contact.address_line_3 = contact_data['address_line_3']
        contact.country = contact_data['country']
        contact.linked_in_approval = contact_data['linked_in_approval']
        contact.save()
    
    def get_profile_for_contact_fields(self):
        fields = ["first-name", "last-name", "specialties", "positions", \
                  "public-profile-url", "summary", "location"]
        
        profile = self.api.GetProfile(fields=fields)

        return profile
    
    def get_contact_data_from_profile(self, profile):
        trimmed_tags = ""
        
        if profile.specialties is not None:
            tags_list = profile.specialties.replace("(","").replace(")","").split(",")
            trimmed_tag_list = []
            try:
                for tag in tags_list:
                    if not len(tag) > 50:
                        trimmed_tag_list.append(tag.strip().capitalize())
                trimmed_tags = ",".join(set(trimmed_tag_list))[0:511]
            except:
                trimmed_tags = ""

        note = "<h4>Summary</h4><p>%s</p><h4>Specialities</h4><p>%s</p>"%(profile.summary,profile.specialties)
        
        country_code = ""
        address_line_3 = ""
            
        if profile.location is not None:
            location_parts = profile.location.split(',')
            
            if len(location_parts) > 0:
                country = location_parts[-1].strip()
                
                country_code = COUNTRY_DICT.get(country, "")
                
                if len(location_parts) > 1:
                    address_line_3 = location_parts[-2]

        organization = ""
        role = ""

        if len(profile.positions) > 0:
            organization = profile.positions[0].company
            role = profile.positions[0].title

        contact_data = {
            'given_name':profile.first_name or "",
            'family_name':profile.last_name or "",
            'linked_in_url':profile.public_url,
            'note':note,
            'tags':trimmed_tags,
            'role':role or "",
            'organization':organization or "",
            'address_line_3':address_line_3,
            'country':country_code,
            'linked_in_approval':True,
        }
    
        return contact_data
