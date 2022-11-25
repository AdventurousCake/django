from django import forms
from django.test import TestCase, Client, override_settings
from django.core.cache import cache
from django.urls import reverse

from core.models import User

from FORM_MSG.models import Message


class MessageTestBase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # cls.user = User.objects.get(username='admin')
        cls.user = User.objects.create_user(username='user1')
        cls.user2 = User.objects.create_user(username='user2')
        cls.message = Message.objects.create(author=cls.user,
                                             name='Name',
                                             text='123')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        self.guest_client = Client()

        """Создаем клиент зарегистрированного пользователя."""
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.authorized_client2 = Client()
        self.authorized_client2.force_login(self.user2)
        cache.clear()


class MessageViewTest(MessageTestBase):
    # Проверка используемых шаблонов
    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары: имя шаблона:reverse(name)
        templates_page_names = {
            'form_msg/msg_list.html': reverse('form_msg:msg_list'),
            'form_msg/msg_BY_ID.html': reverse('form_msg:show_msg', kwargs={'pk': 1}),
            'form_msg/msg_send.html': reverse('form_msg:send_msg'),
            # 'form_msg/msg_send.html': reverse('form_msg:edit_msg'), # kwargs={'slug': 'test-slug'}
            'form_msg/signup.html': reverse('form_msg:signup'),
            'form_msg/USERPAGE.html': reverse('form_msg:users_details', kwargs={'pk': self.user.id}),
        }

        # проверяем что при обращении к name вызывается соотв. шаблон
        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    # todo форма
    # def test_home_page_show_correct_context(self):
    #     """Шаблон home сформирован с правильным контекстом."""
    #     response = self.guest_client.get(reverse('form_msg:send_msg'))
    #     # Словарь ожидаемых типов полей формы:
    #     # указываем, объектами какого класса должны быть поля формы
    #     form_fields = {
    #         'title': forms.fields.CharField,
    #         # При создании формы поля модели типа TextField
    #         # преобразуются в CharField с виджетом forms.Textarea
    #         'text': forms.fields.CharField,
    #         'slug': forms.fields.SlugField,
    #         'image': forms.fields.ImageField,
    #     }
    #
    #     # Проверяем, что типы полей формы в словаре context
    #     # соответствуют ожиданиям
    #     for value, expected in form_fields.items():
    #         with self.subTest(value=value):
    #             form_field = response.context['form'].fields[value]
    #             # Проверяет, что поле формы является экземпляром
    #             # указанного класса
    #             self.assertIsInstance(form_field, expected)

    def test_msg_list_is_1(self):
        """тест контекста"""
        """проверка кол-ва объектов на странице"""
        response = self.authorized_client.get(reverse('form_msg:msg_list'))
        print(response.context['msgs_data'])
        self.assertEqual(response.context['msgs_data'].count(), 1)

    # БЕЗ PAGINATOR
    # Проверяем, что словарь context страницы /msg_list
    # в первом элементе списка object_list содержит ожидаемые значения
    def test_msg_list_page_show_correct_context(self):
        """Шаблон msg_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('form_msg:msg_list'))

        # взяли превый элемент из списка и проверили, что его содержание совпадает с ожидаемым
        first_object = response.context['msgs_data'][0]
        message_author_0 = first_object.author
        message_name_0 = first_object.name
        message_text_0 = first_object.text

        self.assertEqual(message_author_0, self.user)
        self.assertEqual(message_name_0, 'Name')
        self.assertEqual(message_text_0, '123')

    def test_initial_value(self):
        """Предустановленнное значение формы."""
        response = self.authorized_client.get(reverse('form_msg:send_msg'))
        print(response.context['form'])
        print(response.context['form'].fields['text'])

        title_inital = response.context['form'].fields['text'].initial
        self.assertEqual(title_inital, 'Значение по-умолчанию')