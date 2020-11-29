# import pytest
#
# from publications_table.models import Publication
#
#
# @pytest.fixture()
# def create_one_publication():
#     record = Publication.objects.create(
#         authors='Joe Mak',
#         title='TestTitle',
#         type_of_publication='testtype',
#         edition='testedition',
#         published_year=1921,
#         range='1-23',
#         uk_number=123456789,
#     )
#     return record
#
#
# @pytest.fixture()
# def a_few_publications():
#     return (
#         Publication(
#             authors='Joe Mak',
#             title='TestTitle',
#             type_of_publication='testtype',
#             edition='testedition',
#             published_year=1921,
#             range='1-23',
#             uk_number=123456789
#         ),
#         Publication(
#             authors='Joh Loek',
#             title='Somegoodtitle',
#             type_of_publication='sometype',
#             edition='someedition',
#             published_year=1922,
#             range='9-87',
#             uk_number=987654321
#         ),
#     )
#
#
#
# @pytest.fixture
# def db_with_2_publications(a_few_publications):
#     for publication in a_few_publications:
#         Publication.objects.create()
