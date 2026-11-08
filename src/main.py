from fastapi import FastAPI
from src.core.config import settings
from src.db.database import Base, engine
from src.models.document import Document  # noqa: F401 - registra o modelo no metadata
from src.api.routes import router

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title=settings.app_name,
    description="API para enviar documentos, extrair texto, gerar resumos e responder perguntas sobre o conteúdo.",
    version=settings.app_version,
)
app.include_router(router)


@app.get("/health", tags=["Sistema"])
def health_check():
    return {"status": "ok", "version": settings.app_version}


@app.get("/", tags=["Sistema"])
def root():
    return {"message": settings.app_name, "docs": "/docs", "health": "/health"}
