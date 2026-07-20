# AI-Interview-server 온보딩 가이드

이 문서는 AI-Interview-server 레포에 처음 참여하는 사람(또는 에이전트)이
환경 설정부터 실행, 종료까지 빠르게 시작할 수 있도록 안내한다.

---

## 1. 필수 개념

- **FastAPI 서버**: 프론트엔드(AI-Interview-web)에 REST API를 제공하는 Python 백엔드
- **AI 면접 엔진**: 면접 질문 출제, 답변 평가(Rubric 기반), 피드백 생성을 처리하는 AI 파이프라인 (M1부터 구현)
- **Supabase 공유**: web 레포와 동일한 Supabase 프로젝트를 사용하며, Service Role Key로 RLS를 우회
- **비용 최적화**: 무자본 운영이므로 무료/저비용 서비스만 사용 — 월 $5 미만 목표

## 2. 사전 요구사항

| 항목 | 최소 버전 | 확인 명령어 |
|------|----------|-----------|
| Python | 3.13 | `python3.13 --version` |
| Git | 2.x | `git --version` |
| Docker | 20.x (선택) | `docker --version` |

## 3. 설치

```bash
cd AI-Interview-server

# Git pre-commit 훅 활성화 (최초 1회)
git config core.hooksPath .githooks

# 가상환경 생성 및 의존성 설치
python3.13 -m venv .venv
source .venv/bin/activate
pip install uv
uv pip install -e ".[dev]"

# 환경 변수 설정
cp .env.example .env
# .env 파일 편집: Supabase URL, Service Role Key, JWT Secret 입력
```

> `git config core.hooksPath .githooks`를 실행하면 커밋 시 민감 파일(.env, 인증서, DB URL 등) 차단 + 시크릿 패턴 스캔이 자동 수행됩니다.

## 4. 실행

```bash
source .venv/bin/activate

# 개발 서버 (핫 리로드)
uvicorn app.main:app --reload --port 8000

# 또는 Docker
docker-compose up
```

- API 문서: http://localhost:8000/docs
- 헬스체크: http://localhost:8000/v1/health/

## 5. 테스트

```bash
# 전체 테스트
pytest -v

# 린트
ruff check .
```

## 6. 종료

```bash
# 개발 서버: 터미널에서 Ctrl+C
# 가상환경 비활성화: deactivate
# Docker: docker-compose down
```

## 7. 현재 상태

**Phase 5 M0 완료** — FastAPI 서버 인프라 구축

완료 사항:
- FastAPI + Pydantic Settings + Supabase 클라이언트 연동
- JWT 로컬 검증 (python-jose, HS256)
- Health check endpoint (DB 연결 상태 포함)
- CORS 미들웨어 (환경변수 기반)
- Docker (멀티스테이지 빌드) + docker-compose
- GitHub Actions CI (ruff + pytest)
- 테스트 3건 통과

## 8. 프로젝트 구조

```
app/
  main.py                 # FastAPI 앱 초기화, CORS, 라우터 마운트
  core/
    config.py             # Pydantic Settings (환경변수 관리)
    database.py           # Supabase 클라이언트 (lazy 싱글톤)
    security.py           # JWT 검증 (Depends 기반)
  api/v1/
    router.py             # API v1 라우터
    endpoints/
      health.py           # GET /v1/health/
  models/
    common.py             # 공통 응답/에러 스키마
  services/               # 비즈니스 로직 (M1부터)
tests/
  conftest.py             # AsyncClient 픽스처
  test_health.py          # 헬스체크 + CORS 테스트
.claude/agents/           # Claude Code 서브에이전트
  backend-senior.md       # API 서버, LLM 파이프라인
  data-engineer.md        # DB 스키마 설계
  qa-engineer.md          # API 테스트, 프롬프트 QA
```

## 9. AI 모델 전략

- AI 모델 2-Tier 전략 상세: orchestrator 레포 참조
- **서비스 LLM**: Groq 또는 DeepSeek (저비용 고속) — M1에서 결정
- **개발 LLM**: Ollama 로컬 (gemma4:26b) — orchestrator에서 설계용

## 10. 비용 제약

- Supabase: Free Tier (500MB DB, 50K MAU)
- 서버: Railway Free Tier → $5~7/month at scale
- LLM API: Groq/DeepSeek 저비용 tier
- 총 월 $5 미만 목표

## 11. 관련 문서

- `CLAUDE.md` — 에이전트 컨텍스트 (Claude Code용)
- `AI-Interview-web` — 프론트엔드 (API 소비자)
- `AI-Interview-orchestrator` — 에이전트 정의 원본
