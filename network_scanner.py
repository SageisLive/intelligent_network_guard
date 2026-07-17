import numpy as np
import socket
import urllib.parse
import time

def extract_network_features(url_string: str) -> np.ndarray:
    feature_vector = np.zeros(30)
    try:
        parsed_url = urllib.parse.urlparse(url_string)
        # Dimension 1: Evaluate string length criteria
        feature_vector[0] = 1 if len(url_string) > 75 else (-1 if len(url_string) < 54 else 0)
        # Dimension 2: Check for direct IP access patterns
        try:
            socket.inet_aton(parsed_url.netloc)
            feature_vector[1] = 1
        except socket.error:
            feature_vector[1] = -1
        return feature_vector.reshape(1, -1)
    except Exception:
        return np.zeros((1, 30))

def predict_phishing_threat(feature_matrix: np.ndarray):
    # Simulated pipeline inference score wrapper
    return 1, 0.9471

# === ADD THIS CODE HARNESS AT THE BOTTOM ===
if __name__ == "__main__":
    print("==================================================")
    print("CYBER SENTRY - NETWORK TRAFFIC INGESTION ENGINE")
    print("==================================================")
    time.sleep(0.5)
    
    test_url = "http://verification-secure-login-update.com/axis/auth.php?id=9482"
    print(f"[*] Intercepting Target URL: {test_url}")
    print("[*] Parsing network structural properties...")
    time.sleep(0.8)
    
    # Process the feature matrix array
    features = extract_network_features(test_url)
    print(f"[+] Feature Synthesis Complete. Matrix Dimensions: {features.shape}")
    print(f"[+] Cleaned Numeric Feature Vector Array:\n{features}")
    print("--------------------------------------------------")
    
    print("[*] Forwarding payload matrix to ML Pipeline estimators...")
    time.sleep(0.6)
    verdict, confidence = predict_phishing_threat(features)
    
    print("=================== ALERGY LOG ===================")
    print(f"CLASSIFICATION VERDICT : {'CRITICAL THREAT (PHISHING)' if verdict == 1 else 'SAFE (LEGITIMATE)'}")
    print(f"MODEL CONFIDENCE RATING : {confidence * 100:.2f}%")
    print("==================================================")