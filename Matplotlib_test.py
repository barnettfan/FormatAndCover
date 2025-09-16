import numpy as np
import matplotlib.pyplot as plt
import random

# 设置中文字体（根据你系统中安装的字体选择）
plt.rcParams['font.sans-serif'] = ['SimHei', 'FangSong']  # 黑体或仿宋等中文字体
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# 定义变量范围
score = np.linspace(0, 100, 100)
initialGap = 0.5
minGap = 0.15
k_values = [0.1, 0.2, 0.3, 0.4, 0.5,0.6,0.7,0.8,0.9,1]  # 不同的 k 值

# # 给 baseGap 添加随机数
# randomBaseGap = [bG * random.uniform(0.9, 1.1) for bG in baseGap]

# 设置 y 轴刻度：从 0.2 到 0.5，每隔 0.05 一个刻度
yticks = np.arange(0.1, 0.5 + 0.05, 0.05)  # 注意加一个步长确保包含 0.5
plt.yticks(yticks)

# 设置 y 轴范围（可选）
plt.ylim(0.10, 0.55)

# 绘制多条曲线
for k in k_values:
    baseGap = minGap + (initialGap - minGap) / (1.0 + score * k)
    plt.plot(score, baseGap, label=f'k={k}')  # 每个 k 值对应一条曲线，并设置图例

plt.xlabel('分数')
plt.ylabel('间隙百分比')
plt.title('间隙图')
plt.legend()
plt.grid(True)
plt.show()