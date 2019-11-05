from accounts.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from ..models import Board, Topic, Post
from ..views import reply_topic


class ReplyTopicTestCase(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        self.username = 'john'
        self.password = '123'
        self.user = User.objects.create(username=self.username, email='jo@yandex.ru')
        self.user.set_password(self.password)
        self.user.save()
        self.topic = Topic.objects.create(subject='Test_subject', board=self.board, starter=self.user)
        Post.objects.create(message='Another test message', topic=self.topic, created_by=self.user)
        self.url = reverse('reply_topic', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})


class SuccessfulReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'message':'test message'})

    def test_redirection(self):
        url = reverse('topic_posts', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})
        topic_post_url = f'{url}?page=1#2'
        self.assertRedirects(self.response, topic_post_url)

