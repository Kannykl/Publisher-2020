from publications_table.models import Type, Author


def service_filter_publications_by_type_and_published_year(form, publications):
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


def get_all_types():
    types_options = tuple((str(type_of_publication), str(type_of_publication))
                          for type_of_publication in Type.objects.all())
    return types_options


def get_all_enable_types():
    types_options = tuple((str(type_of_publication), str(type_of_publication))
                          for type_of_publication in Type.objects.all()
                          if type_of_publication.enable)
    return types_options


def get_all_authors():
    authors = Author.objects.all()
    return authors
