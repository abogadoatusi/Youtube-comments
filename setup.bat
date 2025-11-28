@echo off
REM YouTube Comments Analyzer セットアップスクリプト (Windows)

echo ========================================
echo YouTube Comments Analyzer - セットアップ
echo ========================================
echo.

REM カレントディレクトリをスクリプトの場所に変更
cd /d "%~dp0"

REM Pythonの確認
echo [1/4] Pythonのバージョン確認...
python --version >nul 2>&1
if errorlevel 1 (
    echo [エラー] Pythonが見つかりません
    echo Pythonをインストールしてください: https://www.python.org/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] %PYTHON_VERSION% が見つかりました
echo.

REM 依存パッケージのインストール
echo [2/4] 依存パッケージをインストール中...
pip install -r requirements.txt
if errorlevel 1 (
    echo [エラー] パッケージのインストールに失敗しました
    pause
    exit /b 1
)
echo [OK] 依存パッケージをインストールしました
echo.

REM .envファイルの作成
echo [3/4] 環境変数ファイルの設定...
if exist .env (
    echo [警告] .envファイルは既に存在します
    set /p response="上書きしますか? (y/n): "
    if /i not "%response%"=="y" (
        echo スキップしました
    ) else (
        copy /y .env.example .env >nul
        echo [OK] .envファイルを作成しました
    )
) else (
    copy .env.example .env >nul
    echo [OK] .envファイルを作成しました
)
echo.

REM APIキーの設定を促す
echo [4/4] YouTube API キーの設定
echo.
echo 次のステップでYouTube APIキーを取得してください:
echo.
echo 📌 手順:
echo   1. https://console.cloud.google.com/ にアクセス
echo   2. 新しいプロジェクトを作成（または既存のプロジェクトを選択）
echo   3. 「APIとサービス」→「ライブラリ」から「YouTube Data API v3」を検索
echo   4. 「有効にする」をクリック
echo   5. 「認証情報」→「認証情報を作成」→「APIキー」を選択
echo   6. 作成されたAPIキーをコピー
echo.
set /p response="APIキーを入力しますか? (y/n) - 後で .env ファイルを直接編集することもできます: "

if /i "%response%"=="y" (
    echo.
    set /p api_key="YouTube API キーを入力してください: "

    if not "!api_key!"=="" (
        powershell -Command "(Get-Content .env) -replace 'YOUTUBE_API_KEY=your_api_key_here', 'YOUTUBE_API_KEY=!api_key!' | Set-Content .env"
        echo [OK] APIキーを設定しました
    ) else (
        echo [警告] APIキーが入力されませんでした
        echo 後で .env ファイルを編集してください
    )
) else (
    echo [警告] 後で .env ファイルを編集してAPIキーを設定してください
)

echo.
echo ========================================
echo [完了] セットアップが完了しました！
echo ========================================
echo.
echo 起動方法:
echo   start.bat をダブルクリック
echo.
echo または:
echo   python app.py
echo.
pause
