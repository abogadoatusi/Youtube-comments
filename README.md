# YouTube Comments Analyzer

YouTube動画のURLを入力すると、コメントを取得して分析できるWebアプリケーションです。

## 🚀 クイックスタート（簡単起動）

### 初回セットアップ（最初の1回のみ）

**Linux/Mac:**
```bash
./setup.sh
```

**Windows:**
```
setup.bat をダブルクリック
```

### アプリケーションの起動

**Linux/Mac:**
```bash
./start.sh
```

**Windows:**
```
start.bat をダブルクリック
```

起動後、ブラウザで `http://localhost:5000` にアクセス！

---

## 機能

- YouTube動画URLからコメントを取得
- コメントの統計情報表示（総コメント数、平均いいね数など）
- **年別コメント推移の分析とグラフ表示**
- 頻出ワードの分析
- コメント一覧の表示（人気コメント、最新コメント）
- **分析結果をデータベースに保存し、専用URLで管理**
- **分析履歴の閲覧と過去の分析結果へのアクセス**
- 分析結果の共有URL機能

## 詳細なセットアップ（手動セットアップの場合）

上記のクイックスタートで起動できない場合は、以下の手順で手動セットアップしてください。

1. 必要なパッケージをインストール:
```bash
pip install -r requirements.txt
```

2. YouTube Data API v3のAPIキーを取得:
   - [Google Cloud Console](https://console.cloud.google.com/)でプロジェクトを作成
   - YouTube Data API v3を有効化
   - APIキーを作成

3. `.env`ファイルを作成:
```bash
cp .env.example .env
```

4. `.env`ファイルにAPIキーを設定:
```
YOUTUBE_API_KEY=your_actual_api_key
```

5. アプリケーションを起動:
```bash
python app.py
```

## 使い方

1. ブラウザで `http://localhost:5000` にアクセス

2. YouTube動画のURLを入力して分析を実行

3. 分析完了後、専用のURLで結果が表示されます（例: `http://localhost:5000/analysis/1`）

4. 分析結果のURLは共有可能です

5. 過去の分析履歴は「分析履歴」リンクから閲覧できます

## 主な機能の説明

### 年別コメント推移
- コメントの投稿年別に集計し、グラフで可視化
- 年ごとのコメント数と平均いいね数を表示
- 長期間にわたる動画の人気推移を把握可能

### URL管理
- 各分析結果に一意のIDが付与され、専用URLでアクセス可能
- 分析結果を他の人と共有できます
- 同じ動画を再分析する場合、既存の結果を表示

### 分析履歴
- 過去に分析した動画の一覧を表示
- 動画タイトル、チャンネル名、分析日時で管理
- クリックで過去の分析結果にアクセス

## 技術スタック

- **バックエンド**: Flask, SQLAlchemy
- **データベース**: SQLite
- **フロントエンド**: HTML, CSS, JavaScript
- **グラフ**: Chart.js
- **API**: YouTube Data API v3

## 注意事項

- YouTube Data APIには1日あたりの利用制限があります
- 大量のコメントがある動画の場合、取得に時間がかかることがあります
- データベースファイル（youtube_analysis.db）は自動的に作成されます
- 同じ動画を複数回分析した場合、最初の分析結果が保持されます
