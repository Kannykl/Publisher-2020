import pytest
import django
from publisher.publications_table.models import Publication

django.setup()


@pytest.mark.django_db
def test_create_publication():
    assert Publication.objects.count() == 0

