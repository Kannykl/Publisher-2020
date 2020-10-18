from django.shortcuts import render
from .models import Publication


def show_all_publications(request):
    publications = Publication.objects.all()
    context = {
        'publications': publications
    }
    return render(request, "publications_table/all_publications.html", context)