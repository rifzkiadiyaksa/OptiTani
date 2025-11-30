from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
import requests
import json
import os
import sys

# --- CONFIGURATION ---
app = FastAPI()

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "login-uns")
LOCATION = "us-central1"

# Setup Vertex AI
model = None
try:
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    # Menggunakan model flash yang cepat
    model = GenerativeModel("gemini-2.5-flash")
    print(f"✅ Vertex AI Ready: {PROJECT_ID}")
except Exception as e:
    print(f"❌ Vertex AI Error: {e}")

# Mount Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve Index
from fastapi.responses import FileResponse
@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

# Model Data
class CalculationRequest(BaseModel):
    crop: str
    land_size: float
    target: float

# --- ERROR HANDLERS ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "validation_message": "Format data input tidak valid.",
            "is_realistic": False,
            "kujang_recommendations": [],
            "generic_recommendations": []
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"🔥 Server Error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "validation_message": f"Terjadi kesalahan sistem: {str(exc)}",
            "is_realistic": False,
            "kujang_recommendations": [],
            "generic_recommendations": []
        }
    )

# --- API ENDPOINT ---
@app.post("/api/calculate")
async def calculate_fertilizer(request: CalculationRequest):
    print(f"📩 Data: {request.dict()}")

    if not model:
        raise Exception("Vertex AI belum siap.")

    kujang_data = "Data produk tidak tersedia."
    try:
        url = "https://admin-web.pupuk-kujang.co.id/api/v1/pemasaran/product"
        resp = requests.get(url, timeout=4)
        if resp.status_code == 200:
            data = resp.json()['data']['products'][:5] 
            kujang_data = json.dumps(data)
    except Exception as e:
        print(f"⚠️ Gagal fetch API Kujang: {e}")

    prompt = f"""
    Peran: Anda adalah Ahli Agronomi Senior di Indonesia.
    Konteks: Bantu petani menghitung kebutuhan pupuk berdasarkan Standar Pertanian Indonesia.
    
    Data Produk Pupuk Kujang (HTML dalam JSON): {kujang_data}
    
    Input Petani:
    - Tanaman: {request.crop}
    - Luas Lahan: {request.land_size} Hektar
    - Target Panen: {request.target} Ton
    
    Tugas:
    1. Ekstrak kandungan N,P,K dari Data Produk.
    2. Analisa apakah target panen tersebut REALISTIS untuk kondisi di Indonesia?
    3. Hitung dosis pupuk. PRIORITASKAN Produk Kujang. Jika kurang, gunakan nama generik.
    
    ATURAN PENTING:
    - GUNAKAN BAHASA INDONESIA yang sopan, jelas, dan memotivasi petani.
    - Output HARUS JSON murni (tanpa markdown ```json).
    - Struktur JSON (Keys dalam bahasa inggris, Values dalam BAHASA INDONESIA):
    {{
        "validation_message": "Kalimat analisa kelayakan target (Contoh: Target 5 Ton sangat realistis untuk...)",
        "is_realistic": true,
        "kujang_recommendations": [{{"product_name": "Nama Produk", "dosage_kg": 100, "reason": "Alasan singkat (Bahasa Indonesia)"}}],
        "generic_recommendations": [{{"product_name": "Nama Generik", "dosage_kg": 50, "reason": "Alasan singkat (Bahasa Indonesia)"}}]
    }}
    """
    
    config = GenerationConfig(response_mime_type="application/json", temperature=0.2)

    try:
        response = model.generate_content(prompt, generation_config=config)
        return json.loads(response.text)
    except Exception as e:
        print(f"❌ AI Generation Error: {e}")
        raise Exception(f"Gagal memproses AI: {e}")