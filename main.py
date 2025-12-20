import os
import sys
import json
import logging
import networkx as nx
from openai import OpenAI
from config import Config
from rag_modules import (
    DataPreparationModule,
    GraphIndexingModule,
    VectorStore,
    GraphRAGRetrieval,
    HybridRetrievalModule,
    GenerationIntegrationModule,
    IntelligentQueryRouter
)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    print("=== GraphRAG 知识问答系统 ===")
    
    # 检查 API Key
    if not Config.API_KEY or "sk-your-key-here" in Config.API_KEY:
        print("错误：请在 .env 文件中设置 SILICONFLOW_API_KEY")
        return
    
    # 初始化 OpenAI 客户端
    llm_client = OpenAI(
        api_key=Config.API_KEY,
        base_url=Config.BASE_URL
    )
    
    # 阶段1：索引构建
    graph_file = Config.GRAPH_OUTPUT_FILE
    vector_file = Config.VECTOR_STORE_PATH
    
    if not os.path.exists(graph_file) or not os.path.exists(vector_file):
        print("\n[阶段 1] 开始构建知识图谱和向量索引...")
        
        try:
            # 读取输入文本
            with open("data/input.txt", "r", encoding="utf-8") as f:
                text = f.read()
            
            # 1. 文本分块
            logger.info("正在进行文本分块...")
            data_prep = DataPreparationModule(Config)
            chunks = data_prep.chunk_text(text)
            logger.info(f"分块完成，共 {len(chunks)} 个块")
            
            # 2. 构建图索引
            logger.info("正在构建知识图谱...")
            graph_indexing = GraphIndexingModule(Config, llm_client)
            graph = graph_indexing.build_graph_from_chunks(chunks)
            
            # 保存图
            graph_data = nx.node_link_data(graph)
            with open(graph_file, 'w', encoding='utf-8') as f:
                json.dump(graph_data, f, ensure_ascii=False, indent=2)
            
            stats = graph_indexing.get_statistics()
            logger.info(f"图谱构建完成: {stats}")
            
            # 3. 构建向量索引
            logger.info("正在构建向量索引...")
            vector_store = VectorStore(Config)
            
            # 准备向量索引的数据
            chunk_texts = chunks
            chunk_metadata = [
                {
                    "text": chunk,
                    "chunk_id": f"chunk_{i}",
                    "recipe_name": f"文档块_{i}"
                } for i, chunk in enumerate(chunks)
            ]
            
            vector_store.add_texts(chunk_texts, chunk_metadata)
            logger.info("向量索引构建完成")
            
            print("✓ 索引构建完成！\n")
            
        except FileNotFoundError:
            print("错误：data/input.txt 文件不存在")
            return
        except Exception as e:
            logger.error(f"索引构建失败: {e}")
            return
    else:
        print(f"\n[阶段 1] 发现已有索引文件，加载中...")
        
        # 加载图
        with open(graph_file, 'r', encoding='utf-8') as f:
            graph_data = json.load(f)
        graph = nx.node_link_graph(graph_data)
        
        # 重建 graph_indexing（用于检索）
        graph_indexing = GraphIndexingModule(Config, llm_client)
        graph_indexing.graph = graph
        graph_indexing._rebuild_kv_stores()
        
        # 加载向量索引
        vector_store = VectorStore(Config)
        vector_store.load()
        
        print(f"✓ 索引加载完成（图: {graph.number_of_nodes()} 节点, {graph.number_of_edges()} 边）\n")
    
    # 阶段2：初始化检索和生成模块
    print("[阶段 2] 初始化检索系统...")
    
    # 图RAG检索
    graph_rag_retrieval = GraphRAGRetrieval(Config, llm_client, graph)
    graph_rag_retrieval.initialize()
    
    # 混合检索
    hybrid_retrieval = HybridRetrievalModule(Config, vector_store, graph_indexing, llm_client)
    hybrid_retrieval.initialize()
    
    # 智能路由器
    query_router = IntelligentQueryRouter(
        traditional_retrieval=hybrid_retrieval,
        graph_rag_retrieval=graph_rag_retrieval,
        llm_client=llm_client,
        config=Config
    )
    
    # 生成模块
    generation = GenerationIntegrationModule(llm_client, Config)
    
    print("✓ 系统初始化完成\n")
    
    # 阶段3：交互式问答
    print("[阶段 3] 进入问答模式（输入 'exit' 退出）\n")
    
    while True:
        try:
            question = input("请输入问题: ").strip()
            
            if question.lower() in ['exit', 'quit', '退出']:
                print("感谢使用！")
                break
            
            if not question:
                continue
            
            print("\n正在思考...\n")
            
            # 使用智能路由器检索
            documents, analysis = query_router.route_query(question, top_k=5)
            
            print(f"检索策略: {analysis.recommended_strategy.value}")
            print(f"置信度: {analysis.confidence:.2f}")
            print(f"推理: {analysis.reasoning}\n")
            
            # 生成答案
            answer = generation.generate_adaptive_answer(question, documents)
            
            print(f"回答:\n{answer}\n")
            print("-" * 80 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n感谢使用！")
            break
        except Exception as e:
            logger.error(f"处理问题时出错: {e}")
            print(f"抱歉，处理您的问题时出现错误：{str(e)}\n")

if __name__ == "__main__":
    main()