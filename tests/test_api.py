import io
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.main import app
from src.db.database import Base, get_db
from src.core.config import settings

engine_test = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(bind=engine_test, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=engine_test)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def setup_function():
    Base.metadata.drop_all(bind=engine_test)
    Base.metadata.create_all(bind=engine_test)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_upload_txt_and_list_and_detail_and_delete():
    response = client.post("/api/v1/documents", files={"file": ("teste.txt", b"Conteudo de teste para consultar documentos.", "text/plain")})
    assert response.status_code == 201, response.text
    document_id = response.json()["id"]
    assert response.json()["file_type"] == "txt"
    assert len(client.get("/api/v1/documents").json()) == 1
    detail = client.get(f"/api/v1/documents/{document_id}")
    assert detail.status_code == 200
    assert "Conteudo de teste" in detail.json()["preview"]
    deleted = client.delete(f"/api/v1/documents/{document_id}")
    assert deleted.status_code == 204
    assert client.get(f"/api/v1/documents/{document_id}").status_code == 404

def test_reject_unsupported_file():
    response = client.post("/api/v1/documents", files={"file": ("arquivo.docx", b"abc", "application/octet-stream")})
    assert response.status_code == 422

def test_reject_empty_file():
    response = client.post("/api/v1/documents", files={"file": ("vazio.txt", b"", "text/plain")})
    assert response.status_code == 400

def test_ai_endpoint_explains_missing_configuration(monkeypatch):
    # Simula ambiente sem IA, mesmo que o .env local tenha uma chave (ex.: Gemini).
    monkeypatch.setattr(settings, "ai_api_key", "")
    monkeypatch.setattr(settings, "ai_model", "")
    upload = client.post("/api/v1/documents", files={"file": ("teste.txt", b"Este documento fala sobre sistemas de informacao.", "text/plain")})
    document_id = upload.json()["id"]
    response = client.post(f"/api/v1/documents/{document_id}/summary")
    assert response.status_code == 503
    assert "AI_API_KEY" in response.json()["detail"]

def test_upload_pdf():
    import fitz
    pdf = fitz.open()
    page = pdf.new_page()
    page.insert_text((72, 72), "Texto de teste dentro de um documento PDF.")
    content = pdf.tobytes()
    pdf.close()
    response = client.post("/api/v1/documents", files={"file": ("teste.pdf", content, "application/pdf")})
    assert response.status_code == 201, response.text
    assert response.json()["file_type"] == "pdf"


def _configure_fake_ai(monkeypatch):
    monkeypatch.setattr(settings, "ai_api_base", "https://generativelanguage.googleapis.com/v1beta/openai/")
    monkeypatch.setattr(settings, "ai_api_key", "chave-falsa")
    monkeypatch.setattr(settings, "ai_model", "gemini-2.5-flash")


def _fake_post(status_code, body, captured=None):
    import httpx

    async def fake_post(self, url, headers=None, json=None):
        if captured is not None:
            captured.update(url=url, headers=headers, json=json)
        return httpx.Response(status_code, json=body, request=httpx.Request("POST", url))
    return fake_post


def test_ai_summary_with_gemini_compatible_response(monkeypatch):
    import httpx
    _configure_fake_ai(monkeypatch)
    captured = {}
    body = {"choices": [{"message": {"role": "assistant", "content": "Resumo gerado."}}]}
    monkeypatch.setattr(httpx.AsyncClient, "post", _fake_post(200, body, captured))
    upload = client.post("/api/v1/documents", files={"file": ("t.txt", b"Texto sobre sistemas.", "text/plain")})
    response = client.post(f"/api/v1/documents/{upload.json()['id']}/summary")
    assert response.status_code == 200, response.text
    assert response.json()["summary"] == "Resumo gerado."
    assert captured["url"] == "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
    assert captured["headers"]["Authorization"] == "Bearer chave-falsa"
    assert captured["json"]["model"] == "gemini-2.5-flash"


def test_ai_provider_error_is_shown(monkeypatch):
    import httpx
    _configure_fake_ai(monkeypatch)
    body = [{"error": {"code": 400, "message": "API key not valid. Please pass a valid API key."}}]
    monkeypatch.setattr(httpx.AsyncClient, "post", _fake_post(400, body))
    upload = client.post("/api/v1/documents", files={"file": ("t.txt", b"Texto sobre sistemas.", "text/plain")})
    response = client.post(f"/api/v1/documents/{upload.json()['id']}/summary")
    assert response.status_code == 503
    assert "API key not valid" in response.json()["detail"]



def test_ai_groq_uses_openai_compatible_endpoint(monkeypatch):
    import httpx
    monkeypatch.setattr(settings, "ai_api_base", "https://api.groq.com/openai/v1")
    monkeypatch.setattr(settings, "ai_api_key", "chave-falsa")
    monkeypatch.setattr(settings, "ai_model", "openai/gpt-oss-20b")
    captured = {}
    body = {"choices": [{"message": {"role": "assistant", "content": "Resumo via Groq."}}]}
    monkeypatch.setattr(httpx.AsyncClient, "post", _fake_post(200, body, captured))
    upload = client.post("/api/v1/documents", files={"file": ("groq.txt", b"Texto de teste.", "text/plain")})
    response = client.post(f"/api/v1/documents/{upload.json()['id']}/summary")
    assert response.status_code == 200, response.text
    assert response.json()["summary"] == "Resumo via Groq."
    assert captured["url"] == "https://api.groq.com/openai/v1/chat/completions"
    assert captured["headers"]["Authorization"] == "Bearer chave-falsa"
    assert captured["json"]["model"] == "openai/gpt-oss-20b"
