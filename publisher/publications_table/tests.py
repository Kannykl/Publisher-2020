from django.test import TestCase
import pytest
from .models import Publication

# @pytest.mark.django_db
# def test_create_publication(create_record):
#
#     """Test create_record должен повлиять на publication.objects.count()"""
#     record = create_record
#


def test_publications_equals():
    assert 1 == 1
