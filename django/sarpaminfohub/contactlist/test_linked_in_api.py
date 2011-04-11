from linkedin.linkedin import LinkedIn, OAuthError, Profile
import hmac
import binascii
import sha

class TestLinkedInApi(LinkedIn):
    def requestToken(self):
        """
        Mock implementation used for testing

        Performs the corresponding API which returns the request token in a query string
        The POST Querydict must include the following:
         * oauth_callback
         * oauth_consumer_key
         * oauth_nonce
         * oauth_signature_method
         * oauth_timestamp
         * oauth_version
        """
        #################
        # BEGIN ROUTINE #
        #################
        # clear everything
        self.clear()
        # initialization
        self.request_oauth_nonce = self._generate_nonce()
        self.request_oauth_timestamp = self._generate_timestamp()
        # create Signature Base String
        method = "POST"
        url = self.getRequestTokenURL()
        query_dict = {"oauth_callback": self.CALLBACK_URL,
                      "oauth_consumer_key": self.API_KEY,
                      "oauth_nonce": self.request_oauth_nonce,
                      "oauth_signature_method": self.signature_method,
                      "oauth_timestamp": self.request_oauth_timestamp,
                      "oauth_version": self.version,
                      }
        query_string = self._quote(self._urlencode(query_dict))
        signature_base_string = "&".join([self._quote(method), self._quote(url), query_string])
        # create actual signature
        hashed = hmac.new(self._quote(self.API_SECRET) + "&", signature_base_string, sha)
        signature = binascii.b2a_base64(hashed.digest())[:-1]
        # it is time to create the heaader of the http request that will be sent
        header = 'OAuth realm="http://api.linkedin.com", '
        header += 'oauth_nonce="%s", '
        header += 'oauth_callback="%s", '
        header += 'oauth_signature_method="%s", '
        header += 'oauth_timestamp="%d", '
        header += 'oauth_consumer_key="%s", '
        header += 'oauth_signature="%s", '
        header += 'oauth_version="%s"'
        header = header % (self.request_oauth_nonce, self._quote(self.CALLBACK_URL),
                           self.signature_method, self.request_oauth_timestamp,
                           self._quote(self.API_KEY), self._quote(signature), self.version)

        response = "oauth_token=7ccce8fb-83e4-4ab7-b8da-7f8b5c32c4ad" + \
            "&oauth_token_secret=f2541842-5e09-41fc-8037-b28149de6773" + \
            "&oauth_callback_confirmed=true" + \
            "&xoauth_request_auth_url=https%3A%2F%2Fapi.linkedin.com%2Fuas%2Foauth%2Fauthorize" + \
            "&oauth_expires_in=599"
        
        oauth_problem = self._get_value_from_raw_qs("oauth_problem", response)
        if oauth_problem:
            self.request_oauth_error = oauth_problem
            return False

        self.request_token = self._get_value_from_raw_qs("oauth_token", response)
        self.request_token_secret = self._get_value_from_raw_qs("oauth_token_secret", response)
        
        return True
    
    
    def accessToken(self, request_token = None, request_token_secret = None, verifier = None):
        """
        Mock implementation used for testing
        
        Performs the corresponding API which returns the access token in a query string
        Accroding to the link (http://developer.linkedin.com/docs/DOC-1008), POST Querydict must include the following:
        * oauth_consumer_key
        * oauth_nonce
        * oauth_signature_method
        * oauth_timestamp
        * oauth_token (request token)
        * oauth_version
        """
        #################
        # BEGIN ROUTINE #
        #################
        
        self.request_token = request_token and request_token or self.request_token
        self.request_token_secret = request_token_secret and request_token_secret or self.request_token_secret
        self.verifier = verifier and verifier or self.verifier
        # if there is no request token, fail immediately
        if self.request_token is None:
            raise OAuthError("There is no Request Token. Please perform 'requestToken' method and obtain that token first.")

        if self.request_token_secret is None:
            raise OAuthError("There is no Request Token Secret. Please perform 'requestToken' method and obtain that token first.")

        if self.verifier is None:
            raise OAuthError("There is no Verifier Key. Please perform 'requestToken' method, redirect user to API authorize page and get the verifier.")
        
        # initialization
        self.access_oauth_nonce = self._generate_nonce()
        self.access_oauth_timestamp = self._generate_timestamp()

        # create Signature Base String
        method = "POST"
        url = self.getAccessTokenURL()
        query_dict = {"oauth_consumer_key": self.API_KEY,
                      "oauth_nonce": self.access_oauth_nonce,
                      "oauth_signature_method": self.signature_method,
                      "oauth_timestamp": self.access_oauth_timestamp,
                      "oauth_token" : self.request_token,
                      "oauth_verifier" : self.verifier,
                      "oauth_version": self.version,
                      }
        query_string = self._quote(self._urlencode(query_dict))
        signature_base_string = "&".join([self._quote(method), self._quote(url), query_string])
        # create actual signature
        hashed = hmac.new(self._quote(self.API_SECRET) + "&" + self._quote(self.request_token_secret), signature_base_string, sha)
        signature = binascii.b2a_base64(hashed.digest())[:-1]
        # it is time to create the heaader of the http request that will be sent
        header = 'OAuth realm="http://api.linkedin.com", '
        header += 'oauth_nonce="%s", '
        header += 'oauth_signature_method="%s", '
        header += 'oauth_timestamp="%d", '
        header += 'oauth_consumer_key="%s", '
        header += 'oauth_token="%s", '
        header += 'oauth_verifier="%s", '
        header += 'oauth_signature="%s", '
        header += 'oauth_version="%s"'
        header = header % (self._quote(self.access_oauth_nonce), self._quote(self.signature_method),
                           self.access_oauth_timestamp, self._quote(self.API_KEY),
                           self._quote(self.request_token), self._quote(self.verifier),
                           self._quote(signature), self._quote(self.version))

        response = "oauth_token=b20ecb6c-7706-4d6b-b9b0-8f53672f179d" + \
            "&oauth_token_secret=1e41d8e9-acd5-48b1-b1df-de0be9ec01fa" + \
            "&oauth_expires_in=0" + \
            "&oauth_authorization_expires_in=0"
        
        oauth_problem = self._get_value_from_raw_qs("oauth_problem", response)
        if oauth_problem:
            self.request_oauth_error = oauth_problem
            return False

        self.access_token = self._get_value_from_raw_qs("oauth_token", response)
        self.access_token_secret = self._get_value_from_raw_qs("oauth_token_secret", response)

        return True

    def GetProfile(self, member_id = None, url = None, fields=[]):
        """
        Mock implementation used for testing

        Gets the public profile for a specific user. It is determined by his/her member id or public url.
        If none of them is given, the information og the application's owner are returned.

        If none of them are given, current user's details are fetched.
        The argument 'fields' determines how much information will be fetched.

        Examples:
        client.GetProfile(merber_id = 123, url = None, fields=['first-name', 'last-name']) : fetches the profile of a user whose id is 123. 

        client.GetProfile(merber_id = None, url = None, fields=['first-name', 'last-name']) : fetches current user's profile

        client.GetProfile(member_id = None, 'http://www.linkedin.com/in/ozgurv') : fetches the profile of a  user whose profile url is http://www.linkedin.com/in/ozgurv
        
        @ Returns Profile instance
        """
        #################
        # BEGIN ROUTINE #
        #################
        # if there is no access token or secret, fail immediately
        if self.access_token is None:
            self.error = "There is no Access Token. Please perform 'accessToken' method and obtain that token first."
            raise OAuthError(self.error)
        
        if self.access_token_secret is None:
            self.error = "There is no Access Token Secret. Please perform 'accessToken' method and obtain that token first."
            raise OAuthError(self.error)
        
        # specify the url according to the parameters given
        raw_url = "/v1/people/"
        if url:
            url = self._quote(url)
            raw_url = (raw_url + "url=%s:public") % url
        elif member_id:
            raw_url = (raw_url + "id=%s" % member_id)
        else:
            raw_url = raw_url + "~"
        if url is None:
            fields = ":(%s)" % ",".join(fields) if len(fields) > 0 else None
            if fields:
                raw_url = raw_url + fields
                
        # generate nonce and timestamp
        nonce = self._generate_nonce()
        timestamp = self._generate_timestamp()

        # create signatrue and signature base string
        method = "GET"
        FULL_URL = "%s://%s%s" % (self.URI_SCHEME, self.API_ENDPOINT, raw_url)
        query_dict = {"oauth_consumer_key": self.API_KEY,
                      "oauth_nonce": nonce,
                      "oauth_signature_method": self.signature_method,
                      "oauth_timestamp": timestamp,
                      "oauth_token" : self.access_token,
                      "oauth_version": self.version
                      }
        
        signature_base_string = "&".join([self._quote(method), self._quote(FULL_URL), self._quote(self._urlencode(query_dict))])
        hashed = hmac.new(self._quote(self.API_SECRET) + "&" + self._quote(self.access_token_secret), signature_base_string, sha)
        signature = binascii.b2a_base64(hashed.digest())[:-1]


        # create the HTTP header
        header = 'OAuth realm="http://api.linkedin.com", '
        header += 'oauth_nonce="%s", '
        header += 'oauth_signature_method="%s", '
        header += 'oauth_timestamp="%d", '
        header += 'oauth_consumer_key="%s", '
        header += 'oauth_token="%s", '
        header += 'oauth_signature="%s", '
        header += 'oauth_version="%s"'
        header = header % (nonce, self.signature_method, timestamp,
                           self._quote(self.API_KEY), self._quote(self.access_token),
                           self._quote(signature), self.version)
        
        response = self.get_test_profile()
        error = self._parse_error(response)
        if error:
            self.error = error
            return None

        return Profile.create(response) # this creates Profile instance or gives you null

    def get_test_profile(self):
        profile_xml = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>" + \
        "<person>" + \
        "  <first-name>Martin</first-name>" + \
        "  <last-name>Burchell</last-name>" + \
        "  <specialties>ANSI C, C++, Java, Lull (what?) and some assembler." + \
        "Unix (Linux, Solaris etc), Windows (various), Palm OS, SuperWaba, RISC OS." + \
        "X/Motif, MFC." + \
        "GNU make, gcc, gdb, CVS, Perforce, Eclipse, MS Visual Studio, various unit testing frameworks, test-driven development" + \
        "HTML, JavaScript, CSS, DOM, PHP, VBA, Excel Kung-Fu" + \
        "Training, Group Facilitation, Consensus-based Decision Making, Project Management, Salad Making</specialties>" + \
        "  <positions total=\"4\">" + \
        "    <position>" + \
        "      <id>16325633</id>" + \
        "      <title>Software Engineer</title>" + \
        "      <start-date>" + \
        "        <year>2007</year>" + \
        "        <month>7</month>" + \
        "      </start-date>" + \
        "      <is-current>true</is-current>" + \
        "      <company>" + \
        "        <name>Aptivate</name>" + \
        "        <size>1-10 employees</size>" + \
        "        <type>Privately Held</type>" + \
        "        <industry>Information Technology and Services</industry>" + \
        "      </company>" + \
        "    </position>" + \
        "    <position>" + \
        "      <id>11387749</id>" + \
        "      <title>Software Engineer</title>" + \
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
        "      <title>Senior Software Engineer</title>" + \
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
        "      <title>Senior Software Engineer</title>" + \
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
        "  <public-profile-url>http://www.linkedin.com/pub/martin-burchell/0/266/926</public-profile-url>" + \
        "  <summary>Since 1994 I've held several software engineering roles in software development. In July 2007, after a few months of volunteering I joined the paid staff at Aptivate, a not-for-profit  IT consultancy, which specialises in ICTs for International Development. At Aptivate my skillset has expanded to include training, group facilitation, consensus-based decision making, answering the telephone and making lunch." + \
        "" + \
        "Prior to joining Aptivate I ported IPTV web browsers to various embedded systems and integrated and extended the browser software to meet customers' requirements." + \
        "" + \
        "I've also spent several years developing applications for spatially-indexed object-orientated databases used by the mapping and charting industry." + \
        "" + \
        "I'm always keen to build on my experience and learn new skills and technologies.</summary>" + \
        "  <location>" + \
        "    <name>Cambridge, United Kingdom</name>" + \
        "    <country>" + \
        "      <code>gb</code>" + \
        "    </country>" + \
        "  </location>" + \
        "  <phone-numbers total=\"0\" />" + \
        "</person>"
        
        return profile_xml