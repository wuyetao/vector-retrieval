from typing import Union, List, Dict, Any, Optional
import psycopg2
import psycopg2.extras
import requests
import os
import dashscope
import json
from http import HTTPStatus
from dashscope.embeddings.multimodal_embedding import (
    MultiModalEmbedding, MultiModalEmbeddingItemAudio,
    MultiModalEmbeddingItemImage, MultiModalEmbeddingItemText, AioMultiModalEmbedding)


class MultimodalVectorSystem:
    def __init__(self,
                 db_config: Dict[str, str]):
        """
        初始化多模态向量系统

        Args:
            db_config: 数据库配置
            aliyun_config: 阿里云API配置
        """
        self.db_config = db_config
        self.db_conn = None
        self.connect_db()

    def connect_db(self):
        """连接数据库"""
        try:
            self.db_conn = psycopg2.connect(**self.db_config)
            print("数据库连接成功")
        except Exception as e:
            print(f"数据库连接失败: {e}")
            raise

    def get_multimodal_embedding(self,
                                 input: str=None) -> List[float]:

        """
        调用阿里云多模态嵌入API获取向量

        Args:
            text: 文本内容
            image_path: 图片路径

        Returns:
            向量嵌入列表
        """

        # 准备请求数据
        data = [MultiModalEmbeddingItemImage(input, 1.0)
                if input.startswith("http") else MultiModalEmbeddingItemText(input, 1.0)]

        try:
            resp = dashscope.MultiModalEmbedding.call(
                model="multimodal-embedding-v1",
                input=data,
                api_key="sk-9eaf454af0e8452b89ef29205c8ecab7"
            )

            if resp.status_code == HTTPStatus.OK:
                result = {
                    "status_code": resp.status_code,
                    "request_id": getattr(resp, "request_id", ""),
                    "code": getattr(resp, "code", ""),
                    "message": getattr(resp, "message", ""),
                    "output": resp.output,
                    "usage": resp.usage
                }
                print(json.dumps(result, ensure_ascii=False, indent=4))
                return result.get("output").get("embeddings")[0].get("embedding")

            else:
                raise Exception(f"API调用失败: {resp.status_code} - {resp.text}")


        except Exception as e:
            print(f"获取嵌入向量失败: {e}")
            raise

    def insert_data(self, content_type: str, content: str,
                    metadata: Dict[str, Any] = None) -> Optional[int]:
        """
        插入数据到数据库

        Args:
            content_type: 内容类型 ('text' 或 'image')
            content: 内容（文本或图片路径）
            metadata: 元数据

        Returns:
            记录ID或None
        """
        embedding = self.get_multimodal_embedding(content)
        content_text = content

        if not embedding:
            print("获取嵌入向量失败，跳过插入")
            return None

        sql = """
        INSERT INTO multimodal_data 
        (content_type, content_text, embedding, metadata)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """

        try:
            with self.db_conn.cursor() as cursor:
                cursor.execute(sql, (
                    content_type,
                    content_text,
                    embedding,
                    json.dumps(metadata) if metadata else None
                ))
                record_id = cursor.fetchone()[0]
                self.db_conn.commit()
                return record_id
        except Exception as e:
            self.db_conn.rollback()
            print(f"插入数据失败: {e}")
            return None

    def search_with_embedding(self, embedding: List[float], top_k: int) -> List[Dict[str, Any]]:
        """使用指定向量进行搜索"""
        sql = """
        SELECT id, content_type, content_text, 
               metadata, embedding <=> %s::vector as similarity
        FROM multimodal_data where content_type = 'image'
        ORDER BY similarity ASC 
        LIMIT %s
        """

        try:
            with self.db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute(sql, (embedding, top_k))
                results = cursor.fetchall()

                return [
                    {
                        'id': row['id'],
                        'content_type': row['content_type'],
                        'content_text': row['content_text'],
                        'metadata': row['metadata'],
                        'similarity': float(row['similarity'])
                    }
                    for row in results
                ]
        except Exception as e:
            print(f"搜索失败: {e}")
            return []

if __name__ == '__main__':
    # 配置信息
    db_config = {
        'host': 'localhost',
        'port': 25432,
        'database': 'postgres',
        'user': 'postgres',
        'password': '19941126'
    }


    # 创建系统实例
    system = MultimodalVectorSystem(db_config)

    # 示例1: 插入文本数据
    # text_id = system.insert_data(
    #     "image",
    #     "https://cn.technode.com/wp-content/blogs.dir/18/files/2020/03/%E6%9D%AD%E5%B7%9E%E4%B8%8B%E5%9F%8E%E5%8C%BA-uai-1200x675.jpg",
    #     {'category': '景点', 'tags': ['杭州', '城市']}
    # )

    # 搜索
    # # search_embedding = system.get_multimodal_embedding("https://res.klook.com/image/upload/fl_lossy.progressive,q_60/cities/votenvae9mlactjurilc.jpg")
    search_embedding = system.get_multimodal_embedding("西湖")
    data = system.search_with_embedding(search_embedding, 5)
    print(data)

