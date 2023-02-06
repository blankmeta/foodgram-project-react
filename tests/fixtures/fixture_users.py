import pytest


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(username='TestUser', password='1234567', email='test@gmail.com')


@pytest.fixture
def user_client(user):
    from rest_framework.test import APIClient

    client = APIClient()

    token_response = client.post('/api/auth/token/login/', data={
        "email": user.email,
        "password": '1234567'
    })

    token = token_response.json()['auth_token']

    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    return client
