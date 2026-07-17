# AI Interview - Server

프론트엔드 엔지니어를 위한 AI 기반 모의 인터뷰 연습 서비스의 백엔드 레포지토리.

## Status

**미착수** - Step 6 (아키텍처 설계) 이후 기술 스택 결정 예정

## Planned Stack

| Category | Candidates |
|----------|-----------|
| Language | Python 3.11+ |
| Framework | FastAPI / Django (TBD) |
| Database | Supabase Free (PostgreSQL) |
| Hosting | Railway Free / Render Free |
| Service LLM | TBD (cost-efficient model) |

## Getting Started

```bash
# Git pre-commit 훅 활성화 (최초 1회)
git config core.hooksPath .githooks

# 기술 스택 확정 후 업데이트 예정
# python3.13 -m venv .venv
# source .venv/bin/activate
# pip install -r requirements.txt
```

## Planned Responsibilities

- REST API server for AI-Interview-web
- AI/LLM pipeline (concept explanation, question generation, answer evaluation)
- Prompt versioning & A/B testing
- Database schema & migrations

## Security

`.githooks/pre-commit` 훅이 커밋 시 민감 파일과 시크릿 패턴을 자동 차단합니다.

```bash
# 훅 활성화 (최초 1회)
git config core.hooksPath .githooks
```

## Related Repositories

- [AI-Interview-web](https://github.com/bongseoksa/AI-Interview-web) - Frontend (Next.js 16)
- [AI-Interview-orchestrator](https://github.com/bongseoksa/AI-Interview-orchestrator) - Agent orchestration (CrewAI + Ollama)
