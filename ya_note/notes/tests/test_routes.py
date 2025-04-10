from http import HTTPStatus

from django.contrib.auth import get_user_model

from .constants import (
    BaseTestCase,
    NOTES_ADD_URL,
    NOTES_SUCCESS_URL,
    USER_LOGIN,
    NOTES_EDIT_URL,
    HOME_URL,
    USER_LOGOUT,
    USER_SIGNUP,
    NOTES_DELETE_URL,
    NOTES_DETAIL_URL,
    NOTES_LIST_URL
)

User = get_user_model()


class TestRoutes(BaseTestCase):
    def tests_one(self):
        case = [
            (self.client, HOME_URL, HTTPStatus.OK),
            (self.client, USER_LOGIN, HTTPStatus.OK),
            (self.client, USER_LOGOUT, HTTPStatus.OK),
            (self.client, USER_SIGNUP, HTTPStatus.OK),

            (self.author_client, NOTES_LIST_URL, HTTPStatus.OK),
            (self.author_client, NOTES_ADD_URL, HTTPStatus.OK),
            (self.author_client, NOTES_SUCCESS_URL, HTTPStatus.OK),

            (self.author_client, NOTES_DETAIL_URL, HTTPStatus.OK),
            (self.author_client, NOTES_EDIT_URL, HTTPStatus.OK),
            (self.author_client, NOTES_DELETE_URL, HTTPStatus.OK),

            (self.reader_client, NOTES_DETAIL_URL, HTTPStatus.NOT_FOUND),
            (self.reader_client, NOTES_EDIT_URL, HTTPStatus.NOT_FOUND),
            (self.reader_client, NOTES_DELETE_URL, HTTPStatus.NOT_FOUND)
        ]
        for client, url, status_code in case:
            with self.subTest(url=url):
                response = client.get(url)
                self.assertEqual(response.status_code, status_code)

    def test_redirects(self):
        urls = (
            NOTES_DETAIL_URL,
            NOTES_EDIT_URL,
            NOTES_DELETE_URL,
            NOTES_ADD_URL,
            NOTES_SUCCESS_URL,
            NOTES_LIST_URL
        )
        for name in urls:
            with self.subTest(name=name):
                expected_url = f'{USER_LOGIN}?next={name}'
                response = self.client.get(name)
                self.assertRedirects(response, expected_url)
