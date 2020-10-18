from django.shortcuts import render
from .models import Publication
from django.views.generic import CreateView, UpdateView, DeleteView


def show_all_publications(request, type_of_sort=0):
    """ Страница отображения всех записей"""
    publications = sort(type_of_sort)
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


def sort(type_of_sort: int):
    """ Сортирует записи по определенному полю"""
    dictionary = {
        '0': Publication.objects.all(),
        '1': Publication.objects.all().order_by('authors__military_rank'),
        '2': Publication.objects.all().order_by('authors__surname'),
        '3': Publication.objects.all().order_by('authors__work_position'),
        '4': Publication.objects.all().order_by('title'),
        '5': Publication.objects.all().order_by('edition'),
        '6': Publication.objects.all().order_by('-published_year'),
        '7': Publication.objects.all().order_by('type_of_publication'),
        '8': Publication.objects.all().order_by('range'),
        '9': Publication.objects.all().order_by('uk_number'),
    }
    publications = dictionary[f'{type_of_sort}']
    return publications
