# Business Analyst — machine 活用パターン

## 基本ルール

1. **計画書を先に書く** — インラインの短い指示文字列での実行は禁止。計画書ファイルを渡す
2. **出力はドラフト** — machine の出力は必ず自分で検証し、`status: approved` にしてから次工程へ
3. **保存場所**: `state/plans/{YYYY-MM-DD}_{概要}.{type}.md`（`/tmp/` 禁止）
4. **レート制限**: chat 5回/session、heartbeat 2回
5. **machine はインフラにアクセスできない** — 記憶・メッセージ・組織情報は計画書に含めること

---

## 概要

Business Analyst は外部ツール（web_search, x_search 等）で収集した生データを machine で構造化・分析する。

- 調査計画の作成 → Analyst 自身が書く
- 外部ツールによるデータ収集 → Analyst 自身が実行
- 収集データの構造化・分析 → machine に委託し、Analyst が検証
- 情報ソースの明記 → Analyst が最終確認

---

## Phase A: データ構造化

### Step 1: 生データを収集する

Strategist の調査依頼に基づき、web_search / x_search 等の外部ツールで生データを収集する。

### Step 2: 構造化計画書を作成する（Analyst 自身が書く）

構造化の目的・対象データ・分類軸を明確にした計画書を作成する。

```bash
write_memory_file(path="state/plans/{date}_{テーマ}.structuring-plan.md", content="...")
```

### Step 3: machine にデータ構造化を投げる

収集した生データ + 構造化計画書を入力として、machine にデータの構造化を依頼する。

```bash
animaworks-tool machine run \
  "$(cat $ANIMAWORKS_ANIMA_DIR/state/plans/{structuring-plan.md})" \
  -d /path/to/workspace
```

machine が実行する処理:
- データの分類・カテゴリ分け
- トレンド抽出
- 統計サマリー

結果を `state/plans/{date}_{テーマ}.market-analysis.md` として保存する（`status: draft`）。

### Step 4: market-analysis.md を検証する

Analyst が market-analysis.md を読み、`analyst/checklist.md` に沿って検証する:

- [ ] 全情報にソース（URL, 日付）が付いているか
- [ ] 事実と解釈が分離されているか
- [ ] machine が推測で補完した箇所がないか

問題があれば Analyst 自身が修正し、`status: approved` に変更する。

---

## Phase B: 競合分析

### Step 5: 競合情報を収集する

複数の競合について、断片的な情報（製品情報、価格、機能、組織情報等）を収集する。

### Step 6: machine に競合分析を投げる

収集した競合情報を入力として、構造化された競合分析を machine に依頼する。

machine が生成する内容:
- 比較マトリクス（機能・価格・市場ポジション）
- 各社の強み・弱み分析
- ポジショニングマップ

結果を `state/plans/{date}_{テーマ}.competitive-report.md` として保存する（`status: draft`）。

### Step 7: competitive-report.md を検証する

Analyst が competitive-report.md を読み、`analyst/checklist.md` に沿って検証する。
情報の正確性・ソースの信頼性を確認し、`status: approved` に変更する。

---

## 市場分析レポートテンプレート（market-analysis.md）

```markdown
# 市場分析レポート: {テーマ}

status: draft
author: {anima名}
date: {YYYY-MM-DD}
type: market-analysis
source: {Strategist の調査依頼パス}

## 調査サマリー

- 調査項目数: {N}
- 信頼度が高いソース: {N} / 信頼度が中程度: {N} / 未確認: {N}

## 情報ソース

| # | ソース | URL | 取得日 | 信頼度 |
|---|--------|-----|--------|--------|
| 1 | {ソース名} | {URL} | {日付} | 高/中/低 |

## 市場動向

{市場全体のトレンド分析}

## セグメント分析

{市場セグメントごとの分析}

## 主要な発見

{Strategist の戦略判断に影響する重要な発見を要約}

## 未確認事項

| # | 項目 | 未確認の理由 | 推奨アクション |
|---|------|------------|-------------|
| 1 | {項目} | {理由} | {次のステップ} |

## セルフチェック結果

- [ ] 全情報にソース付き
- [ ] 事実と解釈が分離
- [ ] データ鮮度を明記
```

## 競合分析レポートテンプレート（competitive-report.md）

```markdown
# 競合分析レポート: {テーマ}

status: draft
author: {anima名}
date: {YYYY-MM-DD}
type: competitive-report

## 比較マトリクス

| 項目 | 自社 | 競合A | 競合B | 競合C |
|------|------|-------|-------|-------|
| {機能1} | {評価} | {評価} | {評価} | {評価} |

## 各社分析

### {競合名}

- **強み**: {分析}
- **弱み**: {分析}
- **市場ポジション**: {分析}
- **最近の動向**: {分析}
- **ソース**: {URL, 日付}

## ポジショニング

{市場内でのポジショニング分析}

## 主要な発見

{Strategist の戦略判断に影響する競合の動向}
```

---

## 制約事項

- machine の出力をそのまま Strategist に納品してはならない（NEVER） — 必ず Analyst が検証する
- 情報ソースの明記は machine への指示に含める（MUST）
- 推測で情報を補完してはならない（NEVER） — 未確認事項は明示する
- `status: approved` でない market-analysis.md を Strategist にフィードバックしてはならない（NEVER）
