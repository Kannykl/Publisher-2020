from mixer.backend.django import mixer
import pytest


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
        publication1 = mixer.blend('publications_table.Publication', title='Статья1')
        ordering = publication1._meta.ordering
        assert ordering[0] == '-published_year'

    def test_ordering_authors(self):
        author = mixer.blend('publications_table.Author', name='Иван', surname='Смирнов', patronymic='Георгиевич')
        ordering = author._meta.ordering
        assert ordering[0] == 'surname'
