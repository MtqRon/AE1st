#!/usr/bin/env python3
"""
Real-ESRGAN Image Upscaler
画像をReal-ESRGANで高解像度化するスクリプト
人物写真とアニメ画像に最適化されたモデルを選択可能
"""

import argparse
import os
import cv2
import numpy as np
from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet
from basicsr.archs.srvgg_arch import SRVGGNetCompact


def preprocess_image(img):
    """画像の前処理を行ってアーティファクトを軽減"""
    # 画像の型と値の範囲を確認
    if img.dtype != np.uint8:
        img = np.clip(img, 0, 255).astype(np.uint8)
    
    # 非常に軽微なノイズ軽減（大きい画像のみ）
    if img.shape[0] * img.shape[1] > 4000000:  # 4MP以上の場合のみ適用
        img = cv2.bilateralFilter(img, 3, 5, 5)
    return img


def postprocess_image(img):
    """画像の後処理を行ってアーティファクトを軽減"""
    # 画像の型と値の範囲を確認・修正
    if img.dtype != np.uint8:
        img = np.clip(img, 0, 255).astype(np.uint8)
    
    # 非常に軽微なアンシャープマスクでぼやけを改善
    # より安全なアプローチ
    blurred = cv2.GaussianBlur(img, (3, 3), 0.5)
    unsharp_mask = cv2.addWeighted(img, 1.1, blurred, -0.1, 0)
    
    # 値の範囲を0-255に制限
    unsharp_mask = np.clip(unsharp_mask, 0, 255).astype(np.uint8)
    return unsharp_mask


# 利用可能なモデル設定
MODELS = {
    'RealESRGAN_x4plus': {
        'description': '汎用的な実写画像向け（最も人物写真に適している）',
        'scale': 4,
        'model': RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4),
        'url': 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth'
    },
    'RealESRGAN_x2plus': {
        'description': '汎用的な実写画像向け（2倍スケール）',
        'scale': 2,
        'model': RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2),
        'url': 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth'
    },
    'RealESRGAN_x4plus_anime_6B': {
        'description': 'アニメ・イラスト画像向け（最もアニメに適している）',
        'scale': 4,
        'model': RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=6, num_grow_ch=32, scale=4),
        'url': 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth'
    },
    'RealESRNet_x4plus': {
        'description': '高品質な実写画像向け（処理時間は長いが高品質）',
        'scale': 4,
        'model': RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4),
        'url': 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.1/RealESRNet_x4plus.pth'
    },
    'realesr-animevideov3': {
        'description': 'アニメ動画向け（静止画にも使用可能）',
        'scale': 4,
        'model': SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=16, upscale=4, act_type='prelu'),
        'url': 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-animevideov3.pth'
    }
}


def list_models():
    """利用可能なモデルの一覧を表示"""
    print("\n=== 利用可能なモデル ===")
    for model_name, config in MODELS.items():
        print(f"{model_name}:")
        print(f"  説明: {config['description']}")
        print(f"  スケール: {config['scale']}x")
        print()


def get_model_recommendation(image_type):
    """画像タイプに基づく推奨モデルを返す"""
    if image_type == 'photo':
        return 'RealESRGAN_x4plus'
    elif image_type == 'anime':
        return 'RealESRGAN_x4plus_anime_6B'
    elif image_type == 'photo2':
        return 'RealESRNet_x4plus'
    else:
        return 'RealESRGAN_x4plus'


def main():
    parser = argparse.ArgumentParser(description='Real-ESRGAN Image Upscaler with Model Selection')
    parser.add_argument('-i', '--input', type=str, help='入力画像のパス')
    parser.add_argument('-o', '--output', type=str, help='出力画像のパス')
    parser.add_argument('-t', '--type', type=str, choices=['photo', 'anime', 'auto'], default='auto',
                       help='画像タイプ: photo (人物写真), anime (アニメ・イラスト), auto (自動選択)')
    parser.add_argument('-n', '--model_name', type=str, default=None,
                       help='使用するモデル名（指定しない場合は画像タイプから自動選択）')
    parser.add_argument('-s', '--scale', type=int, default=None, help='スケール倍率（モデルの既定値を上書き）')
    parser.add_argument('--half', action='store_true', help='半精度を使用してVRAMを節約')
    parser.add_argument('--list-models', action='store_true', help='利用可能なモデルの一覧を表示')
    parser.add_argument('--tile', type=int, default=0, help='タイルサイズ（0で自動、-1で無効、GPUメモリに応じて調整）')
    parser.add_argument('--no-tile', action='store_true', help='タイル処理を無効にする（小さい画像や高品質処理時）')
    parser.add_argument('--no-preprocess', action='store_true', help='前処理を無効にする')
    parser.add_argument('--no-postprocess', action='store_true', help='後処理を無効にする')
    
    args = parser.parse_args()
    
    # モデル一覧表示
    if args.list_models:
        list_models()
        return
    
    # 入力・出力の必須チェック
    if not args.input or not args.output:
        parser.error("入力画像パス(-i)と出力画像パス(-o)は必須です。")
        return
    
    # 入力ファイルの存在確認
    if not os.path.exists(args.input):
        print(f"エラー: 入力ファイル '{args.input}' が見つかりません。")
        return
    
    # モデル選択
    if args.model_name:
        if args.model_name not in MODELS:
            print(f"エラー: モデル '{args.model_name}' はサポートされていません。")
            print("利用可能なモデル:", list(MODELS.keys()))
            return
        selected_model = args.model_name
    else:
        if args.type == 'auto':
            print("画像タイプが指定されていないため、汎用モデルを使用します。")
            print("より良い結果を得るには -t photo または -t anime を指定してください。")
            selected_model = 'RealESRGAN_x4plus'
        else:
            selected_model = get_model_recommendation(args.type)
      # モデル設定の取得
    model_config = MODELS[selected_model]
    scale = args.scale if args.scale else model_config['scale']
    
    print(f"使用モデル: {selected_model}")
    print(f"説明: {model_config['description']}")
    print(f"スケール: {scale}x")
    
    # 画像の読み込み（タイル設定の前に画像サイズを確認するため）
    print(f"\n画像を読み込んでいます: {args.input}")
    img = cv2.imread(args.input, cv2.IMREAD_COLOR)
    if img is None:
        print(f"エラー: 画像を読み込めませんでした: {args.input}")
        return
    
    # 前処理の適用
    if not args.no_preprocess:
        print("前処理を適用しています...")
        img = preprocess_image(img)
    
    # 画像サイズの取得
    height, width = img.shape[:2]
    image_pixels = width * height
    print(f"画像サイズ: {width}x{height} ({image_pixels:,} ピクセル)")
    
    # タイル処理の設定を決定
    use_tile = True
    tile_size = 0
    tile_pad = 10
    
    # --no-tileオプションまたは小さい画像の場合はタイル処理を無効
    if args.no_tile or args.tile == -1:
        use_tile = False
        print("タイル処理: 無効")
    elif image_pixels < 500000:  # 0.5MP未満の小さい画像
        use_tile = False
        print("画像が小さいためタイル処理を無効にします")
    else:
        # タイルサイズの自動調整
        if args.tile == 0:  # 自動設定
            if image_pixels < 1000000:  # 1MP未満
                tile_size = min(1200, max(width, height) + 200)
                tile_pad = 50
            elif image_pixels < 4000000:  # 4MP未満
                tile_size = 800
                tile_pad = 40
            elif image_pixels < 10000000:  # 10MP未満
                tile_size = 600
                tile_pad = 35
            else:  # 10MP以上
                tile_size = 400
                tile_pad = 32
            print(f"タイルサイズを自動設定: {tile_size} (パディング: {tile_pad})")
        else:
            tile_size = args.tile
            # タイルサイズに応じてパディングを調整
            if tile_size >= 800:
                tile_pad = 50
            elif tile_size >= 600:
                tile_pad = 40
            else:
                tile_pad = 32
            print(f"タイルサイズ: {tile_size} (パディング: {tile_pad})")
    
    # Real-ESRGANerの初期化
    print("モデルを初期化しています...")
    try:
        if use_tile:
            upsampler = RealESRGANer(
                scale=scale,
                model_path=model_config['url'],
                model=model_config['model'], 
                tile=tile_size,
                tile_pad=tile_pad,
                pre_pad=0,  # pre_padを0に設定してアーティファクトを軽減
                half=args.half,
                gpu_id=None
            )
        else:
            upsampler = RealESRGANer(
                scale=scale,
                model_path=model_config['url'],
                model=model_config['model'],
                tile=0,  # タイル無効
                tile_pad=0,
                pre_pad=0,
                half=args.half,
                gpu_id=None
            )
    except Exception as e:
        print(f"モデル初期化エラー: {e}")
        print("CPUモードで再試行します...")
        if use_tile:
            upsampler = RealESRGANer(
                scale=scale,
                model_path=model_config['url'],
                model=model_config['model'],
                tile=tile_size,
                tile_pad=tile_pad,
                pre_pad=0,
                half=False,
                device='cpu'
            )
        else:
            upsampler = RealESRGANer(
                scale=scale,
                model_path=model_config['url'],
                model=model_config['model'],
                tile=0,
                tile_pad=0,
                pre_pad=0,                half=False,
                device='cpu'
            )
      # 高解像度化の実行
    print("画像を高解像度化しています...")
    print(f"入力画像の値範囲: {img.min()}-{img.max()}, 型: {img.dtype}")
    
    try:
        output, _ = upsampler.enhance(img, outscale=scale)
        print(f"処理後の値範囲: {output.min()}-{output.max()}, 型: {output.dtype}")
        
        # 出力値の正規化（必要に応じて）
        if output.max() > 255 or output.min() < 0:
            print("値の範囲を0-255に正規化しています...")
            output = np.clip(output, 0, 255)
        
        # 型の確認と変換
        if output.dtype != np.uint8:
            output = output.astype(np.uint8)
        
        # 後処理の適用
        if not args.no_postprocess and use_tile:
            print("後処理を適用してアーティファクトを軽減しています...")
            output = postprocess_image(output)
        
        # 保存前の最終チェック
        print(f"保存前の値範囲: {output.min()}-{output.max()}, 型: {output.dtype}")
        
        # 出力ディレクトリの作成
        output_dir = os.path.dirname(args.output)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 結果の保存
        success = cv2.imwrite(args.output, output)
        if success:
            print(f"\n✓ 高解像度化が完了しました: {args.output}")
        else:
            print(f"\n✗ 画像の保存に失敗しました: {args.output}")
            return
        
        # 元画像と結果のサイズを表示
        original_height, original_width = img.shape[:2]
        output_height, output_width = output.shape[:2]
        print(f"元画像サイズ: {original_width}x{original_height}")
        print(f"出力画像サイズ: {output_width}x{output_height}")
        print(f"拡大率: {output_width/original_width:.1f}x")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        print("\n解決方法:")
        print("- GPUメモリ不足の場合: --half オプションを使用")
        print("- タイル処理を無効にする: --no-tile オプションを使用")
        print("- タイルサイズを小さくする: --tile 200")
        print("- 別のモデルを試す: --list-models で確認")
        
        # メモリ不足の場合は自動的にタイルサイズを小さくして再試行
        if "out of memory" in str(e).lower() or "cuda" in str(e).lower():
            if use_tile and tile_size > 200:
                print(f"\nメモリ不足のため、タイルサイズを{tile_size//2}に縮小して再試行します...")
                try:
                    upsampler = RealESRGANer(
                        scale=scale,
                        model_path=model_config['url'],
                        model=model_config['model'],
                        tile=tile_size//2,
                        tile_pad=tile_pad,
                        pre_pad=0,
                        half=True,  # 半精度を強制                        gpu_id=None
                    )
                    output, _ = upsampler.enhance(img, outscale=scale)
                    
                    # 再試行時も値の範囲をチェック
                    if output.max() > 255 or output.min() < 0:
                        output = np.clip(output, 0, 255)
                    if output.dtype != np.uint8:
                        output = output.astype(np.uint8)
                    
                    # 後処理の適用
                    if not args.no_postprocess:
                        print("後処理を適用してアーティファクトを軽減しています...")
                        output = postprocess_image(output)
                    
                    # 出力ディレクトリの作成
                    output_dir = os.path.dirname(args.output)
                    if output_dir and not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                    
                    cv2.imwrite(args.output, output)
                    print(f"✓ 再試行で高解像度化が完了しました: {args.output}")
                    
                    # サイズ表示
                    original_height, original_width = img.shape[:2]
                    output_height, output_width = output.shape[:2]
                    print(f"元画像サイズ: {original_width}x{original_height}")
                    print(f"出力画像サイズ: {output_width}x{output_height}")
                    print(f"拡大率: {output_width/original_width:.1f}x")
                    
                except Exception as e2:
                    print(f"再試行も失敗しました: {e2}")
            else:
                print("タイルサイズがすでに最小値か、タイル処理が無効です。")
                print("CPUでの処理を試すか、より小さい画像で試してください。")


if __name__ == '__main__':
    main()
