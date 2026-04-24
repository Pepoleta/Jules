import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add the parent directory to sys.path so we can import the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock dependencies if they are not installed
try:
    import undetected_chromedriver as uc
except ImportError:
    mock_uc = MagicMock()
    sys.modules['undetected_chromedriver'] = mock_uc

try:
    import selenium
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
except ImportError:
    mock_sel = MagicMock()
    sys.modules['selenium'] = mock_sel
    sys.modules['selenium.webdriver'] = mock_sel
    sys.modules['selenium.webdriver.common.by'] = mock_sel
    sys.modules['selenium.webdriver.support.ui'] = mock_sel
    sys.modules['selenium.webdriver.support'] = mock_sel
    sys.modules['selenium.webdriver.common.keys'] = mock_sel
# Define necessary constants
class MockBy:
    CSS_SELECTOR = 'css'
class MockKeys:
    ENTER = '\n'

sys.modules['selenium.webdriver.common.by'].By = MockBy
sys.modules['selenium.webdriver.common.keys'].Keys = MockKeys

from gemini_bot import GeminiBot

class TestGeminiBot(unittest.TestCase):

    @patch('gemini_bot.uc.Chrome')
    @patch('gemini_bot.uc.ChromeOptions')
    def setUp(self, mock_options, mock_chrome):
        self.mock_driver = MagicMock()
        mock_chrome.return_value = self.mock_driver
        self.bot = GeminiBot(profile_dir="test_profile")

    @patch('gemini_bot.WebDriverWait')
    def test_navigate_to_gemini(self, mock_wait_class):
        mock_wait_instance = MagicMock()
        mock_wait_class.return_value = mock_wait_instance
        
        self.bot.navigate_to_gemini()
        
        self.mock_driver.get.assert_called_with("https://gemini.google.com/app")
        mock_wait_instance.until.assert_called()

    @patch('gemini_bot.WebDriverWait')
    def test_send_prompt(self, mock_wait_class):
        mock_wait_instance = MagicMock()
        mock_wait_class.return_value = mock_wait_instance
        
        mock_input = MagicMock()
        mock_send_button = MagicMock()
        
        # Configure until to return input_area then send_button
        mock_wait_instance.until.side_effect = [mock_input, mock_send_button]
        
        # Mock _wait_for_response
        with patch.object(self.bot, '_wait_for_response', return_value="Test Response"):
            response = self.bot.send_prompt("Hello Gemini")
            
        mock_input.send_keys.assert_called_with("Hello Gemini")
        mock_send_button.click.assert_called()
        self.assertEqual(response, "Test Response")

    @patch('gemini_bot.WebDriverWait')
    def test_upload_files(self, mock_wait_class):
        mock_wait_instance = MagicMock()
        mock_wait_class.return_value = mock_wait_instance
        
        mock_file_input = MagicMock()
        mock_wait_instance.until.return_value = mock_file_input
        
        self.bot._upload_files(["path/to/file1.txt", "path/to/file2.png"])
        
        mock_file_input.send_keys.assert_called_with("path/to/file1.txt\npath/to/file2.png")

    def tearDown(self):
        # We don't want to actually quit the mock driver in some cases, 
        # but for testing the call is fine.
        self.bot.close()
        self.mock_driver.quit.assert_called()

if __name__ == '__main__':
    unittest.main()
