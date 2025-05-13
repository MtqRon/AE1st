# plot_csv.py
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("result2.csv")
plt.figure(figsize=(8,6))
plt.loglog(df.n, df.bubble, label="Bubble")
plt.loglog(df.n, df.insertion, label="Insertion")
plt.xlabel("n")
plt.ylabel("time (s)")
plt.title("Bubble vs Insertion")
plt.grid(True, which="both", ls="--", lw=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("result.png", dpi=150)   # ← 画像ファイル出力
plt.show()