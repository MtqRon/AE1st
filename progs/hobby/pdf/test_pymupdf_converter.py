#!/usr/bin/env python3
"""
PDF to Image Converter（PyMuPDF版）のテストスクリプト
"""

import os
import sys
from pathlib import Path

def test_pymupdf_converter():
    """PyMuPDF版PDF変換プログラムのテスト"""
    
    # ワークスペース内のPDFファイルを確認
    current_dir = Path(os.getcwd())
    pdf_files = list(current_dir.glob('*.pdf'))
    
    print("=== PDF to Image Converter（PyMuPDF版）テスト ===\n")
    
    if not pdf_files:
        print("❌ テスト用のPDFファイルが見つかりません。")
        return False
    
    print(f"✓ 発見されたPDFファイル: {len(pdf_files)}個")
    for pdf_file in pdf_files:
        print(f"  - {pdf_file.name}")
    
    # 必要なライブラリの確認
    try:
        import fitz  # PyMuPDF
        print("✓ PyMuPDF ライブラリ: インストール済み")
        print(f"  バージョン: {fitz.version[0]}")
    except ImportError:
        print("❌ PyMuPDF ライブラリが見つかりません。")
        print("   インストール: pip install PyMuPDF")
        return False
    
    try:
        from PIL import Image
        print("✓ Pillow ライブラリ: インストール済み")
    except ImportError:
        print("❌ Pillow ライブラリが見つかりません。")
        print("   インストール: pip install Pillow")
        return False
    
    # PyMuPDFでのPDF読み込みテスト
    try:
        test_pdf = pdf_files[0]
        print(f"\n🔍 PyMuPDFテスト: {test_pdf.name} を読み込み中...")
        
        # PDFを開く
        pdf_document = fitz.open(str(test_pdf))
        page_count = len(pdf_document)
        print(f"✓ PDF読み込み成功: {page_count} ページ")
        
        # 最初のページを低解像度で変換テスト
        if page_count > 0:
            page = pdf_document.load_page(0)
            zoom = 72 / 72.0  # 72DPI（低解像度）
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            print(f"✓ ページ変換テスト成功")
            print(f"  ページサイズ: {pix.width} x {pix.height}")
            print(f"  色空間: {pix.colorspace}")
        
        pdf_document.close()
        
    except Exception as e:
        print(f"❌ PyMuPDF エラー: {e}")
        return False
    
    print("\n✅ すべてのテストが正常に完了しました！")
    print("\n使用例:")
    print(f"  python pdf_to_image_pymupdf.py {pdf_files[0].name}")
    print(f"  python pdf_to_image_pymupdf.py {pdf_files[0].name} --format jpeg")
    print(f"  python pdf_to_image_pymupdf.py {pdf_files[0].name} --dpi 600")
    
    return True

def main():
    """メイン関数"""
    success = test_pymupdf_converter()
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
