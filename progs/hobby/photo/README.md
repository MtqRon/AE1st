# Real-ESRGAN Photo Upscaler

Real-ESRGANを使用して画像を高解像度化するツールです。人物写真とアニメ画像に最適化されたモデルを選択でき、タイルアーティファクトを最小限に抑える高度な処理が可能です。

## セットアップ

1. 仮想環境をアクティベート:
```bash
# Windows
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

2. 依存関係をインストール:
```bash
pip install -r requirements.txt
```

## 使用方法

### 基本的な使用方法

```bash
# 人物写真の場合（推奨）
python upscale_image.py -i portrait.jpg -o upscaled_portrait.png -t photo

# アニメ・イラストの場合（推奨）
python upscale_image.py -i anime.jpg -o upscaled_anime.png -t anime

# 汎用（画像タイプを指定しない）
python upscale_image.py -i image.jpg -o upscaled_image.png
```

### 高品質処理とアーティファクト軽減

```bash
# 小さい画像でタイルアーティファクトを避ける
python upscale_image.py -i small_image.jpg -o output.png --no-tile

# 自動タイルサイズ調整（推奨）
python upscale_image.py -i image.jpg -o output.png --tile 0

# 手動でタイルサイズを指定
python upscale_image.py -i image.jpg -o output.png --tile 800

# 前処理・後処理を無効にする（オリジナルの処理のみ）
python upscale_image.py -i image.jpg -o output.png --no-preprocess --no-postprocess
```

### 利用可能なモデル

モデル一覧を確認:
```bash
python upscale_image.py --list-models
```

#### 人物写真に最適なモデル

1. **RealESRGAN_x4plus** (推奨): 汎用的な実写画像向け、人物写真に最適
2. **RealESRNet_x4plus**: 高品質だが処理時間が長い
3. **RealESRGAN_x2plus**: 2倍スケールが必要な場合

#### アニメ・イラストに最適なモデル

1. **RealESRGAN_x4plus_anime_6B** (推奨): アニメ・イラスト専用
2. **realesr-animevideov3**: アニメ動画向け（静止画にも使用可能）

### オプション

#### 基本オプション
- `-i, --input`: 入力画像のパス（必須）
- `-o, --output`: 出力画像のパス（必須）
- `-t, --type`: 画像タイプ（`photo`, `anime`, `auto`）
- `-n, --model_name`: 使用するモデル名（手動選択）
- `-s, --scale`: スケール倍率（モデルの既定値を上書き）
- `--list-models`: 利用可能なモデルの一覧を表示

#### 高度なオプション
- `--half`: 半精度を使用してVRAMを節約
- `--tile`: タイルサイズ（0で自動、-1で無効、カスタム値で手動設定）
- `--no-tile`: タイル処理を完全に無効にする（小さい画像推奨）
- `--no-preprocess`: 前処理（ノイズ軽減）を無効にする
- `--no-postprocess`: 後処理（アーティファクト軽減）を無効にする

### 使用例

```bash
# 人物写真を4倍にアップスケール
python upscale_image.py -i portrait.jpg -o portrait_4x.png -t photo

# アニメイラストを高解像度化
python upscale_image.py -i anime.jpg -o anime_4x.png -t anime

# 特定のモデルを指定
python upscale_image.py -i image.jpg -o output.png -n RealESRGAN_x4plus

# メモリ節約モード
python upscale_image.py -i image.jpg -o output.png -t photo --half --tile 200

# 2倍スケールで高速処理
python upscale_image.py -i image.jpg -o output.png -n RealESRGAN_x2plus

# 高品質処理（タイル無効）
python upscale_image.py -i small_image.jpg -o output.png --no-tile

# 自動タイル調整（推奨）
python upscale_image.py -i image.jpg -o output.png --tile 0
```

## アーティファクト対策

### タイルアーティファクト（ブロック状のノイズ）の軽減

1. **自動タイル調整を使用**: `--tile 0`
2. **小さい画像ではタイル無効**: `--no-tile`
3. **タイルサイズを大きくする**: `--tile 800` 以上
4. **後処理を有効にする**（デフォルトで有効）

### 画像サイズに応じた推奨設定

- **小さい画像（<0.5MP）**: `--no-tile`
- **中程度の画像（0.5-4MP）**: `--tile 0`（自動調整）
- **大きい画像（>4MP）**: `--tile 400` または `--half`

## モデル選択の指針

### 人物写真の場合
- **RealESRGAN_x4plus**: 肌の質感、髪の毛の細部まで自然に拡大
- **RealESRNet_x4plus**: より高品質だが処理時間が長い

### アニメ・イラストの場合
- **RealESRGAN_x4plus_anime_6B**: アニメ特有の線画やグラデーションに最適化
- **realesr-animevideov3**: より軽量で高速

### 自動選択
画像タイプを指定すると、最適なモデルが自動選択されます：
```bash
python upscale_image.py -i image.jpg -o output.png -t photo    # 人物写真用モデル
python upscale_image.py -i image.jpg -o output.png -t anime    # アニメ用モデル
```

## 注意事項

- 初回実行時には、モデルファイルが自動的にダウンロードされます（約17-60MB）
- GPUがない場合はCPUで実行されますが、処理時間が長くなります
- メモリ不足が発生する場合は、`--half`オプションを使用してください

## ファイル構成

- `upscale_image.py`: メインスクリプト
- `requirements.txt`: 依存関係
- `venv/`: 仮想環境
- `input/`: 入力画像フォルダ（任意）
- `output/`: 出力画像フォルダ（任意）

## サポートされるモデル

- **RealESRGAN_x4plus**: 汎用実写画像（人物写真推奨）
- **RealESRGAN_x2plus**: 汎用実写画像（2倍スケール）
- **RealESRGAN_x4plus_anime_6B**: アニメ・イラスト専用
- **RealESRNet_x4plus**: 高品質実写画像（処理時間長）
- **realesr-animevideov3**: アニメ動画向け

## トラブルシューティング

### NumPyエラーが発生する場合

このプロジェクトではNumPy 1.x（< 2.0）を使用しています。NumPy 2.xがインストールされている場合は、以下のコマンドでダウングレードしてください：

```bash
pip install "numpy<2"
```

### メモリ不足エラーが発生する場合

`--half`オプションを使用してVRAMの使用量を削減してください：

```bash
python upscale_image.py -i image.jpg -o output.png -t photo --half
```

### 処理が遅い場合

1. タイルサイズを小さくする：
```bash
python upscale_image.py -i image.jpg -o output.png --tile 200
```

2. 2倍スケールモデルを使用：
```bash
python upscale_image.py -i image.jpg -o output.png -n RealESRGAN_x2plus
```
