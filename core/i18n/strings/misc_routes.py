# AnimaWorks - Digital Anima Framework
# Copyright (C) 2026 AnimaWorks Authors
# SPDX-License-Identifier: Apache-2.0
#
# This file is part of AnimaWorks core/server, licensed under Apache-2.0.
# See LICENSE for the full license text.

"""Domain-specific i18n strings (brainstorm.*, preset.*)."""

from __future__ import annotations

STRINGS: dict[str, dict[str, str]] = {
    "brainstorm.char.challenger": {
        "ja": "挑戦派",
        "en": "Challenger",
    },
    "brainstorm.char.challenger.desc": {
        "ja": "革新・成長・破壊的イノベーションの視点から提案します",
        "en": "Proposes from innovation, growth, and disruptive perspectives",
    },
    "brainstorm.char.challenger.prompt": {
        "ja": (
            "あなたは「挑戦派」のブレスト参加者です。\n既存の枠組みにとらわれず、革新的・破壊的なアイデアを提案します。\n「なぜ今までのやり方を変えないのか？」という視点で切り込んでください。\n大胆な提案を恐れず、成長機会を最大化する方向で考えてください。\n出力はMarkdown形式で、見出し・箇条書きを使って構造化してください。"
        ),
        "en": (
            "You are a 'Challenger' brainstorm participant.\nPropose innovative and disruptive ideas beyond existing frameworks.\nChallenge the status quo: 'Why not change the current approach?'\nBe bold and maximize growth opportunities.\nOutput in Markdown with headings and bullet points."
        ),
    },
    "brainstorm.char.customer": {
        "ja": "顧客視点",
        "en": "Customer Advocate",
    },
    "brainstorm.char.customer.desc": {
        "ja": "UX・ユーザー体験・顧客価値の視点から評価します",
        "en": "Evaluates from UX, user experience, and customer value perspectives",
    },
    "brainstorm.char.customer.prompt": {
        "ja": (
            "あなたは「顧客視点」のブレスト参加者です。\n常にエンドユーザーの体験・満足度・価値を最優先に考えます。\n「ユーザーはこれを使って何が嬉しいのか？」を軸に提案してください。\nペルソナやユースケースを具体的に描写し、UXの改善点を指摘してください。\n出力はMarkdown形式で、見出し・箇条書きを使って構造化してください。"
        ),
        "en": (
            "You are a 'Customer Advocate' brainstorm participant.\nAlways prioritize end-user experience, satisfaction, and value.\nCenter proposals around 'What makes users happy about this?'\nDescribe specific personas and use cases, and point out UX improvements.\nOutput in Markdown with headings and bullet points."
        ),
    },
    "brainstorm.char.engineer": {
        "ja": "実装視点",
        "en": "Technical Implementer",
    },
    "brainstorm.char.engineer.desc": {
        "ja": "技術的実現性・アーキテクチャ・運用負荷の視点から検討します",
        "en": ("Examines from technical feasibility, architecture, and operational load perspectives"),
    },
    "brainstorm.char.engineer.prompt": {
        "ja": (
            "あなたは「実装視点」のブレスト参加者です。\n技術的な実現可能性・アーキテクチャ・運用負荷・スケーラビリティを重視します。\n「これは技術的にどう実装するか？」「運用でどこがボトルネックか？」を分析してください。\n技術スタック・工数見積・技術的リスクを具体的に示してください。\n出力はMarkdown形式で、見出し・箇条書きを使って構造化してください。"
        ),
        "en": (
            "You are a 'Technical Implementer' brainstorm participant.\nFocus on technical feasibility, architecture, operational load, and scalability.\nAnalyze 'How to implement this technically?' and 'Where are operational bottlenecks?'\nProvide specific tech stacks, effort estimates, and technical risks.\nOutput in Markdown with headings and bullet points."
        ),
    },
    "brainstorm.char.realist": {
        "ja": "現実派",
        "en": "Realist",
    },
    "brainstorm.char.realist.desc": {
        "ja": "収益・ROI・コスト・リスクの視点から分析します",
        "en": "Analyzes from revenue, ROI, cost, and risk perspectives",
    },
    "brainstorm.char.realist.prompt": {
        "ja": (
            "あなたは「現実派」のブレスト参加者です。\n常に収益性・ROI・コスト・リスクの観点から提案を行います。\n理想論よりも実行可能性と投資対効果を重視してください。\n提案は具体的な数値やスケジュール感を含めてください。\n出力はMarkdown形式で、見出し・箇条書きを使って構造化してください。"
        ),
        "en": (
            "You are a 'Realist' brainstorm participant.\nAlways propose from revenue, ROI, cost, and risk perspectives.\nPrioritize feasibility and return on investment over ideals.\nInclude specific numbers and timelines in your proposals.\nOutput in Markdown with headings and bullet points."
        ),
    },
    "brainstorm.invalid_model": {
        "ja": "無効なモデルが指定されました",
        "en": "Invalid model specified",
    },
    "brainstorm.no_characters_selected": {
        "ja": "キャラクターが選択されていません",
        "en": "No characters selected",
    },
    "brainstorm.no_constraints": {
        "ja": "特になし",
        "en": "None specified",
    },
    "brainstorm.no_expected_output": {
        "ja": "特になし",
        "en": "None specified",
    },
    "brainstorm.no_model_configured": {
        "ja": "LLMモデルが設定されていません",
        "en": "No LLM model configured",
    },
    "brainstorm.synthesizer_prompt": {
        "ja": (
            "あなたはブレストの統合者です。\n複数の視点からの提案を受け取り、以下の規定フォーマットで整理・統合してください。\n\n## 出力フォーマット（必ずこの5セクション構成で出力すること）\n### 論点\n主要な論点・議論ポイントを箇条書きで列挙\n\n### 案\n各視点からの主要な提案をまとめる\n\n### 比較\n提案の比較表（Markdownテーブル形式。軸: 実現性/コスト/インパクト/リスク）\n\n### 推奨案\n総合的に最も推奨される案とその理由\n\n### 次アクション\n具体的な次のステップを箇条書きで列挙"
        ),
        "en": (
            "You are a brainstorm synthesizer.\nReceive proposals from multiple perspectives and organize them into the following format.\n\n## Output Format (must include all 5 sections)\n### Key Issues\nList main discussion points as bullet points\n\n### Proposals\nSummarize main proposals from each perspective\n\n### Comparison\nComparison table in Markdown (axes: Feasibility/Cost/Impact/Risk)\n\n### Recommendation\nThe overall recommended proposal and reasoning\n\n### Next Actions\nList concrete next steps as bullet points"
        ),
    },
    "brainstorm.synthesizer_user_prompt": {
        "ja": ("テーマ「{theme}」について、以下の各視点からの提案を統合してください。\n\n{proposals}"),
        "en": ('Synthesize the following proposals from multiple perspectives on the theme: "{theme}"\n\n{proposals}'),
    },
    "brainstorm.user_prompt": {
        "ja": (
            "以下のテーマについて、あなたの視点から提案・分析してください。\n\n## テーマ\n{theme}\n\n## 制約条件\n{constraints}\n\n## 期待するアウトプット\n{expected_output}"
        ),
        "en": (
            "Provide your analysis and proposals on the following theme.\n\n## Theme\n{theme}\n\n## Constraints\n{constraints}\n\n## Expected Output\n{expected_output}"
        ),
    },
    "preset.consulting_dev": {
        "ja": "受託開発プロジェクトチーム",
        "en": "Consulting Project Team",
    },
    "preset.consulting_dev.desc": {
        "ja": "受託案件の提案・設計・推進に最適なチーム",
        "en": "Team for consulting project proposal, design, and execution",
    },
    "preset.consulting_research": {
        "ja": "リサーチ・分析チーム",
        "en": "Research & Analysis Team",
    },
    "preset.consulting_research.desc": {
        "ja": "市場調査・データ分析・レポート作成を担うチーム",
        "en": "Team for market research, data analysis, and reporting",
    },
    "preset.ec_dev": {
        "ja": "EC新規立ち上げチーム",
        "en": "E-Commerce Launch Team",
    },
    "preset.ec_dev.desc": {
        "ja": "ECサイトの立ち上げ・商品準備・販売戦略を担うチーム",
        "en": "Team for e-commerce launch, product setup, and sales strategy",
    },
    "preset.ec_ops": {
        "ja": "EC運用チーム",
        "en": "E-Commerce Operations Team",
    },
    "preset.ec_ops.desc": {
        "ja": "受注処理・在庫管理・カスタマー対応の運用チーム",
        "en": "Team for order processing, inventory management, and customer support",
    },
    "preset.general_dev": {
        "ja": "プロジェクト推進チーム",
        "en": "Project Execution Team",
    },
    "preset.general_dev.desc": {
        "ja": "業種を問わない汎用的なプロジェクト推進チーム",
        "en": "General-purpose project execution team",
    },
    "preset.general_ops": {
        "ja": "バックオフィスチーム",
        "en": "Back Office Team",
    },
    "preset.general_ops.desc": {
        "ja": "総務・経理・事務を中心としたバックオフィス運用チーム",
        "en": "Back office operations team for admin, accounting, and general affairs",
    },
    "preset.industry.consulting": {
        "ja": "受託開発・コンサルティング",
        "en": "Consulting",
    },
    "preset.industry.ec": {
        "ja": "EC・物販",
        "en": "E-Commerce",
    },
    "preset.industry.general": {
        "ja": "一般・その他",
        "en": "General",
    },
    "preset.industry.saas": {
        "ja": "SaaS",
        "en": "SaaS",
    },
    "preset.purpose.new_development": {
        "ja": "新規開発",
        "en": "New Development",
    },
    "preset.purpose.operations": {
        "ja": "運用改善",
        "en": "Operations",
    },
    "preset.purpose.research": {
        "ja": "調査・リサーチ",
        "en": "Research",
    },
    "preset.saas_dev": {
        "ja": "SaaS新規開発チーム",
        "en": "SaaS Development Team",
    },
    "preset.saas_dev.desc": {
        "ja": "SaaS製品の企画・開発・ローンチに最適なチーム構成",
        "en": "Optimal team for SaaS product planning, development, and launch",
    },
    "preset.saas_ops": {
        "ja": "SaaS運用チーム",
        "en": "SaaS Operations Team",
    },
    "preset.saas_ops.desc": {
        "ja": "SaaS製品のカスタマーサポート・運用を担うチーム",
        "en": "Team for SaaS customer support and operations",
    },
    "preset.task.analysis_framework": {
        "ja": "分析フレームワーク設計",
        "en": "Design analysis framework",
    },
    "preset.task.background_research": {
        "ja": "背景調査・情報収集",
        "en": "Background research",
    },
    "preset.task.benchmark_study": {
        "ja": "ベンチマーク調査",
        "en": "Conduct benchmark study",
    },
    "preset.task.budget_draft": {
        "ja": "予算案作成",
        "en": "Draft budget",
    },
    "preset.task.calendar_coord": {
        "ja": "カレンダー・予定調整",
        "en": "Calendar coordination",
    },
    "preset.task.client_analysis": {
        "ja": "クライアント要件分析",
        "en": "Analyze client requirements",
    },
    "preset.task.comm_plan": {
        "ja": "コミュニケーション計画策定",
        "en": "Create communication plan",
    },
    "preset.task.competitor_analysis": {
        "ja": "競合分析レポート作成",
        "en": "Create competitor analysis report",
    },
    "preset.task.compliance_check": {
        "ja": "コンプライアンスチェック",
        "en": "Compliance check",
    },
    "preset.task.cs_playbook": {
        "ja": "CS対応マニュアル作成",
        "en": "Create CS playbook",
    },
    "preset.task.customer_inquiry": {
        "ja": "顧客問い合わせ対応",
        "en": "Handle customer inquiries",
    },
    "preset.task.daily_ops_check": {
        "ja": "日次業務チェック",
        "en": "Daily operations check",
    },
    "preset.task.data_collection": {
        "ja": "データ収集・整理",
        "en": "Collect and organize data",
    },
    "preset.task.document_mgmt": {
        "ja": "文書管理・整理",
        "en": "Document management",
    },
    "preset.task.escalation_flow": {
        "ja": "エスカレーションフロー定義",
        "en": "Define escalation flow",
    },
    "preset.task.exec_summary": {
        "ja": "エグゼクティブサマリー作成",
        "en": "Create executive summary",
    },
    "preset.task.expense_tracking": {
        "ja": "経費管理・精算",
        "en": "Expense tracking",
    },
    "preset.task.faq_draft": {
        "ja": "FAQ・ヘルプドキュメント作成",
        "en": "Draft FAQ and help documents",
    },
    "preset.task.feasibility_study": {
        "ja": "実現性調査",
        "en": "Feasibility study",
    },
    "preset.task.findings_report": {
        "ja": "調査結果レポート作成",
        "en": "Create findings report",
    },
    "preset.task.industry_report": {
        "ja": "業界動向レポート作成",
        "en": "Create industry trend report",
    },
    "preset.task.inventory_check": {
        "ja": "在庫確認・補充管理",
        "en": "Inventory check and replenishment",
    },
    "preset.task.kickoff_prep": {
        "ja": "キックオフ準備",
        "en": "Prepare project kickoff",
    },
    "preset.task.knowledge_base": {
        "ja": "ナレッジベース整備",
        "en": "Build knowledge base",
    },
    "preset.task.kpi_setup": {
        "ja": "KPI設定・ダッシュボード構築",
        "en": "Set up KPIs and dashboard",
    },
    "preset.task.launch_checklist": {
        "ja": "ローンチチェックリスト作成",
        "en": "Create launch checklist",
    },
    "preset.task.literature_review": {
        "ja": "文献レビュー・先行調査",
        "en": "Conduct literature review",
    },
    "preset.task.market_research": {
        "ja": "市場調査の実施",
        "en": "Conduct market research",
    },
    "preset.task.meeting_minutes": {
        "ja": "議事録テンプレート整備",
        "en": "Prepare meeting minutes template",
    },
    "preset.task.meeting_setup": {
        "ja": "定例会議セットアップ",
        "en": "Set up recurring meetings",
    },
    "preset.task.metrics_dashboard": {
        "ja": "メトリクスダッシュボード構築",
        "en": "Build metrics dashboard",
    },
    "preset.task.milestone_plan": {
        "ja": "マイルストーン計画策定",
        "en": "Plan milestones",
    },
    "preset.task.monthly_close": {
        "ja": "月次決算準備",
        "en": "Monthly closing preparation",
    },
    "preset.task.onboarding_flow": {
        "ja": "オンボーディングフロー設計",
        "en": "Design onboarding flow",
    },
    "preset.task.order_processing": {
        "ja": "受注処理フロー構築",
        "en": "Build order processing flow",
    },
    "preset.task.pricing_strategy": {
        "ja": "価格戦略策定",
        "en": "Define pricing strategy",
    },
    "preset.task.process_improvement": {
        "ja": "業務プロセス改善",
        "en": "Process improvement",
    },
    "preset.task.product_catalog": {
        "ja": "商品カタログ作成",
        "en": "Create product catalog",
    },
    "preset.task.project_charter": {
        "ja": "プロジェクト憲章作成",
        "en": "Create project charter",
    },
    "preset.task.promotion_plan": {
        "ja": "プロモーション計画策定",
        "en": "Plan promotions",
    },
    "preset.task.proposal_draft": {
        "ja": "提案書ドラフト作成",
        "en": "Draft proposal document",
    },
    "preset.task.refund_process": {
        "ja": "返金処理フロー整備",
        "en": "Set up refund process",
    },
    "preset.task.release_plan": {
        "ja": "リリース計画策定",
        "en": "Create release plan",
    },
    "preset.task.report_weekly": {
        "ja": "週次レポート作成",
        "en": "Create weekly report",
    },
    "preset.task.resource_plan": {
        "ja": "リソース計画策定",
        "en": "Plan resource allocation",
    },
    "preset.task.return_policy": {
        "ja": "返品ポリシー策定",
        "en": "Define return policy",
    },
    "preset.task.review_response": {
        "ja": "レビュー返信対応",
        "en": "Respond to reviews",
    },
    "preset.task.risk_assessment": {
        "ja": "リスクアセスメント実施",
        "en": "Conduct risk assessment",
    },
    "preset.task.roadmap_draft": {
        "ja": "プロダクトロードマップ策定",
        "en": "Draft product roadmap",
    },
    "preset.task.sales_report": {
        "ja": "売上レポート作成",
        "en": "Create sales report",
    },
    "preset.task.schedule_mgmt": {
        "ja": "スケジュール・カレンダー管理",
        "en": "Manage schedule and calendar",
    },
    "preset.task.scope_definition": {
        "ja": "スコープ定義書作成",
        "en": "Create scope definition",
    },
    "preset.task.seo_plan": {
        "ja": "SEO施策計画",
        "en": "Plan SEO strategy",
    },
    "preset.task.shipping_policy": {
        "ja": "配送ポリシー策定",
        "en": "Define shipping policy",
    },
    "preset.task.sla_monitor": {
        "ja": "SLA監視・レポート体制",
        "en": "Set up SLA monitoring and reporting",
    },
    "preset.task.stakeholder_briefing": {
        "ja": "ステークホルダー向けブリーフィング",
        "en": "Stakeholder briefing",
    },
    "preset.task.stakeholder_map": {
        "ja": "ステークホルダーマップ作成",
        "en": "Create stakeholder map",
    },
    "preset.task.supplier_coord": {
        "ja": "仕入先連携管理",
        "en": "Manage supplier coordination",
    },
    "preset.task.tax_filing": {
        "ja": "税務申告準備",
        "en": "Prepare tax filing",
    },
    "preset.task.ticket_triage": {
        "ja": "チケットトリアージ体制構築",
        "en": "Build ticket triage system",
    },
    "preset.task.timeline_draft": {
        "ja": "プロジェクトタイムライン作成",
        "en": "Draft project timeline",
    },
    "preset.task.trend_mapping": {
        "ja": "トレンドマッピング",
        "en": "Trend mapping",
    },
    "preset.task.user_persona": {
        "ja": "ユーザーペルソナ定義",
        "en": "Define user personas",
    },
    "preset.task.vendor_mgmt": {
        "ja": "取引先管理",
        "en": "Vendor management",
    },
}
