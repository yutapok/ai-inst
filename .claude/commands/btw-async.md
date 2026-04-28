# /btw-async command

This command suggests the next asynchronous inspection or decision step from the current state.

## Agent Execution Steps

1. **Read Current Situation**
   - Review the current conversation, recent work, and any existing report files that may already capture prior inspection results.
   - If present, treat `.claude/reports/ql-report-latest.md` and `.claude/reports/drift-report-latest.md` as reusable context, even when they were produced in another session.
2. **Activate Planner Skill**
   - Read `.claude/skills/planner/SKILL.md`.
3. **Recommend the Next Inspection-Oriented Move**
   - Prefer `REVIEW` when broad quality or risk inspection is now justified.
   - Prefer `DRIFT_CHECK` when architectural boundaries or contracts may have shifted.
   - If neither inspection is the real next step, recommend another workflow state instead of forcing review.
4. **Output Suggestion & Stop**
   - Return a short `次のステップ:` recommendation using workflow states.
   - When recommending an inspection, point to `/ql-review` or `/drift-check` as the concrete follow-up command.
   - If an option can be issued independently in parallel, prefix the action with `（Async）`.
   - Prefer keeping the recommended `1.` option as the mainline step, and use `（Async）` for side tasks that do not block it.
   - For each `（Async）` option, include a short handoff envelope with `Goal:`, `Scope:`, `Done:`, and `Non-goals:`.
   - **STOP** after the recommendation.

## Example Output

```markdown
Current Read: トレーサーパスは通っていて、周辺の確認作業は独立に投げられる状態。

次のステップ:
1. （推奨）EXPAND: エラー系の統合テストを追加して CLI 契約を固める
   Verify: `python -m unittest tests.integration.test_codex_contract` を実行して、CLI 契約の統合テストが通ることを確認する
2. REVIEW: （Async）/ql-review を回して命名と責務分割のノイズを先に洗い出す
   Goal: 命名の不整合と責務過多の候補を洗い出して報告する
   Scope: 直近変更の `cli/` と `domain/` の既存差分のみ
   Done: 修正提案を 3 件以内の箇条書きで返す。コード変更はしない
   Non-goals: 新規設計、依存追加、大規模リファクタ
3. DRIFT_CHECK: （Async）/drift-check で新しい設定ファイル追加が境界逸脱でないか確認する
   Goal: 設定ファイル追加が既存の責務境界を壊していないか判定する
   Scope: 新規設定ファイルとその読み込み経路のみ
   Done: `NO_CHANGE` / `MINOR_UPDATE` / `STRUCTURAL_ADJUST` のいずれかで返す
   Non-goals: 実装修正、設定値チューニング、別機能の監査
```
