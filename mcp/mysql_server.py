import mysql.connector
from mysql.connector import Error
import mcp

@mcp.tool()
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='your_database_name',  # 替换为实际的数据库名称
            user='your_username',           # 替换为实际的用户名
            password='your_password'        # 替换为实际的密码
        )
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