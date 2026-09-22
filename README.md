# RSS News Collection System

GitHub Actionsを使用して定期的にニュースを収集し、リポジトリにMarkdown形式で保存する仕組みです。
専用のRSSリーダーを導入せず、GitHubリポジトリを正本（Source of Truth）とすることで、履歴管理、検索、およびLLMによる後処理を容易にします。

## 🏗 設計 (Architecture)

### 全体フロー
**RSS/Atomフィード** $\rightarrow$ **GitHub Actions (Python)** $\rightarrow$ **Markdownファイル** $\rightarrow$ **GitHubリポジトリ**

### ディレクトリ構成
```text
.
├── .github/workflows/
│   └── daily-rss.yml      # 定期実行スケジュールと処理フロー
├── feeds/
│   ├── sources.yaml       # 購読フィードのURLとカテゴリ設定
│   ├── state/
│   │   └── seen.json      # 既読記事のGUIDを保存し、重複取得を防止
│   ├── articles/          # 日次アーカイブ (YYYY/MM/YYYY-MM-DD.md)
│   └── digests/           # カテゴリ別ダイジェスト (YYYY-MM-DD.md)
├── scripts/
│   ├── fetch_rss.py       # フィードの取得とフィルタリング
│   └── generate_digest.py # Markdown形式への整形
└── requirements.txt       # 必要ライブラリ (feedparser, PyYAML等)
```

### 設計のポイント
- **ステート管理**: `seen.json` を利用して記事の重複排除を行い、差分のみを保存します。
- **Markdown形式**: Obsidianや各種LLMと親和性の高い形式で保存し、後から要約やタグ付けがしやすい構成にしています。
- **疎結合**: 「取得 (Fetch)」と「整形 (Generate)」を分けることで、将来的にLLMによる要約ステップを間に入れやすくしています。

## 🚀 使い方 (Usage)

### 1. フィードの追加・変更
`feeds/sources.yaml` に購読したいRSSフィードを追加してください。

```yaml
sources:
  - name: "サイト名"
    url: "https://example.com/rss"
    category: "カテゴリ名 (例: AI, 量子計算)"
    tags: ["タグ1", "タグ2"]
```

### 2. ニュースの収集
- **自動実行**: GitHub Actionsにより、毎日定刻（デフォルト 8:00 UTC）に自動的に実行されます。
- **手動実行**: GitHubリポジトリの `Actions` タブ $\rightarrow$ `Daily RSS Digest` $\rightarrow$ `Run workflow` からいつでも実行可能です。

### 3. 収集結果の確認
実行後、以下のファイルが自動的に生成・更新されます。
- `feeds/articles/`: 取得した記事の全量ログ
- `feeds/digests/`: カテゴリ別に整理されたその日のニュースまとめ

## 🛠 ローカルでの開発・テスト

依存ライブラリをインストールして、スクリプトを直接実行できます。

```bash
pip install -r requirements.txt
python scripts/fetch_rss.py       # 記事の取得
python scripts/generate_digest.py # ダイジェストの生成
```

## 🗺 今後の拡張計画 (Roadmap)
- [ ] **LLM要約**: 収集した記事をClaude等で要約し、ダイジェストに反映させる。
- [ ] **重要度フィルタ**: キーワードやLLMを用いて重要記事のみを抽出する。
- [ ] **通知連携**: 生成されたダイジェストをSlackやDiscordに通知する。
- [ ] **公開**: GitHub Pagesを用いて、ダイジェストをWebページとして公開する。
