import pymysql
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# 数据库配置
DB_CONFIG = {
    'host': 'dechichichi.rwlb.rds.aliyuncs.com',
    'port': 3306,
    'user': 'lyan',
    'password': 'Ly05985481282',
    'database': 'game_agent',
    'charset': 'utf8mb4'
}

def fetch_data():
    conn = pymysql.connect(**DB_CONFIG)
    query = "SELECT * FROM sequential_output_charge"
    data = pd.read_sql(query, conn)
    conn.close()
    return data

def preprocess_data(data):
    # 数据预处理
    data['event_list'] = data['event_list'].apply(lambda x: [int(i) for i in x.split(',')])
    data['stats_item_list'] = data['stats_item_list'].apply(lambda x: [int(i) for i in x.split(',')])
    data['stats_event_list'] = data['stats_event_list'].apply(lambda x: [int(i) for i in x.split(',')])
    return data

def train_model(data):
    # 特征和目标变量
    X = data[['event_list', 'max_level', 'max_viplevel', 'num_event', 'stats_item_list', 'stats_event_list']]
    y = data['target']

    # 将列表特征转换为适合模型的格式
    X = pd.concat([data.drop(['event_list', 'stats_item_list', 'stats_event_list'], axis=1), 
                   pd.DataFrame(data['event_list'].tolist()), 
                   pd.DataFrame(data['stats_item_list'].tolist()), 
                   pd.DataFrame(data['stats_event_list'].tolist())], axis=1)

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 训练模型
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 评估模型
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    data = fetch_data()
    data = preprocess_data(data)
    train_model(data)