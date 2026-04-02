# Corporate Strategist — machine 活用パターン

## 基本ルール

1. **計画書を先に書く** — インラインの短い指示文字列での実行は禁止。計画書ファイルを渡す
2. **出力はドラフト** — machine の出力は必ず自分で検証し、`status: approved` にしてから次工程へ
3. **保存場所**: `state/plans/{YYYY-MM-DD}_{概要}.{type}.md`（`/tmp/` 禁止）
4. **レート制限**: chat 5回/session、heartbeat 2回
5. **machine はインフラにアクセスできない** — 記憶・メッセージ・組織情報は計画書に含めること

---

## 概要

Corporate Strategist は PdM（計画・判断）と Engineer（実行）を兼務する。

- 分析計画（strategic-plan.md）の作成 → Strategist 自身が書く
- 事業環境分析の実行 → machine に委託し、Strategist が検証
- リスク判断の確定 → Strategist 自身が判断
- 検証は2回: machine 分析結果の確認時と、Coordinator からのフィードバック統合時

---

## Phase A: 事業環境分析

### Step 1: Analyst の市場分析レポートを確認する

Analyst から `market-analysis.md`（`status: approved`）を受け取り、内容を把握する。

### Step 2: strategic-plan.md を作成する（Strategist 自身が書く）

分析の目的・対象・フレームワーク選択・内部データの所在を明確にした計画書を作成する。

```bash
write_memory_file(path="state/plans/{date}_{テーマ}.strategic-plan.md", content="...")
```

**strategic-plan.md の「分析目的」「フレームワーク選択」「スコープ」は Strategist の判断の核であり、machine に書かせてはならない（NEVER）。**

### Step 3: machine に事業環境分析を投げる

strategic-plan.md + market-analysis.md を入力として、事業環境の構造分析を machine に依頼する。

```bash
animaworks-tool machine run \
  "$(cat $ANIMAWORKS_ANIMA_DIR/state/plans/{strategic-plan.md})" \
  -d /path/to/workspace
```

machine が実行する分析:
- PEST / SWOT / 5Forces 等のフレームワーク分析
- 「勝てる領域」の抽出
- 機会/脅威の優先順位付け

結果を `state/plans/{date}_{テーマ}.strategy-report.md` として保存する（`status: draft`）。

### Step 4: strategy-report.md を検証する

Strategist が strategy-report.md を読み、`strategist/checklist.md` セクション A に沿って検証する。
問題があれば Strategist 自身が修正し、`status: reviewed` に変更する。

---

## Phase B: 戦略提案書ドラフト

### Step 5: machine に戦略提案書を依頼する

Phase A の分析結果 + OKR を入力として、戦略提案書のドラフトを machine に依頼する。

machine が生成する内容:
- 目標と施策の一覧
- リソース配分案
- リスク分析

結果を `state/plans/{date}_{テーマ}.strategic-proposal.md` として保存する（`status: draft`）。

### Step 6: 戦略提案書を検証する

Strategist が strategic-proposal.md を読み、`strategist/checklist.md` セクション B に沿って検証する。
OKR との整合性、施策の実行可能性、リソース配分の妥当性を確認する。

---

## Phase C: イニシアチブ進捗分析

### Step 7: machine に進捗分析を依頼する

Strategic Initiative Tracker のデータを入力として、進捗分析を machine に依頼する。

machine が実行する分析:
- 停滞イニシアチブの検知（1ヶ月以上ステージ変化なし）
- KPI 達成見込みの評価
- ボトルネック分析

### Step 8: 進捗分析を検証し判断する

Strategist が分析結果を読み、各イニシアチブについて判断する:
- **継続**: 計画通り進行
- **修正**: 施策を変更
- **中止**: 理由を記録して Tracker から除外

`strategist/checklist.md` セクション C に沿って Tracker の全件更新を確認する。

---

## 分析計画書テンプレート（strategic-plan.md）

```markdown
# 戦略分析計画書: {テーマ}

status: draft
author: {anima名}
date: {YYYY-MM-DD}
type: strategic-plan

## 分析目的

{何を明らかにするか — 1〜3文}

## 入力データ

| データ | ソース | 備考 |
|--------|--------|------|
| 市場分析レポート | Analyst: market-analysis.md | {パス} |
| 内部データ | {ソース} | {概要} |

## フレームワーク選択

{Strategist の判断で選択する}

- {フレームワーク1: 例 — PEST分析}
- {フレームワーク2: 例 — SWOT分析}

## 分析スコープ

{何を含め、何を除外するか}

## 出力形式

- 「勝てる領域」の抽出と優先順位
- 機会/脅威の評価マトリクス
- 戦略オプションの提示

## 期限

{deadline}
```

## 分析レポートテンプレート（strategy-report.md）

```markdown
# 戦略分析レポート: {テーマ}

status: draft
author: {anima名}
date: {YYYY-MM-DD}
type: strategy-report
source: state/plans/{元の strategic-plan.md}

## 総合評価

{事業環境の評価サマリー — 1〜3文}

## フレームワーク分析結果

### {フレームワーク名}

{分析結果}

## 「勝てる領域」

| # | 領域 | 根拠 | 優先度 | リスク |
|---|------|------|--------|--------|
| 1 | {領域名} | {根拠} | 高/中/低 | {リスク概要} |

## 機会/脅威の評価

| # | 項目 | 種別 | 影響度 | 対応方針 |
|---|------|------|--------|---------|
| 1 | {項目} | 機会/脅威 | 高/中/低 | {方針} |

## 追加コメント

{Strategist 自身の所見・補足}
```

## 戦略提案書テンプレート（strategic-proposal.md）

```markdown
# 戦略提案書: {テーマ}

status: draft
author: {anima名}
date: {YYYY-MM-DD}
type: strategic-proposal

## OKR との整合性

{対象 OKR と本提案の関係}

## 施策一覧

| # | 施策 | 目標 | リソース | 期限 | リスク |
|---|------|------|---------|------|--------|
| 1 | {施策名} | {達成目標} | {必要リソース} | {期限} | {リスク概要} |

## リソース配分

{全体のリソース配分方針}

## リスク分析

| # | リスク | 影響度 | 発生可能性 | 緩和策 |
|---|--------|--------|-----------|--------|
| 1 | {リスク} | 高/中/低 | 高/中/低 | {緩和策} |
```

---

## 制約事項

- strategic-plan.md は MUST: Strategist 自身が書く
- strategy-report のリスク判断は MUST: Strategist 自身が確定する（machine の出力はドラフトとして検証する）
- `status: reviewed` の付いていない strategy-report.md を Coordinator に渡してはならない（NEVER）
- Strategic Initiative Tracker に記録されたイニシアチブを言及なしで消滅させてはならない（NEVER — silent drop 禁止）
