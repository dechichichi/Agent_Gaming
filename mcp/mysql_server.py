import mysql.connector
from mysql.connector import Error
import mcp
import yaml

# 加载配置文件
with open('config/config.yml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
DB_CONFIG = config['DB_CONFIG']

@mcp.tool()
def connect_to_database():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("Successfully connected to the database.")
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

@mcp.tool()
def insert_data(connection, table_name, data):
    try:
        cursor = connection.cursor()
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        cursor.execute(query, tuple(data.values()))
        connection.commit()
        print("Data inserted successfully.")
        return True
    except Error as e:
        print(f"Error while inserting data: {e}")
        return False