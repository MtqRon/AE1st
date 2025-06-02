# -*- coding: utf-8 -*-
import os

# ファイルパス
input_file = r"c:\Users\MtqRon\Desktop\AE1st\chama_project\[LINE]️💙.txt"
output_file = r"c:\Users\MtqRon\Desktop\AE1st\chama_project\[LINE]️💙_filtered.txt"

try:
    # ファイルを読み込み
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 「くにやす まさき」が含まれていない行のみを抽出
    filtered_lines = [line for line in lines if 'くにやす まさき' not in line]
    
    # 新しいファイルに書き出し
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(filtered_lines)
    
    print(f"フィルタリング完了: {len(lines)} 行から {len(filtered_lines)} 行に削減されました")
    print(f"削除された行数: {len(lines) - len(filtered_lines)} 行")
    print(f"新しいファイルが作成されました: {output_file}")

except Exception as e:
    print(f"エラーが発生しました: {e}")
