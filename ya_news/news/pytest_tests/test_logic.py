from http import HTTPStatus
import pytest

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

from .test_constants import CommentText
from pytest_django.asserts import assertFormError, assertRedirects


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
        detail_url, form_create_data, client
):
    client.post(detail_url, data=form_create_data)
    comment_count = Comment.objects.count()
    assert comment_count == 0


@pytest.mark.django_db
def test_user_can_create_comment(
        detail_url, form_create_data, news, author, author_client
):
    responses = author_client.post(detail_url, data=form_create_data)
    assertRedirects(responses, f'{detail_url}#comments')
    comment_count = Comment.objects.count()
    assert comment_count == 1
    comment = Comment.objects.get()
    assert comment.text == CommentText.COMMENT_TEXT
    assert comment.news == news
    assert comment.author == author


@pytest.mark.django_db
def test_user_cant_use_bad_words(author_client, detail_url):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(detail_url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comment_count = Comment.objects.count()
    assert comment_count == 0


@pytest.mark.django_db
def test_author_can_delete_comment(author_client, delete_url, comment_url):
    responses = author_client.delete(delete_url)
    assertRedirects(responses, comment_url)
    comment_count = Comment.objects.count()
    assert comment_count == 0


@pytest.mark.django_db
def test_author_cant_delete_comment(
        not_author_client, delete_url, comment_url
):
    responses = not_author_client.delete(delete_url)
    assert responses.status_code == HTTPStatus.NOT_FOUND
    comment_count = Comment.objects.count()
    assert comment_count == 1


@pytest.mark.django_db
def test_author_can_edit_comment(
        author_client, edit_url, form_edit_data, comment_url, comment
):
    responses = author_client.post(edit_url, data=form_edit_data)
    assertRedirects(responses, comment_url)
    comment.refresh_from_db()
    assert comment.text == CommentText.UPDATE_COMMENT_TEXT


@pytest.mark.django_db
def test_author_cant_edit_comment(
        not_author_client, edit_url, form_edit_data, comment_url, comment
):
    responses = not_author_client.post(edit_url, data=form_edit_data)
    assert responses.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == CommentText.COMMENT_TEXT
