import socket
import json
from rich import print
from vector_clock import merge_clock
from sorter import sort_logs_by_causality, print_logs_summary

# 存储所有收到的日志
all_logs = []
global_clock = {}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('0.0.0.0', 9999)
sock.bind(server_address)

print("[bold green]✅ 日志接收器已启动，监听 9999 端口...[/bold green]")
print("[yellow]📊 按 Ctrl+C 停止并保存排序后的日志[/yellow]\n")

try:
    while True:
        data, client_address = sock.recvfrom(4096)
        try:
            log_entry = json.loads(data.decode('utf-8'))
            received_clock = log_entry.get('vector_clock', {})
            
            # 合并全局时钟
            global_clock = merge_clock(global_clock, received_clock)
            
            # 存储日志
            all_logs.append(log_entry)
            
            print(f"[cyan]📥 来自 {log_entry['node_id']}: {log_entry['message']}[/cyan]")
            print(f"  时钟: {received_clock}")
            print(f"  已接收: {len(all_logs)} 条")
            print("-" * 40)
            
        except json.JSONDecodeError:
            print(f"[red]❌ 无效JSON: {data}[/red]")
            
except KeyboardInterrupt:
    print("\n[yellow]⏹️  正在停止并排序日志...[/yellow]\n")
    
    # 按因果顺序排序
    print("[bold]🔄 正在按因果顺序排序...[/bold]")
    sorted_logs = sort_logs_by_causality(all_logs)
    
    # 显示摘要
    print_logs_summary(sorted_logs)
    
    # 保存到文件
    output = {
        "total_count": len(sorted_logs),
        "global_clock": global_clock,
        "logs": sorted_logs
    }
    
    with open('sorted_logs.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n[green]✅ 已保存 {len(sorted_logs)} 条排序后的日志到 sorted_logs.json[/green]")
    
    # 显示前3条和后3条
    if len(sorted_logs) > 0:
        print("\n[bold]📋 前3条日志:[/bold]")
        for i, log in enumerate(sorted_logs[:3]):
            print(f"  {i+1}. [{log['node_id']}] {log['message']} (时钟: {log.get('vector_clock', {})})")
        
        if len(sorted_logs) > 6:
            print("  ...")
        
        print("\n[bold]📋 后3条日志:[/bold]")
        for i, log in enumerate(sorted_logs[-3:]):
            idx = len(sorted_logs) - 3 + i
            print(f"  {idx+1}. [{log['node_id']}] {log['message']} (时钟: {log.get('vector_clock', {})})")