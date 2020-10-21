from django import forms
from .models import Publication, Author


class PublicationFilter(forms.Form):
    min_year = forms.IntegerField(label='c', required=False,)
    max_year = forms.IntegerField(label='по', required=False)
    rank_options = (
        ('рядовой', 'рядовой'),
        ('лейтенант', 'лейтенант'),
        ('старший лейтенант', 'старший лейтенант'),
        ('капитан', 'капитан'),
        ('майор', 'майор'),
        ('подполковник', 'подполковник'),
        ('полковник', 'полковник'),
    )
    publication_options = (
        ('Статья', 'Статья'),
        ('Тезис', 'Тезис'),
    )
    rank = forms.MultipleChoiceField(choices=rank_options, required=False, label='',
                                     widget=forms.CheckboxSelectMultiple)
    type_of_publication = forms.MultipleChoiceField(choices=publication_options, required=False,
                                                    label='тип публикации', widget=forms.CheckboxSelectMultiple)


class SearchPublications(forms.Form):
    search = forms.CharField(max_length=255, label='', required=False)


class PublicationCreateForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(Author.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Publication
        fields = '__all__'
        exclude = ['authors']
