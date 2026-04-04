import numpy as np
import matplotlib.pyplot as plt

# ---------- 设置中文字体 ----------
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
# --------------------------------

# 参数设置
T = 2 * np.pi
x = np.linspace(-2 * np.pi, 2 * np.pi, 1000)

# 定义方波原函数
def square_wave(x):
    x_mod = np.mod(x + np.pi, T) - np.pi
    return np.where(x_mod > 0, 1, -1)

# 傅里叶级数部分和
def fourier_series_square(x, N):
    S = np.zeros_like(x)
    for n in range(1, N + 1, 2):
        S += (4 / np.pi) * np.sin(n * x) / n
    return S

# 计算原函数
y_original = square_wave(x)

# 要展示的部分和项数
N_values = [1, 3, 10, 50]

# 创建图形和坐标轴对象
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制原函数
ax.plot(x, y_original, 'k-', linewidth=2, label=r'原函数 $f(x)$')

# 绘制不同N的傅里叶级数
for N in N_values:
    y_fourier = fourier_series_square(x, N)
    ax.plot(x, y_fourier, '--', label=rf'部分和 $S_{{{N}}}(x)$', alpha=0.7)

# 在间断点处标记和函数的值（平均值0）
discontinuities = [-np.pi, 0, np.pi, 2*np.pi]
ax.scatter(discontinuities, [0, 0, 0, 0], color='blue', s=40, zorder=5,
           label=r'和函数值 (间断点平均值 $0$)')

# ---------- 设置坐标轴通过原点 ----------
# 隐藏上边和右边的脊线
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
# 让下边（x轴）和左边（y轴）的脊线通过原点
ax.spines['bottom'].set_position(('data', 0))   # x轴通过 y=0
ax.spines['left'].set_position(('data', 0))     # y轴通过 x=0

# 在原点处添加一个圆点（可选）
ax.plot(0, 0, 'ko', markersize=5)

# 设置坐标轴刻度及标签
ax.set_xlim(-2 * np.pi, 2 * np.pi)
ax.set_ylim(-1.5, 1.5)   # 适当扩大y轴范围，避免线条紧贴边缘
ax.set_xticks([-2*np.pi, -np.pi, 0, np.pi, 2*np.pi])
ax.set_xticklabels([r'$-2\pi$', r'$-\pi$', r'$0$', r'$\pi$', r'$2\pi$'])
ax.set_yticks([-1, 0, 1])
ax.set_yticklabels([r'$-1$', r'$0$', r'$1$'])

# 添加箭头（使坐标轴看起来更像坐标系）
# 在x轴和y轴末端加箭头
ax.annotate('', xy=(2*np.pi+0.2, 0), xytext=(-2*np.pi-0.2, 0),
            arrowprops=dict(arrowstyle='->', color='black', lw=0.8))
ax.annotate('', xy=(0, 1.5), xytext=(0, -1.5),
            arrowprops=dict(arrowstyle='->', color='black', lw=0.8))

# 添加轴标签（放在箭头旁边）
ax.text(2*np.pi+0.3, 0, r'$x$', fontsize=12, va='center')
ax.text(0, 1.55, r'$y$', fontsize=12, ha='center')

# 其他设置
ax.set_title('方波及其傅里叶级数逼近（坐标轴通过原点）')
ax.legend()
ax.grid(alpha=0.3)

plt.tight_layout()
plt.show()