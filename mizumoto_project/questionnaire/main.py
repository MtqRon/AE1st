import matplotlib.pyplot as plt
from sheets import getData, getlines
import matplotlib as mpl
from abc import ABC, abstractmethod
from settings import (
    SEX_LABEL, AGE_LABEL, PREFECTURE_LABEL, PURPOSE_LABEL, EVALUATION_LABEL,
    SEX_CATEGORIES, AGE_CATEGORIES, PREFECTURE_CATEGORIES, PURPOSE_CATEGORIES, EVALUATION_CATEGORIES,
    PREFECTURE_COORDINATES
)
import webbrowser, os
import leafmap.foliumap as leafmap
import pandas as pd

# 日本語フォントの設定
plt.rcParams['font.family'] = 'MS Gothic'  # Windowsの場合
# plt.rcParams['font.family'] = 'Hiragino Sans'  # Macの場合
# plt.rcParams['font.family'] = 'Noto Sans JP'  # Linuxの場合

class CountData(ABC):
    """データ集計の抽象クラス"""
    
    @abstractmethod
    def count(self):
        """データを集計する抽象メソッド"""
        pass

class PlotData(ABC):
    """データプロットの抽象クラス"""
    
    def __init__(self, count_data: CountData):
        self.count_data = count_data
    
    @abstractmethod
    def plot(self):
        """データをプロットする抽象メソッド"""
        pass

class CountSexData(CountData):
    """性別データ集計の具象クラス"""
    
    def __init__(self):
        self.sex_counts = {v: 0 for v in SEX_CATEGORIES.values()}
    
    def count(self):
        """性別データを集計する"""
        for i in range(2, getlines):  # 2行目から開始（ヘッダーをスキップ）
            sex = getData(i, SEX_LABEL)
            # 空白の行はスキップ
            if not sex or sex.strip() == "":
                continue
            # 日本語から英語への変換
            if sex in SEX_CATEGORIES:
                self.sex_counts[SEX_CATEGORIES[sex]] += 1
        
        return self.sex_counts

class CountAgeData(CountData):
    """年齢データ集計の具象クラス"""
    
    def __init__(self):
        self.age_counts = {k: 0 for k in AGE_CATEGORIES.keys()}
    
    def count(self):
        """年齢データを集計する"""
        for i in range(2, getlines):  # 2行目から開始（ヘッダーをスキップ）
            age = getData(i, AGE_LABEL)
            # 空白の行はスキップ
            if not age or age.strip() == "":
                continue
            # 年齢の集計
            try:
                if age == "19歳以下":
                    self.age_counts["Under 19"] += 1
                elif age == "20-29歳":
                    self.age_counts["20-29"] += 1
                elif age == "30-39歳":
                    self.age_counts["30-39"] += 1
                elif age == "40-49歳":
                    self.age_counts["40-49"] += 1
                elif age == "50-59歳":
                    self.age_counts["50-59"] += 1
                elif age == "60-69歳":
                    self.age_counts["60-69"] += 1
                elif age == "70歳以上":
                    self.age_counts["Over 70"] += 1
            except ValueError:
                continue
        
        return self.age_counts

class CountPrefectureData(CountData):
    """都道府県データ集計の具象クラス"""
    
    def __init__(self):
        self.prefecture_counts = {v: 0 for v in PREFECTURE_CATEGORIES.values()}
    
    def count(self):
        for i in range(2, getlines):
            prefecture = getData(i, PREFECTURE_LABEL)

            # ① 取得失敗や空欄をまとめて無視
            if prefecture in ("", None, "error"):
                continue

            # ② 日本語 → 英語に変換してカウント
            if prefecture in PREFECTURE_CATEGORIES:
                self.prefecture_counts[PREFECTURE_CATEGORIES[prefecture]] += 1
        return self.prefecture_counts

class CountPurposeData(CountData):
    """来園目的データ集計の具象クラス"""
    
    def __init__(self):
        self.purpose_counts = {v: 0 for v in PURPOSE_CATEGORIES.values()}
    
    def count(self):
        """来園目的データを集計する"""
        for i in range(2, getlines):  # 2行目から開始（ヘッダーをスキップ）
            purpose = getData(i, PURPOSE_LABEL)
            # 空白の行はスキップ
            if not purpose or purpose.strip() == "":
                continue
            # 日本語から英語への変換
            if purpose in PURPOSE_CATEGORIES:
                self.purpose_counts[PURPOSE_CATEGORIES[purpose]] += 1
        
        return self.purpose_counts

class CountEvaluationData(CountData):
    """評価データ集計の具象クラス"""
    
    def __init__(self):
        self.evaluation_counts = {i: 0 for i in range(1, 6)}  # 1～5の評価
    
    def count(self):
        """評価データを集計する"""
        for i in range(2, getlines):  # 2行目から開始（ヘッダーをスキップ）
            evaluation = getData(i, EVALUATION_LABEL)
            # 空白の行はスキップ
            if not evaluation or evaluation.strip() == "":
                continue
            # 評価値の集計
            try:
                eval_value = int(evaluation)
                if 1 <= eval_value <= 5:
                    self.evaluation_counts[eval_value] += 1
            except ValueError:
                continue
        
        return self.evaluation_counts

class PlotSexData(PlotData):
    """性別データプロットの具象クラス"""
    def plot(self):
        """性別データをプロットする"""
        # データの取得
        sex_counts = self.count_data.count()
        
        # プロットの設定
        plt.figure(figsize=(10, 6))
        
        # 性別に応じた色を設定
        colors = ['#4A90E2', '#F5A623', '#7ED321', '#D0021B']  # 青、オレンジ、緑、赤
        
        # 棒グラフの作成
        bars = plt.bar(sex_counts.keys(), sex_counts.values(), color=colors[:len(sex_counts)])
        
        # グラフの装飾
        plt.title('Gender Distribution', fontsize=14)
        plt.xlabel('Gender', fontsize=12)
        plt.ylabel('Number of Responses', fontsize=12)
        
        # 数値を棒グラフの上に表示
        for i, v in enumerate(sex_counts.values()):
            plt.text(i, v, str(v), ha='center', va='bottom')
        
        # グリッドを追加
        plt.grid(axis='y', alpha=0.3)
        
        # グラフの表示
        plt.tight_layout()
        plt.show()

class PlotAgeData(PlotData):
    """年齢データプロットの具象クラス"""
    def plot(self):
        """年齢データをプロットする"""
        # データの取得
        age_counts = self.count_data.count()
        
        # プロットの設定
        plt.figure(figsize=(12, 6))
        
        # 年齢層に応じた色を設定（グラデーション）
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
        
        # 棒グラフの作成
        bars = plt.bar(age_counts.keys(), age_counts.values(), color=colors[:len(age_counts)])
        
        # グラフの装飾
        plt.title('Age Distribution', fontsize=14)
        plt.xlabel('Age Group', fontsize=12)
        plt.ylabel('Number of Responses', fontsize=12)
        
        # X軸のラベルを回転
        plt.xticks(rotation=45)
        
        # 数値を棒グラフの上に表示
        for i, v in enumerate(age_counts.values()):
            plt.text(i, v, str(v), ha='center', va='bottom')
        
        # グリッドを追加
        plt.grid(axis='y', alpha=0.3)
        
        # グラフの表示
        plt.tight_layout()
        plt.show()

class PlotPrefectureData(PlotData):
    """都道府県データプロットの具象クラス"""
    
    def plot(self):
        """都道府県データをヒートマップでプロットする"""
        # データの取得
        prefecture_counts = self.count_data.count()
        
        # データフレームの作成
        data = []
        for prefecture, count in prefecture_counts.items():
            if count > 0 and prefecture in PREFECTURE_COORDINATES:
                coords = PREFECTURE_COORDINATES[prefecture]
                data.append({
                    'lat': coords['lat'],
                    'lon': coords['lon'],
                    'count': count
                })
        
        df = pd.DataFrame(data)
        
        # 地図の作成
        m = leafmap.Map(center=[36.5, 138.0], zoom=5)
        
        # ヒートマップの追加
        m.add_heatmap(
            df,
            latitude='lat',
            longitude='lon',
            value='count',
            name='Prefecture Distribution',
            radius=20,
        )
        
        # 地図の表示
        html_path = "prefecture_heatmap.html"
        m.to_html(html_path)          # Leafmap推奨の書き出しメソッド
        print(f'ヒートマップを {html_path} に保存しました。')

        # Windows・Macならブラウザを自動起動
        webbrowser.open('file://' + os.path.realpath(html_path))

class PlotPurposeData(PlotData):
    """来園目的データプロットの具象クラス"""
    
    def plot(self):
        """来園目的データを円グラフでプロットする"""
        # データの取得
        purpose_counts = self.count_data.count()
        
        # 空のデータを除外
        filtered_data = {k: v for k, v in purpose_counts.items() if v > 0}
        
        if not filtered_data:
            print("来園目的のデータがありません。")
            return
        
        # プロットの設定
        plt.figure(figsize=(10, 8))
        
        # 円グラフの作成
        wedges, texts, autotexts = plt.pie(
            filtered_data.values(),
            labels=filtered_data.keys(),
            autopct='%1.1f%%',
            startangle=90
        )
        
        # グラフの装飾
        plt.title('Visit Purpose Distribution', fontsize=14)
        
        # テキストのフォントサイズを調整
        for text in texts:
            text.set_fontsize(10)
        for autotext in autotexts:
            autotext.set_fontsize(10)
            autotext.set_color('white')
            autotext.set_weight('bold')
        
        # グラフの表示
        plt.axis('equal')  # 円を正円にする
        plt.tight_layout()
        plt.show()

class PlotEvaluationData(PlotData):
    """評価データプロットの具象クラス"""
    
    def plot(self):
        """評価データを棒グラフでプロットする"""
        # データの取得
        evaluation_counts = self.count_data.count()
        
        # プロットの設定
        plt.figure(figsize=(10, 6))
        
        # X軸のラベル（1～5）
        labels = [str(i) for i in range(1, 6)]
        values = [evaluation_counts[i] for i in range(1, 6)]
        
        # 棒グラフの作成
        bars = plt.bar(labels, values, color=['#ff4444', '#ff8844', '#ffaa44', '#44aa44', '#4444ff'])
        
        # グラフの装飾
        plt.title('Evaluation Distribution', fontsize=14)
        plt.xlabel('Evaluation Score', fontsize=12)
        plt.ylabel('Number of Responses', fontsize=12)
        
        # 数値を棒グラフの上に表示
        for i, v in enumerate(values):
            plt.text(i, v, str(v), ha='center', va='bottom')
        
        # Y軸の範囲を設定
        plt.ylim(0, max(values) * 1.1 if max(values) > 0 else 1)
        
        # グリッドを追加
        plt.grid(axis='y', alpha=0.3)
        
        # グラフの表示
        plt.tight_layout()
        plt.show()

def plot_selected_separate(selected_graphs):
    """選択されたグラフを個別のウィンドウで表示"""
    graph_functions = {
        1: lambda: (CountSexData(), PlotSexData, "性別データ"),
        2: lambda: (CountAgeData(), PlotAgeData, "年齢データ"),
        3: lambda: (CountPurposeData(), PlotPurposeData, "来園目的データ"),
        4: lambda: (CountEvaluationData(), PlotEvaluationData, "評価データ"),
        5: lambda: (CountPrefectureData(), PlotPrefectureData, "都道府県データ")
    }
    
    for graph_num in selected_graphs:
        if graph_num in graph_functions:
            count_data, plot_class, graph_name = graph_functions[graph_num]()
            print(f"{graph_name}を表示中...")
            plot_obj = plot_class(count_data)
            plot_obj.plot()
        else:
            print(f"グラフ番号 {graph_num} は存在しません。")

def plot_all_separate():
    """各グラフを個別のウィンドウで表示"""
    plot_selected_separate([1, 2, 3, 4, 5])

def plot_selected_combined(selected_graphs):
    """選択されたグラフを一つのウィンドウで表示（サブプロット）"""
    # 都道府県データは別途処理
    prefecture_selected = 5 in selected_graphs
    graphs_for_subplot = [g for g in selected_graphs if g != 5]
    
    if not graphs_for_subplot and not prefecture_selected:
        print("表示するグラフが選択されていません。")
        return
    
    if graphs_for_subplot:
        # データの集計
        graph_data = {}
        if 1 in graphs_for_subplot:
            graph_data[1] = CountSexData().count()
        if 2 in graphs_for_subplot:
            graph_data[2] = CountAgeData().count()
        if 3 in graphs_for_subplot:
            graph_data[3] = CountPurposeData().count()
        if 4 in graphs_for_subplot:
            graph_data[4] = CountEvaluationData().count()
        
        # サブプロットの数を決定
        num_plots = len(graphs_for_subplot)
        if num_plots == 1:
            fig, ax = plt.subplots(1, 1, figsize=(10, 6))
            axes = [ax]
        elif num_plots == 2:
            fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        elif num_plots == 3:
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            axes = axes.flatten()[:3]
        else:  # num_plots == 4
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            axes = axes.flatten()
        
        plot_index = 0
        
        # 各グラフをプロット
        for graph_num in sorted(graphs_for_subplot):
            ax = axes[plot_index]
            
            if graph_num == 1:  # 性別データ
                sex_counts = graph_data[1]
                colors_sex = ['#4A90E2', '#F5A623', '#7ED321', '#D0021B']
                ax.bar(sex_counts.keys(), sex_counts.values(), color=colors_sex[:len(sex_counts)])
                ax.set_title('Gender Distribution', fontsize=12)
                ax.set_xlabel('Gender', fontsize=10)
                ax.set_ylabel('Number of Responses', fontsize=10)
                ax.grid(axis='y', alpha=0.3)
                for i, v in enumerate(sex_counts.values()):
                    ax.text(i, v, str(v), ha='center', va='bottom')
            
            elif graph_num == 2:  # 年齢データ
                age_counts = graph_data[2]
                colors_age = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
                ax.bar(age_counts.keys(), age_counts.values(), color=colors_age[:len(age_counts)])
                ax.set_title('Age Distribution', fontsize=12)
                ax.set_xlabel('Age Group', fontsize=10)
                ax.set_ylabel('Number of Responses', fontsize=10)
                ax.tick_params(axis='x', rotation=45)
                ax.grid(axis='y', alpha=0.3)
                for i, v in enumerate(age_counts.values()):
                    ax.text(i, v, str(v), ha='center', va='bottom')
            
            elif graph_num == 3:  # 来園目的データ
                purpose_counts = graph_data[3]
                filtered_purpose = {k: v for k, v in purpose_counts.items() if v > 0}
                if filtered_purpose:
                    wedges, texts, autotexts = ax.pie(
                        filtered_purpose.values(),
                        labels=filtered_purpose.keys(),
                        autopct='%1.1f%%',
                        startangle=90
                    )
                    for text in texts:
                        text.set_fontsize(8)
                    for autotext in autotexts:
                        autotext.set_fontsize(8)
                        autotext.set_color('white')
                        autotext.set_weight('bold')
                else:
                    ax.text(0.5, 0.5, 'No Purpose Data', ha='center', va='center', transform=ax.transAxes)
                ax.set_title('Visit Purpose Distribution', fontsize=12)
            
            elif graph_num == 4:  # 評価データ
                evaluation_counts = graph_data[4]
                labels_eval = [str(i) for i in range(1, 6)]
                values_eval = [evaluation_counts[i] for i in range(1, 6)]
                colors_eval = ['#ff4444', '#ff8844', '#ffaa44', '#44aa44', '#4444ff']
                ax.bar(labels_eval, values_eval, color=colors_eval)
                ax.set_title('Evaluation Distribution', fontsize=12)
                ax.set_xlabel('Evaluation Score', fontsize=10)
                ax.set_ylabel('Number of Responses', fontsize=10)
                ax.grid(axis='y', alpha=0.3)
                for i, v in enumerate(values_eval):
                    ax.text(i, v, str(v), ha='center', va='bottom')
                ax.set_ylim(0, max(values_eval) * 1.1 if max(values_eval) > 0 else 1)
            
            plot_index += 1
          # 未使用のサブプロットを非表示
        if num_plots == 3:
            axes[3].set_visible(False)
            plt.subplots_adjust(hspace=0.3)
        plt.tight_layout()
        
        # フルスクリーンで表示
        mng = plt.get_current_fig_manager()
        mng.window.state('zoomed')  # Windows用フルスクリーン
        
        plt.show()
    
    # 都道府県データの表示
    if prefecture_selected:
        print("\n都道府県データのヒートマップを表示中...")
        count_prefecture = CountPrefectureData()
        plot_prefecture = PlotPrefectureData(count_prefecture)
        plot_prefecture.plot()

def plot_all_combined():
    """すべてのグラフを一つのウィンドウで表示（サブプロット）"""
    plot_selected_combined([1, 2, 3, 4, 5])

def parse_graph_selection(input_str):
    """入力文字列からグラフ番号のリストを解析"""
    try:
        # スペースまたはコンマで分割
        parts = input_str.replace(',', ' ').split()
        
        # 0が含まれている場合の処理
        if '0' in parts:
            all_graphs = {1, 2, 3, 4, 5}
            exclude_graphs = set()
            
            for part in parts:
                num = int(part.strip())
                if num == 0:
                    continue  # 0は全表示の指示なのでスキップ
                elif -5 <= num <= -1:
                    exclude_graphs.add(-num)  # 負の数は除外対象
                elif 1 <= num <= 5:
                    # 0と一緒に正の数が指定された場合は警告
                    print(f"警告: 0（全表示）と正の数 {num} が同時に指定されています。0の設定を優先します。")
                else:
                    print(f"警告: グラフ番号 {num} は無効です（1-5の範囲、-1～-5で除外、または0で全表示）")
            
            # 全グラフから除外グラフを引く
            result_graphs = sorted(list(all_graphs - exclude_graphs))
            return result_graphs
        
        # 従来の処理（0が含まれていない場合）
        graph_numbers = []
        for part in parts:
            num = int(part.strip())
            if num == -1:
                return [1, 2, 3, 4, 5]  # すべてのグラフを表示（従来の機能保持）
            elif 1 <= num <= 5:
                graph_numbers.append(num)
            else:
                print(f"警告: グラフ番号 {num} は無効です（1-5の範囲、-1～-5で除外、または0で全表示）")
        return sorted(list(set(graph_numbers)))  # 重複を除去してソート
    except ValueError:
        print("エラー: 数値以外の文字が含まれています")
        return []

if __name__ == "__main__":
    print("グラフの表示方法を選択してください:")
    print("1: 各グラフを個別のウィンドウで表示")
    print("2: すべてのグラフを一つのウィンドウで表示")
    
    while True:
        try:
            choice = input("\n選択してください (1 または 2): ").strip()
            if choice in ["1", "2"]:
                # 表示方法選択後にグラフ番号リストを表示
                print("\nグラフ番号:")
                print("1: 性別データ")
                print("2: 年齢データ") 
                print("3: 来園目的データ")
                print("4: 評価データ")
                print("5: 都道府県データ")                
                print("0: すべてのグラフを表示（負の数で除外可能）")
                print("例: '0 -2 -3' → 性別、評価、都道府県データのみ表示")
                
                graph_input = input("\n表示するグラフ番号を入力してください（例: 1 2 4 または 0 -2 -3）: ").strip()
                selected_graphs = parse_graph_selection(graph_input)
                
                if selected_graphs:
                    if choice == "1":
                        if len(selected_graphs) == 5:
                            print("すべてのグラフを個別のウィンドウで表示します...")
                        else:
                            print(f"選択されたグラフ {selected_graphs} を個別のウィンドウで表示します...")
                        plot_selected_separate(selected_graphs)
                    else:  # choice == "2"
                        if len(selected_graphs) == 5:
                            print("すべてのグラフを一つのウィンドウで表示します...")
                        else:
                            print(f"選択されたグラフ {selected_graphs} を一つのウィンドウで表示します...")
                        plot_selected_combined(selected_graphs)
                else:
                    print("有効なグラフが選択されませんでした。")
                    continue
                break
            else:
                print("1 または 2 を入力してください。")
        except KeyboardInterrupt:
            print("\n処理を中断しました。")
            break