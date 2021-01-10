from mixer.backend.django import mixer
import pytest
from publications_table.views import Author, Publication


@pytest.mark.django_db
class TestModels:

    def test_author_str_method(self):
        author = mixer.blend('publications_table.Author', name='Иван', surname='Смирнов', patronymic='Георгиевич')
        assert author.__str__() == 'Смирнов И.Г.'

    def test_publication_str_method(self):
        publication = mixer.blend('publications_table.Publication', title='Статья1')
        assert publication.__str__() == 'Статья1'

    def test_publication_repr_method(self):
        publication = mixer.blend('publications_table.Publication', title='Статья1')
        assert publication.__repr__() == 'Статья1'

    def test_author_repr_method(self):
        author = mixer.blend('publications_table.Author', surname='Смирнов')
        assert author.__repr__() == 'Смирнов'

    def test_ordering_publications(self):
        publication1 = mixer.blend('publications_table.Publication', title='Статья1', published_year=2001)
        publication2 = mixer.blend('publications_table.Publication', title='Статья2', published_year=2020)
        assert tuple(Publication.objects.all()) == (publication2, publication1)
        ordering = publication1._meta.ordering
        assert ordering[0] == '-published_year'

    def test_ordering_authors(self):
        author1 = mixer.blend('publications_table.Author', name='Иван', surname='Абрамов', patronymic='Георгиевич')
        author2 = mixer.blend('publications_table.Author', name='Иван', surname='Васильев', patronymic='Георгиевич')
        ordering = author1._meta.ordering
        assert tuple(Author.objects.all()) == (author1, author2)
        assert ordering[0] == 'surname'
