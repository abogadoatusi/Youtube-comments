"""
Comment analysis module
コメントの分析機能を提供
"""

import re
from collections import Counter
from datetime import datetime

class CommentAnalyzer:
    def __init__(self, comments):
        """
        コメント分析器の初期化

        Args:
            comments: コメントのリスト
        """
        self.comments = comments

    def get_statistics(self):
        """
        コメントの統計情報を取得

        Returns:
            統計情報の辞書
        """
        if not self.comments:
            return {
                'total_comments': 0,
                'total_likes': 0,
                'average_likes': 0,
                'max_likes': 0,
                'average_comment_length': 0
            }

        total_likes = sum(c['like_count'] for c in self.comments)
        total_length = sum(len(c['text']) for c in self.comments)
        max_likes = max(c['like_count'] for c in self.comments)

        return {
            'total_comments': len(self.comments),
            'total_likes': total_likes,
            'average_likes': round(total_likes / len(self.comments), 2),
            'max_likes': max_likes,
            'average_comment_length': round(total_length / len(self.comments), 2)
        }

    def get_top_comments(self, n=10):
        """
        いいね数が多いコメントを取得

        Args:
            n: 取得する件数

        Returns:
            コメントのリスト
        """
        sorted_comments = sorted(
            self.comments,
            key=lambda x: x['like_count'],
            reverse=True
        )
        return sorted_comments[:n]

    def get_word_frequency(self, n=20, min_length=2):
        """
        頻出ワードを取得

        Args:
            n: 取得する件数
            min_length: 単語の最小文字数

        Returns:
            (単語, 出現回数) のタプルのリスト
        """
        # すべてのコメントテキストを結合
        all_text = ' '.join(c['text'] for c in self.comments)

        # 日本語、英数字、ひらがな、カタカナを抽出
        # 英単語は単語境界で分割、日本語は文字単位で分割
        words = []

        # 英単語を抽出
        english_words = re.findall(r'\b[a-zA-Z]+\b', all_text)
        words.extend([w.lower() for w in english_words if len(w) >= min_length])

        # 日本語（ひらがな・カタカナ・漢字）を抽出
        japanese_chars = re.findall(r'[ぁ-んァ-ヶー一-龯]+', all_text)
        for text in japanese_chars:
            # 2文字以上の連続した文字列を単語として扱う
            if len(text) >= min_length:
                words.append(text)

        # ストップワード（除外する一般的な単語）
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this',
            'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'が', 'の', 'を', 'に', 'は', 'へ', 'と', 'で', 'や', 'から', 'まで',
            'より', 'も', 'ね', 'よ', 'な', 'だ', 'です', 'ます', 'てす', 'ている'
        }

        # ストップワードを除外
        filtered_words = [w for w in words if w.lower() not in stop_words]

        # 頻度をカウント
        word_freq = Counter(filtered_words)

        return word_freq.most_common(n)

    def get_recent_comments(self, n=10):
        """
        最新のコメントを取得

        Args:
            n: 取得する件数

        Returns:
            コメントのリスト
        """
        sorted_comments = sorted(
            self.comments,
            key=lambda x: x['published_at'],
            reverse=True
        )
        return sorted_comments[:n]
