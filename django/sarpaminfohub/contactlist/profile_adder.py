from django.shortcuts import render_to_response
from sarpaminfohub.contactlist.custom_fields import COUNTRY_DICT
from django.core.exceptions import ObjectDoesNotExist
from sarpaminfohub.contactlist.models import Contact
from django.core.urlresolvers import reverse
from django.core.cache import cache
from sarpaminfohub.contactlist.profile_updater import ProfileUpdater

class ProfileAdder(ProfileUpdater):
    def __init__(self, request, test_data=False, token_timeout=None):
                
        if test_data:
            args = [test_data]
        else:
            args = None
        
        post_authorize_url = request.build_absolute_uri(reverse('authorized_add',
                                                                     args=args))

        ProfileUpdater.__init__(self, request, post_authorize_url, test_data,
                                token_timeout)


    def add_profile(self):
        verifier = self.request.GET.get('oauth_verifier', None)
        request_token = self.request.GET.get('oauth_token', None)

        request_token_secret = cache.get(request_token)

        if request_token_secret is None:
            return render_to_response('contactlist/token_expired.html')
        else:
            return self.create_and_render_contact(verifier=verifier, 
                                                  request_token=request_token, 
                                                  request_token_secret=request_token_secret)
            
    def create_and_render_contact(self,  verifier, request_token, 
                                  request_token_secret):
        if self.api.accessToken(request_token=request_token, verifier=verifier,
                                request_token_secret=request_token_secret):
            fields = ["first-name", "last-name", "specialties", "positions", \
                      "public-profile-url", "summary", "location"]
            
            profile = self.api.GetProfile(fields=fields)

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
            
            try:
                contact = Contact.objects.get(linked_in_url=profile.public_url)
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
            except ObjectDoesNotExist:
                contact = Contact.objects.create(**contact_data)

            contact.access_token = self.api.access_token
            contact.access_token_secret = self.api.access_token_secret
            contact.save()
            cache.delete(request_token)
            extra_context = {
                'redirect_url':contact.get_absolute_url() + '?new_contact=true'
            }
        
        return render_to_response('contactlist/window_closer.html', extra_context)
