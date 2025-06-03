#!/usr/bin/env python3
"""
YouTube Video Downloader
最高画質・最高音質でYouTube動画をダウンロードするプログラム
URLは標準入力から受け取ります
"""

import sys
import os
import yt_dlp
from urllib.parse import urlparse

def is_valid_youtube_url(url: str) -> bool:
    """YouTube URLの有効性をチェック"""
    parsed_url = urlparse(url)
    youtube_domains = ['youtube.com', 'www.youtube.com', 'youtu.be', 'm.youtube.com']
    return parsed_url.netloc in youtube_domains

def download_youtube_video(url: str) -> None:
    """
    YouTube動画を最高画質・最高音質でダウンロード
    """
    print(f"動画をダウンロード中: {url}")
    
    # yt-dlpオプション設定
    ydl_opts = {
        # 最高画質・最高音質の設定
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
          # ファイル名テンプレート（outputフォルダに保存）
        'outtmpl': '../output/%(title)s_%(id)s.%(ext)s',
          # メタデータの設定（動画のみダウンロード）
        'writeinfojson': False,  # 動画情報JSONファイルは不要
        'writethumbnail': False,  # サムネイルは不要
        'writesubtitles': False,  # 字幕は不要
        'writeautomaticsub': False,  # 自動生成字幕も不要
        
        # 品質設定
        'merge_output_format': 'mp4',  # 最終出力形式
        'postprocessor_args': [
            '-c:v', 'copy',  # 映像コーデックはコピー（再エンコードしない）
            '-c:a', 'aac',   # 音声コーデックはAAC
            '-b:a', '320k'   # 音声ビットレート320kbps
        ],
        
        # その他の設定
        'ignoreerrors': False,  # エラーを無視しない
        'no_warnings': False,   # 警告を表示
        'extractflat': False,   # プレイリストも展開
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 動画情報を取得
            info = ydl.extract_info(url, download=False)
            
            # 動画情報を表示
            print(f"\n=== 動画情報 ===")
            print(f"タイトル: {info.get('title', 'N/A')}")
            print(f"アップローダー: {info.get('uploader', 'N/A')}")
            print(f"再生時間: {info.get('duration', 'N/A')}秒")
            print(f"視聴回数: {info.get('view_count', 'N/A')}")
            print(f"動画ID: {info.get('id', 'N/A')}")
            
            # 利用可能な形式を表示
            print(f"\n=== 利用可能な形式 ===")
            formats = info.get('formats', [])
            video_formats = [f for f in formats if f.get('vcodec') != 'none']
            audio_formats = [f for f in formats if f.get('acodec') != 'none' and f.get('vcodec') == 'none']
            
            if video_formats:
                best_video = max(video_formats, key=lambda x: x.get('height', 0) or 0)
                print(f"最高画質: {best_video.get('height', 'N/A')}p ({best_video.get('format_note', 'N/A')})")
            
            if audio_formats:
                best_audio = max(audio_formats, key=lambda x: x.get('abr', 0) or 0)
                print(f"最高音質: {best_audio.get('abr', 'N/A')}kbps")
            
            # ダウンロード開始
            print(f"\n=== ダウンロード開始 ===")
            ydl.download([url])
            
            print(f"\n✅ ダウンロード完了!")
            print(f"ファイル名: {info.get('title', 'unknown')}__{info.get('id', 'unknown')}.mp4")
            
    except yt_dlp.DownloadError as e:
        print(f"❌ ダウンロードエラー: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")
        sys.exit(1)

def main():
    """メイン関数"""
    print("=== YouTube動画ダウンローダー ===")
    print("最高画質・最高音質でダウンロードします")
    print("YouTubeのURLを入力してください:")
    
    try:
        # 標準入力からURLを取得
        url = input().strip()
        
        # URLが空でないかチェック
        if not url:
            print("❌ URLが入力されていません")
            sys.exit(1)
        
        # YouTube URLの有効性をチェック
        if not is_valid_youtube_url(url):
            print("❌ 有効なYouTube URLではありません")
            print("例: https://www.youtube.com/watch?v=VIDEO_ID")
            print("例: https://youtu.be/VIDEO_ID")
            sys.exit(1)
        
        # ダウンロード実行
        download_youtube_video(url)
        
    except KeyboardInterrupt:
        print("\n❌ ユーザーによって中断されました")
        sys.exit(1)
    except EOFError:
        print("\n❌ 入力が終了しました")
        sys.exit(1)

if __name__ == "__main__":
    main()
