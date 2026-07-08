import socket
import json
import time
import random
import sys
from vector_clock import increment_clock  # 导入递增函数

# 从命令行读取节点ID
node_id = sys.argv[1] if len(sys.argv) > 1 else "node-A"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('127.0.0.1', 9999)

counter = 0
# 初始化向量时钟
clock = {}

while True:
    counter += 1
    # 每次发送前，把自己的计数器 +1
    clock = increment_clock(clock, node_id)
    
    log = {
        "node_id": node_id,
        "timestamp": time.time(),
        "level": random.choice(["INFO", "WARN", "ERROR"]),
        "message": f"这是 {node_id} 的第 {counter} 条日志",
        "vector_clock": clock  # 把向量时钟放进日志里
    }
    
    sock.sendto(json.dumps(log).encode('utf-8'), server_address)
    print(f"📤 [{node_id}] 发送: 第 {counter} 条, 时钟: {clock}")
    time.sleep(1)