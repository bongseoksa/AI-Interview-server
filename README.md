# AI Interview - Server

프론트엔드 엔지니어를 위한 AI 기반 모의 인터뷰 연습 서비스의 백엔드 레포지토리.

## Status

**Phase 5 M0 완료** — FastAPI 서버 인프라 구축

## Tech Stack

| Category | Stack |
|----------|-------|
| Language | Python 3.13 |
| Framework | FastAPI |
| Auth | Supabase JWT (python-jose) |
| Database | Supabase PostgreSQL (shared with web) |
| Hosting | Railway (planned) |
| CI/CD | GitHub Actions |
| Container | Docker |

## Getting Started

```bash
# Git pre-commit 훅 활성화 (최초 1회)
git config core.hooksPath .githooks

# 환경 설정
python3.13 -m venv .venv
source .venv/bin/activate
pip install uv
uv pip install -e ".[dev]"

# 환경 변수 설정
cp .env.example .env
# .env 파일에 Supabase URL, Service Role Key, JWT Secret 입력

# 서버 실행
uvicorn app.main:app --reload --port 8000

# API 문서 확인
open http://localhost:8000/docs
```

## Testing

```bash
# 테스트 실행
pytest -v

# 린트
ruff check .
```

## Docker

```bash
# 로컬 개발
docker-compose up

# 프로덕션 빌드
docker build -t ai-interview-server .
docker run -p 8000:8000 --env-file .env ai-interview-server
```

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/v1/health/` | No | Health check with DB status |
| GET | `/docs` | No | Swagger UI |

## Project Structure

```
app/
  main.py              # FastAPI app initialization
  core/
    config.py          # Pydantic Settings
    database.py        # Supabase client
    security.py        # JWT verification
  api/v1/
    router.py          # API v1 router
    endpoints/
      health.py        # Health check
  models/
    common.py          # Shared schemas
  services/            # Business logic (M1+)
tests/
  conftest.py          # Test fixtures
  test_health.py       # Health + CORS tests
```

## Security

`.githooks/pre-commit` 훅이 커밋 시 민감 파일과 시크릿 패턴을 자동 차단합니다.

```bash
git config core.hooksPath .githooks
```

## Related Repositories

- [AI-Interview-web](https://github.com/bongseoksa/AI-Interview-web) - Frontend (Next.js 16)
- [AI-Interview-orchestrator](https://github.com/bongseoksa/AI-Interview-orchestrator) - Agent orchestration (CrewAI + Ollama)
