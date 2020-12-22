from django.urls import reverse, resolve


class TestUrls:

    def test_start_page_url(self):
        path = reverse('all')
        assert resolve(path).view_name == 'all'

    def test_sort_urls(self):
        for type_of_sort in range(0, 7):
            path = reverse('sort', kwargs={'type_of_sort': f'{type_of_sort}'})
            assert resolve(path).view_name == 'sort'

    def test_create_author_url(self):
        path = reverse('create-author')
        assert resolve(path).view_name == 'create-author'

    def test_publication_create_url(self):
        path = reverse('publication-create')
        assert resolve(path).view_name == 'publication-create'

    def test_publication_update_urls(self):
        path = reverse('publication-update', kwargs={'pk': 1})
        assert resolve(path).view_name == 'publication-update'

    def test_delete_publication_urls(self):
        path = reverse('publication-delete', kwargs={'pk': 1})
        assert resolve(path).view_name == 'publication-delete'

    def test_info_urls(self):
        path = reverse('info', kwargs={'id': 1})
        assert resolve(path).view_name == 'info'

    def test_json_search_url(self):
        path = reverse('json_search')
        assert resolve(path).view_name == 'json_search'
