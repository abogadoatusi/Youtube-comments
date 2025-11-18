"""
Flask application for YouTube comment analysis
YouTube コメント分析 Web アプリケーション
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from youtube_api import YouTubeAPI
from analyzer import CommentAnalyzer
from models import db, Analysis
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///youtube_analysis.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# データベース初期化
db.init_app(app)

# YouTube API クライアントの初期化
try:
    youtube_api = YouTubeAPI()
except ValueError as e:
    print(f"Error: {e}")
    youtube_api = None

# データベーステーブルを作成
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    """メインページを表示"""
    return render_template('index.html')

@app.route('/history')
def history():
    """分析履歴ページを表示"""
    return render_template('history.html')

@app.route('/api/history')
def get_history():
    """分析履歴を取得"""
    analyses = Analysis.query.order_by(Analysis.created_at.desc()).all()
    return jsonify([{
        'id': a.id,
        'video_id': a.video_id,
        'video_title': a.video_title,
        'channel_name': a.channel_name,
        'analyzed_comments': a.analyzed_comments,
        'created_at': a.created_at.isoformat() if a.created_at else None
    } for a in analyses])

@app.route('/analysis/<int:analysis_id>')
def view_analysis(analysis_id):
    """保存された分析結果を表示"""
    analysis = Analysis.query.get_or_404(analysis_id)
    return render_template('analysis.html', analysis_id=analysis_id)

@app.route('/api/analysis/<int:analysis_id>')
def get_analysis(analysis_id):
    """保存された分析結果を取得"""
    analysis = Analysis.query.get_or_404(analysis_id)
    return jsonify(analysis.to_dict())

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    YouTube動画のコメントを分析

    Returns:
        JSON形式の分析結果
    """
    if not youtube_api:
        return jsonify({
            'error': 'YouTube API key not configured. Please set YOUTUBE_API_KEY in .env file'
        }), 500

    data = request.get_json()
    url = data.get('url', '')
    max_comments = int(data.get('max_comments', 100))

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    # 動画IDを抽出
    video_id = youtube_api.extract_video_id(url)
    if not video_id:
        return jsonify({'error': 'Invalid YouTube URL'}), 400

    # 既存の分析結果をチェック
    existing_analysis = Analysis.query.filter_by(video_id=video_id).first()
    if existing_analysis:
        # 既存の分析結果がある場合はそのIDを返す
        return jsonify({
            'existing': True,
            'analysis_id': existing_analysis.id,
            'message': 'この動画は既に分析されています。既存の結果を表示しますか？'
        })

    # 動画情報を取得
    video_info = youtube_api.get_video_info(video_id)
    if not video_info:
        return jsonify({'error': 'Video not found'}), 404

    # コメントを取得
    comments = youtube_api.get_comments(video_id, max_results=max_comments)
    if not comments:
        return jsonify({
            'error': 'No comments found. Comments may be disabled for this video.'
        }), 404

    # コメントを分析
    analyzer = CommentAnalyzer(comments)
    statistics = analyzer.get_statistics()
    top_comments = analyzer.get_top_comments(10)
    word_frequency = analyzer.get_word_frequency(20)
    recent_comments = analyzer.get_recent_comments(10)
    yearly_stats = analyzer.get_yearly_statistics()

    # 分析結果をデータベースに保存
    analysis = Analysis.from_analysis_data(
        video_id=video_id,
        video_url=url,
        video_info=video_info,
        statistics=statistics,
        top_comments=top_comments,
        word_frequency=word_frequency,
        recent_comments=recent_comments,
        yearly_stats=yearly_stats
    )
    db.session.add(analysis)
    db.session.commit()

    return jsonify({
        'analysis_id': analysis.id,
        'video_info': video_info,
        'statistics': statistics,
        'top_comments': top_comments,
        'word_frequency': word_frequency,
        'recent_comments': recent_comments,
        'yearly_stats': yearly_stats
    })

@app.errorhandler(404)
def not_found(error):
    """404 エラーハンドラ"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """500 エラーハンドラ"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    if not youtube_api:
        print("\n" + "="*80)
        print("WARNING: YouTube API key not configured!")
        print("Please follow these steps:")
        print("1. Copy .env.example to .env")
        print("2. Get your API key from https://console.cloud.google.com/")
        print("3. Add your API key to .env file")
        print("="*80 + "\n")
    else:
        print("\n" + "="*80)
        print("YouTube Comments Analyzer is running!")
        print("Open your browser and navigate to: http://localhost:5000")
        print("="*80 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
