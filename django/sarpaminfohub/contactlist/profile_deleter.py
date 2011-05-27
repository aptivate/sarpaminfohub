from django.shortcuts import render_to_response
from sarpaminfohub.contactlist.profile_updater import ProfileUpdater
from django.core.urlresolvers import reverse
from django.core.cache import cache
from sarpaminfohub.contactlist.models import Contact
from django.core.exceptions import ObjectDoesNotExist

class ProfileDeleter(ProfileUpdater):
    def __init__(self, request, test_data=None):
        post_authorize_url = request.build_absolute_uri(
                reverse('authorized_delete', args=None))

        ProfileUpdater.__init__(self, request, post_authorize_url, test_data)
        
    def delete_profile(self):
        verifier = self.request.GET.get('oauth_verifier', None)
        request_token = self.request.GET.get('oauth_token', None)

        request_token_secret = cache.get(request_token)
        
        return self.delete_contact(verifier=verifier, 
                            request_token=request_token, 
                            request_token_secret=request_token_secret)
    
    def delete_contact(self, verifier, request_token, request_token_secret):
        if self.api.accessToken(request_token=request_token, verifier=verifier,
                                request_token_secret=request_token_secret):

            fields = ['public-profile-url']
            
            profile = self.api.GetProfile(fields=fields)
            
            redirect_url = reverse('home')
            
            try:
                contact = Contact.objects.get(linked_in_url=profile.public_url)
                contact.delete()
                redirect_url = redirect_url + '?deleted=true'
                
            except ObjectDoesNotExist:
                pass
            
            extra_context = {'redirect_url' : redirect_url}
            
        return render_to_response('contactlist/window_closer.html', extra_context)
