import io
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.main import app
from src.db.database import Base, get_db

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

def test_ai_endpoint_explains_missing_configuration():
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
