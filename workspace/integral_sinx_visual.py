"""
计算 sin(x) 在 [0, π/2] 上的积分
包含可视化展示的完整版本

解析解: ∫₀^{π/2} sin(x) dx = 1
"""

import math

# 生成用于绘图的数据（存储为文本格式，可用于其他绘图工具）
def generate_data():
    a, b = 0, math.pi / 2
    n = 1000
    h = (b - a) / n
    
    # 生成函数数据点
    points = []
    for i in range(n + 1):
        x = a + i * h
        y = math.sin(x)
        points.append((x, y))
    return points

# 所有积分方法汇总
def compute_all_methods():
    exact = 1.0
    
    results = []
    
    # 不同的n值
    ns = [4, 8, 16, 32, 64, 128, 256, 512, 1024, 4096, 16384]
    
    for n in ns:
        row = {"n": n}
        row["左矩形"] = left_rectangle(n)
        row["右矩形"] = right_rectangle(n)
        row["中点矩形"] = midpoint_rectangle(n)
        row["梯形"] = trapezoidal(n)
        row["辛普森1/3"] = simpson(n)
        row["辛普森3/8"] = simpson_38(n)
        results.append(row)
    
    return results, exact

# 复用之前定义的方法
def left_rectangle(n):
    a, b = 0, math.pi / 2
    h = (b - a) / n
    total = 0.0
    for i in range(n):
        x = a + i * h
        total += math.sin(x)
    return total * h

def right_rectangle(n):
    a, b = 0, math.pi / 2
    h = (b - a) / n
    total = 0.0
    for i in range(1, n + 1):
        x = a + i * h
        total += math.sin(x)
    return total * h

def midpoint_rectangle(n):
    a, b = 0, math.pi / 2
    h = (b - a) / n
    total = 0.0
    for i in range(n):
        x = a + (i + 0.5) * h
        total += math.sin(x)
    return total * h

def trapezoidal(n):
    a, b = 0, math.pi / 2
    h = (b - a) / n
    total = 0.5 * (math.sin(a) + math.sin(b))
    for i in range(1, n):
        x = a + i * h
        total += math.sin(x)
    return total * h

def simpson(n):
    if n % 2 != 0:
        n += 1
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

def simpson_38(n):
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

def print_detailed_comparison():
    exact = 1.0
    results, _ = compute_all_methods()
    
    print("=" * 100)
    print(f"{'sin(x) 在 [0, π/2] 上的积分 — 多方法对比'.center(85)}")
    print(f"{'精确值 = 1.0'.center(85)}")
    print("=" * 100)
    
    # 表头
    header = f"{'n':>6} | {'左矩形':>12} | {'右矩形':>12} | {'中点矩形':>12} | {'梯形':>12} | {'辛普森1/3':>12} | {'辛普森3/8':>12}"
    print(header)
    print("-" * 100)
    
    for row in results:
        n = row["n"]
        line = f"{n:>6}"
        for method in ["左矩形", "右矩形", "中点矩形", "梯形", "辛普森1/3", "辛普森3/8"]:
            line += f" | {row[method]:>12.8f}"
        print(line)
    
    print("\n\n" + "=" * 100)
    print(f"{'误差对比 (|结果 - 精确值|)'.center(85)}")
    print("=" * 100)
    print(f"{'n':>6} | {'左矩形':>14} | {'右矩形':>14} | {'中点矩形':>14} | {'梯形':>14} | {'辛普森1/3':>14} | {'辛普森3/8':>14}")
    print("-" * 100)
    
    for row in results:
        n = row["n"]
        line = f"{n:>6}"
        for method in ["左矩形", "右矩形", "中点矩形", "梯形", "辛普森1/3", "辛普森3/8"]:
            err = abs(row[method] - exact)
            line += f" | {err:>14.2e}"
        print(line)
    
    print("\n\n" + "=" * 100)
    print(f"{'收敛阶分析 (误差随n的变化)'.center(85)}")
    print("=" * 100)
    
    print("\n各方法的收敛阶（理论值）：")
    print("  - 左/右矩形法: O(1/n)     — 一阶收敛")
    print("  - 中点矩形法:  O(1/n²)    — 二阶收敛")
    print("  - 梯形法:      O(1/n²)    — 二阶收敛")
    print("  - 辛普森1/3法: O(1/n⁴)    — 四阶收敛")
    print("  - 辛普森3/8法: O(1/n⁴)    — 四阶收敛")
    
    print("\n\n实际误差比（展示收敛阶）：")
    # 取 n=128 和 n=256 的误差比
    err_rows = [r for r in results if r["n"] in [128, 256]]
    if len(err_rows) == 2:
        print(f"{'方法':>12} | {'err(n=128)':>14} | {'err(n=256)':>14} | {'比值':>10} | {'理论阶':>8}")
        print("-" * 60)
        for method in ["左矩形", "右矩形", "中点矩形", "梯形", "辛普森1/3", "辛普森3/8"]:
            e128 = abs(err_rows[0][method] - 1.0)
            e256 = abs(err_rows[1][method] - 1.0)
            ratio = e128 / e256 if e256 != 0 else float('inf')
            print(f"{method:>12} | {e128:>14.2e} | {e256:>14.2e} | {ratio:>10.2f} |", end="")
            if ratio > 3.5 and ratio < 4.5:
                print(f" {'O(1/n²)':>8}")
            elif ratio > 1.5 and ratio < 2.5:
                print(f" {'O(1/n)':>8}")
            elif ratio > 15 and ratio < 17:
                print(f" {'O(1/n⁴)':>8}")
            else:
                print(f" {'?':>8}")
    
    print("\n" + "=" * 100)
    print(f"{'方法对比总结'.center(85)}")
    print("=" * 100)
    
    print("""
精度排名（相同n下）：
  1. 辛普森1/3法    — 精度最高，四阶收敛
  2. 辛普森3/8法    — 精度与辛普森1/3相当
  3. 中点矩形法     — 二阶收敛，精度好
  4. 梯形法         — 二阶收敛，精度稍逊于中点矩形
  5. 左/右矩形法    — 一阶收敛，精度最低

推荐使用：
  - 一般用途: 中点矩形法或梯形法（简单、稳定）
  - 高精度: 辛普森1/3法（四阶收敛，效率高）
  - 自适应需求: 自适应辛普森法
  - 随机模拟教学: 蒙特卡洛法
    
∫₀^{π/2} sin(x) dx = 1   ✅
""")

if __name__ == "__main__":
    print_detailed_comparison()
