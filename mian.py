from multimodalVectorSystem import MultimodalVectorSystem


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



    # 图片相似性搜索
    # search_embedding = system.get_multimodal_embedding("https://res.klook.com/image/upload/fl_lossy.progressive,q_60/cities/votenvae9mlactjurilc.jpg")
    # 文字相似性搜索
    search_embedding = system.get_multimodal_embedding("杭州旅游推荐")
    data = system.search_with_embedding(search_embedding, 3)
    print(data)