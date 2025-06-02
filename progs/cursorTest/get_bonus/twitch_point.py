# filepath: c:\Users\MtqRon\Desktop\AE1st\hobby\twitch_point.py
# カーソルの位置の色を取得する + 自動クリック機能

import colorsys
import csv
import time
import datetime
import keyboard
import pyautogui
import pyperclip
import webbrowser
import requests
import threading

# Twitch API設定（設定ファイルから読み込み）
try:
    from twitch_config import CLIENT_ID, CLIENT_SECRET, STREAMER_NAME, CHECK_INTERVAL
    print("✅ twitch_config.pyから認証情報を読み込みました")
except ImportError:
    CLIENT_ID = "mqalh26s3xf0hbfidughclvwt4x175"
    CLIENT_SECRET = "vvik1nqlgaqlelazuo0lb9p58tjl7z"
    CHECK_INTERVAL = 120  # デフォル"ト値
    STREAMER_NAME = "nyancakew"
    print("❌ twitch_config.pyが見つかりません。デフォルト値を使用します")
    print("⚠️ 認証情報を設定するにはtwitch_config.pyを作成してください")
    print("詳細はREADME_twitch.mdを参照してください")

# 自動クリック機能の設定
TARGET_X = 1670  # 監視する座標X（変更してください）
TARGET_Y = 1000  # 監視する座標Y（変更してください）
# CSVファイル名
CSV_FILE = "click_log.csv"



# 緑色の判定条件（HLS形式、調整可能）
GREEN_THRESHOLD_HLS = {
    'min_h': 0.35,   # 色相の最小値（緑の範囲: 0.2-0.4）
    'max_h': 0.5,   # 色相の最大値
    'min_l': 0.4,   # 明度の最小値
    'max_l': 0.5,   # 明度の最大値
    'min_s': 0.9,    # 彩度の最小値
    'max_s': 1.0    # 彩度の最大値
}

def is_green_color(r, g, b):
    """RGBが緑色かどうかをHLSで判定"""
    # RGB to HLS変換
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    
    return (GREEN_THRESHOLD_HLS['min_h'] <= h <= GREEN_THRESHOLD_HLS['max_h'] and
            GREEN_THRESHOLD_HLS['min_l'] <= l <= GREEN_THRESHOLD_HLS['max_l'] and
            GREEN_THRESHOLD_HLS['min_s'] <= s <= GREEN_THRESHOLD_HLS['max_s'])

def save_to_csv(timestamp, x, y, r, g, b, clicked):
    """CSVファイルにデータを保存"""
    file_exists = False
    try:
        with open(CSV_FILE, 'r'):
            file_exists = True
    except FileNotFoundError:
        pass
    
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # ヘッダーを書き込み（ファイルが新規作成の場合）
        if not file_exists:
            writer.writerow(['timestamp', 'x', 'y', 'r', 'g', 'b', 'is_green', 'clicked'])
        
        # データを書き込み
        writer.writerow([timestamp, x, y, r, g, b, clicked, clicked])

def get_twitch_access_token():
    """Twitch APIのアクセストークンを取得"""
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    
    try:
        response = requests.post(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("access_token")
    except requests.exceptions.RequestException as e:
        print(f"トークン取得エラー: {e}")
        return None

def get_user_id(access_token, username):
    """ユーザー名からユーザーIDを取得"""
    url = "https://api.twitch.tv/helix/users"
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {access_token}"
    }
    params = {"login": username}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data["data"]:
            return data["data"][0]["id"]
        return None
    except requests.exceptions.RequestException as e:
        print(f"ユーザーID取得エラー: {e}")
        return None

def check_stream_status(access_token, user_id):
    """配信状況をチェック"""
    url = "https://api.twitch.tv/helix/streams"
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {access_token}"
    }
    params = {"user_id": user_id}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        is_live = len(data["data"]) > 0
        
        if is_live:
            stream_info = data["data"][0]
            return {
                "is_live": True,
                "title": stream_info.get("title", ""),
                "game_name": stream_info.get("game_name", ""),
                "viewer_count": stream_info.get("viewer_count", 0)
            }
        else:
            return {"is_live": False}
            
    except requests.exceptions.RequestException as e:
        print(f"配信状況チェックエラー: {e}")
        return {"is_live": False}

def color_monitor_mode():
    """元のカーソル位置の色を表示するモード"""
    print("カーソル位置の色を監視中...")
    print("Shiftキーでクリップボードにコピー、Escキーで終了")
    
    while True:
        x, y = pyautogui.position()
        r, g, b = pyautogui.pixel(x, y)
        # RGB to HLS
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        print(f"HLS: {round(h,2)}, {round(l,2)}, {round(s,2)}, Pos: {pyautogui.position()}")
        
        if keyboard.is_pressed("shift"):
            pyperclip.copy(f"HLS: {h}, {l}, {s}, Pos: {pyautogui.position()}")
            print("クリップボードにコピーしました！")
            
        if keyboard.is_pressed("esc"):
            break
            
        time.sleep(0.1)

def bonus_auto_get_mode():
    """ボーナス自動取得モード（配信監視 + 自動クリック）"""
    print(f"ボーナス自動取得モード開始")
    print(f"ストリーマー: {STREAMER_NAME}")
    print(f"監視座標: ({TARGET_X}, {TARGET_Y})")
    print(f"チェック間隔: {CHECK_INTERVAL}秒")
    print(f"緑色判定条件（HLS）: H:{GREEN_THRESHOLD_HLS['min_h']}-{GREEN_THRESHOLD_HLS['max_h']}, L:{GREEN_THRESHOLD_HLS['min_l']}-{GREEN_THRESHOLD_HLS['max_l']}, S≥{GREEN_THRESHOLD_HLS['min_s']}")
    print("プログラムを終了するには Ctrl+C を押してください")
    print("-" * 50)
    
    # API認証情報の確認
    if CLIENT_ID == "YOUR_CLIENT_ID_HERE" or CLIENT_SECRET == "YOUR_CLIENT_SECRET_HERE":
        print("⚠️  Twitch API認証情報が設定されていません。")
        print("twitch_config.pyにCLIENT_IDとCLIENT_SECRETを設定してください。")
        print("詳細はREADME_twitch.mdを参照してください。")
        print("配信監視機能なしで座標監視のみ実行します。")
        print("-" * 50)
        
        # 配信監視なしの座標クリック機能
        simple_auto_click()
        return
    
    # アクセストークンを取得
    print("🔑 Twitch APIに接続中...")
    access_token = get_twitch_access_token()
    if not access_token:
        print("❌ アクセストークンの取得に失敗しました。配信監視機能なしで実行します。")
        simple_auto_click()
        return
      # ユーザーIDを取得
    user_id = get_user_id(access_token, STREAMER_NAME)
    if not user_id:
        print("❌ ユーザーIDの取得に失敗しました。配信監視機能なしで実行します。")
        simple_auto_click()
        return
    
    print(f"✅ API接続成功！{STREAMER_NAME}の配信を監視開始...")
    
    is_stream_opened = False
    was_live_previously = False
    
    try:
        while True:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 配信状況をチェック
            stream_status = check_stream_status(access_token, user_id)
            
            if stream_status.get("is_live", False):
                # 配信中の場合
                if not was_live_previously:
                    # 配信が新しく開始された
                    print(f"🔴 [{timestamp}] 配信開始検出！")
                    print(f"📺 タイトル: {stream_status.get('title', 'タイトルなし')}")
                    print(f"🎮 ゲーム: {stream_status.get('game_name', 'ゲームなし')}")
                    print(f"👥 視聴者数: {stream_status.get('viewer_count', 0)}")
                    
                    # 配信ページを開く
                    twitch_url = f"https://www.twitch.tv/{STREAMER_NAME}"
                    print(f"🚀 配信ページを開いています: {twitch_url}")
                    webbrowser.open(twitch_url)
                    
                    print("🎯 座標監視とクリック機能を開始します...")
                    was_live_previously = True
                    is_stream_opened = True
                
                # 配信中は座標をチェックしてクリック判定
                r, g, b = pyautogui.pixel(TARGET_X, TARGET_Y)
                is_green = is_green_color(r, g, b)
                
                print(f"🔴 [{timestamp}] 配信中 - RGB({r}, {g}, {b}) - 緑色: {is_green} - 視聴者: {stream_status.get('viewer_count', 0)}")
                
                # 緑色の場合はクリック
                if is_green:
                    pyautogui.click(TARGET_X, TARGET_Y)
                    print(f"  🎯 ボーナスクリック実行！")
                    save_to_csv(timestamp, TARGET_X, TARGET_Y, r, g, b, True)
                else:
                    save_to_csv(timestamp, TARGET_X, TARGET_Y, r, g, b, False)
            else:
                # オフライン時
                if was_live_previously:
                    # 配信が終了した
                    print(f"⭕ [{timestamp}] 配信終了検出")
                    print("⏸️  座標監視とクリック機能を一時停止します...")
                    was_live_previously = False
                    is_stream_opened = False
                else:
                    # オフライン状態継続
                    print(f"⭕ [{timestamp}] オフライン - 配信開始を待機中...")
            
            # ESCキーで終了
            if keyboard.is_pressed("esc"):
                print("ESCキーが押されました。終了します。")
                break
            
            # 指定時間待機
            time.sleep(CHECK_INTERVAL)
            
    except KeyboardInterrupt:
        print("\nプログラムを終了しました")

def simple_auto_click():
    """シンプルな自動クリック機能（配信監視なし）"""
    print("📍 座標監視モードで実行中...")
    
    try:
        while True:
            # 指定座標のRGB値を取得
            r, g, b = pyautogui.pixel(TARGET_X, TARGET_Y)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 緑色かどうかを判定
            is_green = is_green_color(r, g, b)
            
            print(f"{timestamp} - RGB({r}, {g}, {b}) - 緑色: {is_green}")
            
            # 緑色の場合はクリック
            if is_green:
                pyautogui.click(TARGET_X, TARGET_Y)
                print(f"  → クリックしました！")
                save_to_csv(timestamp, TARGET_X, TARGET_Y, r, g, b, True)
            else:
                save_to_csv(timestamp, TARGET_X, TARGET_Y, r, g, b, False)
            
            # ESCキーで終了
            if keyboard.is_pressed("esc"):
                print("ESCキーが押されました。終了します。")
                break
            
            # 指定時間待機
            time.sleep(CHECK_INTERVAL)
            
    except KeyboardInterrupt:
        print("\nプログラムを終了しました")

def coordinate_picker_mode():
    """座標選択モード"""
    print("座標選択モード")
    print("マウスカーソルを目的の位置に移動してからスペースキーを押してください")
    print("ESCキーで終了します")
    print("-" * 50)
    
    try:
        while True:
            if keyboard.is_pressed('space'):
                x, y = pyautogui.position()
                r, g, b = pyautogui.pixel(x, y)
                h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
                
                print(f"座標: ({x}, {y})")
                print(f"RGB: ({r}, {g}, {b})")
                print(f"HLS: ({round(h,3)}, {round(l,3)}, {round(s,3)})")
                print(f"TARGET_X = {x}, TARGET_Y = {y} に設定してください")
                print("-" * 30)
                
                # キーが離されるまで待機
                while keyboard.is_pressed('space'):
                    time.sleep(0.1)
            
            if keyboard.is_pressed('esc'):
                break
                
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        pass

def main():
    print("=" * 50)
    print("Twitch Point - カーソル色取得 & 自動クリックツール")
    print("=" * 50)
    print()
    
    print("モードを選択してください:")
    print("1. カーソル位置の色を監視")
    print("2. ボーナス自動取得 (配信監視 + 自動クリック)")
    print("3. 座標選択ヘルパー")
    print("-" * 50)
    
    try:
        choice = input("選択 (1-3): ").strip()
        
        if choice == "1":
            color_monitor_mode()
        elif choice == "2":
            bonus_auto_get_mode()
        elif choice == "3":
            coordinate_picker_mode()
        else:
            print("無効な選択です。1-3の数字を入力してください。")
            
    except KeyboardInterrupt:
        print("\nプログラムを終了しました")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()