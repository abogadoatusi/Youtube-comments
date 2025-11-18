# YouTube Comments Analyzer

YouTube動画のURLを入力すると、コメントを取得して分析できるWebアプリケーションです。

## 機能

- YouTube動画URLからコメントを取得
- コメントの統計情報表示（総コメント数、平均いいね数など）
- 頻出ワードの分析
- ワードクラウド生成
- コメント一覧の表示

## セットアップ

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

## 使い方

1. アプリケーションを起動:
```bash
python app.py
```

2. ブラウザで `http://localhost:5000` にアクセス

3. YouTube動画のURLを入力して分析を実行

## 注意事項

- YouTube Data APIには1日あたりの利用制限があります
- 大量のコメントがある動画の場合、取得に時間がかかることがあります
