from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.forms import NoteForm

from .constants import (
    BaseTestCase,
    NOTES_ADD_URL,
    NOTES_EDIT_URL,
    NOTES_LIST_URL
)

User = get_user_model()


class TestLogicNote(BaseTestCase):
    def test_notes_list_for_different_users(self):
        users_statuses = (
            (self.author_client, True),
            (self.reader_client, False),
        )
        for user, expected_status in users_statuses:
            with self.subTest(user=user, expected_status=expected_status):
                response = user.get(NOTES_LIST_URL)
                object_list = response.context['object_list']
                self.assertIs((self.note in object_list), expected_status)

    def test_pages_contains_form(self):
        urls = (
            NOTES_ADD_URL,
            NOTES_EDIT_URL
        )
        for name in urls:
            with self.subTest(name=name):
                response = self.author_client.get(name)
                self.assertIsInstance(
                    response.context.get('form'),
                    NoteForm
                )
