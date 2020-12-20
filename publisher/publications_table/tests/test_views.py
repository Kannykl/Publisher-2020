import pytest
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.test import RequestFactory
from django.test import TestCase
from mixer.backend.django import mixer
from publications_table.models import Publication, Author
from publications_table.views import show_all_publications, AuthorCreateView, create_publication, update_publication


@pytest.mark.django_db
class TestViews(TestCase):

    def test_show_all_publications(self):
        """ Переход на главную страницу"""
        path = reverse('all')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = show_all_publications(request)
        assert response.status_code == 200

    def test_success_create_author(self):
        """Успешное создание автора"""
        assert list(Author.objects.all()) == list(Author.objects.none())
        path = reverse('create-author')
        request = RequestFactory().post(path, data={
            'name': 'TestName',
            'surname': 'TestSurname',
            'patronymic': 'TestPatronymic',
            'work_position': 'TestWorkPosition',
            'military_rank': 'TestMilitaryRank',
        })
        request.user = AnonymousUser()
        response = AuthorCreateView.as_view()(request)
        assert response.status_code == 302
        assert '/publisher/create_publication/' in response.url
        assert Author.objects.get(pk=1).name == 'TestName'
        assert Author.objects.count() == 1

    def test_success_create_publication(self):
        """Успешное создание публикации"""
        assert Publication.objects.count() == 0
        mixer.blend('publications_table.Author', name='TestName', surname='TestSurname',
                    patronymic='TestPatronymic', work_position='TestWorkPosition', military_rank='TestMilitaryRank')
        path = reverse('publication-create')
        request = RequestFactory().post(path, data={
            'authors': Author.objects.get(name='TestName').id,
            'title': 'Статья1',
            'published_year': 2020,
            'type_of_publication': 'Тезис',
            'edition': 'издание',
            'range': '1-2',
            'uk_number': 2441
        })
        request.user = AnonymousUser()
        response = create_publication(request)
        assert response.status_code == 302
        assert 'publisher/' in response.url
        assert Publication.objects.count() == 1
        assert Publication.objects.all()[0].title == 'Статья1'

    def test_success_delete_publication(self):
        """Успешное удаление публикации"""
        publication = mixer.blend('publications_table.Publication', title='Статья1', published_year='2020',
                                  type_of_publication='Тезис', edition='издание', range='1-2', uk_number='123')
        assert Publication.objects.count() == 1

        response = self.client.post(reverse('publication-delete', kwargs={'pk': publication.pk}))
        assert response.status_code == 302
        assert '/publisher/' in response.url
        assert Publication.objects.count() == 0

    def test_success_update_publication(self):
        """Успешное редактирование публикации"""
        assert Publication.objects.count() == 0
        mixer.blend('publications_table.Author', name='TestName', surname='TestSurname',
                    patronymic='TestPatronymic', work_position='TestWorkPosition', military_rank='TestMilitaryRank')
        publication = mixer.blend('publications_table.Publication', title='СтатьяДоИзменения', published_year='2020',
                                  type_of_publication='Тезис', edition='издание', range='1-2', uk_number='123')
        path = reverse('publication-update', kwargs={'pk': publication.id})
        request = RequestFactory().post(path, data={
            'authors': Author.objects.get(name='TestName').id,
            'title': 'СтатьяПослеИзменения',
            'published_year': 2020,
            'type_of_publication': 'Тезис',
            'edition': 'издание',
            'range': '1-2',
            'uk_number': 2441
        })
        request.user = AnonymousUser()
        response = update_publication(request, pk=publication.id)
        assert response.status_code == 302
        assert f'/publisher/publication_info/{publication.id}' in response.url
        assert Publication.objects.count() == 1
        assert Publication.objects.all()[0].title == 'СтатьяПослеИзменения'
