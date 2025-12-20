import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # SiliconFlow API Configuration
    API_KEY = os.getenv("SILICONFLOW_API_KEY")
    BASE_URL = "https://api.siliconflow.cn/v1"
    
    # Models
    # 推荐使用能力较强的模型进行图提取
    EXTRACT_MODEL = "Qwen/Qwen2.5-72B-Instruct"  # or "deepseek-ai/DeepSeek-V2.5"
    # 检索和回答可以使用稍小的模型以提高速度，或者保持一致
    CHAT_MODEL = "Qwen/Qwen2.5-72B-Instruct" 
    EMBEDDING_MODEL = "BAAI/bge-large-zh-v1.5" # 硅基流动支持的 Embedding 模型，或者使用 text-embedding-3-small
    
    # GraphRAG Parameters
    CHUNK_SIZE = 600
    CHUNK_OVERLAP = 100
    MAX_GRAPH_DEPTH = 2
    
    # Retrieval Configuration (模仿原版 LightRAG Round-robin策略)
    TOP_K = 5  # 检索的文档数量
    
    # Generation Configuration
    TEMPERATURE = 0.1
    MAX_TOKENS = 2048
    
    # LLM 配置别名（为了兼容性）
    llm_model = CHAT_MODEL
    embedding_model = EMBEDDING_MODEL
    top_k = TOP_K
    temperature = TEMPERATURE
    max_tokens = MAX_TOKENS
    
    # Output
    GRAPH_OUTPUT_FILE = "graph_data.json"
    VECTOR_STORE_PATH = "vector_store.pkl"
