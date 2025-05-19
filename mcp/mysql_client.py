from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
import asyncio

# Client会使用这里的配置来启动本地MCP Server
server_params = StdioServerParameters(
    command="python",
    args=["./mysql_server.py"],
    env=None
)

async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print('\n正在调用工具...')
            
            # 连接数据库
            connection_result = await session.call_tool("connect_to_database", {})
            print("Database connection result:", connection_result)
            
            if connection_result:
                # 插入数据
                data = {'user_id': '123', 'event_name': 'Login'}
                insert_result = await session.call_tool("insert_data", {"connection": connection_result, "table_name": "user_event_log", "data": data})
                print("Insert result:", insert_result)
            else:
                print("Failed to connect to the database.")

asyncio.run(main())