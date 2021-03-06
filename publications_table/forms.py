""" Этот модуль содержит django формы """
from django import forms

from .models import Publication, Author, Type


class PublicationFilter(forms.Form):
    """Форма фильтра публикаций."""
    def __init__(self, *args, **kwargs):
        types_options = kwargs.pop('types_options')
        super(PublicationFilter, self).__init__(*args, **kwargs)
        self.fields['type_of_publication'].choices = types_options

    min_year = forms.IntegerField(label='c', required=False, )
    max_year = forms.IntegerField(label='по', required=False)
    type_of_publication = forms.MultipleChoiceField(
        choices=(), required=False, label='тип публикации', widget=forms.CheckboxSelectMultiple)


class SearchPublications(forms.Form):
    """Форма поиска публикаций."""
    search = forms.CharField(max_length=255, label='', required=False)


class PublicationCreateForm(forms.ModelForm):
    """ Форма создания публикации."""
    def __init__(self, *args, **kwargs):
        types_options = kwargs.pop('types_options')
        super(PublicationCreateForm, self).__init__(*args, **kwargs)
        self.fields['type_of_publication'].choices = types_options

    def save(self, commit=True):
        super_form = super(PublicationCreateForm, self).save(commit=commit)
        for i in range(len(self.cleaned_data['authors'])):
            Publication.objects.get(title=self.cleaned_data['title']) \
                .authors.add(self.cleaned_data['authors'][i])
        super_form.save()
        if self.cleaned_data['type_of_publication'] != '':
            type_of_publication = list(Type.objects.all().filter(
                type_of_publication=self.cleaned_data['type_of_publication']))[0]
            Type.objects.get(
                type_of_publication=self.cleaned_data['type_of_publication']).publication_set.add(
                Publication.objects.get(title=self.cleaned_data['title']), bulk=False)
            Publication.objects.get(
                title=self.cleaned_data['title']).type_of_publication = type_of_publication
            Publication.objects.get(title=self.cleaned_data['title']).save()

    authors = forms.ModelMultipleChoiceField(
        Author.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    type_of_publication = forms.ChoiceField(choices=(), required=False)

    class Meta:
        model = Publication
        fields = '__all__'
        exclude = ['authors', 'type_of_publication']


class ExportTableForm(forms.Form):
    """Форма экспорта таблицы."""
    file_name = forms.CharField(max_length=255, label='', required=False)
    select = forms.ModelMultipleChoiceField(
        Publication.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)


class PublicationUpdateForm(forms.ModelForm):
    """ Форма редактирования публикации."""
    def __init__(self, *args, **kwargs):
        types_options = kwargs.pop('types_options')
        super(PublicationUpdateForm, self).__init__(*args, **kwargs)
        publication = Publication.objects.get(title=self.initial['title'])
        self.fields["authors"].initial = (
            Author.objects.all().filter(authors=publication.id)
        )
        self.fields['type_of_publication'].initial = Publication.objects.get(
            title=self.initial['title']).type_of_publication
        self.fields['type_of_publication'].choices = types_options

    def save(self, commit=True):
        super_form = super(PublicationUpdateForm, self).save(commit=commit)
        Publication.objects.get(title=self.cleaned_data['title']).authors.clear()
        for i in range(len(self.cleaned_data['authors'])):
            Publication.objects.get(title=self.cleaned_data['title']) \
                .authors.add(self.cleaned_data['authors'][i])
        super_form.save()

    authors = forms.ModelMultipleChoiceField(
        Author.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    type_of_publication = forms.ChoiceField(choices=(), required=False)

    class Meta:
        model = Publication
        fields = '__all__'
        exclude = ['authors', 'type_of_publication']


class AuthorCreateForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = '__all__'


class TypeCreateForm(forms.ModelForm):

    class Meta:
        model = Type
        fields = '__all__'
