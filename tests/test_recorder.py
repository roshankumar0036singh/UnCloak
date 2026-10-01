from unittest.mock import patch, MagicMock
from uncloak.recorder import record_har

def test_record_har():
    with patch("uncloak.recorder.sync_playwright") as mock_playwright:
        mock_p = MagicMock()
        mock_playwright.return_value.__enter__.return_value = mock_p
        
        mock_browser = mock_p.chromium.launch.return_value
        mock_context = mock_browser.new_context.return_value
        mock_page = mock_context.new_page.return_value
        
        har_path = record_har("https://example.com", "out.har")
        
        assert har_path == "out.har"
        mock_page.goto.assert_called_once_with("https://example.com", wait_until="networkidle")
        mock_browser.close.assert_called_once()
