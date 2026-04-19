from django.test import TestCase
from django.urls import reverse


class ApiDocsEndpointTests(TestCase):
    def test_swagger_docs_endpoint_is_available(self):
        response = self.client.get(reverse('api-docs'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('swagger', response.content.decode().lower())
