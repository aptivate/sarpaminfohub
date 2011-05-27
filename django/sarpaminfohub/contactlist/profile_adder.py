from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.core.cache import cache
from sarpaminfohub.contactlist.profile_updater import ProfileUpdater

class ProfileAdder(ProfileUpdater):
    def __init__(self, request, test_data=None, token_timeout=None):
                
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
            response = self.create_and_render_contact(verifier=verifier, 
                request_token=request_token, 
                request_token_secret=request_token_secret)
            cache.delete(request_token)

            return response
            
    def create_and_render_contact(self, verifier, request_token, 
                                  request_token_secret):
        if self.api.accessToken(request_token=request_token, verifier=verifier,
                                request_token_secret=request_token_secret):
            contact = self.create_or_update_contact_from_profile()
            extra_context = {
                'redirect_url':contact.get_absolute_url() + '?new_contact=true'
            }
    
            return render_to_response('contactlist/window_closer.html',
                                      extra_context)
