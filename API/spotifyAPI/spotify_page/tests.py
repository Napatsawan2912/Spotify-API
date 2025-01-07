from django.test import TestCase
from unittest.mock import patch, MagicMock
from spotify_page.views import get_api_token  

class TestGetApiToken(TestCase):
    @patch('spotify_page.views.requests.post')  
    def test_get_api_token_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Invalid credentials"
        mock_post.return_value = mock_response

        with self.assertRaises(Exception) as context:
            get_api_token()

        self.assertTrue('Failed to obtain token' in str(context.exception))
    

    @patch('spotify_page.views.requests.post')  
    def test_get_api_token_not_found(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_post.return_value = mock_response

        with self.assertRaises(Exception) as context:
            get_api_token()

        self.assertTrue('404' in str(context.exception))
