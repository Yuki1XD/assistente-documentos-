import httpx
from src.core.config import settings


class AIUnavailableError(RuntimeError):
    pass


async def generate_answer(system_prompt: str, user_prompt: str) -> str:
    if not settings.ai_api_key or not settings.ai_model:
        raise AIUnavailableError("Integração de IA não configurada. Defina AI_API_KEY e AI_MODEL no arquivo .env.")
    base = settings.ai_api_base.rstrip("/")
    url = f"{base}/chat/completions"
    headers = {"Authorization": f"Bearer {settings.ai_api_key}", "Content-Type": "application/json"}
    payload = {
        "model": settings.ai_model,
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    try:
        async with httpx.AsyncClient(timeout=settings.ai_timeout_seconds) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            answer = data["choices"][0]["message"]["content"]
            if not isinstance(answer, str) or not answer.strip():
                raise AIUnavailableError("O provedor de IA retornou uma resposta vazia.")
            return answer.strip()
    except AIUnavailableError:
        raise
    except Exception as exc:
        raise AIUnavailableError("Não foi possível obter resposta do serviço de IA. Verifique a configuração e tente novamente.") from exc
