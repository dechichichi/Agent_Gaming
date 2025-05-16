import json
import random
from faker import Faker  # 需先安装：pip install faker

fake = Faker()

# ---------------------- 配置参数 ----------------------
DATA_SCALE = {
    "train": 100000,  # 训练数据量（10万条）
    "eval": 50000,    # 评估数据量（5万条）
    "infer": 30000    # 推理数据量（3万条）
}
OUTPUT_PATH = "./ai_data/"  # 输出文件夹路径


# ---------------------- 训练数据生成函数 ----------------------
def generate_train_data(num_records):
    data = []
    for uid in range(1, num_records + 1):
        # 生成行为序列（5-10个行为，101-120号行为，按时间升序）
        event_length = random.randint(5, 10)
        events = random.sample(range(101, 121), event_length)
        events.sort()
        event_list = json.dumps(events)
        
        # 生成标签（target：付费概率与vip等级正相关）
        vip_level = random.choices([1, 2, 3, 4, 5], weights=[40, 30, 20, 8, 2])[0]
        pay_prob = 0.1 + 0.05 * vip_level  # vip5付费概率35%
        target = 1 if random.random() < pay_prob else 0
        
        # 划分训练集/验证集（前70%为训练集）
        val_row = 1 if uid > num_records * 0.7 else 0
        
        # 生成其他特征（含年龄、性别、vip等级）
        age = random.randint(15, 60)
        gender = random.choices(["male", "female", "unknown"], weights=[45, 45, 10])[0]
        other_feature = {
            "age": age,
            "gender": gender,
            "vip_level": vip_level
        }
        
        data.append({
            "uid": f"user_{uid:06d}",
            "event_list": event_list,
            "target": target,
            "val_row": val_row,
            "other_feature": other_feature
        })
    return data


# ---------------------- 评估数据生成函数 ----------------------
def generate_eval_data(num_records):
    data = []
    for uid in range(1, num_records + 1):
        # 生成行为序列（3-8个行为，201-220号行为，按时间升序）
        event_length = random.randint(3, 8)
        events = random.sample(range(201, 221), event_length)
        events.sort()
        event_list = json.dumps(events)
        
        # 生成标签（target：流失/未流失均衡分布）
        target = random.randint(0, 1)
        
        # 生成其他特征（含年龄、周登录次数）
        age = random.randint(18, 55)
        login_freq = random.randint(1, 7)
        other_feature = {
            "age": age,
            "login_freq": login_freq
        }
        
        data.append({
            "uid": f"eval_user_{uid:05d}",
            "event_list": event_list,
            "target": target,
            "other_feature": other_feature
        })
    return data


# ---------------------- 推理数据生成函数 ----------------------
def generate_infer_data(num_records):
    data = []
    for uid in range(1, num_records + 1):
        # 生成行为序列（4-9个行为，混合101-120和201-220，1%概率插入异常行为999）
        event_length = random.randint(4, 9)
        events = random.sample(range(101, 121), event_length // 2) + random.sample(range(201, 221), event_length // 2)
        if random.random() < 0.01:  # 插入异常行为
            events.append(999)
        events.sort()
        event_list = json.dumps(events)
        
        # 生成其他特征（含设备类型，20%概率缺失特征）
        device_type = random.choice(["mobile", "pc", "tablet"])
        other_feature = {
            "device_type": device_type,
            "random_num": random.randint(0, 100)
        } if random.random() >= 0.2 else None  # 20%概率缺失
        
        data.append({
            "uid": f"infer_user_{uid:05d}",
            "event_list": event_list,
            "other_feature": other_feature  # 无target字段
        })
    return data


# ---------------------- 主函数：生成并保存数据 ----------------------
def main():
    import os
    os.makedirs(OUTPUT_PATH, exist_ok=True)  # 创建输出文件夹
    
    # 生成训练数据
    train_data = generate_train_data(DATA_SCALE["train"])
    with open(f"{OUTPUT_PATH}/train_data.json", "w") as f:
        json.dump(train_data, f, ensure_ascii=False, indent=2)
    print(f"✅ 训练数据生成完成：{len(train_data)}条，保存至 {OUTPUT_PATH}/train_data.json")
    
    # 生成评估数据
    eval_data = generate_eval_data(DATA_SCALE["eval"])
    with open(f"{OUTPUT_PATH}/eval_data.json", "w") as f:
        json.dump(eval_data, f, ensure_ascii=False, indent=2)
    print(f"✅ 评估数据生成完成：{len(eval_data)}条，保存至 {OUTPUT_PATH}/eval_data.json")
    
    # 生成推理数据
    infer_data = generate_infer_data(DATA_SCALE["infer"])
    with open(f"{OUTPUT_PATH}/infer_data.json", "w") as f:
        json.dump(infer_data, f, ensure_ascii=False, indent=2)
    print(f"✅ 推理数据生成完成：{len(infer_data)}条，保存至 {OUTPUT_PATH}/infer_data.json")


if __name__ == "__main__":
    main()