from datetime import datetime, timedelta

import pytest

from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News

from .test_constants import CommentText


TEST_COMMENTS_COUNT = 10


@pytest.fixture
def slug_for_news():
    news = News.objects.create(title='Тест', text='Тестовый текст')
    return (news.id,)


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title='Тестовая новость',
        text='Содержание тестовой новости'
    )


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        text=CommentText.COMMENT_TEXT,
        author_id=author.id,
        news=news
    )
    return comment


@pytest.fixture
def create_news():
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)
    return all_news


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def form_create_data():
    return {'text': CommentText.COMMENT_TEXT}


@pytest.fixture
def form_edit_data():
    return {'text': CommentText.UPDATE_COMMENT_TEXT}


@pytest.fixture
def create_many_comments(news, author):
    now = timezone.now()
    for index in range(TEST_COMMENTS_COUNT):
        comment = Comment.objects.create(
            news=news, author_id=author.id, text=f'Text{index}'
        )
        comment.created = now + timedelta(days=index)
        comment.save()


@pytest.fixture
def comment_url(detail_url):
    return detail_url + '#comments'


@pytest.fixture
def delete_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def edit_url(comment):
    return reverse('news:edit', args=(comment.id,))
