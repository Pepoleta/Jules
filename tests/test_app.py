import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add the parent directory to sys.path so we can import the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock dependencies before importing app
mock_st = MagicMock()
sys.modules['streamlit'] = mock_st

mock_uc = MagicMock()
sys.modules['undetected_chromedriver'] = mock_uc

mock_sel = MagicMock()
sys.modules['selenium'] = mock_sel
sys.modules['selenium.webdriver'] = mock_sel
sys.modules['selenium.webdriver.common.by'] = mock_sel
sys.modules['selenium.webdriver.support.ui'] = mock_sel
sys.modules['selenium.webdriver.support'] = mock_sel
sys.modules['selenium.webdriver.common.keys'] = mock_sel

import app

class MockSessionState(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)
    def __setattr__(self, key, value):
        self[key] = value

class TestStreamlitApp(unittest.TestCase):

    def setUp(self):
        # Reset the mock for each test
        mock_st.reset_mock()
        # Initialize session state mock with attribute access
        app.st.session_state = MockSessionState()
        app.st.session_state.bot = None

    @patch('app.GeminiBot')
    def test_get_bot_initialization(self, mock_bot_class):
        mock_bot_instance = MagicMock()
        mock_bot_class.return_value = mock_bot_instance
        
        bot = app.get_bot()
        
        self.assertEqual(app.st.session_state['bot'], mock_bot_instance)
        mock_bot_instance.navigate_to_gemini.assert_called_once()
        self.assertEqual(bot, mock_bot_instance)

    def test_get_bot_existing(self):
        mock_bot_instance = MagicMock()
        app.st.session_state['bot'] = mock_bot_instance
        
        bot = app.get_bot()
        
        self.assertEqual(bot, mock_bot_instance)
        # Should not call navigate_to_gemini again
        mock_bot_instance.navigate_to_gemini.assert_not_called()

    @patch('app.get_bot')
    @patch('tempfile.mkdtemp')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_main_submit_with_files(self, mock_open, mock_mkdtemp, mock_get_bot):
        # Setup mocks
        mock_mkdtemp.return_value = "/tmp/testdir"
        mock_bot = MagicMock()
        mock_get_bot.return_value = mock_bot
        mock_bot.send_prompt.return_value = "Mocked Response"
        
        # Simulate form submission
        app.st.session_state['bot'] = mock_bot
        app.st.form_submit_button.return_value = True
        app.st.text_area.return_value = "Test Prompt"
        
        mock_file = MagicMock()
        mock_file.name = "test.txt"
        mock_file.getbuffer.return_value = b"test content"
        app.st.file_uploader.return_value = [mock_file]
        
        # Run main (partially, since it's a script)
        # We need to simulate the state where submit_button is True
        app.main()
        
        # Check if bot.send_prompt was called with correct arguments
        expected_path = os.path.join("/tmp/testdir", "test.txt")
        mock_bot.send_prompt.assert_called_once_with("Test Prompt", [expected_path])
        app.st.write.assert_called_with("Mocked Response")

if __name__ == '__main__':
    unittest.main()
