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

    # 1. 科技类数据
    tech_data = [
        {
            "text": "人工智能是计算机科学的一个分支，旨在创造能够执行需要人类智能的任务的机器。",
            "category": "technology",
            "tags": ["AI", "机器学习", "计算机科学"],
        },
        {
            "text": "深度学习是机器学习的一个子领域，它使用包含多个层的神经网络来模拟人脑的学习过程。",
            "category": "technology",
            "tags": ["深度学习", "神经网络", "机器学习"],
        },
        {
            "text": "自然语言处理使计算机能够理解、解释和生成人类语言，广泛应用于聊天机器人和翻译系统。",
            "category": "technology",
            "tags": ["NLP", "语言处理", "人工智能"],
        },
        {
            "text": "计算机视觉是人工智能的一个领域，使计算机能够从数字图像或视频中获取高层次的理解。",
            "category": "technology",
            "tags": ["计算机视觉", "图像识别", "AI"],
        },
        {
            "text": "大数据技术用于处理和分析海量数据集，以发现模式、趋势和关联，支持商业决策。",
            "category": "technology",
            "tags": ["大数据", "数据分析", "数据处理"],
        }
    ]

    # 2. 动物类数据
    animal_data = [
        {
            "text": "大熊猫是中国的国宝，主要生活在四川的竹林中，以竹子为食，是濒危物种。",
            "category": "animal",
            "tags": ["熊猫", "濒危动物", "中国"],
        },
        {
            "text": "非洲象是陆地上最大的动物，拥有长长的象牙和大耳朵，主要生活在撒哈拉以南非洲。",
            "category": "animal",
            "tags": ["大象", "非洲", "野生动物"],
        },
        {
            "text": "帝企鹅是南极洲最大的企鹅物种，能够在极端寒冷的环境中生存和繁殖。",
            "category": "animal",
            "tags": ["企鹅", "南极", "鸟类"],
        },
        {
            "text": "孟加拉虎是大型猫科动物，主要分布在印度次大陆，是濒危的野生动物。",
            "category": "animal",
            "tags": ["老虎", "猫科", "濒危物种"],
        },
        {
            "text": "海豚是高度智能的海洋哺乳动物，以其友好的性格和复杂的社交行为而闻名。",
            "category": "animal",
            "tags": ["海豚", "海洋动物", "哺乳动物"],
        }
    ]

    # 3. 风景类数据
    scenery_data = [
        {
            "text": "桂林山水甲天下，以独特的喀斯特地貌和清澈的漓江而闻名于世。",
            "category": "scenery",
            "tags": ["桂林", "山水", "旅游"],
        },
        {
            "text": "黄山以奇松、怪石、云海、温泉四绝著称，是中国最著名的山脉之一。",
            "category": "scenery",
            "tags": ["黄山", "山脉", "自然景观"],
        },
        {
            "text": "九寨沟以其多彩的湖泊、瀑布和雪山而闻名，是世界自然遗产地。",
            "category": "scenery",
            "tags": ["九寨沟", "湖泊", "自然保护区"],
        },
        {
            "text": "张家界国家森林公园以独特的石英砂岩峰林地貌著称，是《阿凡达》取景地。",
            "category": "scenery",
            "tags": ["张家界", "国家公园", "峰林"],
        },
        {
            "text": "西湖以其湖光山色和众多的文化古迹而闻名，有'人间天堂'的美誉。",
            "category": "scenery",
            "tags": ["西湖", "杭州", "文化遗产"],
        }
    ]

    # 4. 食品类数据
    food_data = [
        {
            "text": "北京烤鸭是北京的传统名菜，以其皮脆肉嫩、色泽红艳而闻名世界。",
            "category": "food",
            "tags": ["烤鸭", "北京菜", "中餐"],
        },
        {
            "text": "四川火锅以麻辣鲜香著称，是川菜的代表，深受全国各地食客喜爱。",
            "category": "food",
            "tags": ["火锅", "川菜", "麻辣"],
        },
        {
            "text": "寿司是日本传统美食，主要材料是用醋调味过的冷饭，再加上鱼肉、海鲜、蔬菜等。",
            "category": "food",
            "tags": ["寿司", "日本料理", "海鲜"],
        },
        {
            "text": "意大利披萨源于那不勒斯，以其薄脆的饼底和丰富的配料而风靡全球。",
            "category": "food",
            "tags": ["披萨", "意大利菜", "西餐"],
        },
        {
            "text": "法式面包以其外脆内软的口感和独特的麦香味而闻名，是法国饮食文化的象征。",
            "category": "food",
            "tags": ["法式面包", "烘焙", "西点"],
        }
    ]

    # 合并所有数据
    all_data = tech_data + animal_data + scenery_data + food_data

    # 添加ID和时间戳
    for item in all_data:

        # 示例1: 插入文本数据
        text_id = system.insert_data(
            "text",
            item['text'],
            {'category': item['category'], 'tags': item['tags']}
        )
        print(f"插入文本数据，ID: {text_id}")

