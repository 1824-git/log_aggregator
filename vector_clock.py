"""
向量时钟工具模块
"""

def merge_clock(existing, new):
    """
    合并两个向量时钟，逐项取最大值
    
    参数:
        existing: 现有的时钟字典，如 {'A': 3, 'B': 1}
        new: 新收到的时钟字典，如 {'A': 2, 'B': 2, 'C': 1}
    
    返回:
        合并后的时钟字典，如 {'A': 3, 'B': 2, 'C': 1}
    """
    result = dict(existing)  # 复制一份
    
    for node, count in new.items():
        if node not in result or count > result[node]:
            result[node] = count
    
    return result


def compare_clocks(clock1, clock2):
    """
    比较两个向量时钟的因果顺序
    
    返回:
        1: clock1 在 clock2 之前（happened-before）
        -1: clock2 在 clock1 之前
        0: 同时发生（并发），无法确定先后
    """
    # 检查是否 clock1 <= clock2
    clock1_le_clock2 = True
    clock2_le_clock1 = True
    
    all_nodes = set(clock1.keys()) | set(clock2.keys())
    
    for node in all_nodes:
        v1 = clock1.get(node, 0)
        v2 = clock2.get(node, 0)
        
        if v1 > v2:
            clock1_le_clock2 = False
        if v2 > v1:
            clock2_le_clock1 = False
    
    if clock1_le_clock2 and not clock2_le_clock1:
        return 1  # clock1 在 clock2 之前
    elif clock2_le_clock1 and not clock1_le_clock2:
        return -1  # clock2 在 clock1 之前
    else:
        return 0  # 并发（同时发生）


def increment_clock(clock, node_id):
    """
    节点产生新事件时，将自己的计数器 +1
    """
    result = dict(clock)
    result[node_id] = result.get(node_id, 0) + 1
    return result