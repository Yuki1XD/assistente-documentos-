# Assistente Inteligente de Documentos

[![Versão](https://img.shields.io/badge/versão-1.0.0-blue)](#) [![Licença](https://img.shields.io/badge/licença-MIT-green)](LICENSE) [![Build](https://img.shields.io/badge/build-testes%20locais-yellow)](#)

## Problema
Ler documentos extensos e localizar informações importantes pode consumir muito tempo. Esta API permite enviar arquivos PDF ou TXT, extrair seu texto, consultar documentos, gerar resumos e fazer perguntas sobre o conteúdo.

## Funcionalidades
- [x] API REST com FastAPI e documentação Swagger.
- [x] Verificação de saúde em `GET /health`.
- [x] Upload e validação de PDF/TXT, com limite configurável.
- [x] Extração de texto de PDF e TXT.
- [x] Persistência dos documentos em SQLite (padrão) ou PostgreSQL.
- [x] Listagem, consulta e exclusão de documentos.
- [x] Recuperação simples de trechos relevantes para perguntas.
- [x] Integração opcional com API compatível com OpenAI para resumo e perguntas.
- [X] OCR para PDFs digitalizados.


## Tecnologias
Python 3.11+, FastAPI, SQLAlchemy, SQLite/PostgreSQL, PyMuPDF, HTTPX e pytest.

## Instalação local
1. Instale Python 3.11 ou superior.
2. Clone o repositório e entre na pasta.
3. Crie ambiente virtual: `python -m venv .venv`.
4. Ative-o: Linux/macOS `source .venv/bin/activate`; Windows `\.venv\Scripts\Activate.ps1`.
5. Instale: `pip install -r requirements.txt`.
6. Copie `.env.example` para `.env` e ajuste as configurações se necessário. SQLite é o padrão e não exige servidor separado.
7. Inicie: `uvicorn src.main:app --reload`.
8. Acesse `http://127.0.0.1:8000/docs`.

## Configurar inteligência artificial
A integração usa o endpoint Chat Completions compatível com OpenAI. No `.env`, configure `AI_API_BASE`, `AI_API_KEY` e `AI_MODEL`. Sem essas configurações, a API principal continua funcionando, mas os endpoints de resumo e perguntas retornam HTTP 503 explicando como configurar a IA. Nunca publique sua chave no GitHub.

**Usando o Groq (configuração recomendada e testada):**
```env
AI_API_BASE=https://api.groq.com/openai/v1
AI_API_KEY=sua_chave_do_groq
AI_MODEL=openai/gpt-oss-20b
AI_TIMEOUT_SECONDS=60
```
A chave pode ser criada no painel do Groq. Neste projeto, que monta a URL com `httpx`, a base precisa terminar em `/openai/v1`; não use somente `https://api.groq.com` (essa base simplificada foi usada no teste separado com o SDK oficial).

**Usando o Gemini:** `AI_API_BASE=https://generativelanguage.googleapis.com/v1beta/openai/`, `AI_MODEL=gemini-2.5-flash` e `AI_API_KEY` com a chave do Google AI Studio. Também é possível usar outros provedores que ofereçam endpoint compatível com Chat Completions.

## Endpoints
| Método | Rota | Função |
|---|---|---|
| GET | `/health` | Verificar API |
| POST | `/api/v1/documents` | Enviar PDF/TXT |
| GET | `/api/v1/documents` | Listar documentos |
| GET | `/api/v1/documents/{id}` | Consultar documento |
| DELETE | `/api/v1/documents/{id}` | Excluir documento |
| POST | `/api/v1/documents/{id}/summary` | Gerar resumo com IA |
| POST | `/api/v1/documents/{id}/ask` | Perguntar sobre o documento |

## Testes
Execute `pytest -q`. Os testes usam banco SQLite temporário em memória e não precisam de chave de IA.

## Banco PostgreSQL com Docker (opcional)
Execute `docker compose up -d db`, depois configure `DATABASE_URL` no `.env` para `postgresql+psycopg://assistente:altere_esta_senha@localhost:5432/assistente_docs`. Troque a senha de exemplo antes de qualquer uso real.

## Documentação do projeto
- [Project Charter](docs/project-charter.md)
- [Requisitos](docs/requisitos.md)
- [Casos de uso](docs/casos-de-uso.md)
- [Histórias de usuário](docs/user-stories.md)
- [Git Flow](docs/git-flow.md)
- [Issues planejadas](docs/issues/)

## Git Flow e commits
Não faça commits diretamente em `main`. Use `main` para versões estáveis, `develop` para integração e branches `feature/nome-da-issue` criadas a partir de `develop`. Abra PRs para `develop` e, depois de validar, para `main`. Use Conventional Commits, por exemplo `feat: adiciona upload de documentos`, `fix: trata PDF corrompido` e `docs: atualiza instruções`. Relacione PRs às issues reais usando `Closes #N`. Use tags anotadas no formato SemVer, como `v1.0.0`.

## Limitações e segurança
Esta versão é um MVP acadêmico de uso local e **não está pronta para exposição pública**: ainda não tem autenticação nem separação de documentos por usuário. O SQLite é o padrão para facilitar testes; PostgreSQL é suportado por configuração. PDFs digitalizados exigem OCR, ainda não incluído. O sistema guarda o texto extraído no banco e não mantém o arquivo original. Conteúdo de documentos é tratado como dado não confiável durante a integração com IA. Configure limite de upload e mantenha segredos fora do repositório.

## Situação do projeto
A API e os testes básicos estão implementados. As funcionalidades que dependem de credenciais de um provedor de IA precisam de configuração no ambiente para funcionar com respostas geradas por modelo. As issues em `docs/issues/` são propostas para cadastro no GitHub; ainda não são issues criadas automaticamente.
