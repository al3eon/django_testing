from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News


TEST_COMMENTS_COUNT = 10
COMMENT_TEXT = 'Текст комментария'
UPDATE_COMMENT_TEXT = 'Текст измененного комментария'


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


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
    return Comment.objects.create(
        text=COMMENT_TEXT,
        author_id=author.id,
        news=news
    )


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
    return {'text': COMMENT_TEXT}


@pytest.fixture
def form_edit_data():
    return {'text': UPDATE_COMMENT_TEXT}


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


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def news_detail_url(news):
    return reverse('news:detail', args=[news.id])


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def logout_url():
    return reverse('users:logout')


@pytest.fixture
def signup_url():
    return reverse('users:signup')
