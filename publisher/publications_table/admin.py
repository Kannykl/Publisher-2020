from django.contrib import admin
from .models import Publication, Author, Table

admin.site.register(Publication)
admin.site.register(Author)
admin.site.register(Table)
