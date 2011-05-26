from haystack.management.commands import rebuild_index
from django.test.testcases import TestCase
from sarpaminfohub.contactlist.models import Contact

class ContactListTestCase(TestCase):
    def delete_contacts(self):
        # pylint: disable-msg=E1101
        Contact.objects.all().delete()
    
    def create_contacts(self):
        self.contact1 = Contact(given_name="My", family_name="Name", phone="(12345) 678910",
                   email="a@b.c", address_line_1="123 A Road Name, Somewhere", 
                   role="Head of Surgery", tags="Hospital, Medicine, Surgeon", organization="London Teaching Hospital",
                   note="Note Very Important")
        self.contact1.save()
        self.contact2 = Contact(
                   given_name="Anew", family_name="Person", phone="(54321) 123456",
                   email="d@e.f", address_line_1="456 A Road, Through the Looking Glass",
                   role="Pharmacist", tags="Medicine", organization="Selby's Pharmacy"
                   )
        self.contact2.save()
        self.contact3 = Contact(given_name="Aptivate", family_name="Employee", phone="(32543) 523566",
                   email="g@h.i", address_line_1="999 Letsbe Avenue", tags="academia", note="Death Note",
                   role="Researcher", organization="Imperial College"
                   )
        self.contact3.save()
    
    def rebuild_search_index(self):
        rebuild_index.Command().handle(verbosity=0, interactive=False)
