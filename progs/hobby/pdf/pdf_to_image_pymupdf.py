#!/usr/bin/env python3
"""
PDF⇔画像変換プログラム（PyMuPDF版）

機能:
1. PDFファイルを画像（PNG/JPEG）に変換
2. 画像ファイルをPDFに変換

使用方法:
    python pdf_to_image_pymupdf.py [OPTIONS]

必要なライブラリ:
    pip install PyMuPDF Pillow
    
この版では、Popplerは不要です。
"""

import os
import sys
import argparse
import glob
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image


def pdf_to_images_pymupdf(pdf_path, output_dir=None, output_format='png', dpi=300, quality=95):
    """
    PDFファイルを画像に変換する（PyMuPDF版）
      Args:
        pdf_path (str): PDFファイルのパス
        output_dir (str): 出力ディレクトリ（Noneの場合、outputディレクトリ）
        output_format (str): 出力フォーマット（'png' または 'jpeg'）
        dpi (int): 解像度（DPI）
        quality (int): JPEG品質（1-100、PNGの場合は無視）
    
    Returns:
        list: 作成された画像ファイルのパスリスト
    """
      # PDFファイルの存在確認
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDFファイルが見つかりません: {pdf_path}")
      # 出力ディレクトリの設定
    if output_dir is None:
        # デフォルトでoutputディレクトリを使用
        output_dir = os.path.join(os.getcwd(), "output")
    
    # 出力ディレクトリの作成
    os.makedirs(output_dir, exist_ok=True)
    
    # PDFファイル名（拡張子なし）を取得
    pdf_name = Path(pdf_path).stem
    
    try:
        print(f"PDFを変換中: {pdf_path}")
        print(f"DPI: {dpi}, フォーマット: {output_format.upper()}")
        
        # PDFを開く
        pdf_document = fitz.open(pdf_path)
        output_files = []
        
        # 各ページを処理
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            
            # DPIを基にズーム倍率を計算（デフォルト72DPIから指定DPIへ）
            zoom = dpi / 72.0
            mat = fitz.Matrix(zoom, zoom)
            
            # ページを画像として取得
            pix = page.get_pixmap(matrix=mat)
            
            # 出力ファイル名を生成
            output_filename = f"{pdf_name}_page_{page_num + 1:03d}.{output_format}"
            output_path = os.path.join(output_dir, output_filename)
            
            if output_format.lower() == 'jpeg':
                # JPEG形式で保存
                pix.save(output_path, output="jpeg", jpg_quality=quality)
            else:
                # PNG形式で保存
                pix.save(output_path)
            
            output_files.append(output_path)
            print(f"ページ {page_num + 1} を保存: {output_filename}")
        
        pdf_document.close()
        
        print(f"\n変換完了！ {len(output_files)} ページを変換しました。")
        print(f"出力ディレクトリ: {output_dir}")
        
        return output_files
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return []


def images_to_pdf(image_pattern, output_pdf=None, output_dir=None):
    """
    画像ファイルをPDFに変換する
      Args:
        image_pattern (str): 画像ファイルのパターン（例: "*.png", "image_*.jpg"）
        output_pdf (str): 出力PDFファイル名（Noneの場合は自動生成）
        output_dir (str): 出力ディレクトリ（Noneの場合はoutputディレクトリ）
    
    Returns:
        str: 作成されたPDFファイルのパス
    """
      # 画像ファイルを検索
    if os.path.isabs(image_pattern):
        image_files = glob.glob(image_pattern)
    else:
        # デフォルトでinputディレクトリから検索
        input_dir = os.path.join(os.getcwd(), "input")
        image_files = glob.glob(os.path.join(input_dir, image_pattern))
    
    if not image_files:
        raise FileNotFoundError(f"画像ファイルが見つかりません: {image_pattern}")
    
    # ファイル名でソート（ページ順序を保持）
    image_files.sort()
    
    # 出力ディレクトリの設定
    if output_dir is None:
        # デフォルトでoutputディレクトリを使用
        output_dir = os.path.join(os.getcwd(), "output")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 出力PDFファイル名の設定
    if output_pdf is None:
        # パターンから基本名を推測
        if "*" in image_pattern:
            base_name = image_pattern.replace("*", "").replace(".png", "").replace(".jpg", "").replace(".jpeg", "")
            if base_name.endswith("_page_"):
                base_name = base_name[:-6]  # "_page_"を除去
            output_pdf = f"{base_name.strip('_')}converted_from_images.pdf"
        else:
            output_pdf = "converted_from_images.pdf"
    
    output_path = os.path.join(output_dir, output_pdf)
    
    try:
        print(f"画像をPDFに変換中...")
        print(f"対象画像: {len(image_files)} ファイル")
        
        # 新しいPDFドキュメントを作成
        pdf_document = fitz.open()
        
        for i, image_file in enumerate(image_files, 1):
            print(f"処理中: {os.path.basename(image_file)} ({i}/{len(image_files)})")
            
            try:
                # 画像を開く
                pil_image = Image.open(image_file)
                
                # RGBAをRGBに変換（必要に応じて）
                if pil_image.mode == 'RGBA':
                    # 白い背景を作成
                    rgb_image = Image.new('RGB', pil_image.size, (255, 255, 255))
                    rgb_image.paste(pil_image, mask=pil_image.split()[-1])  # アルファチャンネルをマスクとして使用
                    pil_image = rgb_image
                elif pil_image.mode != 'RGB':
                    pil_image = pil_image.convert('RGB')
                
                # 一時的にPNG形式で保存（PyMuPDFに渡すため）
                temp_path = f"temp_image_{i}.png"
                pil_image.save(temp_path, "PNG")
                
                # PyMuPDFでページを作成
                img_doc = fitz.open(temp_path)
                pdf_bytes = img_doc.convert_to_pdf()
                img_doc.close()
                
                # 一時ファイルを削除
                os.remove(temp_path)
                
                # ページをメインPDFに追加
                img_pdf = fitz.open("pdf", pdf_bytes)
                pdf_document.insert_pdf(img_pdf)
                img_pdf.close()
                
            except Exception as e:
                print(f"警告: {image_file} の処理中にエラー: {e}")
                continue
        
        # PDFを保存
        if len(pdf_document) > 0:
            pdf_document.save(output_path)
            pdf_document.close()
            
            print(f"\n変換完了！")
            print(f"出力ファイル: {output_path}")
            print(f"ページ数: {len(image_files)}")
            
            return output_path
        else:
            print("\n変換に失敗しました。有効な画像ファイルがありませんでした。")
            return None
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None


def show_menu():
    """メニューを表示する"""
    print("\n" + "="*50)
    print("     PDF⇔画像変換プログラム（PyMuPDF版）")
    print("="*50)
    print("1. PDFを画像に変換")
    print("2. 画像をPDFに変換") 
    print("3. 終了")
    print("="*50)


def interactive_mode():
    """対話モードでプログラムを実行"""
    
    while True:
        show_menu()
        
        try:
            choice = input("\n選択してください (1-3): ").strip()
            
            if choice == '1':
                # PDF to Image
                pdf_to_image_interactive()
                
            elif choice == '2':
                # Image to PDF
                image_to_pdf_interactive()
                
            elif choice == '3':
                print("\nプログラムを終了します。")
                break
                
            else:
                print("\n無効な選択です。1-3の数字を入力してください。")
                
        except KeyboardInterrupt:
            print("\n\nプログラムを終了します。")
            break
        except Exception as e:
            print(f"\nエラーが発生しました: {e}")


def pdf_to_image_interactive():
    """PDF→画像変換の対話モード"""
    print("\n--- PDFを画像に変換 ---")
      # PDFファイルの選択
    input_dir = os.path.join(os.getcwd(), "input")
    pdf_files = list(Path(input_dir).glob('*.pdf'))
    
    if not pdf_files:
        print("inputディレクトリにPDFファイルが見つかりません。")
        pdf_path = input("PDFファイルのパスを入力してください: ").strip()
        if not pdf_path or not os.path.exists(pdf_path):
            print("無効なファイルパスです。")
            return
    elif len(pdf_files) == 1:
        pdf_path = str(pdf_files[0])
        print(f"PDFファイル: {pdf_files[0].name}")
    else:
        print("\n利用可能なPDFファイル:")
        for i, pdf_file in enumerate(pdf_files, 1):
            print(f"  {i}. {pdf_file.name}")
        
        try:
            choice = int(input(f"\n選択してください (1-{len(pdf_files)}): "))
            if 1 <= choice <= len(pdf_files):
                pdf_path = str(pdf_files[choice - 1])
            else:
                print("無効な選択です。")
                return
        except ValueError:
            print("数字を入力してください。")
            return
    
    # 出力フォーマットの選択
    print("\n出力フォーマット:")
    print("1. PNG（デフォルト）")
    print("2. JPEG")
    
    format_choice = input("選択してください (1-2, Enterでデフォルト): ").strip()
    output_format = 'jpeg' if format_choice == '2' else 'png'
    
    # DPIの設定
    dpi_choice = input("DPI設定 (デフォルト: 300): ").strip()
    try:
        dpi = int(dpi_choice) if dpi_choice else 300
    except ValueError:
        dpi = 300
    
    # JPEG品質の設定（JPEG選択時のみ）
    quality = 95
    if output_format == 'jpeg':
        quality_choice = input("JPEG品質 1-100 (デフォルト: 95): ").strip()
        try:
            quality = int(quality_choice) if quality_choice else 95
            quality = max(1, min(100, quality))  # 1-100の範囲に制限
        except ValueError:
            quality = 95
    
    # 変換実行
    try:
        output_files = pdf_to_images_pymupdf(
            pdf_path=pdf_path,
            output_format=output_format,
            dpi=dpi,
            quality=quality
        )
        
        if output_files:
            print(f"\n✓ 変換成功: {len(output_files)} 個のファイルを作成しました。")
        
    except Exception as e:
        print(f"\nエラー: {e}")


def image_to_pdf_interactive():
    """画像→PDF変換の対話モード"""
    print("\n--- 画像をPDFに変換 ---")
      # 画像ファイルパターンの入力
    input_dir = os.path.join(os.getcwd(), "input")
    
    # 利用可能な画像ファイルを表示
    png_files = list(Path(input_dir).glob('*.png'))
    jpg_files = list(Path(input_dir).glob('*.jpg')) + list(Path(input_dir).glob('*.jpeg'))
    
    if png_files or jpg_files:
        print("\ninputディレクトリの画像ファイル:")
        if png_files:
            print(f"  PNG: {len(png_files)} ファイル")
        if jpg_files:
            print(f"  JPEG: {len(jpg_files)} ファイル")
    
    print("\n画像ファイルパターンの例:")
    print("  *.png           - すべてのPNGファイル")
    print("  *.jpg           - すべてのJPGファイル") 
    print("  filename_*.png  - 特定のパターンのPNGファイル")
    
    pattern = input("\n画像ファイルパターンを入力してください: ").strip()
    if not pattern:
        pattern = "*.png"
        print(f"デフォルトパターンを使用: {pattern}")
    
    # 出力PDFファイル名の入力
    output_name = input("出力PDFファイル名 (Enterで自動生成): ").strip()
    if output_name and not output_name.endswith('.pdf'):
        output_name += '.pdf'
    
    # 変換実行
    try:
        output_file = images_to_pdf(
            image_pattern=pattern,
            output_pdf=output_name if output_name else None
        )
        
        if output_file:
            print(f"\n✓ 変換成功: {output_file}")
        
    except Exception as e:
        print(f"\nエラー: {e}")


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="PDF⇔画像変換プログラム（PyMuPDF版）",
        formatter_class=argparse.RawDescriptionHelpFormatter,        epilog="""
使用例:
    # inputディレクトリのPDFを自動検出して変換（PNG形式、300DPI）
    python pdf_to_image_pymupdf.py
    
    # 特定のPDFファイルを指定して変換
    python pdf_to_image_pymupdf.py input/document.pdf
    
    # JPEG形式で変換
    python pdf_to_image_pymupdf.py --format jpeg
    
    # 高解像度（600DPI）で変換
    python pdf_to_image_pymupdf.py --dpi 600
    
    # 出力ディレクトリを指定
    python pdf_to_image_pymupdf.py --output custom_output/
    
    # JPEG品質を指定
    python pdf_to_image_pymupdf.py --format jpeg --quality 85
        """
    )
    
    parser.add_argument(
        'pdf_file',        nargs='?',
        help='変換するPDFファイルのパス'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='出力ディレクトリ（指定しない場合はoutputディレクトリ）'
    )
    
    parser.add_argument(        '--format', '-f',
        choices=['png', 'jpeg'],
        default='png',
        help='出力フォーマット（デフォルト: png）'
    )
    
    parser.add_argument(
        '--dpi', '-d',
        type=int,
        default=300,
        help='解像度（DPI）（デフォルト: 300）'
    )
    
    parser.add_argument(
        '--quality', '-q',
        type=int,
        default=95,
        help='JPEG品質 1-100（デフォルト: 95）'
    )
    
    args = parser.parse_args()
      # PDFファイルが指定されていない場合
    if not args.pdf_file:
        # inputディレクトリ内のPDFファイルを探す
        input_dir = os.path.join(os.getcwd(), "input")
        pdf_files = list(Path(input_dir).glob('*.pdf'))
        
        if not pdf_files:
            print("inputディレクトリにPDFファイルが見つかりません。")
            print("使用方法: python pdf_to_image_pymupdf.py [PDF_FILE_PATH]")
            print("または、inputディレクトリにPDFファイルを配置してください。")
            sys.exit(1)
        elif len(pdf_files) == 1:
            args.pdf_file = str(pdf_files[0])
            print(f"PDFファイルを自動検出: {args.pdf_file}")
        else:
            print("複数のPDFファイルが見つかりました:")
            for i, pdf_file in enumerate(pdf_files, 1):
                print(f"  {i}. {pdf_file.name}")
            print("\nファイルを指定してください:")
            print("python pdf_to_image_pymupdf.py [PDF_FILE_PATH]")
            sys.exit(1)
      # 品質の範囲チェック
    if not (1 <= args.quality <= 100):
        print("エラー: JPEG品質は1-100の範囲で指定してください。")
        sys.exit(1)
    
    try:
        # PDF変換実行
        output_files = pdf_to_images_pymupdf(
            pdf_path=args.pdf_file,
            output_dir=args.output,
            output_format=args.format,
            dpi=args.dpi,
            quality=args.quality
        )
        
        if output_files:
            print(f"\n✓ 変換成功: {len(output_files)} 個のファイルを作成しました。")
        else:
            print("\n✗ 変換に失敗しました。")
            sys.exit(1)
            
    except Exception as e:
        print(f"\nエラー: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
