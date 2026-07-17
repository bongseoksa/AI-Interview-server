# CLAUDE.md — AI-Interview-server

AI Interview 서비스의 백엔드 서버 레포.

## 레포 목적

- API 서버 (Python 기반, 프레임워크 TBD)
- AI/LLM 파이프라인 (개념 설명 생성, 면접 질문 출제, 답변 평가)
- 데이터베이스 관리

## 상태

미착수 — 기술 스택 미정 (Step 6 아키텍처 설계 이후 결정)

## AI 모델 전략

- **Orchestrator 2-Tier**: 자료 수집·개발용은 Gemma 4 26B (고성능 고정), 유저 대면 콘텐츠는 Gemma 4 12B (경량) — 상세는 orchestrator CLAUDE.md 참조
- **서비스 LLM**: TBD (Step 6 아키텍처 설계 시 결정). 유저 대면 기능이므로 비용 효율적인 모델 선택 예정
- **LLM 호출 방식**: TBD (서버 프록시 vs Next.js Route Handlers 직접 호출)

## 비용 제약

- 서비스 AI 기능은 비용 효율적인 경량 모델 우선 활용
- DB: Supabase 무료 티어
- 서버: 무료 호스팅 (Railway Free, Render Free 등)

## 관련 레포

- `AI-Interview-web` — 프론트엔드 (Next.js 16)
- `AI-Interview-orchestrator` — 에이전트 정의 및 워크플로우
