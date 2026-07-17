Cyber Sentry: Intelligent Network Guard (Zero-Trust Endpoint Protection)

Author: Muslim Olasubomi Badmus (Matric No: 22/9634)

Institution: Caleb University, Imota, Lagos | Department of Computer Science

Supervisor: Dr. Odegbesan Omobolaji

Year: 2026

📌 Project Overview

This repository contains the complete source code for my B.Sc. Final Year Project: "Design of an Intelligent Network Guard based on Zero-Trust Principles."

Cyber Sentry is a localized, AI-driven endpoint protection framework. Unlike traditional cloud-tethered cybersecurity solutions that export user data to central servers (risking latency and privacy breaches), this project pioneers a decoupled, local-first framework. It utilizes a Multi-Layer Perceptron (MLP) machine learning algorithm to detect phishing payloads strictly on local hardware, maintaining zero-trust principles without compromising data sovereignty.

✨ Core Features

100% Local Execution: No external cloud dependency. Absolute user data sovereignty is maintained at all times.

Zero-Trust Loopback Routing: Enforces strict token-bound isolation for all internal API requests to prevent unauthorized process access.

Mathematical Feature Synthesis: Converts raw URL strings into 30-dimensional numeric vectors strictly in active memory (RAM), ensuring no persistent tracking.

Predictive Threat ML: Powered by a Multi-Layer Perceptron (MLP) model trained on a 2021-2024 phishing dataset, achieving an F1-Score of 0.9594.

Live Hardware Telemetry: Integrates OS kernel hooks via psutil to dynamically monitor and restrict system consumption (Sub-85% CPU, Sub-8 GB RAM).

🛠️ Technology Stack

Frontend UI: HTML5, Vanilla JavaScript, Tailwind CSS, Lucide Icons.

Backend Engine: Python 3.x, FastAPI, Uvicorn.

Machine Learning: Scikit-Learn, NumPy, Pandas.

System Diagnostics: Psutil (Hardware constraints monitoring).

🚀 Installation & Setup Instructions

To evaluate the system locally, ensure Python 3.9+ is installed on the host machine.

1. Clone the repository:

git clone https://github.com/SageisLive/intelligent_network_guard.git
cd intelligent_network_guard


2. Install required dependencies:

pip install fastapi uvicorn scikit-learn numpy pandas psutil pydantic


3. Initialize the backend engine:

python app.py


(Note: The server boots strictly on local loopback http://127.0.0.1:8000 to prevent external exposure).

4. Launch the Dashboard:
Double-click the index.html file in the frontend directory to open the Cyber Sentry UI in any modern web browser.

📊 System Evaluation Metrics

During hardware stress testing and adversarial evaluation, the system successfully maintained sub-second explanation latency while successfully intercepting malicious socket queries. The Multi-Layer Perceptron model out-performed baseline decision trees, mitigating false negatives effectively within the constrained physical bounds.

This software was developed as part of a B.Sc. Computer Science Final Year Project defense. It is intended for academic evaluation and localized network routing research.
