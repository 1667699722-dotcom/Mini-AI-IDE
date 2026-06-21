import math

# 定义被积函数
def f(x):
    return math.sin(x)

# 使用数值积分（辛普森法）计算 sin(x) 在 [0, 2] 上的积分
a = 0.0
b = 2.0
n = 10000  # 区间划分数（偶数）
h = (b - a) / n

# 辛普森 1/3 法则
s = f(a) + f(b)
for i in range(1, n):
    x = a + i * h
    if i % 2 == 0:
        s += 2 * f(x)
    else:
        s += 4 * f(x)

result = (h / 3) * s
print(f"sin(x) 在 [0, 2] 上的定积分 ≈ {result}")
print(f"精确值（理论）： -cos(2) - (-cos(0)) = 1 - cos(2) = {1 - math.cos(2)}")
