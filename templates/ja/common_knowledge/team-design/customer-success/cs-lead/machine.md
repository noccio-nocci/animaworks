# CS Lead — machine 活用パターン

## 基本ルール

1. **計画書を先に書く** — インラインの短い指示文字列での実行は禁止。計画書ファイルを渡す
2. **出力はドラフト** — machine の出力は必ず自分で検証し、`status: approved` にしてから次工程へ
3. **保存場所**: `state/plans/{YYYY-MM-DD}_{概要}.{type}.md`（`/tmp/` 禁止）
4. **レート制限**: chat 5回/session、heartbeat 2回
5. **machine はインフラにアクセスできない** — 記憶・メッセージ・組織情報は計画書に含めること

---

## 概要

CS Lead は PdM（計画・判断）と Engineer（実行）を兼務する。4つのフェーズで machine を活用する。

- Phase A: cs-handoff.md を分析し、オンボーディング計画を策定 → CS Lead が検証
- Phase B: Health Tracker + 問い合わせ履歴を分析し、チャーン予測・介入推奨 → CS Lead が判断
- Phase C: リテンション施策・対応コンテンツを制作 → CS Lead が検証
- Phase D: VoC（顧客の声）を集約し、プロダクトフィードバックレポートを作成 → CS Lead が確定

---

## Phase A: オンボーディング分析・計画

### Step 1: cs-handoff.md を受け取り確認する

営業 Director から `cs-handoff.md`（`status: draft`）を受け取る。全セクション（顧客概要、営業プロセス要約、合意事項、未解決事項、コミュニケーション特性）を確認する。

### Step 2: オンボーディング計画指示書を作成する（CS Lead 自身が書く）

オンボーディングの目的・顧客特性に基づく重点事項・スコープを明確にした指示書を作成する。

```bash
write_memory_file(path="state/plans/{date}_{企業名}.onboarding-request.md", content="...")
```

**指示書の「オンボーディング目的」「重点事項」「スコープ」は CS Lead の判断の核であり、machine に書かせてはならない（NEVER）。**

### Step 3: machine にオンボーディング計画を投げる

指示書 + cs-handoff.md の内容を入力として、オンボーディング計画の策定を machine に依頼する。

```bash
animaworks-tool machine run \
  "$(cat $ANIMAWORKS_ANIMA_DIR/state/plans/{onboarding-request.md})" \
  -d /path/to/workspace
```

結果を `state/plans/{date}_{企業名}.onboarding-plan.md` として保存する（`status: draft`）。

### Step 4: onboarding-plan.md を検証する

CS Lead が checklist セクション A に沿って検証する:
- [ ] cs-handoff.md の全項目がカバーされているか
- [ ] 合意事項・要望が具体的なステップに落ちているか
- [ ] 未解決事項に対する対応方針が含まれているか
- [ ] コミュニケーション特性が考慮されているか

問題があれば CS Lead 自身が修正し、`status: approved` に変更する。

### Step 5: Support に委譲する

`delegate_task` で `onboarding-plan.md`（`status: approved`）を Support に渡す。

---

## Phase B: 顧客ヘルス分析

### Step 6: ヘルス分析指示書を作成する（CS Lead 自身が書く）

Health Tracker の現状 + 直近の問い合わせ履歴を整理した指示書を作成する。

```bash
write_memory_file(path="state/plans/{date}_health-analysis-request.md", content="...")
```

### Step 7: machine にヘルス分析を投げる

指示書を入力として、ヘルススコアの算出・チャーン予測・介入推奨を machine に依頼する。

```bash
animaworks-tool machine run \
  "$(cat $ANIMAWORKS_ANIMA_DIR/state/plans/{health-analysis-request.md})" \
  -d /path/to/workspace
```

結果を `state/plans/{date}_health-analysis.md` として保存する（`status: draft`）。

### Step 8: 分析結果に基づいて判断する

CS Lead が machine の分析結果を確認し、アクションを決定する:
- Green → 経過観察。Health Tracker を更新
- Yellow → Phase C でリテンション施策を策定
- Red → 即座に Phase C + 上位にエスカレーション

**ヘルススコアの最終判定は CS Lead が確定する（machine の出力はドラフトとして検証する）。**

---

## Phase C: 対応コンテンツ制作

### Step 9: 対応指示書を作成する（CS Lead 自身が書く）

対応が必要な顧客・状況・目的を明確にした指示書を作成する。

```bash
write_memory_file(path="state/plans/{date}_{企業名}.retention-request.md", content="...")
```

**対応方針・トーン・目的は CS Lead の判断の核であり、machine に書かせてはならない（NEVER）。**

### Step 10: machine に対応コンテンツ制作を投げる

指示書を入力として、カスタマイズ対応ドラフトの作成を machine に依頼する。

対象コンテンツ例:
- リテンション施策提案書
- 顧客向け改善報告メール
- エスカレーション対応の要約・提案
- カスタマイズ支援ガイド

### Step 11: 成果物を検証する

CS Lead が checklist セクション C に沿って検証する:
- [ ] 顧客状況に適したカスタマイズがされているか
- [ ] トーンが適切か（コミュニケーション特性を考慮）
- [ ] コンプライアンス上の問題がないか

問題があれば CS Lead 自身が修正する。

---

## Phase D: VoC集約・プロダクトフィードバック

### Step 12: VoC 集約指示書を作成する（CS Lead 自身が書く）

対象期間の問い合わせパターン・顧客フィードバック・Support からの報告を整理した指示書を作成する。

```bash
write_memory_file(path="state/plans/{date}_voc-request.md", content="...")
```

### Step 13: machine に VoC 分析を投げる

指示書を入力として、傾向分析・インサイト抽出・改善提案を machine に依頼する。

結果を `state/plans/{date}_voc-report.md` として保存する（`status: draft`）。

### Step 14: VoC レポートを確定する

CS Lead が checklist セクション D に沿って検証する:
- [ ] 問い合わせ傾向が正確に反映されているか
- [ ] 改善提案に根拠があるか
- [ ] COO 報告の体裁が整っているか

確認後、`status: approved` に変更し、COO に `send_message (intent: report)` で送信する。

---

## ドキュメントテンプレート

### onboarding-plan.md

```markdown
# オンボーディング計画: {企業名}

status: draft
author: {anima名}
date: {YYYY-MM-DD}
type: onboarding-plan
source: cs-handoff.md

## 顧客概要（cs-handoff.md より）

{cs-handoff.md の要約}

## オンボーディング目標

{達成すべきゴール — 1〜3点}

## ステップ

| # | ステップ | 担当 | 期限 | 完了条件 |
|---|---------|------|------|---------|
| 1 | {内容} | {Support/CS Lead} | {日付} | {条件} |

## 重点事項

{cs-handoff.md の合意事項・要望に基づく重点}

## 未解決事項への対応

{cs-handoff.md の未解決事項に対する方針}

## コミュニケーション方針

{キーパーソンの特性に基づく対応方針}
```

### health-analysis.md

```markdown
# 顧客ヘルス分析: {対象期間}

status: draft
author: {anima名}
date: {YYYY-MM-DD}
type: health-analysis

## 分析対象

| # | 企業名 | 現在のスコア | 前回のスコア | 変化 |
|---|--------|------------|------------|------|
| CS-1 | {名称} | {Green/Yellow/Red} | {前回} | {↑/→/↓} |

## 要注意顧客

{Yellow/Red の顧客に対する分析と推奨アクション}

## チャーン予測

{チャーンリスクの高い顧客とその根拠}

## 推奨アクション

| 優先度 | 企業名 | アクション | 根拠 |
|--------|--------|----------|------|
| 高 | {名称} | {具体的アクション} | {根拠} |
```

### retention-action.md

```markdown
# リテンション施策: {企業名}

status: draft
author: {anima名}
date: {YYYY-MM-DD}
type: retention-action
health_score: {Yellow/Red}

## 現状分析

{顧客の現在の状況と課題}

## 施策内容

{具体的なリテンション施策}

## 期待効果

{施策実施後の期待効果}

## 顧客向けコミュニケーション案

{メール・提案の下書き}
```

### voc-report.md

```markdown
# VoC レポート: {対象期間}

status: draft
author: {anima名}
date: {YYYY-MM-DD}
type: voc-report
period: {YYYY-MM-DD} ~ {YYYY-MM-DD}

## サマリー

{主要トレンドの要約 — 3〜5点}

## 問い合わせ傾向

| カテゴリ | 件数 | 前期比 | 代表的な内容 |
|---------|------|--------|------------|
| {カテゴリ} | {N} | {↑/→/↓} | {内容} |

## 顧客フィードバック分析

### ポジティブ

{好評なポイント}

### ネガティブ

{不満・課題}

## 改善提案

| # | 提案 | 根拠 | 影響範囲 | 優先度 |
|---|------|------|---------|--------|
| 1 | {提案内容} | {VoC データの根拠} | {影響する顧客数/セグメント} | {高/中/低} |

## 次回アクション

{COO・開発チームに求めるアクション}
```

---

## 制約事項

- cs-handoff.md の受領判断は CS Lead 自身が行う（MUST）
- ヘルススコアの最終判定は CS Lead が確定する（machine の出力はドラフトとして検証する）
- 対応方針・トーン・目的は CS Lead の判断の核であり、machine に書かせてはならない（NEVER）
- Health Tracker の項目を言及なしで消滅させてはならない（NEVER — silent drop 禁止）
