from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Publication, Author
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from .forms import PublicationFilter, SearchPublications, PublicationCreateForm, ExportTableForm
from .export import export_in_xls
from .authorization import check_user


def show_all_publications(request, type_of_sort=0):
    """ Страница отображения всех записей"""
    start_publications = sort(type_of_sort)
    filtered_publications, form1 = filter_publications(request, start_publications)
    form2 = SearchPublications(request.GET)
    form3 = export_table(filtered_publications, request)
    context = {
        'publications': filtered_publications,
        'form': form1,
        'form2': form2,
        'form3': form3,
    }
    return render(request, "publications_table/all_publications.html", context)


class PublicationUpdateView(UpdateView):
    """ Страница редактирования существующей записи в таблице"""
    model = Publication
    fields = '__all__'
    template_name = 'publications_table/publication_update.html'
    context_object_name = 'publication'
    success_url = '/publisher/all_publications/'

    def form_valid(self, form):
        return super().form_valid(form)


class PublicationDeleteView(DeleteView):
    """ Страница удаления записи из таблицы """
    model = Publication
    template_name = 'publications_table/publication_delete.html'
    success_url = '/publisher/all_publications/'


def sort(type_of_sort: int):
    """ Сортирует записи по определенному полю"""
    dictionary = {
        '0': Publication.objects.all(),
        '4': Publication.objects.all().order_by('title'),
        '5': Publication.objects.all().order_by('edition'),
        '6': Publication.objects.all().order_by('-published_year'),
        '7': Publication.objects.all().order_by('type_of_publication'),
        '8': Publication.objects.all().order_by('range'),
        '9': Publication.objects.all().order_by('uk_number'),
    }
    publications = dictionary[f'{type_of_sort}']
    return publications


def filter_publications(request, publications):
    """Фильтрует записи"""
    if request.method == 'GET':
        form = PublicationFilter(request.GET)
        if form.is_valid():
            if form.cleaned_data['min_year']:
                publications = publications.filter(published_year__gte=form.cleaned_data['min_year'])

            if form.cleaned_data['max_year']:
                publications = publications.filter(published_year__lte=form.cleaned_data['max_year'])

            if form.cleaned_data['type_of_publication']:
                publications = publications.filter(type_of_publication__in=
                                                   form.cleaned_data['type_of_publication'])
        return publications, form


class AuthorCreateView(CreateView):
    """ Добавление автора пользователем """
    model = Author
    template_name = 'publications_table/author_create.html'
    fields = '__all__'
    success_url = '/publisher/create_publication/'

    def form_valid(self, form):
        return super().form_valid(form)


def create_publication(request):
    """ Страница добавления записи в таблицу"""
    if request.method == 'POST':
        form = PublicationCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/publisher/all_publications/')
    else:
        form = PublicationCreateForm()
    return render(request, 'publications_table/publication_create.html', {'form': form})


class JsonSearchPublicationsView(ListView):
    """Поиск записей по фамилии автора, названию статьи, изданию и номеру УК"""

    def get_queryset(self):
        if self.request.GET.get('search').isdigit():
            queryset = Publication.objects.order_by('title').filter(
                Q(uk_number=self.request.GET.get("search")) |
                Q(edition=self.request.GET.get("search"))
            ).distinct().values("title", "published_year", "uk_number",
                                "edition", "type_of_publication", "range", "id"
                                )
        else:
            queryset = Publication.objects.order_by('title').filter(
                Q(title=self.request.GET.get("search")) |
                Q(authors__surname__in=self.request.GET.getlist("search")) |
                Q(edition=self.request.GET.get("search"))
            ).distinct().values("title", "published_year", "uk_number",
                                "edition", "type_of_publication", "range", "id"
                                )
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"publications": queryset})


def export_table(publications, request):
    """ Эскпорт в Excel таблицу"""
    if request.method == 'GET':
        form = ExportTableForm(request.GET)
        if form.is_valid():
            if form.cleaned_data['file_name']:
                file_name = form.cleaned_data['file_name']
                export_in_xls(publications, file_name)
    else:
        form = ExportTableForm()
    return form


def get_publication_info(request, id: int):
    """Информация о записи в таблице"""
    publication = Publication.objects.get(pk=id)
    print(publication)
    context = {
        "publication": publication,
    }
    return render(request, "publications_table/publication_info.html", context)
