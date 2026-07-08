from vector_clock import merge_clock, compare_clocks, increment_clock

# 测试1: 合并
print("=== 测试合并 ===")
existing = {'A': 3, 'B': 1}
new = {'A': 2, 'B': 2, 'C': 1}
merged = merge_clock(existing, new)
print(f"合并前: {existing}")
print(f"合并后: {merged}")
print()

# 测试2: 比较
print("=== 测试因果比较 ===")
c1 = {'A': 3, 'B': 1}
c2 = {'A': 4, 'B': 1}
c3 = {'A': 2, 'B': 2}

result1 = compare_clocks(c1, c2)  # c1 在 c2 之前
result2 = compare_clocks(c1, c3)  # 并发

print(f"c1 {c1}")
print(f"c2 {c2}")
print(f"c1 vs c2: {'c1在c2之前' if result1 == 1 else 'c2在c1之前' if result1 == -1 else '并发'}")
print()
print(f"c1 {c1}")
print(f"c3 {c3}")
print(f"c1 vs c3: {'c1在c3之前' if result2 == 1 else 'c3在c1之前' if result2 == -1 else '并发'}")
print()

# 测试3: 递增
print("=== 测试递增 ===")
clock = {'A': 3, 'B': 1}
new_clock = increment_clock(clock, 'A')
print(f"原时钟: {clock}")
print(f"A递增后: {new_clock}")