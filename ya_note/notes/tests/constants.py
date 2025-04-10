from django.test import TestCase

from django.urls import reverse

from django.test import Client

from django.contrib.auth import get_user_model

from notes.models import Note

User = get_user_model()

NOTE_SLUG = 'note-slug'

NOTES_LIST_URL = reverse('notes:list')
NOTES_ADD_URL = reverse('notes:add')
NOTES_EDIT_URL = reverse('notes:edit', args=[NOTE_SLUG])
NOTES_DELETE_URL = reverse('notes:delete', args=[NOTE_SLUG])

NOTES_SUCCESS = reverse('notes:success')

USER_LOGIN = reverse('users:login')
USER_LOGOUT = reverse('users:logout')


class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username='Автор')
        cls.reader = User.objects.create_user(username='Читатель')

        cls.author_client = Client()
        cls.reader_client = Client()

        cls.author_client.force_login(cls.author)
        cls.reader_client.force_login(cls.reader)

        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug='note-slug',
            author=cls.author,
        )
        cls.form_data = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'new-slug'
        }
