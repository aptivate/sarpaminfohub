# Create your views here.

from django.shortcuts import render_to_response

def search_form(request):
    return render_to_response('search.html')