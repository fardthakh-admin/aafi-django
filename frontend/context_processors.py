# context_processors.py
from .views import get_all_collections
from .models import *
from django.shortcuts import render

def collections_processor(request):
    collections_data = get_all_collections(request)
    return {'collections': collections_data['collections']}

