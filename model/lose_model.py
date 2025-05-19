import pymysql
from pymysql.cursors import DictCursor

# 数据库配置
DB_CONFIG = {
    'host': 'dechichichi.rwlb.rds.aliyuncs.com',
    'port': 3306,
    'user': 'lyan',
    'password': 'Ly05985481282',
    'database': 'game_agent',
    'charset': 'utf8mb4',
    'cursorclass': DictCursor,
    'connect_timeout': 30
}

def create_model(cursor, model_name, train_table):
    """
    创建模型
    :param cursor: 数据库游标
    :param model_name: 模型名称
    :param train_table: 训练数据表
    """
    create_model_query = f"""
    /*polar4ai*/ CREATE MODEL {model_name}
    WITH (model_class='bst', 
    x_cols='event_list,max_level,max_viplevel,num_event,stats_item_list,stats_event_list', 
    y_cols='target',
    model_parameter=(model_task_type='classification',
                window_size=100,
                success_id=2,
                sequence_length=3000,
                batch_size=128,
                learning_rate=0.002,
                max_epoch=5,
                val_flag=1,
                val_metric='f1score',
                auto_data_statics='on',
                auto_heads=0,
                num_heads=8,
                version=1,
                data_normalization=1,
                x_seq_cols='event_list',
                x_value_cols='max_level,max_viplevel,num_event',
                x_statics_cols='stats_item_list,stats_event_list',
                remove_seq_adjacent_duplicates = 'on'
    )) 
    AS (SELECT * FROM {train_table});
    """
    cursor.execute(create_model_query)
    print(f"模型 {model_name} 创建成功！")

def evaluate_model(cursor, model_name, evaluate_table):
    """
    评估模型
    :param cursor: 数据库游标
    :param model_name: 模型名称
    :param evaluate_table: 评估数据表
    """
    evaluate_query = f"""
    /*polar4ai*/SELECT user_id,target FROM EVALUATE (MODEL {model_name}, 
    SELECT * FROM {evaluate_table}) WITH 
    (x_cols = 'event_list,max_level,max_viplevel,num_event,stats_item_list,stats_event_list',y_cols='target',s_cols='user_id,target',metrics='Fscore');
    """
    cursor.execute(evaluate_query)
    evaluation_result = cursor.fetchall()
    print(f"模型 {model_name} 评估结果:", evaluation_result)

def main():
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # 流失预测模型
    lose_model_name = "GameName_7to14_train_val_lose_20250401_20250430"
    lose_train_table = "sequential_output_lose"

    create_model(cursor, lose_model_name, lose_train_table)
    evaluate_model(cursor, lose_model_name, lose_train_table)

    conn.close()

if __name__ == "__main__":
    main()