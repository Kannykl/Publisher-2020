from django import forms
from .models import Publication, Author


class PublicationFilter(forms.Form):
    min_year = forms.IntegerField(label='c', required=False,)
    max_year = forms.IntegerField(label='по', required=False)
    publication_options = (
        ('Статья', 'Статья'),
        ('Тезис', 'Тезис'),
    )
    type_of_publication = forms.MultipleChoiceField(choices=publication_options, required=False,
                                                    label='тип публикации', widget=forms.CheckboxSelectMultiple)


class SearchPublications(forms.Form):
    search = forms.CharField(max_length=255, label='', required=False)


class PublicationCreateForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(Author.objects.all(), widget=forms.CheckboxSelectMultiple)

    def save(self, commit=True):
        b = super(PublicationCreateForm, self).save(commit=commit)
        for i in range(len(self.cleaned_data['authors'])):
            Publication.objects.get(uk_number=self.cleaned_data['uk_number'])\
                .authors.add(self.cleaned_data['authors'][i])

        b.save()

    class Meta:
        model = Publication
        fields = '__all__'
        exclude = ['authors']


class ExportTableForm(forms.Form):
    file_name = forms.CharField(max_length=255, label='', required=False)
