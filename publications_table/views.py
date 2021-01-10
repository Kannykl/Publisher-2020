from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from .models import Publication, Author, Type
from .forms import (PublicationFilter,
                    SearchPublications,
                    PublicationCreateForm,
                    ExportTableForm,
                    PublicationUpdateForm,
                    )
from .export import export_in_xls


def show_all_publications(request, type_of_sort=0):
    """ Страница отображения всех записей"""
    start_publications = sort(type_of_sort)
    filtered_publications, form1 = filter_publications(request, start_publications)
    form2 = SearchPublications(request.GET)
    form3, table = export_table(filtered_publications, request)
    paginator = Paginator(filtered_publications, 10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    context = {
        'publications': page,
        'form': form1,
        'form2': form2,
        'form3': form3,
        'table': table,
    }
    return render(request, "publications_table/all_publications.html", context)


class PublicationDeleteView(DeleteView):
    """ Страница удаления записи из таблицы """
    model = Publication
    template_name = 'publications_table/publication_delete.html'
    success_url = '/publisher/'


def sort(type_of_sort: int):
    """ Сортирует записи по определенному полю """
    dictionary = {
        '0': Publication.objects.all(),
        '1': Publication.objects.all().order_by('title'),
        '2': Publication.objects.all().order_by('edition'),
        '3': Publication.objects.all().order_by('-published_year'),
        '4': Publication.objects.all().order_by('type_of_publication__type_of_publication'),
        '5': Publication.objects.all().order_by('range'),
        '6': Publication.objects.all().order_by('uk_number'),
    }
    publications = dictionary[f'{type_of_sort}']
    return publications


def filter_publications(request, publications):
    """ Фильтрует записи """
    types_options = tuple((str(type_of_publication), str(type_of_publication))
                          for type_of_publication in Type.objects.all())
    if request.method == 'GET':
        form = PublicationFilter(request.GET, types_options=types_options)
        if form.is_valid():
            type_of_publications = tuple(
                (Type.objects.get(type_of_publication=type_of_publication).id
                 for type_of_publication in form.cleaned_data['type_of_publication']))

            if form.cleaned_data['min_year']:
                publications = publications.filter(published_year__gte=
                                                   form.cleaned_data['min_year'])

            if form.cleaned_data['max_year']:
                publications = publications.filter(published_year__lte=
                                                   form.cleaned_data['max_year'])

            if form.cleaned_data['type_of_publication']:
                publications = publications.filter(type_of_publication__in=
                                                   type_of_publications)
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
    types_options = tuple((str(type_of_publication), str(type_of_publication))
                          for type_of_publication in Type.objects.all()
                          if type_of_publication.enable)
    if request.method == 'POST':
        form = PublicationCreateForm(request.POST, types_options=types_options)
        if form.is_valid():
            form.save()
            return redirect('/publisher/')
    else:
        form = PublicationCreateForm(types_options=types_options)
    return render(request, 'publications_table/publication_create.html', {'form': form})


def update_publication(request, pk):
    """ Страница редактирования публикации """
    publication = get_object_or_404(Publication, id=pk)
    types_options = tuple((str(type_of_publication), str(type_of_publication))
                          for type_of_publication in Type.objects.all()
                          if type_of_publication.enable)
    if request.method == "POST":
        form = PublicationUpdateForm(data=request.POST,
                                     instance=publication,
                                     types_options=types_options)
        if form.is_valid():
            new_type_of_publication = Type.objects.get(type_of_publication=
                                                       form.cleaned_data['type_of_publication'])
            old_type_of_publication = Type.objects.get(type_of_publication=
                                                       form.fields['type_of_publication'].initial)
            publication.uk_number = form.cleaned_data['uk_number']
            publication.save()
            old_type_of_publication.publication_set.remove(publication)
            new_type_of_publication.publication_set.add(
                Publication.objects.get(uk_number=form.cleaned_data['uk_number']),
            )
            publication.type_of_publication = new_type_of_publication
            publication.save()
            form.save()
            return redirect(f'/publisher/publication_info/{publication.id}')
    else:
        form = PublicationUpdateForm(instance=publication, types_options=types_options)
    return render(request, 'publications_table/publication_update.html',
                  {'form': form, 'publication': publication})


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
    table = None
    if request.method == 'GET':
        form = ExportTableForm(request.GET)
        if form.is_valid():
            if form.cleaned_data['file_name']:
                file_name = form.cleaned_data['file_name']
                table = export_in_xls(publications, file_name)
    else:
        form = ExportTableForm()
    return form, table


def get_publication_info(request, pk: int):
    """Страница информации о записи в таблице"""
    publication = Publication.objects.get(pk=pk)
    context = {
        "publication": publication,
    }
    return render(request, "publications_table/publication_info.html", context)


class AuthorDeleteView(DeleteView):
    """ Страница удаления автора из списка """
    model = Author
    template_name = 'publications_table/author_delete.html'
    success_url = '/publisher/authors/'


def show_all_authors(request):
    """ Страница отображения всех авторов"""
    authors = Author.objects.all()
    paginator = Paginator(authors, 10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    context = {
        'authors': page,
    }
    return render(request, "publications_table/all_authors.html", context)


def get_author_info(request, pk: int):
    """ Страница информации об авторе"""
    author = Author.objects.get(pk=pk)
    context = {
        "author": author,
    }
    return render(request, "publications_table/author_info.html", context)


class AuthorUpdateView(UpdateView):
    """ Страница изменение параметров автора """
    model = Author
    template_name = 'publications_table/author_update.html'
    fields = '__all__'
    success_url = '/publisher/authors'

    def form_valid(self, form):
        return super().form_valid(form)


def show_all_types(request):
    """ Страница отображения всех авторов"""
    types = tuple((type_of_publication
                   for type_of_publication in Type.objects.all() if type_of_publication.enable))
    paginator = Paginator(types, 10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    context = {
        'types': page,
    }
    return render(request, "publications_table/all_types.html", context)


class TypeUpdateView(UpdateView):
    """ Страница изменение типа публикации """
    model = Type
    template_name = 'publications_table/type_update.html'
    fields = '__all__'
    success_url = '/publisher/types'

    def form_valid(self, form):
        return super().form_valid(form)


class TypeCreateView(CreateView):
    """ Страница создания типа публикации """
    model = Type
    template_name = 'publications_table/type_create.html'
    fields = '__all__'
    success_url = '/publisher/create_publication/'

    def form_valid(self, form):
        return super().form_valid(form)


def delete_type_of_publication(request, pk):
    """ Страница удаления типа публикации """
    type_of_publication = Type.objects.get(id=pk)
    if request.method == 'POST':
        type_of_publication.enable = False
        type_of_publication.save()
        return redirect('/publisher/types/')
    context = {
        'object': type_of_publication
    }
    return render(request, 'publications_table/type_delete.html', context)
