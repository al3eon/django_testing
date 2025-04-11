from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects

HOME_URL = pytest.lazy_fixture('home_url')
NEWS_DETAIL_URL = pytest.lazy_fixture('news_detail_url')
LOGIN_URL = pytest.lazy_fixture('login_url')
LOGOUT_URL = pytest.lazy_fixture('logout_url')
SIGNUP_URL = pytest.lazy_fixture('signup_url')
NEWS_EDIT_URL = pytest.lazy_fixture('edit_url')
NEWS_DELETE_URL = pytest.lazy_fixture('delete_url')


@pytest.mark.parametrize(
    'url, client_fixture, expected_status',
    [
        (HOME_URL, 'client', HTTPStatus.OK),
        (NEWS_DETAIL_URL, 'client', HTTPStatus.OK),
        (LOGIN_URL, 'client', HTTPStatus.OK),
        (LOGOUT_URL, 'client', HTTPStatus.OK),
        (SIGNUP_URL, 'client', HTTPStatus.OK),
        (NEWS_EDIT_URL, 'author_client', HTTPStatus.OK),
        (NEWS_DELETE_URL, 'author_client', HTTPStatus.OK),
        (NEWS_EDIT_URL, 'not_author_client', HTTPStatus.NOT_FOUND),
        (NEWS_DELETE_URL, 'not_author_client', HTTPStatus.NOT_FOUND),
    ]
)
def test_pages_availability(request, url, client_fixture, expected_status):
    client = request.getfixturevalue(client_fixture)
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name',
    (
        NEWS_EDIT_URL,
        NEWS_DELETE_URL,
    ),
)
def test_redirects(client, name, comment):
    loging_url = reverse('users:login')
    expected_url = f'{loging_url}?next={name}'
    response = client.get(name)
    assertRedirects(response, expected_url)
