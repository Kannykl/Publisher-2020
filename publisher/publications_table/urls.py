from django.urls import path
from .views import (
    show_all_publications,
    PublicationUpdateView,
    PublicationDeleteView,
    JsonSearchPublicationsView,
    create_publication,
    AuthorCreateView,
)

urlpatterns = [
    path('all_publications/', show_all_publications, name='all'),
    path('all_publications/<int:type_of_sort>', show_all_publications, name='sort'),

    path('json-search/', JsonSearchPublicationsView.as_view(), name='json_search'),

    path('create_author/', AuthorCreateView.as_view(), name='create-author'),
    path('create_publication/', create_publication, name='publication-create'),

    path('update_publication/<int:pk>', PublicationUpdateView.as_view(), name='publication-update'),
    path('delete_publication/<int:pk>', PublicationDeleteView.as_view(), name='publication-delete'),
]
