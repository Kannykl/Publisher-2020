from django import forms
from .models import Publication, Author, Type


class PublicationFilter(forms.Form):
    def __init__(self, *args, **kwargs):
        types_options = kwargs.pop('types_options')
        super(PublicationFilter, self).__init__(*args, **kwargs)
        self.fields['type_of_publication'].choices = types_options

    min_year = forms.IntegerField(label='c', required=False, )
    max_year = forms.IntegerField(label='по', required=False)
    type_of_publication = forms.MultipleChoiceField(choices=(), required=False,
                                                    label='тип публикации', widget=forms.CheckboxSelectMultiple)


class SearchPublications(forms.Form):
    search = forms.CharField(max_length=255, label='', required=False)


class PublicationCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        types_options = kwargs.pop('types_options')
        super(PublicationCreateForm, self).__init__(*args, **kwargs)
        self.fields['type_of_publication'].choices = types_options

    def save(self, commit=True):
        b = super(PublicationCreateForm, self).save(commit=commit)
        for i in range(len(self.cleaned_data['authors'])):
            Publication.objects.get(uk_number=self.cleaned_data['uk_number']) \
                .authors.add(self.cleaned_data['authors'][i])
        b.save()
        type_of_publication = list(Type.objects.all().filter(type_of_publication
                                                             =self.cleaned_data['type_of_publication']))[0]
        Type.objects.get(type_of_publication=self.cleaned_data['type_of_publication']).publication_set.add \
            (Publication.objects.get(uk_number=self.cleaned_data['uk_number']), bulk=False)
        Publication.objects.get(uk_number=self.cleaned_data['uk_number']).type_of_publication = type_of_publication

    authors = forms.ModelMultipleChoiceField(Author.objects.all(), widget=forms.CheckboxSelectMultiple)
    type_of_publication = forms.ChoiceField(choices=())

    class Meta:
        model = Publication
        fields = '__all__'
        exclude = ['authors', 'type_of_publication']


class ExportTableForm(forms.Form):
    file_name = forms.CharField(max_length=255, label='', required=False)


class PublicationUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        types_options = kwargs.pop('types_options')
        super(PublicationUpdateForm, self).__init__(*args, **kwargs)
        publication = Publication.objects.get(uk_number=self.initial['uk_number'])
        self.fields["authors"].initial = (
            Author.objects.all().filter(authors=publication.id)
        )
        self.fields['type_of_publication'].initial = Publication.objects.get(uk_number=self.initial['uk_number']).type_of_publication
        self.fields['type_of_publication'].choices = types_options

    def save(self, commit=True):
        b = super(PublicationUpdateForm, self).save(commit=commit)
        Publication.objects.get(uk_number=self.cleaned_data['uk_number']).authors.clear()
        for i in range(len(self.cleaned_data['authors'])):
            Publication.objects.get(uk_number=self.cleaned_data['uk_number']) \
                .authors.add(self.cleaned_data['authors'][i])
        type_of_publication = list(Type.objects.all().filter(type_of_publication
                                                             =self.cleaned_data['type_of_publication']))[0]
        Type.objects.get(type_of_publication=self.fields['type_of_publication'].initial).publication_set.remove(
            Publication.objects.get(uk_number=self.cleaned_data['uk_number'])
        )
        Type.objects.get(type_of_publication=self.cleaned_data['type_of_publication']).publication_set.add \
            (Publication.objects.get(uk_number=self.cleaned_data['uk_number']), bulk=False)
        Publication.objects.get(uk_number=self.cleaned_data['uk_number']).type_of_publication = type_of_publication
        b.save()

    authors = forms.ModelMultipleChoiceField(Author.objects.all(), widget=forms.CheckboxSelectMultiple, )
    type_of_publication = forms.ChoiceField(choices=())

    class Meta:
        model = Publication
        fields = '__all__'
        exclude = ['authors', 'type_of_publication']


class TypeDeleteForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = '__all__'
