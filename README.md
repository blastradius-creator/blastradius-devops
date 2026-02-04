# Snowflake FastAPI Serverless Pipeline

A production-grade, serverless API implementation utilizing **FastAPI**, **Docker**, and **AWS Lambda**, orchestrated by a robust **GitHub Actions** CI/CD pipeline. This project demonstrates "Safety-First" deployment—where unit tests are executed inside the container build process to guarantee that only verified code reaches the registry.

## 🚀 Architecture Overview

### 1. Python API (`FastAPI`)
The core application is built with **Python 3.13** and **FastAPI**, designed to run in a serverless environment via the **Mangum** adapter.
*   **Snowflake Integration:** Securely connects to Snowflake using the `snowflake-connector-python` with `DictCursor` for JSON-friendly data handling.
*   **Endpoints:** Includes health checks (`/test`), Snowflake versioning (`/snowflake-version`), and dynamic data retrieval (`/menu-items`).
*   **Testing:** Uses `pytest` and `httpx` with `unittest.mock` to simulate Snowflake responses, ensuring logic is tested without requiring live database credentials.

### 2. Dockerization
The project uses a **multi-stage Docker build** based on the official **AWS Lambda Python 3.13** image.
*   **Base Stage:** Installs core dependencies from `requirements.txt`.
*   **Test Stage:** Injects `pytest`, sets the `PYTHONPATH`, and executes unit tests. If tests fail, the build process terminates immediately.
*   **Final Stage:** Produces a slim, production-ready image containing only the application code and required runtime libraries.

### 3. AWS Infrastructure
*   **Amazon ECR:** Serves as the private container registry for the Docker images.
*   **AWS Lambda:** Host environment (Container Image support) triggered via API Gateway or Lambda Function URLs.
*   **IAM Security:** Utilizes GitHub Secrets (`AWS_KEY`, `AWS_SECRET`) for secure authentication via the `aws-actions/configure-aws-credentials` action.

### 4. GitHub Actions CI/CD
The automation pipeline is defined in `.github/workflows/` and manages the entire lifecycle:

| Feature | Description |
| :--- | :--- |
| **Triggers** | Runs on `pull_request` to `main` and `push` to `main`. |
| **Branch Rules** | Enforces naming conventions (e.g., `feature/*`, `fix/*`) to maintain repo hygiene. |
| **Versioning** | Uses **GitVersion** to automatically calculate the next Semantic Version (SemVer). |
| **Conditional Logic** | Builds images for every PR, but only **pushes** to ECR and **creates Releases** on merges to `main`. |
| **Permissions** | Configured with `contents: write` to allow the automated creation of GitHub Releases. |

---

## 🛠 Project Structure

```text
.
├── .github/workflows/       # GitHub Actions pipeline definitions
├── snowflake-api/
│   ├── main.py              # FastAPI application & Mangum handler
│   ├── Dockerfile           # Multi-stage Lambda-ready Dockerfile
│   ├── requirements.txt     # Production and test dependencies
│   └── tests/
│       └── test_main.py     # Pytest suite with Snowflake mocking
└── README.md
