from django.test import TestCase
from django.contrib.auth import  get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREAT_USER_URL = reverse('user:creat')

def creat_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
    def test_create_user_success(self):
        payload = {
            'email': 'test@exapmle.com',
            'password': 'testpass123',
            'name': 'Test name',
        }
        res = self.client.post(CREAT_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().object.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
    def test_user_with_email_exists_error(self):
        payload = {
                'email': 'test@exapmle.com',
                'password': 'testpass123',
                'name': 'Test name',
            }
        creat_user(**payload)

        res = self.client.post(CREAT_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test name',
        }
        res = self.client.post(CREAT_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertEqual(user_exist)

