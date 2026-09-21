# python_jenkins_project
Enterprise-grade Python microservice CI/CD pipeline using Jenkins Declarative Pipelines. Integrates automated GitHub Webhooks, parallel pytest execution, SonarQube quality gates, OWASP/Trivy security scanning, Docker containerization, and Slack notifications.


# Enterprise Python CI/CD Multistage Pipeline

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Flask-lightgrey.svg)](https://flask.palletsprojects.com/)
[![CI/CD](https://img.shields.io/badge/Jenkins-Declarative_Pipeline-red.svg)](https://www.jenkins.io/)
[![Security](https://img.shields.io/badge/Scanner-Trivy_%26_OWASP-green.svg)](https://aquasecurity.github.io/trivy/)

A production-ready, security-focused CI/CD pipeline built with **Jenkins Declarative Pipelines** for a Python microservice. This project demonstrates enterprise DevOps best practices, including automated webhook triggers, parallel testing and static analysis, multi-layered security scanning, container security compliance, and dynamic Slack alerts.

---

## 🏗️ Architecture & Pipeline Flow

The CI/CD pipeline automatically executes the following stages upon code push:


```

[ Developer Push ] ──► [ GitHub Webhook ] ──► [ Jenkins Pipeline ]
│
┌────────────────────────────────────────────────┴────────────────────────────────┐
│                                                                                 │
▼                                                                                 ▼
[ Code Checkout ]                                                            [ Setup VirtualEnv ]
│                                                                                 │
├─────────────────────────────────────────────────────────────────────────────────┘
│
▼
[ Parallel Execution ] ───────────► 1. Code Linting (Flake8)
│                               2. Unit Tests & Coverage (Pytest)
│                               3. Code Analysis (SonarQube)
▼
[ Quality Gate Check ]
│
▼
[ Security Scans ] ───────────────► 1. Dependency Vulnerability Scan (Safety)
│                               2. File System Scan (Trivy)
▼
[ Docker Build & Scan ] ──────────► 1. Multi-stage Docker Build
│                               2. Container Layer Scan (Trivy)
▼
[ Docker Push & Deploy ] ─────────► Push to Registry & Environment Deployment
│
▼
[ Post-Build Housekeeping ] ──────► Workspace Cleanup & Slack Alerts

```

---

## 🧰 Tech Stack & Tools

* **Application Framework:** Python 3.11, Flask, Gunicorn
* **Build & Test Automation:** `pytest`, `pytest-cov`, `flake8`
* **CI/CD Engine:** Jenkins (Declarative Pipeline using Groovy)
* **Code Quality & Analysis:** SonarQube Community / Enterprise
* **Security & Vulnerability Scanners:** Trivy, Safety (Python Dependency Scanner)
* **Containerization:** Docker (Multi-stage, Non-root execution)
* **Notifications:** Slack Webhook integration

---

## 📁 Repository Structure

```text
.
├── .github/
│   └── CODEOWNERS              # Pull Request ownership definitions
├── app/
│   ├── __init__.py             # Package initializer
│   └── main.py                 # Core Flask application API
├── tests/
│   ├── __init__.py             # Test package initializer
│   └── test_main.py            # Pytest suite with code coverage
├── .gitignore                  # Excluded build artifacts and virtual environments
├── Dockerfile                  # Secure, non-root multi-stage Docker build
├── Jenkinsfile                 # Multistage Declarative CI/CD pipeline script
├── README.md                   # Project documentation
├── requirements.txt            # Application & test dependencies
└── sonar-project.properties     # SonarQube scanner configuration

```

---

## 🚀 Quickstart & Local Setup

### 1. Prerequisites

* Python 3.11+
* Docker Desktop or Engine installed locally

### 2. Run Locally

```bash
# Clone the repository
git clone [https://github.com/your-username/my-python-app.git](https://github.com/your-username/my-python-app.git)
cd my-python-app

# Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run linting and unit tests
flake8 app/
pytest tests/ --cov=app

# Start the local development server
python -m app.main

```

### 3. Run via Docker

```bash
# Build Docker image
docker build -t my-python-app:latest .

# Run container
docker run -d -p 5000:5000 my-python-app:latest

# Verify health endpoint
curl http://localhost:5000/health

```

---

## ⚙️ Jenkins CI/CD Setup Guide

### 1. Required Jenkins Plugins

Ensure the following plugins are active on your Jenkins master node:

* `GitHub Plugin`
* `Pipeline: Stage View`
* `SonarQube Scanner`
* `Slack Notification Plugin`
* `Docker Pipeline`

### 2. Configuring Jenkins Credentials

Add the following credentials under **Manage Jenkins $\rightarrow$ Credentials**:

| Credential ID | Type | Description |
| --- | --- | --- |
| `docker-hub-credentials` | Username with Password | Docker Hub registry authentication |
| `slack-token` | Secret Text | Slack Webhook integration token |
| `sonar-token` | Secret Text | SonarQube authentication token |

### 3. GitHub Webhook Configuration

1. Navigate to repository **Settings $\rightarrow$ Webhooks $\rightarrow$ Add webhook**.
2. **Payload URL:** `http://<YOUR_JENKINS_HOST>:8080/github-webhook/`
3. **Content Type:** `application/json`
4. Select **Just the push event**.

---

## 🛡️ Security & Compliance Measures

1. **Non-Root Docker Execution:** The application container runs as `appuser` (UID 8888) to mitigate container escape vulnerabilities.
2. **Automated Security Gates:** Pipeline fails automatically if Trivy or SonarQube flags `CRITICAL` vulnerability thresholds.
3. **Clean Workspace Post-Build:** The `post` block purges temporary environment variables, Docker image artifacts, and virtual environments after execution.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

```

<ElicitationsGroup message="Would you like to generate additional documentation for this project?">
  <Elicitation label="Generate a MIT LICENSE file" query="Generate a standard MIT LICENSE file for this repository."/>
  <Elicitation label="Create a CONTRIBUTING guide for developers" query="Create a CONTRIBUTING.md file outlining guidelines for pull requests and code style."/>
</ElicitationsGroup>

```
