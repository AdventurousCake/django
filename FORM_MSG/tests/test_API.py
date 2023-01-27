from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from FORM_MSG.models import Message, Like
from core.models import User


class UpdateLikeViewAPITestCase(APITestCase):
    pass


class UpdateLikeViewAPITest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser', password='testpass')
        cls.msg = Message.objects.create(text='Test message', author=cls.user)
        # cls.client.force_authenticate(cls.user)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        # self.user = User.objects.create_user(username='testuser', password='testpass')
        # self.msg = Message.objects.create(text='Test message', author=self.user)
        self.client.force_authenticate(self.user)
        pass

    def test_post_like(self):
        response = self.client.post(reverse('form_msg:like', kwargs={'pk': self.msg.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(Like.objects.first().message, self.msg)

    def test_post_like_MIX_Router(self):
        # for routers form_msg:like_router-detail
        response = self.client.patch(reverse('form_msg:like_router-detail', kwargs={'pk': self.msg.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Like.objects.count(), 1)
        # self.assertEqual(Like.objects.first().message, self.msg)

    # def test_post_like_again(self):
    #     Like.objects.create(user=self.user, message=self.msg)