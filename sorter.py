"""
日志排序器：按向量时钟的因果顺序排序
"""
from vector_clock import compare_clocks

def sort_logs_by_causality(logs):
    """
    按向量时钟的因果顺序对日志排序
    
    参数:
        logs: 日志列表，每条日志必须包含 'vector_clock' 字段
    
    返回:
        按因果关系排序后的日志列表（最早的在前）
    """
    # 复制一份，避免修改原列表
    sorted_logs = list(logs)
    
    # 使用冒泡排序（简单易懂，适合小数据量）
    n = len(sorted_logs)
    for i in range(n):
        for j in range(0, n - i - 1):
            clock1 = sorted_logs[j].get('vector_clock', {})
            clock2 = sorted_logs[j + 1].get('vector_clock', {})
            
            # 比较两个日志的因果顺序
            result = compare_clocks(clock1, clock2)
            
            # 如果 clock1 在 clock2 之后，交换位置
            if result == -1:  # clock2 在 clock1 之前
                sorted_logs[j], sorted_logs[j + 1] = sorted_logs[j + 1], sorted_logs[j]
    
    return sorted_logs


def print_logs_summary(logs):
    """
    打印日志摘要
    """
    print(f"\n[bold]📊 日志摘要[/bold]")
    print(f"  总条数: {len(logs)}")
    
    if not logs:
        return
    
    print(f"  时间范围: {logs[0].get('timestamp', 'N/A')} ~ {logs[-1].get('timestamp', 'N/A')}")
    
    # 按节点统计
    node_stats = {}
    for log in logs:
        node = log.get('node_id', 'unknown')
        node_stats[node] = node_stats.get(node, 0) + 1
    
    print("  各节点分布:")
    for node, count in node_stats.items():
        print(f"    {node}: {count} 条")