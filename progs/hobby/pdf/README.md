# PDF⇔画像変換プログラム（PyMuPDF版）

PDFファイルを画像（PNG/JPEG）に変換したり、画像ファイルをPDFに変換したりできるプログラムです。

## 機能

1. **PDFファイルを画像（PNG/JPEG）に変換**
2. **画像ファイルをPDFに変換**

## フォルダ構造

```
pdf/
├── input/           # 入力ファイル用フォルダ
│   ├── *.pdf       # 変換したいPDFファイルをここに配置
│   └── *.png/*.jpg # PDF化したい画像ファイルをここに配置
├── output/          # 出力ファイル用フォルダ
│   ├── *.png/*.jpg # 変換された画像ファイル
│   └── *.pdf       # 変換されたPDFファイル
└── pdf_to_image_pymupdf.py  # メインプログラム
```

## 必要なライブラリ

```bash
pip install PyMuPDF Pillow
```

## 使用方法

### 1. 基本的な使用方法

**PDFを自動検出して変換：**
```bash
python pdf_to_image_pymupdf.py
```
- `input/`フォルダ内のPDFファイルを自動検出
- `output/`フォルダに画像ファイルを出力

### 2. コマンドライン引数

**特定のPDFファイルを指定：**
```bash
python pdf_to_image_pymupdf.py input/document.pdf
```

**JPEG形式で変換：**
```bash
python pdf_to_image_pymupdf.py --format jpeg
```

**高解像度（600DPI）で変換：**
```bash
python pdf_to_image_pymupdf.py --dpi 600
```

**出力ディレクトリを指定：**
```bash
python pdf_to_image_pymupdf.py --output custom_output/
```

**JPEG品質を指定：**
```bash
python pdf_to_image_pymupdf.py --format jpeg --quality 85
```

### 3. 対話モード

引数なしで実行すると対話モードになります：
```bash
python pdf_to_image_pymupdf.py
```

メニューから以下を選択できます：
1. PDFを画像に変換
2. 画像をPDFに変換
3. 終了

### 4. 画像からPDFへの変換

Pythonスクリプト内で直接関数を呼び出すこともできます：
```python
from pdf_to_image_pymupdf import images_to_pdf

# input/フォルダ内の画像をPDFに変換
images_to_pdf('*.png', 'converted.pdf')
```

## オプション

| オプション | 短縮形 | デフォルト | 説明 |
|-----------|--------|-----------|------|
| `--output` | `-o` | `output/` | 出力ディレクトリ |
| `--format` | `-f` | `png` | 出力フォーマット（png/jpeg） |
| `--dpi` | `-d` | `300` | 解像度（DPI） |
| `--quality` | `-q` | `95` | JPEG品質（1-100） |

## 特徴

- **自動フォルダ作成**: `output/`フォルダが存在しない場合は自動で作成
- **自動PDFファイル検出**: `input/`フォルダ内のPDFファイルを自動検出
- **高品質変換**: PyMuPDFを使用した高品質な変換
- **対話モード**: ユーザーフレンドリーなメニュー式操作
- **柔軟な設定**: DPI、品質、フォーマットなど詳細設定可能

## エラーハンドリング

- ファイルが見つからない場合の適切なエラーメッセージ
- 無効なパラメータの範囲チェック
- 変換エラー時の詳細な情報表示

## 注意事項

- この版では、Popplerは不要です（PyMuPDFのみ使用）
- 大容量のPDFファイルは処理に時間がかかる場合があります
- JPEG品質は1-100の範囲で指定してください
