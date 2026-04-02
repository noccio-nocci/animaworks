# Strategy Coordinator — machine 活用パターン

## 基本ルール

1. **計画書を先に書く** — インラインの短い指示文字列での実行は禁止。計画書ファイルを渡す
2. **出力はドラフト** — machine の出力は必ず自分で検証し、`status: approved` にしてから次工程へ
3. **保存場所**: `state/plans/{YYYY-MM-DD}_{概要}.{type}.md`（`/tmp/` 禁止）
4. **レート制限**: chat 5回/session、heartbeat 2回
5. **machine はインフラにアクセスできない** — 記憶・メッセージ・組織情報は計画書に含めること

---

## 概要

Coordinator は **machine に検証スキャンを委託し、そのスキャン結果の正当性を検証する（メタ検証）**。

- 検証観点の設計 → Coordinator 自身が判断
- 仮定の検証・KPI整合チェック・Tracker照合の実行 → machine に委託
- 検出結果の正当性検証 → Coordinator 自身が判断
- 実行可能性の最終判断 → Coordinator 自身が判断

machine はデータの整合チェック・仮定の論理検証・Tracker の照合を高速に行えるが、
実行可能性の総合判断や組織的制約の評価は Coordinator の責務である。

---

## ワークフロー

### Step 1: 検証計画書を作成する（Coordinator 自身が書く）

検証の観点・対象・基準を明確にした計画書を作成する。

```bash
write_memory_file(path="state/plans/{date}_{テーマ}.verification.md", content="...")
```

作成前に以下の情報を Anima 側で準備する:
- Strategist の `strategy-report.md` と `strategic-plan.md`
- Strategic Initiative Tracker（前回との比較用）
- 関連する KPI データ（部門から収集）

### Step 2: machine に検証スキャンを投げる

```bash
animaworks-tool machine run \
  "$(cat $ANIMAWORKS_ANIMA_DIR/state/plans/{verification計画書})" \
  -d /path/to/workspace
```

結果を `state/plans/{date}_{テーマ}.verification-result.md` に保存する（`status: draft`）。

### Step 3: 検証結果をメタ検証する

Coordinator が verification-result.md を読み、以下を確認する:

- [ ] 仮定チャレンジの結果は論理的か（machine の指摘が的を射ているか）
- [ ] KPI 整合チェックのデータソースが正確か
- [ ] Tracker 照合に漏れがないか
- [ ] 誤検出（False Positive）がないか
- [ ] Coordinator 自身の観点で追加すべき指摘がないか

Coordinator 自身が修正・補足し、実行可能性の最終判断を加える。

### Step 4: verification-report.md を作成する

メタ検証済みの結果を verification-report.md にまとめ、`status: approved` に変更する。
approved の verification-report.md を Strategist に送付する。

---

## 検証計画書テンプレート（verification-plan.md）

```markdown
# 検証計画書: {検証対象の概要}

status: draft
author: {anima名}
date: {YYYY-MM-DD}
type: verification-plan

## 検証観点

- [ ] 仮定チャレンジ: Strategist の前提仮定に対する反証的検証
- [ ] KPI整合: 各部門の KPI 実態と戦略目標の乖離確認
- [ ] Tracker照合: Strategic Initiative Tracker の全件ステータス更新確認
- [ ] データソース検証: 市場分析レポートのソース信頼性チェック
- [ ] 実行可能性: リソース・期間・組織体制の制約との整合

## 対象

- strategy-report.md: {パス}
- strategic-plan.md: {パス}
- Strategic Initiative Tracker: {パス}
- KPI データ: {ソース / 格納場所}

## 出力形式（必須）

以下の形式で検証結果を出力すること。**この形式に従わない出力は無効とする。**

- **Critical**: 修正必須の問題（仮定崩壊・KPI乖離・silent drop）
- **Warning**: 修正推奨の問題（根拠不足・データ鮮度）
- **Info**: 情報提供・改善提案
```

## 検証報告書テンプレート（verification-report.md）

```markdown
# 検証報告書: {テーマ}

status: draft
author: {anima名}
date: {YYYY-MM-DD}
type: verification-report

## 総合判定

{APPROVE / REQUEST_CHANGES / COMMENT}

## 仮定チャレンジ結果

| # | 仮定 | Strategist の根拠 | 検証結果 | 最悪シナリオ | 推奨 |
|---|------|-----------------|---------|------------|------|
| 1 | {仮定} | {根拠} | {妥当/根拠不足/崩壊} | {仮定が崩れた場合} | {修正案} |

## KPI 整合チェック

| # | KPI | 戦略目標 | 実態値 | 乖離 | 判定 |
|---|-----|---------|--------|------|------|
| 1 | {KPI名} | {目標} | {実態} | {乖離幅} | {OK / NG} |

## Tracker 照合

| # | イニシアチブ | 前回ステージ | 今回ステージ | 停滞 | 判定 |
|---|------------|------------|------------|------|------|
| 1 | {名称} | {前回} | {今回} | {Y/N} | {OK / 要対応} |

## Coordinator 所見

{Coordinator 自身の分析・追加観察・推奨事項}
- 実行可能性の総合評価
- 組織的制約の考慮
- 各部門への施策伝達時の留意点
```

---

## 制約事項

- 検証計画書（何を観点に検証するか）は MUST: Coordinator 自身が書く
- machine の検証結果をそのまま Strategist に渡してはならない（NEVER） — 必ず Coordinator がメタ検証する
- `status: approved` でない verification-report.md を Strategist にフィードバックしてはならない（NEVER）
- 実行可能性の最終判断は machine に任せず Coordinator 自身が行う（MUST）
