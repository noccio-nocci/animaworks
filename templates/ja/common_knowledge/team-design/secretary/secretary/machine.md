# Secretary — machine 活用パターン

## 基本ルール

1. **人間の指示が先** — 書類作成は人間の依頼を起点とする。自主的な書類作成は原則行わない
2. **出力はドラフト** — machine の出力は必ず自分で検証し、人間に提示してから配信する
3. **保存場所**: `state/plans/{YYYY-MM-DD}_{概要}.{type}.md`（`/tmp/` 禁止）
4. **レート制限**: chat 5回/session、heartbeat 2回
5. **machine はインフラにアクセスできない** — 必要な情報（宛先、会社情報等）は指示文に含めること

---

## 概要

Secretary は情報トリアージ・代行送信を主務とし、書類作成・PDF化を machine に委託する。

- ビジネス文書の作成 → machine が生成し、Secretary が検証
- レポート整形・PDF化 → machine が変換し、Secretary が品質確認
- 人間に提示し、承認後に配信する

---

## Phase A: ビジネス文書作成

### Step 1: 人間の指示を確認する

人間から書類作成の依頼を受け、以下を明確にする:
- 文書の種類（契約書・レター・報告書・議事録等）
- 宛先・必要な情報
- 期限・フォーマット要件

不明点がある場合はチャットで人間に確認する（推測で進めない）。

### Step 2: machine に文書作成を依頼する

指示文を作成し、machine に委託する。

```bash
animaworks-tool machine run \
  "$(cat $ANIMAWORKS_ANIMA_DIR/state/plans/{指示文ファイル})" \
  -d /path/to/workspace
```

結果を `state/plans/{date}_{概要}.document.md` として保存する。

**指示文に含めるべき情報**:
- 文書の種類・目的
- 宛先の正式名称・敬称
- 本文に含めるべき事項
- フォーマット指定（ビジネスレター形式、報告書形式等）
- 署名欄の情報

### Step 3: 品質チェック

Secretary が `checklist.md` セクション C に沿って検証する:

- [ ] 事実の誤記がないか（人名・会社名・法人形態・日付・金額）
- [ ] 宛先・敬称が正しいか
- [ ] 依頼内容が漏れなく反映されているか
- [ ] 不適切な表現がないか

問題があれば Secretary 自身が修正する。

### Step 4: 人間に提示する

検証済みの文書を人間にチャットで提示し、承認を求める。

---

## Phase B: レポート整形・PDF化

### Step 5: 入力を準備する

Markdown / テキストを入力として、machine に整形・レイアウト調整を依頼する。

### Step 6: machine に整形を依頼する

整形指示を作成し、machine に委託する。

結果を `state/plans/{date}_{概要}.formatted.md` として保存する。

### Step 7: PDF 変換

整形済みドキュメントを PDF に変換する。

**docx 生成の場合**:
```bash
python3 -c "
from docx import Document
doc = Document()
# ... ドキュメント生成コード
doc.save('/path/to/output.docx')
"
```

**MD → HTML → PDF の場合**:
```bash
pandoc input.md -o output.html --standalone
python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('file:///path/to/output.html')
    page.pdf(path='/path/to/output.pdf')
    browser.close()
"
```

### Step 8: PDF 品質確認

生成された PDF を全ページ確認する（MUST）:
- [ ] レイアウトが崩れていないか
- [ ] 文字化け・フォント欠落がないか
- [ ] ページ分割が適切か
- [ ] ヘッダー・フッターが正しいか

### Step 9: 人間に提示・配信

品質確認済みの PDF を人間に提示し、承認後に URL を配信する。

---

## ドキュメントテンプレート

### ビジネスレター

```markdown
# {文書タイトル}

status: draft
author: {anima名}
date: {YYYY-MM-DD}
type: business-letter

## 宛先

{宛先の正式名称}
{部署・役職}
{担当者名} 様

## 本文

{本文}

## 署名

{署名欄}
```

### 報告書

```markdown
# {報告書タイトル}

status: draft
author: {anima名}
date: {YYYY-MM-DD}
type: report

## 概要

{1〜3文の要旨}

## 詳細

{本文}

## 添付資料

{添付がある場合}
```

---

## 制約事項

- 機密情報を含むドキュメントの外部配信は人間の承認なしに行わない（NEVER）
- 法人情報（住所・代表者名・法人番号等）は事前に人間に確認してから記載する（MUST）
- PDF 生成後は必ず全ページ読み確認する（MUST）
- 人間の承認前にドキュメントを外部に配信しない（NEVER）
