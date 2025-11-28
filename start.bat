@echo off
REM YouTube Comments Analyzer 起動スクリプト (Windows)

echo ==================================
echo YouTube Comments Analyzer
echo ==================================
echo.

REM カレントディレクトリをスクリプトの場所に変更
cd /d "%~dp0"

REM .envファイルの確認
if not exist .env (
    echo [警告] .envファイルが見つかりません
    echo.
    echo 初回セットアップが必要です:
    echo 1. .env.exampleを.envにコピー
    echo 2. .envファイルにYouTube APIキーを設定
    echo.
    set /p response=".envファイルを作成しますか? (y/n): "
    if /i "%response%"=="y" (
        copy .env.example .env
        echo [OK] .envファイルを作成しました
        echo.
        echo 次のステップ:
        echo 1. Google Cloud ConsoleでYouTube Data API v3を有効化
        echo 2. APIキーを取得
        echo 3. .envファイルを開いてYOUTUBE_API_KEY=your_api_keyを設定
        echo.
        echo .envファイルの設定後、再度このスクリプトを実行してください
        pause
        exit /b 0
    ) else (
        echo 起動を中止しました
        pause
        exit /b 1
    )
)

REM Pythonの確認
python --version >nul 2>&1
if errorlevel 1 (
    echo [エラー] Pythonが見つかりません
    echo Pythonをインストールしてください: https://www.python.org/
    pause
    exit /b 1
)

REM 依存パッケージのチェック
echo [チェック中] 依存パッケージを確認中...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo 依存パッケージをインストールします...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [エラー] パッケージのインストールに失敗しました
        pause
        exit /b 1
    )
    echo [OK] パッケージをインストールしました
)

echo.
echo [起動中] アプリケーションを起動中...
echo.
echo ブラウザで以下のURLにアクセスしてください:
echo 👉 http://localhost:5000
echo.
echo 終了するには Ctrl+C を押してください
echo.
echo ==================================
echo.

REM アプリケーション起動
python app.py

pause
