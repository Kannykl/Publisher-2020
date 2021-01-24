"""Этот модуль содержит бизнес логику"""
from publications_table.models import Type, Author, Publication


def service_filter_publications_by_type_and_published_year(form, publications):
    """Фильтрует полученные публикации по типу и году выпуска."""
    type_of_publications = tuple(
        (Type.objects.get(type_of_publication=type_of_publication).id
         for type_of_publication in form.cleaned_data['type_of_publication']))

    if form.cleaned_data['min_year']:
        publications = publications.filter(published_year__gte=form.cleaned_data['min_year'])

    if form.cleaned_data['max_year']:
        publications = publications.filter(published_year__lte=form.cleaned_data['max_year'])

    if form.cleaned_data['type_of_publication']:
        publications = publications.filter(type_of_publication__in=type_of_publications)

    return publications


def get_all_types_options():
    """Возвращает все возможные типы для фильтра."""
    types_options = tuple((str(type_of_publication), str(type_of_publication))
                          for type_of_publication in Type.objects.all())
    return types_options


def get_all_enable_types_options():
    """Возвращает все активные типы для создания/изменения публикаций."""
    types_options = tuple((str(type_of_publication), str(type_of_publication))
                          for type_of_publication in Type.objects.all()
                          if type_of_publication.enable)
    return types_options


def get_all_enable_types():
    """Получает все видимые типы."""
    types = (tuple((type_of_publication
                    for type_of_publication in Type.objects.all() if type_of_publication.enable)))
    return types


def get_all_authors():
    """Возвращает всех авторов."""
    authors = Author.objects.all()
    return authors


def update_type_of_publication(form, publication):
    """Обновляет тип публикации у записи."""
    if form.cleaned_data['type_of_publication'] != '':
        new_type_of_publication = Type.objects.get(
            type_of_publication=form.cleaned_data['type_of_publication'])
        publication.title = form.cleaned_data['title']
        publication.save()
        old_type_of_publication = Publication.objects.get(
            title=form.cleaned_data['title']).type_of_publication
        if old_type_of_publication is not None:
            old_type_of_publication.publication_set.remove(publication)
        new_type_of_publication.publication_set.add(
            Publication.objects.get(title=form.cleaned_data['title']),
        )
        publication.type_of_publication = new_type_of_publication
        publication.save()


def service_delete_type_of_publication(type_of_publication):
    """Делает тип публикации недоступным в общем списке"""
    type_of_publication.enable = False
    type_of_publication.save()
