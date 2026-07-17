# AI-Interview-server 온보딩 가이드

이 문서는 AI-Interview-server 레포에 처음 참여하는 사람(또는 에이전트)이
환경 설정부터 실행, 종료까지 빠르게 시작할 수 있도록 안내한다.

---

## 1. 필수 개념

- **API 서버**: 프론트엔드(AI-Interview-web)에 REST/GraphQL API를 제공하는 Python 백엔드
- **AI/LLM 파이프라인**: 개념 설명 생성, 면접 질문 출제, 답변 평가를 처리하는 AI 워크플로우
- **프롬프트 엔지니어링**: LLM에 전달하는 프롬프트를 버전 관리하고 A/B 테스트 가능한 구조로 관리
- **비용 최적화**: 무자본 운영이므로 무료 DB/호스팅/LLM만 사용 — 모든 설계에 비용 제약 반영

## 2. 사전 요구사항

| 항목 | 최소 버전 | 확인 명령어 |
|------|----------|-----------|
| Python | 3.11+ | `python3 --version` |
| Git | 2.x | `git --version` |

## 3. 설치

```bash
cd AI-Interview-server

# 현재 미착수 상태 — 기술 스택 확정 후 설치 가이드 업데이트 예정
# 예상 설치 흐름:
# python3.13 -m venv .venv
# source .venv/bin/activate
# pip install -r requirements.txt
```

## 4. 실행

```bash
# 현재 미착수 — 프레임워크 확정 후 실행 명령어 업데이트 예정
# 예상 실행 흐름:
# source .venv/bin/activate
# python -m uvicorn main:app --reload --port 8000
```

## 5. 종료

```bash
# 개발 서버: 터미널에서 Ctrl+C
# 가상환경 비활성화: deactivate
```

## 6. 현재 상태

**미착수** — Step 6 (아키텍처 설계) 이후 기술 스택 결정 예정

확정 예정 사항:
- Python 웹 프레임워크 (FastAPI / Django 등)
- 데이터베이스 (Supabase Free / PlanetScale Free 등)
- AI/LLM 통합 방식
- 호스팅 (Railway Free / Render Free 등)

## 7. 프로젝트 구조 (예정)

```
# 기술 스택 확정 후 구조 업데이트 예정
.claude/agents/       # Claude Code 서브에이전트 (3개, 배포 완료)
  backend-senior.md   # API 서버, LLM 파이프라인
  data-engineer.md    # DB 스키마 설계
  qa-engineer.md      # API 테스트, 프롬프트 QA
```

## 8. AI 모델 전략

- **Orchestrator 2-Tier (Ollama 로컬)**: 자료 수집·개발은 Gemma 4 26B (고성능 고정), 유저 대면 콘텐츠는 Gemma 4 12B (경량) — orchestrator 레포 참조
- **서비스 LLM**: TBD (Step 6 아키텍처 설계 시 결정). 유저 대면이므로 비용 효율적인 경량 모델 예정

## 9. 비용 제약

- LLM API: 유저 대면은 비용 효율적인 경량 모델 우선 활용
- DB: Supabase 무료 티어 (용량/연결 수 제한 고려)
- 서버: 무료 호스팅 (Railway Free, Render Free 등)
- 모든 외부 서비스: qhdtjd4517@gmail.com 계정으로 가입

## 10. 관련 문서

- `CLAUDE.md` — 에이전트 컨텍스트 (Claude Code용)
- Notion 사업계획서: 레포지토리 3.2 섹션
- `AI-Interview-web` — 프론트엔드 (API 소비자)
- `AI-Interview-orchestrator` — 에이전트 정의 원본
