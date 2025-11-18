"""
Database models for storing analysis results
分析結果を保存するためのデータベースモデル
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Analysis(db.Model):
    """分析結果を保存するモデル"""
    __tablename__ = 'analyses'

    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.String(50), nullable=False, index=True)
    video_title = db.Column(db.String(500))
    channel_name = db.Column(db.String(200))
    video_url = db.Column(db.String(500))

    # 動画情報
    view_count = db.Column(db.Integer)
    like_count = db.Column(db.Integer)
    comment_count = db.Column(db.Integer)
    published_at = db.Column(db.DateTime)

    # 分析結果（JSON形式で保存）
    statistics = db.Column(db.Text)  # 統計情報
    top_comments = db.Column(db.Text)  # 人気コメント
    word_frequency = db.Column(db.Text)  # 頻出ワード
    recent_comments = db.Column(db.Text)  # 最新コメント
    yearly_stats = db.Column(db.Text)  # 年別統計

    # メタ情報
    analyzed_comments = db.Column(db.Integer)  # 分析したコメント数
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Analysis {self.id}: {self.video_title}>'

    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'video_id': self.video_id,
            'video_title': self.video_title,
            'channel_name': self.channel_name,
            'video_url': self.video_url,
            'video_info': {
                'title': self.video_title,
                'channel': self.channel_name,
                'view_count': self.view_count,
                'like_count': self.like_count,
                'comment_count': self.comment_count,
                'published_at': self.published_at.isoformat() if self.published_at else None
            },
            'statistics': json.loads(self.statistics) if self.statistics else {},
            'top_comments': json.loads(self.top_comments) if self.top_comments else [],
            'word_frequency': json.loads(self.word_frequency) if self.word_frequency else [],
            'recent_comments': json.loads(self.recent_comments) if self.recent_comments else [],
            'yearly_stats': json.loads(self.yearly_stats) if self.yearly_stats else {},
            'analyzed_comments': self.analyzed_comments,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @staticmethod
    def from_analysis_data(video_id, video_url, video_info, statistics, top_comments,
                          word_frequency, recent_comments, yearly_stats):
        """分析データからモデルインスタンスを作成"""
        analysis = Analysis(
            video_id=video_id,
            video_url=video_url,
            video_title=video_info['title'],
            channel_name=video_info['channel'],
            view_count=video_info['view_count'],
            like_count=video_info['like_count'],
            comment_count=video_info['comment_count'],
            published_at=datetime.fromisoformat(video_info['published_at'].replace('Z', '+00:00')),
            statistics=json.dumps(statistics, ensure_ascii=False),
            top_comments=json.dumps(top_comments, ensure_ascii=False),
            word_frequency=json.dumps(word_frequency, ensure_ascii=False),
            recent_comments=json.dumps(recent_comments, ensure_ascii=False),
            yearly_stats=json.dumps(yearly_stats, ensure_ascii=False),
            analyzed_comments=statistics['total_comments']
        )
        return analysis
