from django.shortcuts import render
from .models import Publication
from django.views.generic import CreateView, UpdateView, DeleteView


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


class PublicationUpdateView(UpdateView):
    """ Страница редактирования существубщей записи в таблице"""
    model = Publication
    fields = '__all__'
    template_name = 'publications_table/publication_update.html'
    context_object_name = 'publication'
    success_url = '/all_publications/'

    def form_valid(self, form):
        return super().form_valid(form)


class PublicationDeleteView(DeleteView):
    """ Страница удаления записи из таблицы """
    model = Publication
    template_name = 'publications_table/publication_delete.html'
    success_url = '/all_publications/'
