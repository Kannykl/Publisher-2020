import pytest
from django.urls import reverse
from django.test import RequestFactory
from django.test import TestCase
from mixer.backend.django import mixer
from publications_table.models import Publication


@pytest.mark.django_db
class TestViews(TestCase):

    def test_delete_publication(self):
        publication = mixer.blend('publications_table.Publication', title='Статья1', published_year='2020',
                                  type_of_publication='Тезис', edition='издание', range='1-2', uk_number='123')
        assert Publication.objects.count() == 1

        response = self.client.post(reverse('publication-delete', kwargs={'pk': publication.pk}))
        assert response.status_code == 302
        assert '/publisher/' in response.url
        assert Publication.objects.count() == 0
