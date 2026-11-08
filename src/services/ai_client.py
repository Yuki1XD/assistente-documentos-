import httpx
from src.core.config import settings


class AIUnavailableError(RuntimeError):
    pass


def _provider_error_detail(response: httpx.Response) -> str:
    """Extrai a mensagem de erro do provedor (OpenAI e Gemini usam formatos parecidos)."""
    try:
        data = response.json()
    except ValueError:
        return response.text[:300]
    if isinstance(data, list) and data:
        data = data[0]
    if isinstance(data, dict):
        error = data.get("error", data)
        if isinstance(error, dict) and error.get("message"):
            return str(error["message"])[:300]
    return str(data)[:300]


async def generate_answer(system_prompt: str, user_prompt: str) -> str:
    if not settings.ai_api_key or not settings.ai_model:
        raise AIUnavailableError("Integração de IA não configurada. Defina AI_API_KEY e AI_MODEL no arquivo .env.")
    base = settings.ai_api_base.strip().rstrip("/")
    url = f"{base}/chat/completions"
    headers = {"Authorization": f"Bearer {settings.ai_api_key.strip()}", "Content-Type": "application/json"}
    payload = {
        "model": settings.ai_model.strip(),
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    try:
        async with httpx.AsyncClient(timeout=settings.ai_timeout_seconds) as client:
            response = await client.post(url, headers=headers, json=payload)
    except httpx.TimeoutException as exc:
        raise AIUnavailableError(f"O serviço de IA não respondeu em {settings.ai_timeout_seconds}s. Tente novamente.") from exc
    except httpx.HTTPError as exc:
        raise AIUnavailableError(f"Não foi possível conectar ao serviço de IA em {base} ({type(exc).__name__}).") from exc

    if response.status_code >= 400:
        detail = _provider_error_detail(response)
        hints = {
            400: "Verifique AI_MODEL e a chave (o Gemini devolve 400 para chave inválida).",
            401: "Chave de API inválida ou do provedor errado.",
            403: "Chave sem permissão para este modelo/projeto.",
            404: "Endereço ou modelo não encontrado. Confira AI_API_BASE e AI_MODEL.",
            429: "Limite de uso/cota atingido. Aguarde ou verifique seu plano.",
        }
        hint = hints.get(response.status_code, "Verifique a configuração do provedor.")
        raise AIUnavailableError(f"O provedor de IA retornou HTTP {response.status_code}: {detail} — {hint}")

    try:
        data = response.json()
        answer = data["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError) as exc:
        raise AIUnavailableError("O provedor de IA retornou uma resposta em formato inesperado.") from exc
    if not isinstance(answer, str) or not answer.strip():
        raise AIUnavailableError("O provedor de IA retornou uma resposta vazia.")
    return answer.strip()
