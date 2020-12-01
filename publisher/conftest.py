import pytest
import django

django.setup()


@pytest.fixture
def test_author_name():
    return 'Ivan'


@pytest.fixture
def test_author_surname():
    return 'Smirnov'


@pytest.fixture
def test_author_patronymic():
    return 'Vladimirovich'


@pytest.fixture
def test_author_military_rank():
    return 'colonel'


@pytest.fixture
def test_author_work_position():
    return 'Teacher'


@pytest.fixture
def test_publication_title():
    return 'Science'


@pytest.fixture
def test_publication_title():
    return 'Science'
