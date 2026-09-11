---
name: Code and Architecture Review
description: Fast, zero-bloat adversarial self-critique enforcing YAGNI, MVP lean core, and contract invariance while blocking confirmation bias.
---

# Adversarial Self-Review (Devil's Advocate Protocol)

このSkillは、直前の実装に対するエージェント自身の「甘い判断・自己正当化バイアス」を物理的に排除し、コードとテストを最小のMVP状態（Lean Core）に削ぎ落とすための敵対的セルフレビューである。

## 3つの絶対ルール (Inviolable Rules)

1. **現状追認・承認（褒めること）の禁止**:
   「問題ありません」「適切に実装されています」「LGTM」等の承認文言の出力を禁止する。
2. **Negative Quota（最低2点の指摘ノルマ）**:
   以下のいずれかの観点から、改善・削ぎ落とすべき箇所を必ず2点以上特定して出力しなければならない（見つからない場合は「これ以上削れない理由」を行単位で説明せよ）。
   - **YAGNI違反**: 1箇所でしか使われていないInterface、先回りした汎用化引数、不要な抽象化ラッパー、過剰なファイル分割。
   - **過剰テスト**: 内部プライベート関数に対する過剰なモックテスト、変更に脆い実装結合テスト。
   - **契約の脆さ**: 空文字、巨大入力、異常終了時のエラーハンドリング漏れや未処理パニック（Panic / Uncaught Exception）の余地。
3. **Hard Boundary, Lean Core**:
   外部契約（CLI入出力・終了コード・エラー分類）のみをインプロセス統合テスト（Tier A: `app.Run`）で厳格に固定し、内部実装は最も愚直で短いコード（単一関数・単一構造体）に留める。

## レビューの観点 (Audit Lenses)

### ① YAGNI & 差分マイナス化 (Subtraction over Addition)
- この変更で追加された行のうち、**削除しても契約テストが通る行**はないか？
- 将来の拡張を先回りした汎用引数や設定項目が含まれていないか？
- 中間ラッパーや不要なヘルパー関数をインライン化（直書き）できないか？

### ② 契約保護と後戻り防止 (Rollback Prevention)
- CLI引数、標準入力、標準出力、終了コードがインプロセス統合テスト（`app.Run`）でロックされているか？
- 想定外の入力で未捕捉パニックが発生する余地はないか？

### ③ テストの過剰性排除 (MVP Test Suite)
- 内部のプライベート実装に結合した脆いモックテストを書いていないか？
- 外部契約の検証に必要な最小限のテストケース（正常系1件＋代表的異常系1件＋PBT不変条件）に絞られているか？

## 出力フォーマット (Kill / Keep / Fix Checklist)

冗長なレポート作成によるボトルネック化を禁止する。以下の極小フォーマット（10行以内）で出力し、直ちに修正または `DEAD_CODE_CLEANUP` へ移行せよ。

```markdown
### 👿 Adversarial Self-Review
- **Contract Health**: [PASS (Locked) | BREACH (Specify)]
- **Kill (削除・インライン化候補 - 最低1点)**:
  1. `[file:line]`: [不要な抽象化/関数の理由と削除提案]
  2. `[file:line]`: [過剰なテスト/設定の理由と削除提案]
- **Fix (契約保護・脆さ対策 - 0〜1点)**:
  - `[file:line]`: [エッジケース処理の愚直な追加]
- **Action**: [TRIGGER_CLEANUP | RETRY_TRACER | PROCEED]
```
