# CLAUDE.md — AI-Interview-server

AI Interview 서비스의 백엔드 서버 레포.

## 레포 목적

- API 서버 (Python 기반, 프레임워크 TBD)
- AI/LLM 파이프라인 (개념 설명 생성, 면접 질문 출제, 답변 평가)
- 데이터베이스 관리

## 상태

미착수 — 기술 스택 미정 (Step 6 아키텍처 설계 이후 결정)

## 비용 제약

- Claude API 토큰 직접 사용 불가 (orchestrator와 동일)
- 서비스 AI 기능은 무료/최소 비용 LLM 활용 방안 설계 필요
- DB: 무료 티어만 사용
- 서버: 무료 호스팅 (Railway Free, Render Free 등)

## 관련 레포

- `AI-Interview-web` — 프론트엔드 (Next.js 16)
- `AI-Interview-orchestrator` — 에이전트 정의 및 워크플로우
