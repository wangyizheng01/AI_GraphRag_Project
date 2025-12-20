# GraphRAG 知识问答系统

这是一个基于图检索增强生成（Graph RAG）的智能问答系统，旨在通过结合知识图谱和向量检索技术，提升大语言模型在特定领域知识问答中的准确性和深度。

## ✨ 项目亮点

- **双路检索架构**：融合了基于 NetworkX 的图结构检索和基于 scikit-learn 的向量语义检索。
- **智能查询路由**：内置智能路由器，根据问题复杂度自动选择最佳检索策略（图检索、向量检索或混合检索）。
- **轻量级实现**：无需依赖 Neo4j 或 Milvus 等重型数据库，利用本地文件系统和内存即可运行，非常适合个人项目展示和快速原型开发。
- **模块化设计**：系统解耦为数据准备、索引构建、检索、路由和生成等独立模块，易于扩展和维护。
- **完整 RAG 流程**：实现了从文本分块、实体关系抽取、图谱构建到最终问答的全流程。

## 🚀 快速开始

### 1. 环境准备

确保你的系统安装了 Python 3.8+。

```bash
# 克隆项目
git clone https://github.com/your-username/graphrag-resume-project.git
cd graphrag-resume-project

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 API Key

本项目使用兼容 OpenAI 接口的模型服务（如 SiliconFlow）。请复制 `.env.example` 为 `.env` 并填入你的 API Key。

```bash
cp .env.example .env
```

在 `.env` 文件中：

```env
SILICONFLOW_API_KEY=your-api-key-here
```

### 3. 准备数据

将你需要构建知识库的文本文件命名为 `input.txt` 并放置在 `data/` 目录下。

### 4. 运行系统

```bash
python main.py
```

首次运行时，系统会自动进行：
1. 文本分块
2. 实体与关系抽取（构建知识图谱）
3. 向量索引构建

索引构建完成后，你就可以在命令行中与系统进行交互问答了。

## 🏗️ 项目结构

```
graphrag-resume-project/
├── data/                    # 数据存储目录
│   └── input.txt            # 输入文本数据
├── rag_modules/             # 核心功能模块
│   ├── __init__.py
│   ├── data_preparation.py  # 文本预处理与分块
│   ├── graph_indexing.py    # 实体关系抽取与图谱构建
│   ├── vector_store.py      # 轻量级向量存储实现
│   ├── graph_rag_retrieval.py # 图 RAG 检索逻辑
│   ├── hybrid_retrieval.py  # 混合检索逻辑
│   ├── intelligent_query_router.py # 智能查询路由
│   └── generation_integration.py   # 答案生成模块
├── config.py               # 全局配置参数
├── main.py                 # 程序入口
├── requirements.txt        # 项目依赖
└── README.md               # 项目说明文档
```

## 🛠️ 技术栈

- **语言**：Python
- **图计算**：NetworkX
- **向量检索**：scikit-learn (Cosine Similarity)
- **大模型接口**：OpenAI Python Client
- **工具库**：NumPy, python-dotenv

## 📝 实现细节

本项目模仿了生产级 GraphRAG 系统的核心逻辑，但进行了轻量化改造：

1. **图谱构建**：使用 LLM 从文本中提取实体（Entities）和关系（Relationships），构建 NetworkX 图对象。
2. **向量存储**：使用内存级向量存储，支持基于余弦相似度的语义检索。
3. **混合检索**：结合关键词匹配、向量相似度和图遍历算法，全面召回相关上下文。
4. **自适应回答**：根据检索到的上下文丰富度，动态生成回答。

## 📄 许可证

[MIT License](LICENSE)