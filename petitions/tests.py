from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Petition


class PetitionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')

    def test_create_and_vote(self):
        # user1 creates a petition
        self.client.login(username='user1', password='pass')
        resp = self.client.post('/petitions/create/', {'title': 'Add Inception', 'description': 'Please add it.'})
        self.assertEqual(resp.status_code, 302)
        petition = Petition.objects.first()
        self.assertIsNotNone(petition)
        self.assertEqual(petition.title, 'Add Inception')

        # user2 votes yes
        self.client.logout()
        self.client.login(username='user2', password='pass')
        resp = self.client.post(f'/petitions/{petition.id}/vote/', {'vote': 'yes'})
        self.assertEqual(resp.status_code, 302)
        petition.refresh_from_db()
        self.assertEqual(petition.yes_count(), 1)
        self.assertEqual(petition.no_count(), 0)

        # user1 changes vote to no
        self.client.logout()
        self.client.login(username='user1', password='pass')
        resp = self.client.post(f'/petitions/{petition.id}/vote/', {'vote': 'no'})
        petition.refresh_from_db()
        self.assertEqual(petition.yes_count(), 1)
        self.assertEqual(petition.no_count(), 1)
