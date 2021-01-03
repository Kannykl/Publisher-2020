from django.urls import path
from .views import (
    show_all_publications,
    PublicationDeleteView,
    JsonSearchPublicationsView,
    create_publication,
    AuthorCreateView,
    AuthorDeleteView,
    AuthorUpdateView,
    get_publication_info,
    update_publication,
    show_all_authors,
    get_author_info,
)

urlpatterns = [
    path('', show_all_publications, name='all'),
    path('<int:type_of_sort>', show_all_publications, name='sort'),

    path('json-search/', JsonSearchPublicationsView.as_view(), name='json_search'),

    path('create_author/', AuthorCreateView.as_view(), name='create-author'),
    path('authors/', show_all_authors, name='all_authors'),
    path('delete_author/<int:pk>', AuthorDeleteView.as_view(), name='author-delete'),
    path('author_info/<int:id>', get_author_info, name='author_info'),
    path('author_update/<int:pk>', AuthorUpdateView.as_view(), name='author-update'),

    path('create_publication/', create_publication, name='publication-create'),
    path('update_publication/<int:pk>', update_publication, name='publication-update'),
    path('delete_publication/<int:pk>', PublicationDeleteView.as_view(), name='publication-delete'),
    path('publication_info/<int:id>', get_publication_info, name='info'),

]
