import pytest
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.test import RequestFactory
from django.test import TestCase
from mixer.backend.django import mixer
from publications_table.models import Publication, Author, Table
from publications_table.views import (
    show_all_publications,
    AuthorCreateView,
    create_publication,
    update_publication,
    sort,
    filter_publications,
    JsonSearchPublicationsView,
    get_publication_info,
    export_table,
)
import json


@pytest.mark.django_db
class TestViews(TestCase):

    def test_show_all_publications(self):
        """ Переход на главную страницу"""
        path = reverse('all')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = show_all_publications(request)
        assert response.status_code == 200

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
        assert Author.objects.all()[0].name == 'TestName'
        assert Author.objects.count() == 1

    def test_success_delete_publication(self):
        """Успешное удаление публикации"""
        publication = mixer.blend('publications_table.Publication', title='Статья1', published_year=2020,
                                  type_of_publication='Тезис', edition='издание', range='1-2', uk_number=123)
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
        publication = mixer.blend('publications_table.Publication', title='СтатьяДоИзменения', published_year=2020,
                                  type_of_publication='Тезис', edition='издание', range='1-2', uk_number=123)
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

    def test_sort(self):
        """Проверка сортировки публикаций"""
        publication1 = mixer.blend('publications_table.Publication', title='Статья1', published_year=2020,
                                   type_of_publication='Тезис', edition='издание2', range='1-2', uk_number=987)
        publication2 = mixer.blend('publications_table.Publication', title='Статья2', published_year=2019,
                                   type_of_publication='Статья', edition='издание1', range='1-23', uk_number=123)
        ordered_publications = sort(1)
        assert list(ordered_publications) == [publication1, publication2]
        ordered_publications = sort(2)
        assert list(ordered_publications) == [publication2, publication1]
        ordered_publications = sort(3)
        assert list(ordered_publications) == [publication1, publication2]
        ordered_publications = sort(4)
        assert list(ordered_publications) == [publication2, publication1]
        ordered_publications = sort(5)
        assert list(ordered_publications) == [publication1, publication2]
        ordered_publications = sort(6)
        assert list(ordered_publications) == [publication2, publication1]

    def test_filter_publications(self):
        """Проверка фильтрации публикаций"""
        publication1 = mixer.blend('publications_table.Publication', title='Статья1', published_year=2020,
                                   type_of_publication='Тезис', edition='издание2', range='1-2', uk_number=1234)
        publication2 = mixer.blend('publications_table.Publication', title='Статья2', published_year=2019,
                                   type_of_publication='Статья', edition='издание1', range='1-23', uk_number=1235)
        publication3 = mixer.blend('publications_table.Publication', title='Статья3', published_year=2018,
                                   type_of_publication='Тезис', edition='издание1', range='1-23', uk_number=1236)
        publication4 = mixer.blend('publications_table.Publication', title='Статья4', published_year=2017,
                                   type_of_publication='Статья', edition='издание1', range='1-23', uk_number=1237)
        path = reverse('all')
        request = RequestFactory().get(path, data={
            'type_of_publication': 'Статья'
        })
        request.user = AnonymousUser()
        filtered_publications, _ = filter_publications(request, Publication.objects.all())

        assert list(filtered_publications) == [publication2, publication4]
        request = RequestFactory().get(path, data={
            'type_of_publication': 'Тезис'
        })
        filtered_publications, _ = filter_publications(request, Publication.objects.all())
        assert list(filtered_publications) == [publication1, publication3]

        request = RequestFactory().get(path, data={
            'min_year': 2017
        })
        filtered_publications, _ = filter_publications(request, Publication.objects.all())
        assert list(filtered_publications) == [publication1, publication2, publication3, publication4]

        request = RequestFactory().get(path, data={
            'min_year': 2018
        })
        filtered_publications, _ = filter_publications(request, Publication.objects.all())
        assert list(filtered_publications) == [publication1, publication2, publication3]

        request = RequestFactory().get(path, data={
            'max_year': 2018
        })
        filtered_publications, _ = filter_publications(request, Publication.objects.all())
        assert list(filtered_publications) == [publication3, publication4]

        request = RequestFactory().get(path, data={
            'min_year': 2018,
            'max_year': 2019
        })
        filtered_publications, _ = filter_publications(request, Publication.objects.all())
        assert list(filtered_publications) == [publication2, publication3]

    def test_search_publications(self):
        """Проверка поиска публикаций"""
        mixer.blend('publications_table.Author', name='TestName', surname='TestSurname',
                    patronymic='TestPatronymic', work_position='TestWorkPosition', military_rank='TestMilitaryRank')
        mixer.blend('publications_table.Publication',
                    title='Статья1', published_year=2020,
                    type_of_publication='Тезис', edition='издание1', range='1-2', uk_number=1234)
        mixer.blend('publications_table.Publication', title='Статья2', published_year=2019,
                    authors=Author.objects.get(name='TestName').id,
                    type_of_publication='Статья', edition='издание2', range='1-23', uk_number=1235)
        mixer.blend('publications_table.Publication', title='Статья3', published_year=2018,
                    type_of_publication='Тезис', edition='издание3', range='1-23', uk_number=1236)
        mixer.blend('publications_table.Publication', title='Статья4', published_year=2017,
                    type_of_publication='Статья', edition='издание4', range='1-23', uk_number=1237)

        path = reverse('json_search')

        request = RequestFactory().get(path, data={
            'search': 'Статья1'
        })
        response = JsonSearchPublicationsView.as_view()(request)
        json_response = json.loads(response.content)
        assert response.status_code == 200
        assert json_response['publications'][0]['title'] == 'Статья1'

        request = RequestFactory().get(path, data={
            'search': 'TestSurname'
        })
        response = JsonSearchPublicationsView.as_view()(request)
        json_response = json.loads(response.content)
        assert response.status_code == 200
        assert json_response['publications'][0]['title'] == 'Статья2'

        request = RequestFactory().get(path, data={
            'search': 'издание4'
        })
        response = JsonSearchPublicationsView.as_view()(request)
        json_response = json.loads(response.content)
        assert response.status_code == 200
        assert json_response['publications'][0]['title'] == 'Статья4'

        request = RequestFactory().get(path, data={
            'search': 1236
        })
        response = JsonSearchPublicationsView.as_view()(request)
        json_response = json.loads(response.content)
        assert response.status_code == 200
        assert json_response['publications'][0]['title'] == 'Статья3'

        request = RequestFactory().get(path, data={
            'search': 'Какой-то неправильный поиск'
        })
        response = JsonSearchPublicationsView.as_view()(request)
        json_response = json.loads(response.content)
        assert response.status_code == 200
        assert json_response['publications'] == []

    def test_publications_info(self):
        """Проверка работоспособности странички информации о публикации"""
        mixer.blend('publications_table.Author', name='TestName', surname='TestSurname',
                    patronymic='TestPatronymic', work_position='TestWorkPosition', military_rank='TestMilitaryRank')
        publication = mixer.blend('publications_table.Publication', title='Статья2', published_year=2019,
                                  authors=Author.objects.get(name='TestName').id,
                                  type_of_publication='Статья', edition='издание2', range='1-23', uk_number=1235)
        path = reverse('info', kwargs={'id': publication.id})
        request = RequestFactory().get(path)
        response = get_publication_info(request, id=publication.id)
        assert response.status_code == 200

    def test_export_table(self):
        """ Проверка работы экспорта таблицы"""
        mixer.blend('publications_table.Author', name='TestName', surname='TestSurname',
                    patronymic='TestPatronymic', work_position='TestWorkPosition', military_rank='TestMilitaryRank')
        publication = mixer.blend('publications_table.Publication', title='Статья2', published_year=2019,
                                  authors=Author.objects.get(name='TestName').id,
                                  type_of_publication='Статья', edition='издание2', range='1-23', uk_number=1235)

        path = reverse('all')
        request = RequestFactory().get(path, data={
            'file_name': '1234.xls'
        })
        export_table(Publication.objects.all(), request)
        assert Table.objects.count() == 1

    def test_fail_create_author_without_name(self):
        """ Неудачное создание автора, не хватает имени автора"""
        assert list(Author.objects.all()) == list(Author.objects.none())
        path = reverse('create-author')
        request = RequestFactory().post(path, data={
            'surname': 'TestSurname',
            'patronymic': 'TestPatronymic',
            'work_position': 'TestWorkPosition',
            'military_rank': 'TestMilitaryRank',
        })
        request.user = AnonymousUser()
        response = AuthorCreateView.as_view()(request)
        assert response.status_code == 200
        assert Author.objects.count() == 0

    def test_fail_create_publication_without_author(self):
        """ Неудачное создание публикации, без автора """
        assert list(Publication.objects.all()) == list(Publication.objects.none())

        path = reverse('publication-create')
        request = RequestFactory().get(path, data={
            'title': 'СтатьяПослеИзменения',
            'published_year': 2020,
            'type_of_publication': 'Тезис',
            'edition': 'издание',
            'range': '1-2',
            'uk_number': 2441,
        })
        response = create_publication(request)
        assert response.status_code == 200
        assert list(Publication.objects.all()) == list(Publication.objects.none())

    def test_fail_create_publication_with_wrong_type_of_publication(self):
        """ Неудачное создание публикации, с несуществующим типом публикации """
        assert list(Publication.objects.all()) == list(Publication.objects.none())

        mixer.blend('publications_table.Author', name='TestName', surname='TestSurname',
                    patronymic='TestPatronymic', work_position='TestWorkPosition', military_rank='TestMilitaryRank')
        path = reverse('publication-create')
        request = RequestFactory().post(path, data={
            'authors': Author.objects.get(name='TestName').id,
            'title': 'Статья1',
            'published_year': 2020,
            'type_of_publication': 'Несущестующий тип',
            'edition': 'издание',
            'range': '1-2',
            'uk_number': 2441
        })
        response = create_publication(request)
        assert response.status_code == 200
        assert list(Publication.objects.all()) == list(Publication.objects.none())

    def test_fail_delete_not_exist_publication(self):
        """ Неудачная попытка удаления несуществующей записи """
        assert list(Publication.objects.all()) == list(Publication.objects.none())
        assert Publication.objects.count() == 0

        response = self.client.post(reverse('publication-delete', kwargs={'pk': 1}))
        assert response.status_code == 404
        assert list(Publication.objects.all()) == list(Publication.objects.none())
        assert Publication.objects.count() == 0