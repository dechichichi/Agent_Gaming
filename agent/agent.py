import pymysql
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import yaml

class GamingAgent:
    def __init__(self):
        # 加载配置文件
        with open('config/config.yml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        self.DB_CONFIG = config['DB_CONFIG']
        self.model = self.train_model()

    def fetch_data(self):
        conn = pymysql.connect(**self.DB_CONFIG)
        query = "SELECT * FROM sequential_output_charge"
        data = pd.read_sql(query, conn)
        conn.close()
        return data

    def preprocess_data(self, data):
        # 数据预处理
        data['event_list'] = data['event_list'].apply(lambda x: [int(i) for i in x.split(',')])
        data['stats_item_list'] = data['stats_item_list'].apply(lambda x: [int(i) for i in x.split(',')])
        data['stats_event_list'] = data['stats_event_list'].apply(lambda x: [int(i) for i in x.split(',')])
        return data

    def train_model(self):
        data = self.fetch_data()
        data = self.preprocess_data(data)
        # 特征和目标变量
        X = data[['event_list', 'max_level', 'max_viplevel', 'num_event', 'stats_item_list', 'stats_event_list']]
        y = data['target']

        # 将列表特征转换为适合模型的格式
        X = pd.concat([data.drop(['event_list', 'stats_item_list', 'stats_event_list'], axis=1), 
                       pd.DataFrame(data['event_list'].tolist()), 
                       pd.DataFrame(data['stats_item_list'].tolist()), 
                       pd.DataFrame(data['stats_event_list'].tolist())], axis=1)

        # 训练模型
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
        return model

    def predict(self, user_data):
        user_data = self.preprocess_data(pd.DataFrame([user_data]))
        X = user_data[['event_list', 'max_level', 'max_viplevel', 'num_event', 'stats_item_list', 'stats_event_list']]
        X = pd.concat([user_data.drop(['event_list', 'stats_item_list', 'stats_event_list'], axis=1), 
                       pd.DataFrame(user_data['event_list'].tolist()), 
                       pd.DataFrame(user_data['stats_item_list'].tolist()), 
                       pd.DataFrame(user_data['stats_event_list'].tolist())], axis=1)
        prediction = self.model.predict(X)
        return prediction[0]


if __name__ == "__main__":
    agent = GamingAgent()
    user_data = {
        'event_list': '1,2,3',
        'max_level': 10,
        'max_viplevel': 2,
        'num_event': 5,
        'stats_item_list': '101,102',
        'stats_event_list': 'Login,Logout'
    }
    prediction = agent.predict(user_data)
    print("Prediction:", prediction)