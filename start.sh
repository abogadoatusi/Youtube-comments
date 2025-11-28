#!/bin/bash
# YouTube Comments Analyzer 起動スクリプト

echo "=================================="
echo "YouTube Comments Analyzer"
echo "=================================="
echo ""

# カレントディレクトリをスクリプトの場所に変更
cd "$(dirname "$0")"

# .envファイルの確認
if [ ! -f .env ]; then
    echo "⚠️  .envファイルが見つかりません"
    echo ""
    echo "初回セットアップが必要です:"
    echo "1. .env.exampleを.envにコピー"
    echo "2. .envファイルにYouTube APIキーを設定"
    echo ""
    echo ".envファイルを作成しますか? (y/n)"
    read -r response
    if [ "$response" = "y" ] || [ "$response" = "Y" ]; then
        cp .env.example .env
        echo "✓ .envファイルを作成しました"
        echo ""
        echo "次のステップ:"
        echo "1. Google Cloud ConsoleでYouTube Data API v3を有効化"
        echo "2. APIキーを取得"
        echo "3. .envファイルを開いてYOUTUBE_API_KEY=your_api_keyを設定"
        echo ""
        echo ".envファイルの設定後、再度このスクリプトを実行してください"
        exit 0
    else
        echo "起動を中止しました"
        exit 1
    fi
fi

# Pythonの確認
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3が見つかりません"
    echo "Pythonをインストールしてください: https://www.python.org/"
    exit 1
fi

# 依存パッケージのチェック
echo "📦 依存パッケージを確認中..."
if ! python3 -c "import flask" &> /dev/null; then
    echo "依存パッケージをインストールします..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ パッケージのインストールに失敗しました"
        exit 1
    fi
    echo "✓ パッケージをインストールしました"
fi

echo ""
echo "🚀 アプリケーションを起動中..."
echo ""
echo "ブラウザで以下のURLにアクセスしてください:"
echo "👉 http://localhost:5000"
echo ""
echo "終了するには Ctrl+C を押してください"
echo ""
echo "=================================="
echo ""

# アプリケーション起動
python3 app.py
