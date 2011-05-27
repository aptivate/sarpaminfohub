from django.shortcuts import render_to_response
from sarpaminfohub.contactlist.models import Contact
from sarpaminfohub.contactlist.profile_updater import ProfileUpdater

class BatchUpdater(ProfileUpdater):
    def __init__(self, request, test_data=None):
        ProfileUpdater.__init__(self, request, post_authorize_url=None, \
                                test_data=test_data)
    
    def update(self):
        contacts = Contact.objects.all()
        
        batch_report = []
        
        for contact in contacts:
            full_name = contact.get_full_name()

            status = None
            
            self.api.access_token = contact.access_token
            self.api.access_token_secret = contact.access_token_secret

            if self.api.access_token:
                updated_contact = self.update_contact_from_profile(contact)
                if updated_contact is None:
                    if self.api.error.startswith("[unauthorized]"):
                        contact.delete()
                        status = "Deleted"
                    else:
                        status = "Error:" + self.api.error
                else:
                    full_name = updated_contact.get_full_name()

                    status = "Updated"
            else:
                status = "No LinkedIn Profile"
                    
            batch_report.append({full_name : status})
            
        extra_context = {'batch_report' : batch_report}
        
        return render_to_response('contactlist/batch_report.html',
                                  extra_context)
