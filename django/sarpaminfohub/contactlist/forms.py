from django import forms
from tagging.models import Tag


class SearchForm(forms.Form):
    search_term = forms.CharField()
    tag = forms.ModelChoiceField(Tag.objects.all())
    