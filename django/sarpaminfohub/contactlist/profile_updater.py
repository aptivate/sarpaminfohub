from django.core.cache import cache
from django.shortcuts import redirect
from django.conf import settings
from sarpaminfohub.contactlist.test_linked_in_api import TestLinkedInApi
from linkedin import linkedin

class ProfileUpdater(object):
    ONE_MINUTE = 60

    def __init__(self, request, post_authorize_url, test_data=False,
                 token_timeout=None):
        self.request = request
        
        if token_timeout is None:
            self.token_timeout = self.ONE_MINUTE
        else:
            self.token_timeout = token_timeout

        api_key = settings.LINKED_IN_API_KEY
        secret_key = settings.LINKED_IN_SECRET_KEY
    
        if test_data:
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
