from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import resolve, reverse
from ..models import Board, Topic, Post
from ..views import PostListView
from django.contrib.auth.models import User


class TopicPostsTest(TestCase):
    def setUp(self):
        board = Board.objects.create(name='TestName', description='Test description.')
        user = User.objects.create(username='testname', email='email@example.com', password='asdqwe123')
        topic = Topic.objects.create(subject='Hello, wordl!', board=board, starter=user)
        Post.objects.create(message='Lorem sdfsaf asgsadg', topic=topic, created_by=user)
        url = reverse('topic_posts', kwargs={'pk': board.pk, 'topic_pk': topic.pk})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_func(self):
        view = resolve('/boards/1/topics/1/')
        self.assertEquals(view.func.view_class, PostListView)