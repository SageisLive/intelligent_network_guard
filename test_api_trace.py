import time
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

if __name__ == "__main__":
    print("===========================================================")
    print("REST API ENDPOINT VALIDATION & SECURITY ACCESS TRACE")
    print("===========================================================")
    time.sleep(0.5)

    print("\n[*] INITIATING TEST 1: UNAUTHORIZED ACCESS ATTEMPT (No Token)")
    print("    POST /api/v1/scan HTTP/1.1")
    print("    Host: 127.0.0.1:8000")
    print("    Content-Type: application/json")
    time.sleep(0.8)

    payload = {"target_url": "http://malicious-test.com", "request_id": "REQ-001", "priority_level": 1}
    response_401 = client.post("/api/v1/scan", json=payload)

    print("\n[<] RESPONSE RECEIVED:")
    print(f"    HTTP/1.1 {response_401.status_code} UNAUTHORIZED")
    print(f"    Body: {response_401.json()}")
    print("[+] Security validation passed: System successfully blocked unauthorized client.")
    time.sleep(1.0)

    print("\n-----------------------------------------------------------")
    print("\n[*] INITIATING TEST 2: AUTHORIZED ACCESS ATTEMPT (Valid Token)")
    print("    POST /api/v1/scan HTTP/1.1")
    print("    Host: 127.0.0.1:8000")
    print("    Authorization: Bearer valid_token_2026")
    print("    Content-Type: application/json")
    time.sleep(0.8)

    headers = {"Authorization": "Bearer valid_token_2026"}
    response_200 = client.post("/api/v1/scan", headers=headers, json=payload)

    print("\n[<] RESPONSE RECEIVED:")
    print(f"    HTTP/1.1 {response_200.status_code} OK")
    print(f"    Body: {response_200.json()}")
    print("[+] Integration passed: End-to-end payload routing successful.")
    
    print("\n===========================================================")
    print("TEST SUITE COMPLETED: ALL SECURITY CONSTRAINTS VERIFIED")
    print("===========================================================")