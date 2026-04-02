# COO — machine 活用パターン

## 基本ルール

1. **計画書を先に書く** — 分析目的を明確にしてから machine に投入する。目的なき分析は禁止
2. **出力はドラフト** — machine の出力は分析素材であり最終判断ではない。COO が判断を付加してから報告する
3. **保存場所**: `state/plans/{YYYY-MM-DD}_{概要}.{type}.md`（`/tmp/` 禁止）
4. **レート制限**: chat 5回/session、heartbeat 2回
5. **machine はインフラにアクセスできない** — 必要な情報（org_dashboard 出力、activity_log データ等）は指示文に含めること

---

## 概要

COO は委任判断・部門監視・経営報告を主務とし、組織分析・KPI集計・報告書ドラフト作成を machine に委託する。

- 組織状況の構造化分析 → machine が分析し、COO が判断
- KPI集計・統計情報の抽出 → machine が集約し、COO が検証
- 人間向けレポートの作成 → machine がドラフトし、COO が判断コメントを追加

**COO 自身が判断を行うことが必須（MUST）。machine の出力をそのまま人間に報告しない。**

---

## Phase A: 組織分析

### Step 1: 分析対象を特定する

org_dashboard / audit_subordinate の出力を取得し、分析すべき範囲を決定する:
- 全体概況の定期分析（日次・週次）
- 特定部門の異常検知（STALE タスク、エラー率上昇等）
- 部門間ボトルネックの特定

### Step 2: 分析計画書を作成する

```markdown
# 組織分析計画書

status: draft
author: {anima名}
date: {YYYY-MM-DD}
type: org-analysis

## 分析目的
{何を明らかにしたいか}

## 対象部門
{全体 / 特定部門名}

## 分析期間
{直近24h / 直近1週間 / 特定日付範囲}

## 入力データ
{org_dashboard の出力、audit_subordinate の結果、activity_log の抜粋等}

## 分析観点
- タスク消化状況（STALE / OVERDUE の有無）
- エラー・障害の有無と影響範囲
- 部門間の依存・ブロッキング
- リソース偏り（特定メンバーに負荷集中等）
```

### Step 3: machine に分析を依頼する

```bash
animaworks-tool machine run \
  "$(cat $ANIMAWORKS_ANIMA_DIR/state/plans/{計画書ファイル})" \
  -d /path/to/workspace
```

結果を `state/plans/{date}_{概要}.org-analysis.md` として保存する。

### Step 4: COO が結果を確認・判断する

machine の分析結果を確認し、以下を付加する:
- 異常検知時のアクション判断（委任 / エスカレーション / 経過観察）
- 判断根拠の明記
- 必要に応じて直属部下に指示（delegate_task / send_message）

---

## Phase B: KPI集計

### Step 5: 集計指示書を作成する

```markdown
# KPI集計指示書

status: draft
author: {anima名}
date: {YYYY-MM-DD}
type: kpi-summary

## 集計目的
{定期報告 / 特定課題の分析}

## 集計期間
{直近24h / 直近1週間 / 月次}

## 入力データ
{activity_log の抜粋、task_queue の統計、org_dashboard の数値等}

## 集計項目
- 部門別活動量（tool_use 回数、メッセージ送受信数）
- タスク消化率（完了 / 進行中 / STALE / OVERDUE）
- エラー率（error タイプのアクティビティ数 / 全アクティビティ数）
- 部門別応答時間（DM 受信→返信の平均所要時間）
- {追加の組織固有KPI}
```

### Step 6: machine に集計を依頼する

指示書に基づき machine に集計を依頼する。
結果を `state/plans/{date}_{概要}.kpi-summary.md` として保存する。

### Step 7: COO が検証する

machine の集計結果を検証する:
- [ ] 集計対象期間が正しいか
- [ ] 数値に明らかな異常（桁違い、マイナス値等）がないか
- [ ] 全部門がカバーされているか

---

## Phase C: 報告書ドラフト

### Step 8: 報告書指示を作成する

Phase A + B の結果を入力として、人間向けレポートのドラフト作成を指示する。

```markdown
# 報告書ドラフト指示

status: draft
author: {anima名}
date: {YYYY-MM-DD}
type: report-draft

## 報告種別
{日次ダイジェスト / 週次振り返り / 月次戦略レビュー / 臨時報告}

## 入力
- 組織分析結果: state/plans/{org-analysis ファイル}
- KPI集計結果: state/plans/{kpi-summary ファイル}

## 報告フォーマット
### 経営サマリー（3〜5行）
{全体の状況を簡潔に}

### 部門別詳細
{部門ごとの主要トピック}

### 注意事項・リスク
{要注意の案件、エスカレーションが必要な事項}

### アクションアイテム
{COOとして実行する / 実行予定のアクション}
```

### Step 9: machine にドラフト作成を依頼する

結果を `state/plans/{date}_{概要}.report-draft.md` として保存する。

### Step 10: COO が判断コメントを追加する

machine のドラフトに以下を追加する（MUST）:
- COO 自身の状況判断・所見
- 人間へのアクションアイテム提案
- エスカレーションが必要な事項の明示

### Step 11: 報告・配信

- `call_human` で人間に報告する
- 正式な書類が必要な場合は秘書に PDF 化を依頼する（`send_message`）

---

## 制約事項

- 組織分析の「判断」はCOO自身が行う（MUST）。machine の出力をそのまま判断として扱わない
- 人間への報告にはCOO自身の判断コメントを必ず付加する（MUST）
- machine の出力に個人情報・機密情報が含まれる場合、外部配信時は削除・マスクする（MUST）
- 監査結果を改変してから報告しない（NEVER）。内部監査の独立性を担保する
