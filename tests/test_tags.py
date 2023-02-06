from rest_framework import status

from tests.fixtures.fixture_data import TAGS_COUNT


class TestTags:
    def test_get_tags(self, user_client):
        """Аутентифицированный пользователь может получить список тэгов."""

        response = user_client.get('/api/tags/')

        assert response.status_code == status.HTTP_200_OK

    def test_tags_count(self, user_client, create_three_tags):
        """Пользователь получает строгое количество тэгов, которые есть в базе."""

        response = user_client.get('/api/tags/')
        test_data = response.json()
        print(test_data)
        print(test_data)
        print(test_data)

        assert len(test_data) == TAGS_COUNT
