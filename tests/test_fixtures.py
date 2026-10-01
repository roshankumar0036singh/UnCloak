import json
import os
import re
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent / "fixtures"

def test_fixtures_structure():

        
    fixture_dirs = [d for d in FIXTURES_DIR.iterdir() if d.is_dir() and d.name != "fixtures_private"]
    
    assert len(fixture_dirs) >= 5, f"Expected at least 5 fixtures, found {len(fixture_dirs)}"
    
    for fdir in fixture_dirs:
        har_path = fdir / "capture.har"
        expected_path = fdir / "expected.json"
        text_path = fdir / "visible_text.txt"
        
        assert har_path.exists(), f"Missing capture.har in {fdir.name}"
        assert expected_path.exists(), f"Missing expected.json in {fdir.name}"
        assert text_path.exists(), f"Missing visible_text.txt in {fdir.name}"
        
        # Check HAR is valid JSON
        with open(har_path, "r", encoding="utf-8") as f:
            har_data = json.load(f)
            assert "log" in har_data
            assert "entries" in har_data["log"]
            
        # Check expected.json has required keys
        with open(expected_path, "r", encoding="utf-8") as f:
            expected_data = json.load(f)
            assert "correct_endpoint" in expected_data
            assert "noise_domains" in expected_data
            assert "site_type" in expected_data
            
        # Check text is non-empty
        with open(text_path, "r", encoding="utf-8") as f:
            assert len(f.read().strip()) > 0
            
        # Check for leaked secrets
        with open(har_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Very basic check for common token patterns that shouldn't be in anonymized HARs
            assert "ghp_" not in content # github token
            assert "xoxb-" not in content # slack token
            assert "Bearer real_" not in content
