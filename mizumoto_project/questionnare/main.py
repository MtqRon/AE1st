import matplotlib.pyplot as plt
from sheets import getData, getlines
import matplotlib as mpl
from abc import ABC, abstractmethod

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
        self.sex_counts = {
            "Male": 0,
            "Female": 0,
            "Other": 0,
            "No answer": 0
        }
    
    def count(self):
        """性別データを集計する"""
        for i in range(2, getlines):  # 2行目から開始（ヘッダーをスキップ）
            sex = getData(i, "sex")
            # 空白の行はスキップ
            if not sex or sex.strip() == "":
                continue
            # 日本語から英語への変換
            if sex == "男性":
                self.sex_counts["Male"] += 1
            elif sex == "女性":
                self.sex_counts["Female"] += 1
            elif sex == "どちらでもない":
                self.sex_counts["Other"] += 1
            elif sex == "回答しない/その他":
                self.sex_counts["No answer"] += 1
        
        return self.sex_counts

class CountAgeData(CountData):
    """年齢データ集計の具象クラス"""
    
    def __init__(self):
        self.age_counts = {
            "Under 19": 0,
            "20-29": 0,
            "30-39": 0,
            "40-49": 0,
            "50-59": 0,
            "60-69": 0,
            "Over 70": 0
        }
    
    def count(self):
        """年齢データを集計する"""
        for i in range(2, getlines):  # 2行目から開始（ヘッダーをスキップ）
            age = getData(i, "age")
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

class PlotSexData(PlotData):
    """性別データプロットの具象クラス"""
    
    def plot(self):
        """性別データをプロットする"""
        # データの取得
        sex_counts = self.count_data.count()
        
        # プロットの設定
        plt.figure(figsize=(10, 6))
        plt.bar(sex_counts.keys(), sex_counts.values())
        
        # グラフの装飾
        plt.title('Gender Distribution', fontsize=14)
        plt.xlabel('Gender', fontsize=12)
        plt.ylabel('Number of Responses', fontsize=12)
        
        # 数値を棒グラフの上に表示
        for i, v in enumerate(sex_counts.values()):
            plt.text(i, v, str(v), ha='center', va='bottom')
        
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
        plt.bar(age_counts.keys(), age_counts.values())
        
        # グラフの装飾
        plt.title('Age Distribution', fontsize=14)
        plt.xlabel('Age Group', fontsize=12)
        plt.ylabel('Number of Responses', fontsize=12)
        
        # X軸のラベルを回転
        plt.xticks(rotation=45)
        
        # 数値を棒グラフの上に表示
        for i, v in enumerate(age_counts.values()):
            plt.text(i, v, str(v), ha='center', va='bottom')
        
        # グラフの表示
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    # 性別データの集計とプロット
    count_sex = CountSexData()
    plot_sex = PlotSexData(count_sex)
    plot_sex.plot()
    
    # 年齢データの集計とプロット
    count_age = CountAgeData()
    plot_age = PlotAgeData(count_age)
    plot_age.plot()
