from django.contrib.auth.models import User
from django.urls import reverse
from exam import fixture

from ..utils import PyCoinsTestCase


class UserDetailApiTests(PyCoinsTestCase):
    @fixture
    def url(self):
        return reverse('api:user-detail', kwargs={'pk': self.user.pk})

    def test_user_detail_api__get__no_auth(self):
        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_user_detail_api__get__no_staff(self):
        self.login_as_user(self.api_client)
        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_user_detail_api__get__auth_staff(self):
        self.login_as_staff(self.api_client)

        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json(), {
            'email': 'big_trouble@little_china.com',
            'first_name': '',
            'id': 'http://testserver/api/v0.1/users/{}/'.format(self.user.pk),
            'last_name': '',
            'username': 'jack_burton'
        })

    def test_user_detail_api__put(self):
        self.login_as_staff(self.api_client)

        response = self.api_client.put(self.url, {
            'email': 'big_trouble@littlechina.com',
            'first_name': 'Jack',
            'last_name': 'Burton',
            'id': self.user.pk,
            'username': 'jack_burton'
        }, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['first_name'], 'Jack')

    def test_user_detail_api__delete(self):
        self.login_as_staff(self.api_client)

        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, 200)

        response = self.api_client.delete(self.url)
        self.assertEqual(response.status_code, 204)

        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, 404)


class UserListApiTests(PyCoinsTestCase):
    @fixture
    def url(self):
        return reverse('api:user-list')

    def assertUserListEquals(self, user_list_json, user_list_db):
        return self.assertEqual(
            {user['username'] for user in user_list_json},
            {user.username for user in user_list_db}
        )

    def test_user_list_api__get__no_auth(self):
        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_user_list_api__get__as_user(self):
        self.login_as_user(self.api_client)
        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_user_list_api__get__as_staff(self):
        self.user
        self.staff

        self.login_as_staff(self.api_client)

        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertUserListEquals(response.json(), [self.user, self.staff])

    def test_user_list_api__post(self):
        self.login_as_staff(self.api_client)

        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

        response = self.api_client.post(self.url, {
            'email': 'escapefrom@newyork.com',
            'first_name': 'Snake',
            'last_name': 'Plissken',
            'username': 'snake',
            'password': 'CallMeSnake',
        }, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.get(username='snake').password.startswith('md5$'))

        response = self.api_client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
