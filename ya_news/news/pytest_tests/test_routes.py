from http import HTTPStatus
import pytest

from django.urls import reverse

from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'name, args',
    [
        ('news:home', None),
        ('news:detail', pytest.lazy_fixture('slug_for_news')),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
    ]
)
@pytest.mark.django_db
def test_pages_availability(client, name, args):
    # Адрес страницы получаем через reverse():
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    [
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ],
)
@pytest.mark.parametrize(
    'name',
    (
        'news:edit',
        'news:delete'
    ),
)
def test_availability_for_comment_edit_and_delete(
        parametrized_client, expected_status, comment, name
):
    url = reverse(name, args=[comment.id])
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name',
    (
        'news:edit',
        'news:delete',
    ),
)
def test_redirects(client, name, comment):
    loging_url = reverse('users:login')
    url = reverse(name, args=[comment.id])
    expected_url = f'{loging_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
