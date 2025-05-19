import json
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# ---------------------- 配置参数 ----------------------
DATA_SCALE = 10000  # 生成的数据量
OUTPUT_FILE = "./data/user_event_log.json"  # 输出文件名

# 事件类型及其对应的事件信息生成逻辑
EVENT_TYPES = {
    'Login': lambda: {"device": fake.random_element(elements=("PC", "Mobile", "Tablet"))},
    'Logout': lambda: {"duration": random.randint(1, 7200)},  # 登录时长，单位秒
    'Purchase': lambda: {
        "money_value": round(random.uniform(1, 1000), 2),
        "money_type": f"{random.randint(1, 999):03d}",
        "reduce": random.randint(0, 1)
    },
    'LevelUp': lambda: {"new_level": random.randint(1, 100)}
}

# ---------------------- 数据生成函数 ----------------------
def generate_user_event_log(num_records):
    data = []
    used_event_times = set()  # 用于存储已经生成的时间戳，确保唯一性
    
    while len(data) < num_records:
        # 生成用户ID
        user_id = fake.uuid4()
        
        # 随机选择事件类型
        event_name = random.choice(list(EVENT_TYPES.keys()))
        
        # 生成事件时间戳（随机生成过去30天内的某个时间）
        event_time = int((datetime.now() - timedelta(days=random.randint(0, 30))).timestamp())
        
        # 确保生成的时间戳是唯一的
        if event_time in used_event_times:
            continue  # 如果时间戳已经存在，重新生成
        used_event_times.add(event_time)  # 将新生成的时间戳加入集合
        
        # 生成日期（从时间戳中提取）
        part_date = datetime.fromtimestamp(event_time).strftime("%Y/%m/%d")
        
        # 根据事件类型生成事件的其他相关信息
        event_info = EVENT_TYPES[event_name]()
        
        # 将生成的数据添加到列表中
        data.append({
            "user_id": user_id,
            "event_time": event_time,
            "event_name": event_name,
            "part_date": part_date,
            "event_info": event_info
        })
    
    return data

# ---------------------- 主函数：生成并保存数据 ----------------------
def main():
    # 生成数据
    user_event_log_data = generate_user_event_log(DATA_SCALE)
    
    # 保存为JSON文件
    with open(OUTPUT_FILE, "w") as f:
        json.dump(user_event_log_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 数据生成完成：{len(user_event_log_data)}条，保存至 {OUTPUT_FILE}")

if __name__ == "__main__":
    main()