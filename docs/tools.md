# 工具类文档

## 概述

工具类（`Tools`）是一个用于管理各种工具的统一接口，提供了用户数据分析、风险评估、留存分析和推荐等功能。

## 功能特性

- 用户数据获取和处理
- 用户指标计算
- 风险评估
- 留存分析
- 用户推荐

## 安装依赖

```bash
pip install -r requirements.txt
```

## 环境变量配置

1. 复制环境变量示例文件：
```bash
cp config/env.example .env
```

2. 编辑 `.env` 文件，设置必要的环境变量：
```env
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database

# 其他配置...
```

3. 确保 `.env` 文件不会被提交到版本控制系统（已在 `.gitignore` 中配置）

## 配置说明

工具类使用配置文件（`config/config.yml`）进行配置，主要包括：

- 数据库配置
- 模型配置
- Agent配置
- 日志配置

## 使用示例

```python
from utils.tools import Tools

# 初始化工具类
tools = Tools()

# 获取用户指标
metrics = tools.get_user_metrics(user_id)

# 获取风险评估
risk_assessment = tools.get_risk_assessment(user_id)

# 获取留存分析
retention_analysis = tools.get_retention_analysis(user_id)

# 获取用户推荐
recommendations = tools.get_user_recommendations(user_id)
```

## API文档

### Tools类

#### `__init__()`

初始化工具类，加载配置信息。

#### `get_user_data(user_id: str, start_date: str, end_date: str) -> pd.DataFrame`

获取用户数据。

参数：
- `user_id`: 用户ID
- `start_date`: 开始日期
- `end_date`: 结束日期

返回：
- `pd.DataFrame`: 用户数据

#### `get_user_metrics(user_id: str, days: int = 7) -> Dict[str, Any]`

获取用户指标。

参数：
- `user_id`: 用户ID
- `days`: 天数（默认7天）

返回：
- `Dict[str, Any]`: 用户指标

#### `get_risk_assessment(user_id: str) -> Dict[str, Any]`

获取用户风险评估。

参数：
- `user_id`: 用户ID

返回：
- `Dict[str, Any]`: 风险评估结果

#### `get_retention_analysis(user_id: str) -> Dict[str, Any]`

获取用户留存分析。

参数：
- `user_id`: 用户ID

返回：
- `Dict[str, Any]`: 留存分析结果

#### `get_user_recommendations(user_id: str) -> List[Dict[str, Any]]`

获取用户推荐。

参数：
- `user_id`: 用户ID

返回：
- `List[Dict[str, Any]]`: 推荐列表

## 错误处理

工具类使用统一的错误处理机制，所有方法都会捕获异常并记录日志。如果发生错误，会抛出异常并包含详细的错误信息。

## 日志说明

工具类使用统一的日志记录机制，日志文件保存在 `logs` 目录下，按日期命名。日志级别可以通过配置文件进行调整。

## 测试

运行测试：

```bash
python -m unittest tests/test_tools.py
```

## 示例代码

完整的示例代码请参考 `examples/tools_example.py`。

## 注意事项

1. 使用前请确保配置文件正确设置
2. 数据库连接信息请妥善保管
3. 建议在生产环境中使用环境变量管理敏感信息
4. 定期检查日志文件，及时处理异常情况 