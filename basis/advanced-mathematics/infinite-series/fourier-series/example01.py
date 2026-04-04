import numpy as np
import matplotlib.pyplot as plt

# 可选：指定 Matplotlib 后端（在某些环境下避免 GUI 问题）
# plt.switch_backend('TkAgg')   # 如果默认后端有问题，取消注释

# ---------- 设置中文字体 ----------
# 根据你的操作系统选择可用的中文字体
# 常见字体：
#   Windows: 'SimHei', 'Microsoft YaHei'
#   macOS:   'Noto Sans CJK SC', 'PingFang SC'
#   Linux:   'WenQuanYi Micro Hei', 'Noto Sans CJK SC'
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC']  # 请根据实际字体名称修改
plt.rcParams['axes.unicode_minus'] = False              # 解决负号显示问题
# ---------------------------------

# 参数设置
T = 2 * np.pi          # 周期
x = np.linspace(-2 * np.pi, 2 * np.pi, 1000)  # 画两个周期

# 定义原函数（分段周期函数）
def f_original(x):
    # 将 x 映射到 [-pi, pi)
    x_mod = np.mod(x + np.pi, T) - np.pi
    return np.where(x_mod > 0, 1, -1)

# 傅里叶级数部分和（仅正弦项）
def fourier_series(x, N):
    S = np.zeros_like(x)
    for n in range(1, N + 1, 2):  # 只取奇数项
        S += (4 / np.pi) * np.sin(n * x) / n
    return S

# 计算绘图数据
y_original = f_original(x)
N_values = [1, 3, 10, 50]  # 不同项数

# 创建图形
plt.figure(figsize=(10, 6))

# 绘制原函数（黑色实线）
plt.plot(x, y_original, 'k-', linewidth=2, label=r'原函数 $f(x)$')

# 绘制不同 N 的傅里叶级数逼近（彩色虚线）
for N in N_values:
    y_fourier = fourier_series(x, N)
    plt.plot(x, y_fourier, '--', label=rf'傅里叶级数 $S_{{{N}}}(x)$', alpha=0.7)

# 设置坐标轴范围及刻度
plt.xlim(-2 * np.pi, 2 * np.pi)
plt.xticks([-2 * np.pi, -np.pi, 0, np.pi, 2 * np.pi],
           [r'$-2\pi$', r'$-\pi$', r'$0$', r'$\pi$', r'$2\pi$'])
plt.xlabel(r'$x$')
plt.ylabel(r'$f(x)$')
plt.title('分段周期函数及其傅里叶级数')

# 添加图例、网格
plt.legend()
plt.grid(alpha=0.3)

# 显示图像
plt.show()