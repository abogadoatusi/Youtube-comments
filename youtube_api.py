"""
YouTube Data API integration module
YouTubeコメントを取得するための機能を提供
"""

import os
import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

load_dotenv()

class YouTubeAPI:
    def __init__(self):
        """YouTube Data API クライアントの初期化"""
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        if not self.api_key:
            raise ValueError("YouTube API key not found. Please set YOUTUBE_API_KEY in .env file")
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def extract_video_id(self, url):
        """
        YouTube URLから動画IDを抽出

        Args:
            url: YouTube動画のURL

        Returns:
            動画ID (str) または None
        """
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?]*)',
            r'youtube\.com\/embed\/([^&\n?]*)',
            r'youtube\.com\/v\/([^&\n?]*)'
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def get_video_info(self, video_id):
        """
        動画の基本情報を取得

        Args:
            video_id: YouTube動画ID

        Returns:
            動画情報の辞書
        """
        try:
            request = self.youtube.videos().list(
                part='snippet,statistics',
                id=video_id
            )
            response = request.execute()

            if not response['items']:
                return None

            video = response['items'][0]
            return {
                'title': video['snippet']['title'],
                'channel': video['snippet']['channelTitle'],
                'published_at': video['snippet']['publishedAt'],
                'view_count': int(video['statistics'].get('viewCount', 0)),
                'like_count': int(video['statistics'].get('likeCount', 0)),
                'comment_count': int(video['statistics'].get('commentCount', 0))
            }
        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            return None

    def get_comments(self, video_id, max_results=100):
        """
        動画のコメントを取得

        Args:
            video_id: YouTube動画ID
            max_results: 取得する最大コメント数

        Returns:
            コメントのリスト
        """
        comments = []

        try:
            request = self.youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=min(max_results, 100),
                textFormat='plainText',
                order='relevance'
            )

            while request and len(comments) < max_results:
                response = request.execute()

                for item in response['items']:
                    comment = item['snippet']['topLevelComment']['snippet']
                    comments.append({
                        'author': comment['authorDisplayName'],
                        'text': comment['textDisplay'],
                        'like_count': comment['likeCount'],
                        'published_at': comment['publishedAt']
                    })

                # 次のページがある場合
                if 'nextPageToken' in response and len(comments) < max_results:
                    request = self.youtube.commentThreads().list(
                        part='snippet',
                        videoId=video_id,
                        pageToken=response['nextPageToken'],
                        maxResults=min(max_results - len(comments), 100),
                        textFormat='plainText',
                        order='relevance'
                    )
                else:
                    break

            return comments[:max_results]

        except HttpError as e:
            if e.resp.status == 403:
                print("Comments are disabled for this video")
            else:
                print(f"An HTTP error occurred: {e}")
            return []
