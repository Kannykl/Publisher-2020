from django.urls import path
from .views import show_all_publications


urlpatterns = [
    path('all_publications/', show_all_publications, name='all'),
]
