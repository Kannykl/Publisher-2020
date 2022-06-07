""" Этот модуль содержит django представления """
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .export import export_in_xls
from .forms import (PublicationFilter,
                    SearchPublications,
                    PublicationCreateForm,
                    ExportTableForm,
                    AuthorCreateForm,
                    TypeCreateForm,
                    PublicationUpdateForm,
                    )
from .models import Publication, Author, Type
from .services import (service_filter_publications_by_type_and_published_year,
                       get_all_enable_types_options,
                       get_all_authors, update_type_of_publication,
                       service_delete_type_of_publication,
                       get_all_enable_types, select_publications_for_export,
                       get_all_existing_in_publications_types)


class PublicationsListView(ListView):
    template_name = "publications_table/all_publications.html"
    model = Publication
    context_object_name = 'publications'
    ordering = 'title'

    def get_queryset(self):
        type_of_sort = int(self.kwargs['type_of_sort'])
        return sort(type_of_sort)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        filtered_publications, filter_form = filter_publications(self.request, self.get_queryset())
        export_form, table = export_table(filtered_publications, self.request)
        search_form = SearchPublications(self.request.GET)
        context["table"] = table
        context["form"] = filter_form
        context["form3"] = export_form
        context["clear_publications"] = self.get_queryset()
        context["search_form"] = search_form
        return context


def show_all_publications(request, type_of_sort=0):
    """ Страница отображения всех записей"""
    start_publications = sort(type_of_sort)
    filtered_publications, filter_form = filter_publications(request, start_publications)
    search_form = SearchPublications(request.GET)
    export_form, table = export_table(filtered_publications, request)
    paginator = Paginator(filtered_publications, 10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    context = {
        'publications': page,
        'form': filter_form,
        'form2': search_form,
        'form3': export_form,
        'table': table,
        'clear_publications': Publication.objects.all(),
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
    if str(type_of_sort) in dictionary.keys():
        publications = dictionary[f'{type_of_sort}']
    else:
        publications = dictionary['0']
    return publications


def filter_publications(request, publications):
    """ Фильтрует записи по году выпуска и типу статьи """
    types_options = get_all_existing_in_publications_types()
    if request.method == 'GET':
        form = PublicationFilter(request.GET, types_options=types_options)
        if form.is_valid():
            publications = service_filter_publications_by_type_and_published_year(
                form=form, publications=publications)
    else:
        form = PublicationFilter()
    return publications, form


class AuthorCreateView(CreateView):
    """ Добавление автора пользователем """
    model = Author
    template_name = 'publications_table/author_create.html'
    fields = '__all__'

    def get(self, request, *args, **kwargs):
        page = request.META['HTTP_REFERER']
        request.session['return_path'] = page
        return render(request, template_name=self.template_name, context={"form": AuthorCreateForm()})

    def get_success_url(self):
        return self.request.session['return_path']

    def form_valid(self, form):
        return super().form_valid(form)


def create_publication(request):
    """ Страница добавления записи в таблицу"""
    types_options = get_all_enable_types_options()
    authors = get_all_authors()
    if request.method == 'POST':
        form = PublicationCreateForm(request.POST, types_options=types_options)
        if form.is_valid():
            form.save()
            return redirect('/publisher/')
    else:
        form = PublicationCreateForm(types_options=types_options)
    return render(request, 'publications_table/publication_create.html', {'form': form,
                                                                          'authors': authors})


def update_publication(request, pk):
    """ Страница редактирования публикации """
    publication = get_object_or_404(Publication, id=pk)
    types_options = get_all_enable_types_options()
    authors = Author.objects.all()
    if request.method == "POST":
        form = PublicationUpdateForm(
            data=request.POST,
            instance=publication,
            types_options=types_options
        )
        if form.is_valid():
            update_type_of_publication(form, publication)
            messages.success(request, f'{publication.title} успешно изменена')
            form.save()
            return redirect('/publisher/')
    else:
        form = PublicationUpdateForm(instance=publication, types_options=types_options)
    return render(request, 'publications_table/publication_update.html',
                  {'form': form, 'publication': publication,
                   'authors': authors,
                   })


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
    """Эскпорт в Excel таблицу."""
    table = None
    if request.method == 'GET':
        form = ExportTableForm(request.GET)
        if form.is_valid():
            select_publications_for_export(form)
            if form.cleaned_data['file_name']:
                file_name = form.cleaned_data['file_name']
                table = export_in_xls(publications, file_name)
    else:
        form = ExportTableForm()
    return form, table


def get_publication_info(request, pk: int):
    """Страница информации о записи в таблице."""
    publication = Publication.objects.get(pk=pk)
    context = {
        "publication": publication,
    }
    return render(request, "publications_table/publication_info.html", context)


class AuthorDeleteView(DeleteView):
    """Страница удаления автора из списка."""
    model = Author
    template_name = 'publications_table/author_delete.html'
    success_url = '/publisher/authors/'


def show_all_authors(request):
    """Страница отображения всех авторов."""
    authors = Author.objects.all()
    paginator = Paginator(authors, 10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    context = {
        'authors': page,
    }
    return render(request, "publications_table/all_authors.html", context)


def get_author_info(request, pk: int):
    """Страница информации об авторе."""
    author = Author.objects.get(pk=pk)
    context = {
        "author": author,
    }
    return render(request, "publications_table/author_info.html", context)


class AuthorUpdateView(UpdateView):
    """Страница изменение параметров автора."""
    model = Author
    template_name = 'publications_table/author_update.html'
    fields = '__all__'
    success_url = '/publisher/authors'

    def form_valid(self, form):
        return super().form_valid(form)


def show_all_types(request):
    """Страница отображения всех типов."""
    types = get_all_enable_types()
    paginator = Paginator(types, 10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    context = {
        'types': page,
    }
    return render(request, "publications_table/all_types.html", context)


class TypeUpdateView(UpdateView):
    """Страница изменение типа публикации."""
    model = Type
    template_name = 'publications_table/type_update.html'
    fields = '__all__'
    success_url = '/publisher/types'

    def form_valid(self, form):
        return super().form_valid(form)


class TypeCreateView(CreateView):
    """Страница создания типа публикации."""
    model = Type
    template_name = 'publications_table/type_create.html'
    fields = '__all__'

    def get(self, request, *args, **kwargs):
        page = request.META['HTTP_REFERER']
        request.session['return_path'] = page
        return render(request, template_name=self.template_name, context={'form': TypeCreateForm()})

    def get_success_url(self):
        return self.request.session['return_path']

    def form_valid(self, form):
        return super().form_valid(form)


def delete_type_of_publication(request, pk):
    """Страница удаления типа публикации."""
    type_of_publication = Type.objects.get(id=pk)
    if request.method == 'POST':
        service_delete_type_of_publication(type_of_publication)
        return redirect('/publisher/types/')
    context = {
        'object': type_of_publication
    }
    return render(request, 'publications_table/type_delete.html', context)
