from django.urls import path
from .views import (
    show_all_publications,
    PublicationCreateView
)

urlpatterns = [
    path('all_publications/', show_all_publications, name='all'),
    path('create_publication/', PublicationCreateView.as_view(), name='publication-create'),
]
