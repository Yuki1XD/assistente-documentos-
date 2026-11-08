from pathlib import Path
import fitz


class DocumentExtractionError(ValueError):
    pass


def extract_text(filename: str, content: bytes) -> tuple[str, str]:
    suffix = Path(filename).suffix.lower()
    if suffix == ".txt":
        try:
            text = content.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise DocumentExtractionError("O arquivo TXT precisa estar codificado em UTF-8.") from exc
        file_type = "txt"
    elif suffix == ".pdf":
        if not content.startswith(b"%PDF"):
            raise DocumentExtractionError("O arquivo não parece ser um PDF válido.")
        try:
            with fitz.open(stream=content, filetype="pdf") as pdf:
                text = "\n".join(page.get_text("text") for page in pdf)
        except Exception as exc:
            raise DocumentExtractionError("Não foi possível ler o PDF. Verifique se o arquivo não está corrompido ou protegido.") from exc
        file_type = "pdf"
    else:
        raise DocumentExtractionError("Formato não permitido. Envie somente PDF ou TXT.")

    text = "\n".join(line.rstrip() for line in text.splitlines()).strip()
    if not text:
        raise DocumentExtractionError("Não foi encontrado texto no documento. PDFs digitalizados precisam de OCR, que ainda não está disponível.")
    return text, file_type
