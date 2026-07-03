from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
from accounts.models import CustomUser, MasterUniversitas

class RegisterPesertaTestCase(TestCase):
    @patch('accounts.views._sync_to_firebase')
    @patch('accounts.views._verify_appcheck')
    @patch('urllib.request.urlopen')
    def test_register_peserta_success(self, mock_urlopen, mock_verify_appcheck, mock_sync_firebase):
        # Mock reCAPTCHA verification success
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"success": true}'
        mock_urlopen.return_value = mock_response

        # Mock Firebase App Check success
        mock_verify_appcheck.return_value = (True, None)

        client = Client()
        url = reverse('register_peserta')
        
        post_data = {
            'nama_lengkap': 'Budi Setiawan',
            'nim': '12345678',
            'universitas': 'Universitas Pelita Bangsa',
            'email': 'budi@example.com',
            'password': 'password123',
            'password_confirm': 'password123',
            'g-recaptcha-response': 'dummy-response'
        }
        
        # Verify the database doesn't have the user or university yet
        self.assertFalse(CustomUser.objects.filter(email='budi@example.com').exists())
        self.assertFalse(MasterUniversitas.objects.filter(nama='Universitas Pelita Bangsa').exists())

        response = client.post(url, post_data)
        
        # Assert redirect to login_peserta after successful registration
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login_peserta'))

        # Check database records
        self.assertTrue(CustomUser.objects.filter(email='budi@example.com').exists())
        user = CustomUser.objects.get(email='budi@example.com')
        self.assertEqual(user.first_name, 'Budi Setiawan')
        self.assertEqual(user.nim, '12345678')
        
        # Verify MasterUniversitas was created and associated
        self.assertTrue(MasterUniversitas.objects.filter(nama='Universitas Pelita Bangsa').exists())
        self.assertEqual(user.universitas.nama, 'Universitas Pelita Bangsa')

