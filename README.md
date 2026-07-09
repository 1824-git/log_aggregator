# 基于向量时钟的分布式日志聚合系统

## 系统架构图

```mermaid
flowchart TB
    subgraph 客户端
        A[node-A] --> E[UDP发送]
        B[node-B] --> E
        C[node-C] --> E
    end

    E --> F[server.py 接收]
    F --> G[向量时钟合并]
    G --> H[日志存储]
    H --> I[因果排序]
    I --> J[sorted_logs.json]
    J --> K[query.py 关键词查询]
```

## 向量时钟算法流程

### 节点发送日志流程

```mermaid
flowchart TD
    A[节点准备发送日志] --> B[读取当前向量时钟]
    B --> C[将自己的计数器 +1]
    C --> D[构造 JSON 日志]
    D --> E[通过 UDP 发送到服务端]
```

### 服务端接收合并流程

```mermaid
flowchart TD
    A[服务端收到日志] --> B[解析 JSON 提取向量时钟]
    B --> C[与全局时钟合并]
    C --> D[遍历新时钟的每个节点]
    D --> E[取最大值更新全局时钟]
    E --> F[日志存入列表]
```

### 因果比较逻辑

```mermaid
flowchart TD
    A[输入两个时钟 c1, c2] --> B[遍历所有节点]
    B --> C{c1值 > c2值?}
    C -->|是| D[c1不早于c2]
    C -->|否| E{c2值 > c1值?}
    E -->|是| F[c2不早于c1]
    E -->|否| G[继续检查下一节点]
    D --> H[返回: c1在c2之后]
    F --> I[返回: c2在c1之前]
    G --> J{所有节点检查完?}
    J -->|否| B
    J -->|是| K[返回: 并发/无因果关系]
```

## 日志格式 Schema

```json
{
  "node_id": "string",
  "vector_clock": {"node_id": "integer"},
  "timestamp": "float",
  "level": "INFO|WARN|ERROR",
  "message": "string"
}
```

## 运行演示

```bash
# 启动服务端
python server.py

# 启动3个节点（各开一个终端）
python client.py node-A
python client.py node-B
python client.py node-C

# 运行10秒后按 Ctrl+C 停止

# 查询日志
python query.py INFO
python query.py node-A
```

## 项目文件说明

| 文件 | 功能 |
|------|------|
| `vector_clock.py` | 向量时钟核心算法 |
| `client.py` | 日志采集 Agent |
| `server.py` | 聚合 Server |
| `sorter.py` | 因果排序器 |
| `query.py` | 关键词查询工具 |
| `test_vector_clock.py` | 单元测试 |

## 技术栈

- **语言**: Python 3.14
- **网络**: UDP Socket
- **存储**: JSON 文件
- **辅助库**: rich (彩色终端输出)

## 作者

1824-git
