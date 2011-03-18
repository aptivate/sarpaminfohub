from django.template.loader import render_to_string
class Menu():
    def as_html(self):
        return render_to_string('menu.html', {'menu':self})
    
    def __init__(self, entries):
        self.entries = entries
