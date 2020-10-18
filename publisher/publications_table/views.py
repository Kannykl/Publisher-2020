from django.shortcuts import render
from .models import Publication
from django.views.generic import CreateView


def show_all_publications(request):
    """ Страница отображения всех записей"""
    publications = Publication.objects.all()
    context = {
        'publications': publications
    }
    return render(request, "publications_table/all_publications.html", context)


class PublicationCreateView(CreateView):
    """ Страница создания новой записи"""
    model = Publication
    template_name = 'publications_table/publication_create.html'
    fields = '__all__'
    success_url = '/all_publications/'

    def form_valid(self, form):
        return super().form_valid(form)
