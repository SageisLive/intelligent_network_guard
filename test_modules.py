import pytest
from fastapi.testclient import TestClient
import numpy as np
import network_scanner as scanner
import system_monitor as monitor
from main import app

client = TestClient(app)

def test_feature_extraction_matrix_dimensions():
    """Verify that the network scanner outputs exactly a 1x30 matrix."""
    test_url = "http://malicious-login-update.com/auth"
    features = scanner.extract_network_features(test_url)
    assert type(features) == np.ndarray
    assert features.shape == (1, 30)

def test_feature_extraction_empty_handling():
    """Verify that the scanner handles malformed inputs safely."""
    features = scanner.extract_network_features("")
    assert features.shape == (1, 30)
    assert features[0][0] == -1  # Length constraint for empty string

def test_system_telemetry_keys():
    """Verify system monitor returns all required diagnostic keys."""
    stats = monitor.get_system_diagnostics()
    expected_keys = ["timestamp", "cpu_utilisation", "memory_utilisation", "system_status"]
    for key in expected_keys:
        assert key in stats

def test_api_root_redirect():
    """Verify the root endpoint redirects to the documentation."""
    response = client.get("/", follow_redirects=False)
    # 307 is the standard HTTP status code for Temporary Redirect in FastAPI
    assert response.status_code == 307 

def test_api_scan_endpoint():
    """Verify the ML prediction endpoint returns the correct JSON schema."""
    payload = {
        "target_url": "http://secure-billing-verify.net",
        "request_id": "REQ-99482",
        "priority_level": 1
    }
    response = client.post("/api/v1/scan", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["request_id"] == "REQ-99482"
    assert data["status"] == "processed"
    assert "verdict" in data
    assert "confidence_score" in data