# Agentic Architecture Pattern: Portable Development Loop for Antigravity

## Core Principles

1. **Test is Specification**
   The source of truth lies in observable behavior, not in lengthy documentation.
2. **Start Small, Expand Later**
   Do not aim for a complete architecture from the start. Pass the minimal end-to-end path first, and only abstract or split when necessary.
3. **Tracer Bullet First**
   When facing uncertainty, build a "tracer bullet"—the minimal technical path that works—first, and run it locally.
4. **Investigate Before Modifying**
   Do not write code based on assumptions. Gather facts, separate hypotheses, and decide the next action first.

## Core 7 Skills & State Machine

Antigravity operates on **7 Core Skills** connected as an explicit execution state graph:

```mermaid
stateDiagram-v2
    [*] --> investigation: 1. 課題・コードベース調査 (事実と仮説)
    investigation --> tracer_bullet: 事実確定
    tracer_bullet --> test_first: 2. 最小E2E開通 & 契約固定
    test_first --> review: 3. PBT/不変条件保護 & テスト拡張
    
    review --> architecture: 4. 品質・設計クリア
    review --> tracer_bullet: 欠陥発見・差し戻し (Back Edge)
    
    state architecture {
        [*] --> Drift判定
        Drift判定 --> NO_CHANGE
        Drift判定 --> MINOR_UPDATE
        Drift判定 --> STRUCTURAL_ADJUST
    }
    
    STRUCTURAL_ADJUST --> [*]: 【STOP】 人間へのADR提案
    NO_CHANGE --> dead_code_cleanup: 5. 境界維持確認
    MINOR_UPDATE --> dead_code_cleanup: ドキュメント修正
    
    dead_code_cleanup --> pre_commit_leak_review: 6. 不要コード刈り取り
    pre_commit_leak_review --> [*]: 7. 漏洩検査完了・コミット準備
```

## Role-Specific Guidance: Antigravity 2.0 & Gemini 3.8+

Antigravity 2.0 equips the agent with first-class primitives: **Artifacts**, **Subagents**, **Lifecycle Hooks**, and **Terminal Sandboxing**. Gemini provides a vast context window, fast reasoning, and multimodal understanding. To maximize quality:

- **Artifact-Driven Outputs**:
  - Never dump massive reports, complete files, or raw test ledgers directly into the conversation chat.
  - Deliver plans, mission summaries, and reviews as **Artifacts** (`write_to_file` into the artifact directory) so the human can review them directly in the Canvas panel without polluting conversation context.
- **Executable Diagrams & Canvas Review**:
  - In `CONTRACT_LOCK` and investigation, formulate Mermaid.js sequence or DAG diagrams directly inside Markdown Artifacts. Bind each path/node to a Scenario ID (e.g., `SCN-001-HAPPY-PATH`) or Component Identifier.
  - Review diagrams natively in Gemini Canvas without generating standalone HTML files, keeping the workflow clean and zero-overhead.
- **Subagent Parallelism**:
  - When investigating broad unfamiliar repositories or evaluating 2–3 competing technical approaches for a tracer bullet, spawn subagents with isolated workspaces (`share` or `branch`).

## Language Standards (Dual-First-Class: Go & Python)

- **Go**:
  - Structured logging with `log/slog` (no raw `fmt.Println` in production code).
  - Concurrency checks with `go test -race`.
  - In-process CLI contract testing via `app.Run(args, in, out)`.
  - Property-Based Testing with `rapid` or `testing/quick`.
- **Python**:
  - Structured logging with `structlog` or standard `logging` JSON formatter.
  - Concurrency checks with `pytest-asyncio` / unhandled task checks.
  - In-process CLI contract testing via Click `CliRunner` or `argparse` handlers.
  - Property-Based Testing with `hypothesis`.

## Architectural Guardrails

Architecture is not a "perfect blueprint" but a "minimal set of constraints to prevent excessive drift."

- **Preserve Observable Boundaries**: Define and lock the contract (CLI inputs/outputs, exit codes, error classifications) before implementation, and do not break it.
- **Dependency Direction**: Strictly adhere to unidirectional dependencies: `CLI/UI → Domain → Adapters`.
- **No Cyclic Dependencies**: Do not create circular references between modules.
- **Minimal Boundaries**: Keep the structure simple; do not prematurely split into components until the scope demands it.

## Drift Classification

Every change must be evaluated and classified into one of three categories:

| Classification | State | Action |
|---|---|---|
| **NO_CHANGE** | Fits completely within existing ADRs, boundaries, contracts, and dependency rules. | Proceed as is. |
| **MINOR_UPDATE** | Direction is valid, but requires minor documentation updates, compatible CLI flag additions, or code cleanup. | Clean up and proceed. |
| **STRUCTURAL_ADJUST** | Cannot be explained by existing guardrails. Breaks a boundary, responsibility, or public contract. | **[STOP]** Immediately halt the implementation and propose an Architecture Decision Record (ADR) and evolution plan to the human. |

## Safety Restrictions

The following destructive actions are strictly prohibited without explicit human confirmation:
- Mass file deletion
- Widespread filesystem rewrites
- External side effects (e.g., executing structural changes on live infrastructure)
