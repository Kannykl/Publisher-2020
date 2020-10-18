from django.urls import path
from .views import (
    show_all_publications,
    PublicationCreateView,
    PublicationUpdateView,
    PublicationDeleteView,
)

urlpatterns = [
    path('all_publications/', show_all_publications, name='all'),
    path('all_publications/<int:type_of_sort>', show_all_publications, name='sort'),
    path('create_publication/', PublicationCreateView.as_view(), name='publication-create'),
    path('update_publication/<int:pk>', PublicationUpdateView.as_view(), name='publication-update'),
    path('delete_publication/<int:pk>', PublicationDeleteView.as_view(), name='publication-delete'),
]
