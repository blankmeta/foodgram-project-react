import pytest
from rest_framework import status


class TestUsers:
    USER_PASSWORD = '1234567'

    @pytest.mark.django_db(transaction=True)
    def test_register_user(self, client):
        """Пользователь может зарегистрироваться."""
        data = {
            'username': 'test_username',
            'password': 'test_password',
            'email': 'test_email@gmail.com',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name'
        }
        response = client.post('/api/users/', data=data)

        assert response.status_code == status.HTTP_201_CREATED, (
            'Пользователь должен иметь возможность создать аккаунт'
        )

    def test_get_users(self, user_client):
        """Аутентифицированный пользователь может получить список юзеров."""
        response = user_client.get('/api/users/', )
        test_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(test_data) == 4

    def test_change_password(self, user_client):
        """Аутентифицированный пользователь может поменять свой пароль."""
        data = {
            'new_password': 'aboba123',
            'current_password': self.USER_PASSWORD
        }
        response = user_client.post('/api/users/set_password/', data=data)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_subscribe(self, user_client, user2):
        """Пользователь может подписаться на другого пользователя."""
        response = user_client.post(f'/api/users/1/subscribe/')

        assert response.status_code == status.HTTP_201_CREATED
