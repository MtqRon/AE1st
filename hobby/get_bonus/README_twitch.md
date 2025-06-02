# Twitch配信監視プログラム

nyancakewの配信が開始したら自動的にブラウザでTwitchページを開くプログラムです。

## セットアップ手順

### 1. 必要なライブラリのインストール
```bash
pip install requests
```

### 2. Twitch API認証情報の取得
1. [Twitch Developer Console](https://dev.twitch.tv/console) にアクセス
2. 「Applications」→「Register Your Application」をクリック
3. アプリケーション情報を入力：
   - **Name**: 任意の名前（例: Stream Monitor）
   - **OAuth Redirect URLs**: `http://localhost`
   - **Category**: Application Integration
4. 「Create」をクリック
5. 作成されたアプリケーションの「Manage」をクリック
6. 「Client ID」と「Client Secret」をコピー

### 3. 設定ファイルの編集
`twitch_config.py` を開いて、取得した認証情報を設定：

```python
CLIENT_ID = "あなたのClient ID"
CLIENT_SECRET = "あなたのClient Secret"
STREAMER_NAME = "nyancakew"
CHECK_INTERVAL = 60  # チェック間隔（秒）
```

### 4. プログラムの実行
```bash
python twitch_stream_monitor.py
```

## 機能

- **配信開始検出**: nyancakewの配信が開始されると自動的にTwitchページを開く
- **リアルタイム監視**: 60秒間隔で配信状況をチェック
- **配信情報表示**: タイトル、ゲーム名、視聴者数などを表示
- **状態管理**: 配信開始/終了を正確に検出

## 使用方法

1. プログラムを実行すると、nyancakewの配信監視が開始されます
2. 配信が開始されると、自動的にブラウザでTwitchページが開きます
3. プログラムを終了するには `Ctrl+C` を押してください

## 注意事項

- Twitch APIには利用制限があります（1分間に800リクエスト）
- 認証情報は秘密に保管してください
- インターネット接続が必要です
