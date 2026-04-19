import io
import shutil
from datetime import timedelta
from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase

from apps.user.models import User


class UserListAPIViewTests(APITestCase):
    # Task 7 ucun list endpoint davranishi burada butov paket kimi yoxlanilir.
    url = reverse('user-list')

    @classmethod
    def setUpTestData(cls):
        # Auth test-leri ve protected endpoint yoxlamalari ucun ayrica user saxlanilir.
        cls.authenticated_user = User.objects.create_user(
            username='auth-user',
            email='auth@example.com',
            password='StrongPass123!',
        )

        # Pagination, filter ve ordering testleri menali olsun deye sayca kifayet qeder user yaradilir.
        base_time = timezone.now() - timedelta(days=1)
        cls.created_users = []

        for index in range(15):
            user = User.objects.create_user(
                username=f'user{index}',
                email=f'user{index}@example.com',
                password='StrongPass123!',
                is_active=index % 2 == 0,
            )
            User.objects.filter(pk=user.pk).update(
                created_at=base_time + timedelta(minutes=index)
            )
            user.refresh_from_db()
            cls.created_users.append(user)

        cls.ali_user = User.objects.create_user(
            username='ali-user',
            email='special@example.com',
            password='StrongPass123!',
            is_active=True,
        )
        User.objects.filter(pk=cls.ali_user.pk).update(
            created_at=base_time + timedelta(minutes=20)
        )
        cls.ali_user.refresh_from_db()

        cls.inactive_ali_user = User.objects.create_user(
            username='inactive-ali',
            email='inactive.ali@example.com',
            password='StrongPass123!',
            is_active=False,
        )
        User.objects.filter(pk=cls.inactive_ali_user.pk).update(
            created_at=base_time + timedelta(minutes=21)
        )
        cls.inactive_ali_user.refresh_from_db()

    def authenticate(self):
        # Tekrar olunan auth addimini her testde qisa saxlamaq ucun helper method yazilib.
        self.client.force_authenticate(user=self.authenticated_user)

    def test_authentication_required_for_user_list(self):
        response = self.client.get(self.url)

        # Task 9-dan sonra auth xetasi raw DRF detail formasinda yox,
        # standart success/error envelope formasinda qayitmalidir.
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data['success'])
        self.assertEqual(
            response.data['error'],
            'Authentication credentials were not provided.',
        )

    def test_user_list_is_paginated_for_authenticated_requests(self):
        self.authenticate()

        response = self.client.get(self.url)

        # Task 9-a gore pagination datasi artiq response.data daxilinde yox,
        # response.data['data'] daxilinde saxlanilir.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], 'Data fetched successfully.')
        self.assertIn('count', response.data['data'])
        self.assertIn('next', response.data['data'])
        self.assertIn('previous', response.data['data'])
        self.assertIn('results', response.data['data'])
        self.assertEqual(response.data['data']['count'], 18)
        self.assertEqual(len(response.data['data']['results']), 10)

    def test_second_page_returns_remaining_results(self):
        self.authenticate()

        response = self.client.get(self.url, {'page': 2})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']['results']), 8)
        self.assertIsNone(response.data['data']['next'])
        self.assertIsNotNone(response.data['data']['previous'])

    def test_page_size_query_param_is_applied(self):
        self.authenticate()

        response = self.client.get(self.url, {'page_size': 5})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']['results']), 5)

    def test_search_filters_by_username(self):
        self.authenticate()

        response = self.client.get(self.url, {'search': 'ali-user'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usernames = [item['username'] for item in response.data['data']['results']]
        self.assertEqual(usernames, ['ali-user'])

    def test_search_filters_by_email(self):
        self.authenticate()

        response = self.client.get(self.url, {'search': 'inactive.ali@example.com'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usernames = [item['username'] for item in response.data['data']['results']]
        self.assertEqual(usernames, ['inactive-ali'])

    def test_filter_returns_only_active_users(self):
        self.authenticate()

        response = self.client.get(self.url, {'is_active': 'true'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(item['is_active'] for item in response.data['data']['results']))
        self.assertEqual(response.data['data']['count'], 10)

    def test_filter_returns_only_inactive_users(self):
        self.authenticate()

        response = self.client.get(self.url, {'is_active': 'false'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(not item['is_active'] for item in response.data['data']['results']))
        self.assertEqual(response.data['data']['count'], 8)

    def test_search_filter_and_pagination_work_together(self):
        self.authenticate()

        response = self.client.get(
            self.url,
            {'search': 'ali', 'is_active': 'true', 'page': 1},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usernames = [item['username'] for item in response.data['data']['results']]
        self.assertEqual(usernames, ['ali-user'])

    def test_ordering_by_created_at_is_supported(self):
        self.authenticate()

        response = self.client.get(self.url, {'ordering': 'created_at'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usernames = [item['username'] for item in response.data['data']['results'][:3]]
        self.assertEqual(usernames, ['user0', 'user1', 'user2'])

    def test_invalid_ordering_falls_back_to_default_order(self):
        self.authenticate()

        response = self.client.get(self.url, {'ordering': 'invalid'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usernames = [item['username'] for item in response.data['data']['results'][:2]]
        self.assertEqual(usernames, ['auth-user', 'inactive-ali'])


class UserAvatarUploadAPIViewTests(APITestCase):
    # Task 8 ucun upload endpoint-in auth, validation ve storage davranishi ayrica yoxlanilir.
    url = reverse('user-avatar-upload')

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        project_root = Path(__file__).resolve().parents[2]
        # Test zamani real media qovlugunu cirklendirmemek ucun ayrica test_media istifade olunur.
        cls.temp_media_root = project_root / 'test_media'
        shutil.rmtree(cls.temp_media_root, ignore_errors=True)
        cls.temp_media_root.mkdir(exist_ok=True)
        cls.media_override = override_settings(MEDIA_ROOT=cls.temp_media_root)
        cls.media_override.enable()

    @classmethod
    def tearDownClass(cls):
        cls.media_override.disable()
        shutil.rmtree(cls.temp_media_root, ignore_errors=True)
        super().tearDownClass()

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='avatar-user',
            email='avatar@example.com',
            password='StrongPass123!',
        )

    def authenticate(self):
        self.client.force_authenticate(user=self.user)

    def create_test_image(
        self,
        filename='avatar.png',
        image_format='PNG',
        size=(100, 100),
        color='blue',
        content_type='image/png',
    ):
        # PIL ile memory daxilinde shekil yaradilir ki, test ucun ayrica fayl saxlamaqa ehtiyac qalmasin.
        file_object = io.BytesIO()
        image = Image.new('RGB', size=size, color=color)
        image.save(file_object, format=image_format)
        file_object.seek(0)

        return SimpleUploadedFile(
            filename,
            file_object.getvalue(),
            content_type=content_type,
        )

    def test_authentication_required_for_avatar_upload(self):
        response = self.client.patch(self.url, {}, format='multipart')

        # Avatar upload endpoint-i ucun de auth xetasi vahid error formatinda olmalidir.
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data['success'])
        self.assertEqual(
            response.data['error'],
            'Authentication credentials were not provided.',
        )

    def test_authenticated_user_can_upload_avatar(self):
        self.authenticate()
        avatar = self.create_test_image()

        response = self.client.patch(
            self.url,
            {'avatar': avatar},
            format='multipart',
        )

        # Success cavabi Task 9-dan sonra data/message ile qayitdigi ucun
        # avatar linki de response.data['data'] icinden yoxlanilir.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], 'Avatar updated successfully.')
        self.user.refresh_from_db()
        self.assertTrue(self.user.avatar.name.startswith('avatars/'))
        self.assertIn('/media/avatars/', response.data['data']['avatar'])

    def test_invalid_file_type_is_rejected(self):
        self.authenticate()
        avatar = self.create_test_image(
            filename='avatar.gif',
            image_format='GIF',
            content_type='image/gif',
        )

        response = self.client.patch(
            self.url,
            {'avatar': avatar},
            format='multipart',
        )

        # Validation xetalari field-list formasinda yox, sade error string kimi qayitmalidir.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertEqual(
            response.data['error'],
            'Only JPG, JPEG, PNG, and WEBP files are allowed.',
        )

    @override_settings(MAX_UPLOAD_IMAGE_SIZE=1024)
    def test_oversized_image_is_rejected(self):
        self.authenticate()
        avatar = self.create_test_image(
            filename='large-avatar.jpg',
            image_format='JPEG',
            size=(1500, 1500),
            content_type='image/jpeg',
        )

        response = self.client.patch(
            self.url,
            {'avatar': avatar},
            format='multipart',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertEqual(
            response.data['error'],
            'Image size must be 0 MB or less.',
        )
