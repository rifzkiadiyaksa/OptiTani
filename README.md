# OptiTani: Precision Agriculture Assistant 🌾

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-009688?logo=fastapi&logoColor=white)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-Run-4285F4?logo=google-cloud&logoColor=white)
![Vertex AI](https://img.shields.io/badge/Vertex_AI-Gemini_1.5-orange?logo=google-gemini&logoColor=white)

**OptiTani** is a precision agriculture tool designed to help farmers optimize fertilizer usage. By combining real-time product data from **PT Pupuk Kujang** with the reasoning capabilities of **Google Vertex AI (Gemini)**, the system analyzes target yields and provides precise, cost-effective nutrient recommendations.

This project was built for the **BNB Marathon 2025** to demonstrate the impact of Generative AI in the Agritech sector.

---

## 🏗 System Architecture

The application follows a clean **Client-Server** architecture deployed on Google Cloud Platform.

1.  **Frontend:** Static HTML5 + Tailwind CSS (served via FastAPI).
2.  **Backend:** Python FastAPI for business logic and API orchestration.
3.  **AI Engine:** Google Vertex AI (Gemini 1.5 Flash) for agronomy reasoning and data extraction.
4.  **Data Source:** PT Pupuk Kujang Public API (Real-time product availability).
5.  **Infrastructure:** Dockerized container hosted on Google Cloud Run.



---

## ✨ Key Features

* **Yield Feasibility Analysis:** The AI evaluates if a farmer's harvest target (in Tons) is realistic for their specific land size (in Hectares) based on regional agronomy standards.
* **Unstructured Data Processing:** Automatically extracts Nutrient values (N, P, K) from raw HTML descriptions provided by the Kujang API.
* **Prioritized Recommendations:** Algorithmically prioritizes local government-backed products (Pupuk Kujang) before suggesting generic alternatives.
* **Stateless & Secure:** Uses Application Default Credentials (ADC) for zero-trust security. No hardcoded API keys.

---

## 🛠 Project Structure

```bash
optitani/
├── main.py              # Application entry point & Backend logic
├── Dockerfile           # Container configuration for Cloud Run
├── requirements.txt     # Python dependencies
├── static/              # Frontend assets
│   └── index.html       # Single-page UI
└── .gitignore           # Security rules
🚀 Getting Started (Local Development)
Follow these steps to run the application on your local machine.

Prerequisites
Python 3.9+

Google Cloud SDK (gcloud CLI) installed and authenticated.

1. Clone the Repository
Bash

git clone [https://github.com/rifzkiadiyaksa/OptiTani.git](https://github.com/rifzkiadiyaksa/OptiTani.git)
cd OptiTani
2. Setup Virtual Environment
Bash

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
3. Google Cloud Authentication
Since this project uses Vertex AI, you must authenticate your local machine to your Google Cloud project.

Bash

gcloud auth application-default login
4. Run the Application
Set your Project ID environment variable (replace with your actual ID) and start the server.

Bash

# Linux/Mac
export GOOGLE_CLOUD_PROJECT="your-google-cloud-project-id"

# Windows (Powershell)
$env:GOOGLE_CLOUD_PROJECT="your-google-cloud-project-id"

# Start Server
uvicorn main:app --reload
Access the app at: http://127.0.0.1:8000

☁️ Deployment (Google Cloud Run)
This project is optimized for Cloud Run. You do not need to manage servers.

1. Build Container

Bash

gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/optitani-app .
2. Deploy Service Replace YOUR_DB_PASSWORD with your actual database credentials (if connecting to Cloud SQL), or leave blank if running in demo mode.

Bash

gcloud run deploy optitani-app \
  --image gcr.io/YOUR_PROJECT_ID/optitani-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars DB_USER=postgres,DB_PASS=YOUR_DB_PASSWORD,DB_NAME=optitani_db,DB_HOST=127.0.0.1
🔒 Security Note
This repository is Safe by Design:

No API Keys: Access to Vertex AI is managed via IAM Service Accounts.

Environment Variables: Sensitive configuration (Project IDs, DB Credentials) are injected at runtime, not hardcoded.

Public Data: The fertilizer data is fetched from a public endpoint and contains no PII.

📄 Developed by Rifzki Adiyaksa for BNB Marathon 2025.
