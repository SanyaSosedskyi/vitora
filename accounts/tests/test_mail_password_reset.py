from django.test import TestCase
from django.core import mail
from django.urls import reverse
from django.contrib.auth.models import User


class PasswordResetMailTests(TestCase):
    def setUp(self):
        User.objects.create(username='john', email='john@example.com', password='123asd123')
        self.response = self.client.post(reverse('password_reset'), {'email': 'john@example.com'})
        self.email = mail.outbox[0]

    def test_email_subject(self):
        self.assertEquals('[RockLab] Please reset your password', self.email.subject)

    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        })
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn('john', self.email.body)
        self.assertIn('john@example.com', self.email.body)

    def test_email_to(self):
        self.assertEqual(['john@example.com', ], self.email.to)
