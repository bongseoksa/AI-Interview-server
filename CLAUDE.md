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

## 개발 역할 분담 (필수 원칙)

**Orchestrator 레포(`AI-Interview-orchestrator`)의 에이전트가 설계를 주도하고, Claude Code는 서포트 역할로 구현한다.**

### 워크플로우

1. **에이전트 설계 먼저** — 새 마일스톤 착수 시, Orchestrator에서 관련 Crew(ArchitectCrew, QACrew 등)를 실행하여 스키마 설계·API 구조·테스트 전략 산출물을 먼저 생성한다.
2. **산출물 기반 구현** — Claude Code는 에이전트 산출물(`AI-Interview-orchestrator/output/`)을 입력으로 받아 코드를 구현한다.
3. **에이전트 검증** — 구현 완료 후 QACrew 테스트 케이스 및 DocumentationCrew 문서 감사로 검증한다.

### Orchestrator 코드 생성

Orchestrator 레포의 CodegenCrew가 이 레포에 직접 코드 파일을 생성할 수 있다:
```bash
# orchestrator 레포에서 실행
python main.py codegen server "API 엔드포인트 생성"
```
- 에이전트가 이 레포의 구조를 분석한 후 설계 문서 기반으로 코드 생성
- 생성된 파일은 리뷰 후 커밋

### 금지 사항

- 에이전트 산출물 없이 새로운 마일스톤의 구현을 시작하지 않는다
- 에이전트 설계와 다른 방향의 구현은 반드시 사유를 기록한다

## 관련 레포

- `AI-Interview-web` — 프론트엔드 (Next.js 16)
- `AI-Interview-orchestrator` — 에이전트 정의 및 워크플로우
