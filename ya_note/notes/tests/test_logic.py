from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note

from .constants import (
    BaseTestCase,
    NOTES_ADD_URL,
    NOTES_DELETE_URL,
    NOTES_EDIT_URL,
    NOTES_SUCCESS_URL,
    USER_LOGIN,
)

User = get_user_model()


class TestCreateNote(BaseTestCase):
    def test_user_can_create_note(self):
        Note.objects.all().delete()
        response = self.author_client.post(NOTES_ADD_URL, self.form_data)
        self.assertRedirects(response, NOTES_SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get()
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        count_notes = Note.objects.count()
        response = self.client.post(NOTES_ADD_URL, self.form_data)
        expected_url = f'{USER_LOGIN}?next={NOTES_ADD_URL}'
        self.assertRedirects(response, expected_url)
        self.assertEqual(Note.objects.count(), count_notes)

    def test_empty_slug(self):
        Note.objects.all().delete()
        url = reverse('notes:add')
        self.form_data.pop('slug')
        self.client.force_login(self.author)
        response = self.client.post(url, self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)

    def test_not_unique_slug(self):
        count_notes = Note.objects.count()
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(NOTES_ADD_URL, self.form_data)
        self.assertFormError(
            response,
            'form',
            'slug',
            errors=(self.note.slug + WARNING)
        )
        self.assertEqual(Note.objects.count(), count_notes)

    def test_author_can_edit_note(self):
        old_note = Note.objects.get(pk=self.note.pk)
        response = self.author_client.post(NOTES_EDIT_URL, self.form_data)
        self.assertRedirects(response, reverse('notes:success'))

        updated_note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(updated_note.title, self.form_data['title'])
        self.assertEqual(updated_note.text, self.form_data['text'])
        self.assertEqual(updated_note.slug, self.form_data['slug'])
        self.assertEqual(updated_note.author, old_note.author)

    def test_other_user_cant_edit_note(self):
        response = self.reader_client.post(NOTES_EDIT_URL, self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)
        self.assertEqual(self.note.author, note_from_db.author)

    def test_author_can_delete_note(self):
        count_notes = Note.objects.count()
        response = self.author_client.post(NOTES_DELETE_URL)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(Note.objects.count(), count_notes - 1)

    def test_other_user_cant_delete_note(self):
        count_notes = Note.objects.count()
        response = self.reader_client.post(NOTES_DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), count_notes)
