#!/bin/bash
# YouTube Comments Analyzer セットアップスクリプト

echo "========================================"
echo "YouTube Comments Analyzer - セットアップ"
echo "========================================"
echo ""

# カレントディレクトリをスクリプトの場所に変更
cd "$(dirname "$0")"

# Pythonの確認
echo "1️⃣  Pythonのバージョン確認..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3が見つかりません"
    echo "Pythonをインストールしてください: https://www.python.org/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✓ $PYTHON_VERSION が見つかりました"
echo ""

# 依存パッケージのインストール
echo "2️⃣  依存パッケージをインストール中..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ パッケージのインストールに失敗しました"
    exit 1
fi
echo "✓ 依存パッケージをインストールしました"
echo ""

# .envファイルの作成
echo "3️⃣  環境変数ファイルの設定..."
if [ -f .env ]; then
    echo "⚠️  .envファイルは既に存在します"
    echo "上書きしますか? (y/n)"
    read -r response
    if [ "$response" != "y" ] && [ "$response" != "Y" ]; then
        echo "スキップしました"
    else
        cp .env.example .env
        echo "✓ .envファイルを作成しました"
    fi
else
    cp .env.example .env
    echo "✓ .envファイルを作成しました"
fi
echo ""

# APIキーの設定を促す
echo "4️⃣  YouTube API キーの設定"
echo ""
echo "次のステップでYouTube APIキーを取得してください:"
echo ""
echo "📌 手順:"
echo "  1. https://console.cloud.google.com/ にアクセス"
echo "  2. 新しいプロジェクトを作成（または既存のプロジェクトを選択）"
echo "  3. 「APIとサービス」→「ライブラリ」から「YouTube Data API v3」を検索"
echo "  4. 「有効にする」をクリック"
echo "  5. 「認証情報」→「認証情報を作成」→「APIキー」を選択"
echo "  6. 作成されたAPIキーをコピー"
echo ""
echo "APIキーを入力しますか? (y/n)"
echo "（後で .env ファイルを直接編集することもできます）"
read -r response

if [ "$response" = "y" ] || [ "$response" = "Y" ]; then
    echo ""
    echo "YouTube API キーを入力してください:"
    read -r api_key

    if [ -n "$api_key" ]; then
        # macOS用とLinux用の両方のsedコマンドに対応
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s/YOUTUBE_API_KEY=your_api_key_here/YOUTUBE_API_KEY=$api_key/" .env
        else
            sed -i "s/YOUTUBE_API_KEY=your_api_key_here/YOUTUBE_API_KEY=$api_key/" .env
        fi
        echo "✓ APIキーを設定しました"
    else
        echo "⚠️  APIキーが入力されませんでした"
        echo "後で .env ファイルを編集してください"
    fi
else
    echo "⚠️  後で .env ファイルを編集してAPIキーを設定してください"
fi

echo ""
echo "========================================"
echo "✅ セットアップが完了しました！"
echo "========================================"
echo ""
echo "起動方法:"
echo "  ./start.sh を実行してください"
echo ""
echo "または:"
echo "  python3 app.py"
echo ""
