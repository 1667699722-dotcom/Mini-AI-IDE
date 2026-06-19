"""
计算 sin(x) 在 [0, π/2] 上的积分
多种数值积分方法实现

解析解: ∫₀^{π/2} sin(x) dx = [-cos(x)]₀^{π/2} = -cos(π/2) - (-cos(0)) = 0 + 1 = 1
"""

import math

def exact_integral():
    """解析解"""
    return 1.0

# ========== 方法1: 矩形法 (左矩形) ==========
def left_rectangle(n):
    """左矩形法：用n个矩形逼近"""
    a, b = 0, math.pi / 2
    h = (b - a) / n
    total = 0.0
    for i in range(n):
        x = a + i * h
        total += math.sin(x)
    return total * h

# ========== 方法2: 矩形法 (右矩形) ==========
def right_rectangle(n):
    """右矩形法：用n个矩形逼近"""
    a, b = 0, math.pi / 2
    h = (b - a) / n
    total = 0.0
    for i in range(1, n + 1):
        x = a + i * h
        total += math.sin(x)
    return total * h

# ========== 方法3: 中点矩形法 ==========
def midpoint_rectangle(n):
    """中点矩形法：用n个矩形逼近，取每个子区间中点"""
    a, b = 0, math.pi / 2
    h = (b - a) / n
    total = 0.0
    for i in range(n):
        x = a + (i + 0.5) * h
        total += math.sin(x)
    return total * h

# ========== 方法4: 梯形法 ==========
def trapezoidal(n):
    """梯形法：用n个梯形逼近"""
    a, b = 0, math.pi / 2
    h = (b - a) / n
    total = 0.5 * (math.sin(a) + math.sin(b))
    for i in range(1, n):
        x = a + i * h
        total += math.sin(x)
    return total * h

# ========== 方法5: 辛普森法 (Simpson's 1/3 rule) ==========
def simpson(n):
    """
    辛普森1/3法则
    要求 n 必须为偶数
    """
    if n % 2 != 0:
        n += 1  # 调整为偶数
    a, b = 0, math.pi / 2
    h = (b - a) / n
    total = math.sin(a) + math.sin(b)
    for i in range(1, n):
        x = a + i * h
        if i % 2 == 0:
            total += 2 * math.sin(x)
        else:
            total += 4 * math.sin(x)
    return total * h / 3

# ========== 方法6: 辛普森3/8法则 ==========
def simpson_38(n):
    """
    辛普森3/8法则
    要求 n 是3的倍数
    """
    if n % 3 != 0:
        n = ((n // 3) + 1) * 3
    a, b = 0, math.pi / 2
    h = (b - a) / n
    total = math.sin(a) + math.sin(b)
    for i in range(1, n):
        x = a + i * h
        if i % 3 == 0:
            total += 2 * math.sin(x)
        else:
            total += 3 * math.sin(x)
    return total * 3 * h / 8

# ========== 方法7: 自适应辛普森法 ==========
def adaptive_simpson(f, a, b, tol=1e-6, depth=0, max_depth=50):
    """自适应辛普森法，自动细分区间以达到精度要求"""
    def simpson_rule(f, a, b):
        c = (a + b) / 2
        return (b - a) / 6 * (f(a) + 4 * f(c) + f(b))
    
    c = (a + b) / 2
    S = simpson_rule(f, a, b)
    S_left = simpson_rule(f, a, c)
    S_right = simpson_rule(f, c, b)
    
    if depth >= max_depth:
        return S
    
    if abs(S_left + S_right - S) < 15 * tol:
        return S_left + S_right + (S_left + S_right - S) / 15
    else:
        return (adaptive_simpson(f, a, c, tol/2, depth+1, max_depth) + 
                adaptive_simpson(f, c, b, tol/2, depth+1, max_depth))

# ========== 方法8: 蒙特卡洛法 ==========
def monte_carlo(n):
    """
    蒙特卡洛积分法
    在 [0, π/2] × [0, 1] 矩形区域内随机撒点
    统计落在曲线下方的点比例
    """
    import random
    a, b = 0, math.pi / 2
    count_under = 0
    for _ in range(n):
        x = random.uniform(a, b)
        y = random.uniform(0, 1)
        if y <= math.sin(x):
            count_under += 1
    rect_area = (b - a) * 1.0  # 矩形面积
    return rect_area * count_under / n

# ========== 方法9: 蒙特卡洛法(平均值法) ==========
def monte_carlo_mean(n):
    """
    蒙特卡洛积分法 - 平均值法
    ∫f(x)dx ≈ (b-a) * mean(f(x_i))
    """
    import random
    a, b = 0, math.pi / 2
    total = 0.0
    for _ in range(n):
        x = random.uniform(a, b)
        total += math.sin(x)
    return (b - a) * total / n

# ========== 测试和比较 ==========
def test_all_methods():
    exact = exact_integral()
    print(f"{'='*70}")
    print(f"sin(x) 在 [0, π/2] 上的积分")
    print(f"解析解 (精确值): {exact}")
    print(f"{'='*70}")
    
    ns = [4, 10, 100, 1000, 10000]
    
    methods = [
        ("左矩形法", left_rectangle),
        ("右矩形法", right_rectangle),
        ("中点矩形法", midpoint_rectangle),
        ("梯形法", trapezoidal),
        ("辛普森1/3法", simpson),
        ("辛普森3/8法", simpson_38),
    ]
    
    for name, method in methods:
        print(f"\n--- {name} ---")
        print(f"{'n':>6} | {'结果':>12} | {'误差':>14}")
        print("-" * 40)
        for n in ns:
            result = method(n)
            error = abs(result - exact)
            print(f"{n:>6} | {result:>12.8f} | {error:>14.2e}")
    
    # 自适应辛普森法
    print(f"\n--- 自适应辛普森法 ---")
    for tol in [1e-3, 1e-6, 1e-9]:
        result = adaptive_simpson(math.sin, 0, math.pi/2, tol)
        error = abs(result - exact)
        print(f"tol={tol:1.0e}: 结果={result:.12f}, 误差={error:.2e}")
    
    # 蒙特卡洛法
    print(f"\n--- 蒙特卡洛法 (平均值法) ---")
    import random
    random.seed(42)
    mc_ns = [100, 1000, 10000, 100000]
    print(f"{'n':>7} | {'结果':>12} | {'误差':>14}")
    print("-" * 40)
    for n in mc_ns:
        result = monte_carlo_mean(n)
        error = abs(result - exact)
        print(f"{n:>7} | {result:>12.8f} | {error:>14.2e}")

if __name__ == "__main__":
    test_all_methods()
