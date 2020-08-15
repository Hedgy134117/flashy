import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from cards.models import Set, Card
from cards.serializers import SetSerializer
from django.contrib.auth.models import User

client = Client()

class GetSetListTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testUser', password='test')
        Set.objects.create(name='Test Set 1', owner=user)
        Set.objects.create(name='Test Set 2', owner=user)
        Set.objects.create(name='Test Set 3', owner=user)
        Set.objects.create(name='Test Set 4', owner=user)
    
    def test_get_all_sets(self):
        response = client.get(reverse('set-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'GET returns no errors')

class PostSetListTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testUser')
        user.set_password('test')
        user.save()

        self.url = reverse('set-list')

        self.validPost = json.dumps({
            'name': 'Test Set 1'
        })

        self.invalidNoName = json.dumps({
            'name': ''
        })

        self.contentType = 'application/json'
    
    def test_post_unauthorized(self):
        response = client.post(self.url, self.validPost, self.contentType)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'POST without auth returns unauthorized')

    def test_post_invalid_data(self):
        client.login(username='testUser', password='test')
        response = client.post(self.url, self.invalidNoName, self.contentType)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'POST with invalid data returns bad request')
        client.logout()

    def test_post_valid_data(self):
        client.login(username='testUser', password='test')
        response = client.post(self.url, self.validPost, self.contentType)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'POST with valid data and auth returns created')
        client.logout()

class SetDetail(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testUser')
        user.set_password('test')
        user.save()

        self.testSet = Set.objects.create(name='Test Set 1', owner=user)
        self.validPost = json.dumps({
            'front': 'Test Card Front',
            'back': 'Test Card Back'
        })
        self.validPut = json.dumps({
            'name': 'Test Set 1 after PUT'
        })
        self.invalidPost = json.dumps({
            'front': 'Test Card Front with no back'
        })

        self.url = reverse('set-detail', kwargs={'pk': self.testSet.pk})
        self.contentType = 'application/json'
    
    def test_get_set_detail(self):
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'GET with id returns ok')
    
    def test_post_put_detail_unauthorized(self):
        response = client.post(self.url, self.validPost, self.contentType)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'POST without auth returns unauthorized')
        response = client.put(self.url, self.validPut, self.contentType)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'PUT without auth returns unauthorized')
    
    def test_post_put_detail_invalid(self):
        client.login(username='testUser', password='test')
        response = client.post(self.url, self.invalidPost, self.contentType)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'POST with invalid data returns bad request')
        # No PUT because there can't be an invalid PUT request
        client.logout()
    
    def test_post_put_detail_valid(self):
        client.login(username='testUser', password='test')
        response = client.post(self.url, self.validPost, self.contentType)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'POST with valid data returns created')
        response = client.put(self.url, self.validPut, self.contentType)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'PUT with valid data returns ok')
        client.logout()
    
    def test_delete_set_unauthorized(self):
        response = client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'DELETE unauthorized returns unauthorized')
    
    def test_delete_set_authorized(self):
        client.login(username='testUser', password='test')
        response = client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 'DELETE authorized returns no content (successful deletion)')
        client.logout()
    
class CardDetail(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testUser')
        user.set_password('test')
        user.save()

        testSet = Set.objects.create(name='Test Set for cards', owner=user)
        self.testCard = Card.objects.create(group=testSet, front='Card 1 Front', back='Card 1 Back')
        self.validPut = json.dumps({
            'front': 'Edited card front',
            'back': self.testCard.back
        })

        self.url = reverse('card-detail', kwargs={'pk': self.testCard.pk})
        self.contentType = 'application/json'
    
    def test_get_card(self):
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'GETting a card returns no errors')
    
    def test_put_card_unauthorized(self):
        response = client.put(self.url, self.validPut, self.contentType)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'PUT unauthorized returns unauthorized')
    
    def test_put_card_authorized(self):
        client.login(username='testUser', password='test')
        response = client.put(self.url, self.validPut, self.contentType)
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'PUT authorized returns ok')
        client.logout()
    
    def test_delete_card_unauthorized(self):
        response = client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'DELETE unauthorized returns unauthorized')
    
    def test_delete_card_authorized(self):
        client.login(username='testUser', password='test')
        response = client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 'DELETE authorized returns no content (successful delete)')
        client.logout()