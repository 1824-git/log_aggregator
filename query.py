"""
日志查询工具：按关键词搜索
"""
import json
import sys

def search_logs(file_path, keyword):
    """
    在日志文件中搜索包含关键词的日志
    
    参数:
        file_path: 日志文件路径（sorted_logs.json）
        keyword: 要搜索的关键词
    
    返回:
        匹配的日志列表
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logs = data.get('logs', [])
    except FileNotFoundError:
        print(f"[red]❌ 文件 {file_path} 不存在，请先运行 server.py 生成日志[/red]")
        return []
    
    results = []
    for log in logs:
        message = log.get('message', '')
        node = log.get('node_id', '')
        level = log.get('level', '')
        
        # 在消息、节点ID、级别中搜索关键词
        if (keyword.lower() in message.lower() or 
            keyword.lower() in node.lower() or 
            keyword.lower() in level.lower()):
            results.append(log)
    
    return results


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python query.py <关键词>")
        print("示例: python query.py node-A")
        print("示例: python query.py INFO")
        print("示例: python query.py 第5条")
        return
    
    keyword = sys.argv[1]
    print(f"[bold]🔍 正在搜索关键词: '{keyword}'[/bold]")
    
    results = search_logs('sorted_logs.json', keyword)
    
    if not results:
        print("[yellow]❌ 没有找到匹配的日志[/yellow]")
        return
    
    print(f"[green]✅ 找到 {len(results)} 条匹配的日志:[/green]\n")
    for i, log in enumerate(results, 1):
        print(f"{i}. [{log.get('node_id', 'N/A')}] {log.get('message', 'N/A')}")
        print(f"   级别: {log.get('level', 'N/A')}")
        print(f"   时钟: {log.get('vector_clock', {})}")
        print(f"   时间: {log.get('timestamp', 'N/A')}")
        print("-" * 30)

if __name__ == "__main__":
    main()