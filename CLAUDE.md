# CLAUDE.md — AI-Interview-server

AI Interview 서비스의 백엔드 서버 레포.

## 레포 목적

- FastAPI 기반 REST API 서버
- AI/LLM 파이프라인 (면접 질문 출제, 답변 평가, 피드백 생성)
- Supabase PostgreSQL 연동 (web 레포와 동일 프로젝트 공유)

## 상태

Phase 5 M0 완료 — FastAPI 인프라 구축, 배포 파이프라인 준비

## 기술 스택

| Category | Stack |
|----------|-------|
| Language | Python 3.13 |
| Framework | FastAPI >= 0.115 |
| Auth | Supabase JWT 로컬 검증 (ES256 JWKS primary + HS256 fallback, python-jose) |
| Database | Supabase Free (PostgreSQL, web 레포와 공유) |
| Hosting | Railway (예정) |
| CI/CD | GitHub Actions (ruff + pytest) |
| Container | Docker (멀티스테이지 빌드, python:3.13-slim) |
| Package Manager | uv + pyproject.toml |

## 프로젝트 구조

```
app/
  main.py                 # FastAPI 앱 초기화, CORS, 라우터 마운트
  core/
    config.py             # Pydantic Settings (환경변수 관리)
    database.py           # Supabase 클라이언트 (lazy 싱글톤)
    security.py           # JWT 검증 (ES256 JWKS + HS256 fallback, Depends 기반)
  api/v1/
    router.py             # API v1 라우터
    endpoints/
      health.py           # GET /v1/health/ (DB 연결 상태 포함)
  models/
    common.py             # 공통 응답/에러 스키마 (Pydantic v2)
  services/               # 비즈니스 로직 (M1부터 구현)
tests/
  conftest.py             # AsyncClient 픽스처
  test_health.py          # 헬스체크 + CORS 테스트
  test_auth.py            # JWT 검증 테스트 (ES256 + HS256 + 에러 케이스)
Dockerfile                # 멀티스테이지 빌드
docker-compose.yml        # 로컬 개발용
.github/workflows/ci.yml  # GitHub Actions CI
pyproject.toml            # 의존성 + ruff + pytest 설정
.env.example              # 환경변수 템플릿
```

## 실행 명령어

```bash
# 환경 설정
python3.13 -m venv .venv
source .venv/bin/activate
pip install uv && uv pip install -e ".[dev]"
cp .env.example .env  # Supabase 키 입력

# 서버 실행
uvicorn app.main:app --reload --port 8000

# 테스트
pytest -v

# 린트
ruff check .

# Docker
docker-compose up
```

## 환경 변수 (.env)

| 변수 | 설명 |
|------|------|
| `SUPABASE_URL` | Supabase 프로젝트 URL |
| `SUPABASE_SERVICE_ROLE_KEY` | 서비스 롤 키 (RLS 우회) |
| `SUPABASE_JWT_SECRET` | HS256 레거시 폴백용 시크릿 (ES256은 JWKS에서 자동 취득) |
| `JWKS_CACHE_TTL` | JWKS 캐시 유지 시간 (초, 기본 86400=24h) |
| `CORS_ORIGINS` | 허용 Origin (JSON 배열 형식) |
| `DEBUG` | 디버그 모드 (true/false) |

## API 엔드포인트

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/v1/health/` | No | 헬스체크 (DB 연결 상태 포함) |
| GET | `/docs` | No | Swagger UI |

## Phase 5 마일스톤

| 마일스톤 | 상태 | 내용 |
|----------|------|------|
| **M0** | 완료 | FastAPI 인프라 + Docker + CI/CD |
| **M1** | 미착수 | AI 면접 코어 (상태 머신 + 질문 선택) |
| **M2** | 미착수 | 피드백 엔진 (Rubric 채점) |
| **M3** | 미착수 | 면접 UI 연동 (FE↔BE) |
| **M4** | 미착수 | 수익 실험 + Beta Launch |

## AI 모델 전략

- AI 모델 2-Tier 전략 상세: `AI-Interview-orchestrator/CLAUDE.md` 참조
- **서비스 LLM**: Groq 또는 DeepSeek (저비용 고속) — M1에서 결정
- **개발 LLM**: Ollama 로컬 (gemma4:26b) — orchestrator에서 설계용

## 비용 제약

- Supabase: Free Tier (500MB DB, 50K MAU auth)
- 서버: Railway Free Tier → $5~7/month at scale
- LLM API: Groq/DeepSeek 저비용 tier 활용
- 총 운영 비용 목표: 월 $5 미만

## 개발 역할 분담 (필수 원칙)

**Orchestrator 레포(`AI-Interview-orchestrator`)의 에이전트가 설계를 주도하고, Claude Code는 서포트 역할로 구현한다.**

### 워크플로우

1. **에이전트 설계 먼저** — 새 마일스톤 착수 시, Orchestrator에서 관련 Crew를 실행하여 설계 산출물을 먼저 생성한다.
2. **산출물 기반 구현** — Claude Code는 에이전트 산출물(`AI-Interview-orchestrator/output/`)을 입력으로 받아 코드를 구현한다.
3. **에이전트 검증** — 구현 완료 후 QACrew 테스트 케이스 및 DocumentationCrew 문서 감사로 검증한다.

### Orchestrator 코드 생성

Orchestrator 레포의 CodegenCrew가 이 레포에 직접 코드 파일을 생성할 수 있다:
```bash
# orchestrator 레포에서 실행
python main.py codegen server "API 엔드포인트 생성"
```

### 금지 사항

- 에이전트 산출물 없이 새로운 마일스톤의 구현을 시작하지 않는다
- 에이전트 설계와 다른 방향의 구현은 반드시 사유를 기록한다

## 관련 레포

- `AI-Interview-web` — 프론트엔드 (Next.js 16)
- `AI-Interview-orchestrator` — 에이전트 정의 및 워크플로우
