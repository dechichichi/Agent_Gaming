# Agent Gaming

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE-APACHE)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE-GPL)
[![License: BSD 3-Clause](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](LICENSE-BSD)

一个基于AI的游戏用户行为分析和预测系统，用于游戏运营和用户留存优化。

## 项目概述

Agent Gaming 是一个综合性的游戏用户行为分析系统，集成了用户行为分析、流失预测、付费预测等功能。系统采用模块化设计，包含智能Agent、预测模型、数据分析工具等多个组件。

### 核心功能

- 用户行为分析
- 流失风险预测
- 付费行为预测
- 智能干预推荐
- 数据可视化展示

## 系统架构

```
Agent Gaming
├── agent/           # 智能Agent模块
│   ├── agent.py     # Agent核心实现
│   ├── tools.py     # Agent工具集
│   └── prompt.py    # 提示词模板
├── model/           # 预测模型模块
│   ├── lose_model.py    # 流失预测模型
│   └── charge_model.py  # 付费预测模型
├── utils/           # 工具类模块
│   ├── db.py        # 数据库工具
│   ├── data_processor.py # 数据处理工具
│   └── metrics.py   # 评估指标工具
├── api/             # API接口模块
├── config/          # 配置文件
├── docs/            # 文档
├── tests/           # 测试用例
└── examples/        # 示例代码
```

## 技术栈

### 后端技术
- **Python 3.8+**: 主要开发语言
- **MySQL 5.7+**: 主数据库，用于存储用户行为数据和模型训练数据
- **Redis 6.0+**: 缓存层，用于提高数据访问性能
- **PolarDB for AI**: 用于模型训练和推理的AI数据库
- **Docker**: 容器化部署

### AI/ML技术
- **BST (Behavior Sequence Transformer)**: 核心预测模型
  - 序列长度: 100-3000
  - 批量大小: 128
  - 学习率: 0.002
  - 多注意力头机制
- **Transformer架构**: 用于行为序列分析
- **分类算法**: 用于流失预测
- **回归算法**: 用于付费预测

### 数据处理
- **数据清洗工具**: 用于处理原始用户行为数据
- **特征工程**: 
  - 行为序列特征
  - 统计特征
  - 数值特征
- **数据归一化**: 用于模型训练前的数据预处理

### 部署与运维
- **Docker Compose**: 服务编排
- **环境变量配置**: 用于不同环境的配置管理
- **API服务**: RESTful接口
- **异步任务处理**: 用于模型训练和预测

### 监控与评估
- **模型评估指标**:
  - F1 Score
  - Precision
  - Recall
  - AUC
- **业务指标监控**
- **模型效果评估工具**

## 快速开始

### 环境要求

- Python 3.8+
- MySQL 5.7+
- Redis 6.0+

### 安装步骤

1. 克隆项目
```bash
git clone https://github.com/yourusername/Agent_Gaming.git
cd Agent_Gaming
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
```bash
cp config/env.example .env
# 编辑 .env 文件，设置必要的环境变量
```

4. 初始化数据库
```bash
python scripts/init_db.py
```

### 运行服务

1. 启动API服务
```bash
python api/api.py
```

2. 启动Agent服务
```bash
python agent/main.py
```

## 功能模块

### 智能Agent模块

- 用户行为分析
- 风险预警
- 干预策略生成
- 效果评估

### 预测模型模块

- 流失预测模型
  - 基于用户行为序列
  - 多维度特征分析
  - 实时预测能力

- 付费预测模型
  - 用户价值评估
  - 付费意愿预测
  - 个性化推荐

### 工具类模块

- 数据库工具
  - 连接池管理
  - 查询优化
  - 事务处理

- 数据处理工具
  - 数据清洗
  - 特征工程
  - 序列处理

- 评估指标工具
  - 模型评估
  - 业务指标
  - 效果分析

## 配置说明

### 环境变量

主要环境变量配置：
```env
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=game_agent

# 模型配置
MODEL_DIR=models
MODEL_VERSION=1.0.0

# Agent配置
AGENT_MODEL=gpt-4-turbo
AGENT_TEMPERATURE=0
AGENT_MAX_TOKENS=2000
```

### 配置文件

- `config/config.yml`: 主配置文件
- `config/model_config.yml`: 模型配置文件
- `config/agent_config.yml`: Agent配置文件

## 开发指南

### 代码规范

- 遵循PEP 8规范
- 使用类型注解
- 编写单元测试
- 保持文档更新

### 测试

运行测试：
```bash
python -m pytest tests/
```

### 文档

- API文档：`docs/api.md`
- 开发文档：`docs/development.md`
- 部署文档：`docs/deployment.md`

## 部署

### Docker部署

1. 构建镜像
```bash
docker build -t agent-gaming .
```

2. 运行容器
```bash
docker-compose up -d
```

### 服务器部署

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 配置服务
```bash
cp config/env.example .env
# 编辑配置文件
```

3. 启动服务
```bash
python api/api.py
python agent/main.py
```

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

本项目采用多重许可证：

- [Apache License 2.0](LICENSE-APACHE)
- [GNU General Public License v3.0](LICENSE-GPL)
- [BSD 3-Clause License](LICENSE-BSD)

你可以根据你的需求选择使用其中任何一个许可证。每个许可证的具体条款和条件请查看相应的许可证文件。


第一、为什么会出现 MCP？
如果你开发了一个 AI 应用，无论是 ChatBot 还是复杂的 Agent，都不会仅限于简单的 LLM 对话。很多时候，你需要与外部世界连接，以访问数据源或使用工具。例如：

操控浏览器实现自动化；
访问本地文件；
访问数据库结构，以便更好地让 AI 参与编程；
调用 CRM 的 API 以驱动智能客服流程。
在这种情况下，你需要连接不同的对象，使用不同的接口协议。你可能需要熟悉 SQL、HTTP 调用、Playwright 等接口，甚至还需要使用搜索引擎、访问云存储、调用第三方开放API等。这些都涉及大量的"粘合"工作。

![alt text](image-1.png)
![alt text](image-2.png)


第二、MCP 有哪些好处？
这种设计范式在软件系统中其实很常见，比如：一些大模型 API 网关会将不同厂家的大模型协议转化为统一的 OpenAI 兼容协议，方便应用接入。它的具体意义主要体现在以下几点：

简化 LLM 应用：无需适配各种私有协议，只需学会连接 MCP Server 即可。
快速扩展 LLM 应用：随时可以"插拔"新的 MCP Server，需要更多功能时，简单添加即可。
快速适应变化：如果外部资源的接口发生变化，只需在对应的 MCP Server 上进行修改，所有连接的 LLM 应用都能无缝适应。
构建新的 AI 能力共享生态：通过共享 MCP Server，新的 LLM 应用能够快速获得各种工具，形成一种新的合作体系，从而提升整体的效用。
![alt text](image-3.png)

![alt text](image-4.png)

# 数据构建

用户原始日志数据需要加工成这样的数据。

需要构造三类数据：

- 训练数据：训练数据中根据数据用途分成两个类型，一个是模型直接用来训练的数据（Train），另一个是在训练过程中验证模型好坏，选择最佳参数的验证数据（Validation）。通常会按时间，前半段时间的数据用来训练，后半段时间的数据用来验证。最终数据中需要带上用户标签。
- 评估数据：和训练数据构造方法类似，但不需要区分用来训练还是验证。最终数据中需要带上用户标签（是否付费/是否流失）。
- 推理数据：和训练数据构造方法类似，但因为无法知道用户的表现，所以最终数据中的用户标签未知。

| **参数名称**  | **必选/可选** | **列类型**         | **列描述**                                                   | **示例**                   |
| ------------- | ------------- | ------------------ | ------------------------------------------------------------ | -------------------------- |
| uid           | 必选          | VARCHAR(255)       | 用于标记每条待预测数据的ID。如用户ID、商品ID等。             | 123213                     |
| event_list    | 必选          | TEXT               | 输入表中用于训练的行为序列，序列中数据用`,`分割，序列内数据用INT型标记每一种行为ID，序列内数据按照对应时间戳排序，时间戳越大，数据越靠近序列末端。 | 例："[183, 238, 153, 152]" |
| target        | 可选          | INT、FLOAT、DOUBLE | 算法模型创建时必选，用于计算当前模型误差的样本标签。         | 0                          |
| val_row       | 可选          | INT                | 为了避免模型过拟合，支持指定验证集。`val_row`是用于标记训练数据和验证数据的，训练数据的值为`0`，验证数据的值标记为`1`。 | 0                          |
| other_feature | 可选          | LONGTEXT           | 模型的其他特征，在使用时需要在训练参数`x_value_cols`和`x_statics_cols`配置中包含所需特征列名。`other_feature`为`LONGTEXT`类型时，文本内支持格式：JSON、列表，或者以`,`分割的字符串。可以填写多个other_feature参数，例如：`other_feature1`、`other_feature2`等。 | other_feature1             |

### **模型评估数据表格式**

| **列名称**    | **必选/可选** | **列类型**                   | **列描述**                                                   | **示例**               |
| ------------- | ------------- | ---------------------------- | ------------------------------------------------------------ | ---------------------- |
| uid           | 必选          | VARCHAR(255)                 | 标记每条待预测数据的ID（用户ID、商品ID等）。                 | 123213                 |
| event_list    | 必选          | LONGTEXT                     | 输入表中用于创建模型的行为序列，序列中数据用逗号`,`分隔，序列内数据用INT类型标记每一种行为ID，序列内数据按照其对应的时间戳大小升序排序。 | "[183, 238, 153, 152]" |
| target        | 必选          | INT、FLOAT、DOUBLE           | 计算当前算法模型误差的样本标签。                             | 0                      |
| other_feature | 可选          | INT、FLOAT、DOUBLE、LONGTEXT | 模型的其他特征，与创建模型数据表保持一致。在使用时需要在创建模型参数`x_value_cols`和`x_statics_cols`的配置中包含所需特征列名。 | 2                      |

### **模型推理数据表格式**

| **列名称**    | **必选/可选** | **列类型**                   | **列描述**                                                   | **示例**               |
| ------------- | ------------- | ---------------------------- | ------------------------------------------------------------ | ---------------------- |
| uid           | 必选          | VARCHAR(255)                 | 标记每条待预测数据的ID（用户ID、商品ID等）。                 | 123213                 |
| event_list    | 必选          | LONGTEXT                     | 输入表中用于创建模型的行为序列，序列中数据用逗号`,`分隔，序列内数据用`INT`类型标记每一种行为ID，序列内数据按照其对应的时间戳大小升序排序。 | "[183, 238, 153, 152]" |
| other_feature | 可选          | INT、FLOAT、DOUBLE、LONGTEXT | 模型的其他特征，与创建模型数据表保持一致。在使用时需要在创建模型参数`x_value_cols`和`x_statics_cols`的配置中包含所需特征列名。 | 2                      |

## **数据加工参考样例**

用户行为分析模型会利用用户基础日志，通常用户基础日志已经存在数据仓库等介质中，需要将日志数据转化成模型需要的训练数据。数据加工的方法有很多，用户可以选择符合自身需要的方法。下面来通过和一个公司合作共建的数据加工，来详细说明如何从用户基础日志加工成BST需要的数据格式。

在PolarDB中有数据库表`user_event_log`。该表是用户基础日志表，存储着用户一段时间的行为日志，要求OSS中的存储形式和这个表保持一致。其中OSS地址需要配置为正确地址。

 

```sql
-- 创建 user_event_log，OSS 地址需要配置为正确地址，同一个数据库执行一次即可
CREATE TABLE `user_event_log` (
  `user_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '用户唯一ID',
  `event_time` bigint(20) NOT NULL COMMENT '用户事件发生的十位时间戳',
  `event_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '用户事件的名称，比如反映用户付费的行为（是否付费、付费金额等）',
  `part_date` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '日期时间，格式是YYYY-MM-dd',
  `event_info` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin COMMENT '用户事件的其他相关信息，JSON类型（付费行为的子类型、付费金额等）',
  PRIMARY KEY (`event_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='columnar=1' CONNECTION='OSS://xxxx:dxxx@oss-cn-shanghai-internal.aliyuncs.com/xx/xxxx/'
```

### **user_event_log数据示例**

| **user_id** | **event_time** | **event_name** | **part_date** | **event_info**                                  |
| ----------- | -------------- | -------------- | ------------- | ----------------------------------------------- |
| example001  | 1724513952     | Money          | 2024/7/30     | {"money_value":50,"money_type":001,"reduce":0}  |
| example002  | 1724513951     | Money          | 2024/7/30     | {"money_value":300,"money_type":002,"reduce":0} |
| example003  | 1724513956     | Money          | 2024/7/30     | {"money_value":100,"money_type":058,"reduce":0} |
| example001  | 1724513951     | Money          | 2024/7/30     | {"money_value":30,"money_type":005,"reduce":1}  |
| example001  | 1724513959     | Money          | 2024/7/30     | {"money_value":150,"money_type":005,"reduce":0} |
| example004  | 1724513962     | Money          | 2024/7/30     | {"money_value":950,"money_type":028,"reduce":1} |
| example002  | 1724513967     | Money          | 2024/7/30     | {"money_value":300,"money_type":002,"reduce":0} |
| example002  | 1724513967     | Money          | 2024/7/30     | {"money_value":1,"money_type":011,"reduce":0}   |
| example003  | 1724513962     | Money          | 2024/7/30     | {"money_value":3,"money_type":033,"reduce":0}   |
| example004  | 1724513970     | Money          | 2024/7/30     | {"money_value":15,"money_type":005,"reduce":1}  |

**说明**

同一个`user_id`可以出现多条不同的记录。

构建下面六个函数

| **场景**                                                     | **函数**                                                     | **函数说明**                                                 | **输出表**                                                   |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 用户付费场景                                                 | gen_user_label_charge(seq_time_start,seq_time_end,label_time_start,label_time_end) | 用于生成用户是否付费的标记数据。对于`seq_time_start`这一日期产生的新用户，判断其在`label_time_start`至`label_time_end`时间段是否有付费事件产生，发生付费为1，否则为0。其中：seq_time_start：表示M测N中的M的起始日期。seq_time_end：表示M测N中的M的结束日期。label_time_start：表示M测N中的N的起始日期。label_time_end：表示M测N中的N的结束日期。 | user_label_charge：会生成两类数据，一类是user_id,另一类是标记数据的标签target。 |
| gen_sequential_output_charge(seq_time_start,seq_time_end,label_time_start,label_time_end) | 用于生成付费场景下的用户行为序列，并按照时间戳先后顺序生成时间序列。其中：seq_time_start：表示M测N中的M的起始日期。seq_time_end：表示M测N中的M的结束日期。label_time_start：表示M测N中的N的起始日期。label_time_end：表示M测N中的N的结束日期。 | sequential_output_charge：会生成三类数据：用户ID，数据特征数据，是否付费`target`。 |                                                              |
| gen_user_label_money(seq_time_start,seq_time_end,label_time_start,label_time_end) | 用于生成用户付费金额的标记数据。对于`seq_time_start`这一日期产生的新用户，统计其在`label_time_start`至`label_time_end`时间段内的具体付费金额，记为`target`。其中：seq_time_start：表示M测N中的M的起始日期。seq_time_end：表示M测N中的M的结束日期。label_time_start：表示M测N中的N的起始日期。label_time_end：表示M测N中的N的结束日期。 | user_label_money：会生成两类数据，一类是`user_id`，另一类是标记数据的标签`target`。 |                                                              |
| gen_sequential_output_money(seq_time_start,seq_time_end,label_time_start,label_time_end) | 用于生成付费场景下的用户行为序列，并按照时间戳先后顺序生成时间序列。其中：seq_time_start：表示M测N中的M的起始日期。seq_time_end：表示M测N中的M的结束日期。label_time_start：表示M测N中的N的起始日期。label_time_end：表示M测N中的N的结束日期。 | sequential_output_charge：会生成三类数据：用户ID，数据特征数据，付费金额`target`。 |                                                              |
| 用户流失场景                                                 | gen_user_label_lose(seq_time_start,seq_time_end,label_time_start,label_time_end) | 用于生成用户是否流失的标记数据。判断其在对于`seq_time_start`至`seq_time_end`这一日期中的所有活跃用户，判断其在`label_time_start`至`label_time_end`时间段是否有行为事件产生，如果没有任何活跃事件则标记为1，否则为0。其中：seq_time_start：表示M测N中的M的起始日期。seq_time_end：表示M测N中的M的结束日期。label_time_start：表示M测N中的N的起始日期。label_time_end：表示M测N中的N的结束日期。 | user_label_lose：会生成两类数据，一类是`user_id`，另一类是标记数据的标签`target`。 |
| gen_sequential_output_lose(seq_time_start,seq_time_end,label_time_start,label_time_end) | 用于生成流失场景下的用户行为序列，并按照时间戳先后顺序生成时间序列。其中：seq_time_start：表示M测N中的M的起始日期seq_time_end：表示M测N中的M的结束日期label_time_start：表示M测N中的N的起始日期label_time_end：表示M测N中的N的结束日期 | sequential_output_charge：会生成三类数据：用户ID，数据特征数据，是否流失`target`。 |                                                              |

**说明**

`sequential_output_charge`就是一天的用户序列的训练数据。可以通过修改时间参数，得到新的一天的训练数据。

### **付费预测（7测7）**

训练数据构造分两步，首先是调用`gen_user_label_charge`构造用户标签数据，即对用户是否付费进行标记；其次调用`gen_sequential_output_charge`将用户的行为序列和标记数据关联。执行这两个命令后可以生成表`sequential_output_charge`。

因为一天的数据作为训练数据往往数据量不够，而且数据可能存在波动，需要多取一些天作为训练数据。可以通过重复调用这两个procedure，通过将日期往后推移来生成更多的数据。比如先生成20240720的数据，再继续生成20240721，20240722……。

最终的训练数据表的样例如下：

| **train_start_date** | **train_end_date** | **test_start_date** | **test_end_date** | **user_id** | **is_prepay** | **target** | **part_date** | **event_list**          | **stats_item_list** | **stats_event_list** | **num_event** | **max_level** | **max_viplevel** | **val_row** |
| -------------------- | ------------------ | ------------------- | ----------------- | ----------- | ------------- | ---------- | ------------- | ----------------------- | ------------------- | -------------------- | ------------- | ------------- | ---------------- | ----------- |
| 2024/7/20            | 2024/7/26          | 2024/7/27           | 2024/8/2          | example001  | 1             | 0          | 2024/7/20     | [1,12,44,334]           | 0,12,22,21,231,1    | 1,1,3,21,12          | 4             | 43            | 600              | 0           |
| 2024/7/21            | 2024/7/27          | 2024/7/28           | 2024/8/3          | example002  | 0             | 1          | 2024/7/21     | [1,12,44,334,234,22]    | 2,34,12,12,2,90     | 23,0,2,1,1           | 6             | 3             | 600              | 0           |
| 2024/7/20            | 2024/7/26          | 2024/7/27           | 2024/8/2          | example007  | 0             | 0          | 2024/7/20     | [1,12,2,334]            | 0,12,2,21,231,1     | 0,1,3,21,12          | 4             | 2             | 1200             | 1           |
| 2024/7/21            | 2024/7/27          | 2024/7/28           | 2024/8/3          | example008  | 1             | 1          | 2024/7/21     | [1,12,44,1,234,22,2,32] | 2,34,2,12,2,90      | 9,0,2,1,1            | 8             | 19            | 1200             | 1           |

**说明**

- train_start_date：表示M测N中的M的起始日期。
- train_end_date：表示M测N中的M的结束日期。
- test_start_date：表示M测N中的N的起始日期。
- test_end_date：表示M测N中的N的结束日期。
- user_id：用户ID。
- is_prepay：表示是否在M天内已经付费，1表示已付费，0表示未付费。
- target：表示是否在N天内已经付费，1表示已付费，0表示未付费。
- part_date：表示按天加工的数据表的日期，通常和`train_start_date`一致。
- event_list：游戏行为构成的时间序列，按发生事件排序。
- stats_item_list：游戏道具出现频数列表，按游戏道具的ID排序。
- stats_event_list：游戏行为频数列表，按游戏行为ID排序。
- num_event：事件总数量。
- max_level：最高等级。
- max_viplevel：最高VIP等级。

对待推理的数据，因为我们需要预测未来用户是否付费，所以我们无法知道用户标签，推理数据的生成只需要构造用户标签数据。

最终的推理数据表的样例如下：

| **train_start_date** | **train_end_date** | **test_start_date** | **test_end_date** | **user_id** | **is_prepay** | **target** | **part_date** | **event_list**          | **stats_item_list** | **stats_event_list** | **num_event** | **max_level** | **max_viplevel** |
| -------------------- | ------------------ | ------------------- | ----------------- | ----------- | ------------- | ---------- | ------------- | ----------------------- | ------------------- | -------------------- | ------------- | ------------- | ---------------- |
| 2024/7/20            | 2024/7/26          | 2024/7/27           | 2024/8/2          | example001  | 1             | 0          | 2024/7/20     | [1,12,44,334]           | 0,12,22,21,231,1    | 1,1,3,21,12          | 4             | 43            | 600              |
| 2024/7/21            | 2024/7/27          | 2024/7/28           | 2024/8/3          | example002  | 0             | 0          | 2024/7/21     | [1,12,44,334,234,22]    | 2,34,12,12,2,90     | 23,0,2,1,1           | 6             | 3             | 600              |
| 2024/7/20            | 2024/7/26          | 2024/7/27           | 2024/8/2          | example007  | 0             | 0          | 2024/7/20     | [1,12,2,334]            | 0,12,2,21,231,1     | 0,1,3,21,12          | 4             | 2             | 1200             |
| 2024/7/21            | 2024/7/27          | 2024/7/28           | 2024/8/3          | example008  | 1             | 0          | 2024/7/21     | [1,12,44,1,234,22,2,32] | 2,34,2,12,2,90      | 9,0,2,1,1            | 8             | 19            | 1200             |

**说明**

由于`target`的区间不存在（未知），默认全部置为0。

### **流失预测（7测14）**

和付费预测类似，训练数据构造分两步，首先是利用`gen_user_label_lose`构造用户标签数据，即对用户是否流失进行标记。其次再用`gen_sequential_output_lose`将用户的行为序列和标记数据关联。与付费预测不同的是，是否流失是看未来一段时间内是否有用户行为记录，理论上来说，流失的用户的用户行为是空的。因此，需要用之前一段时间的用户行为记录以UID为Key，去`LEFT JOIN`未来一段时间的用户行为数据，空的数据即为用户已经流失。因为一天的数据作为训练数据可能数据量不够，而且数据可能存在波动。可以通过重复调用这两个方法，生成更多的数据。

## **模型开发及上线**

分类模型

回归模型

**说明**

- 分类算法用于将输入数据分配到离散的类别标签中。目标变量在分类问题中是有限的类别或标签。
- 通常用于识别或区分不同类别的任务，例如垃圾邮件检测（三个类别：垃圾邮件、非垃圾邮件）、图像分类（多个类别：狗、猫、鸟等）等。

1. 模型创建

   1. 常见分类模型包括流失预测7测7，14测14；付费预测7测7，14测7等，由于与行为特征相关，流失预测往往比付费预测效果更优。我们会以流失场景讲解如何创建模型：

      训练表：GameName_train_val_lose_7_to_14_2024_07_20_2024_07_26，训练表示例：

      | **train_start_date** | **train_end_date** | **test_start_date** | **test_end_date** | **user_id** | **is_prepay** | **target** | **part_date** | **event_list**       | **stats_item_list** | **stats_event_list** | **num_event** | **max_level** | **max_viplevel** | **val_row** |
      | -------------------- | ------------------ | ------------------- | ----------------- | ----------- | ------------- | ---------- | ------------- | -------------------- | ------------------- | -------------------- | ------------- | ------------- | ---------------- | ----------- |
      | 2024/7/20            | 2024/7/26          | 2024/7/27           | 2024/8/9          | example001  | 1             | 0          | 2024/7/20     | [1,12,2,1]           | 0,1,1               | 1,2,32               | 4             | 43            | 600              | 0           |
      | 2024/7/21            | 2024/7/27          | 2024/7/28           | 2024/8/10         | example002  | 1             | 0          | 2024/7/21     | [1,12,2,134,23]      | 3,1,5               | 8,90,3               | 5             | 3             | 600              | 0           |
      | 2024/7/26            | 2024/8/1           | 2024/8/2            | 2024/8/15         | example007  | 1             | 0          | 2024/7/26     | [1,12,2,134,23,2,12] | 1,2,3               | 3,4,5                | 7             | 2             | 1200             | 1           |

      **说明**

      其中，训练数据表中，所需分区时间段的数据被合并至同一张表中。关键列说明如下：

      - event_list：游戏行为构成的时间序列，按发生事件排序。
      - stats_item_list：游戏道具出现频数列表，按游戏道具的ID排序。
      - stats_event_list：游戏行为频数列表，按游戏行为ID排序。
      - num_event：事件总数量。
      - max_level：最高等级。
      - max_viplevel：最高VIP等级。
      - val_row：区别训练集和验证集的标记：0表示训练集、1表示验证集。
      - target：是否流失，1表示流失，0表示未流失。
      - 其他列并不是必需的，可以忽略。

   2. 训练SQL：

       

      ```sql
      -- 使用前确保原先的同名模型已被删除
      /*polar4ai*/ CREATE MODEL GameName_7to14_train_val_lose_20240720_20240726
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
      AS (SELECT * FROM GameName_train_val_lose_7_to_14_2024_07_20_2024_07_26);
      ```

      **说明**

      - success_id：对应代表付费的行为id，流失可以不填。
      - 生成模型名：GameName_7to14_train_val_lose_20240720_20240726。

2. 模型微调

   深度学习模型涉及的参数很多，原生的调优的过程比较复杂，涉及到的参数比较多。目前，我们已经尽量将模型调优封装到以下参数中：

   - window_size：此参数用来对行为ID进行嵌入编码，因此不能小于行为ID最大值加1，同时不需要设置过大，保证embedding过程正确即可。
   - sequence_length：用于表示行为序列在算法模型中参与运算的长度，此参数越大，代表包含信息量越大，然而在数据集数量偏少时，例如小于10万条数据，`sequence_length`参数增加使得模型参数无法充分得到训练。`sequence_length`过小会导致信息不充分，因此，适宜的`sequence_length`应当在100至3000之间，根据数据量自行调节。
   - batch_size：此参数指的是在一次迭代中用于训练模型的样本数量。在显存/内存允许的范围内不应当设置过小（比如2/4/8），可适当增加`batch_size`提高模型迭代速度，参数设置往往是2的指数，比如16/32/64/128。`batch_size`过大时，会有爆内存和GPU显存的风险。
   - learning_rate：控制着优化算法在迭代过程中更新模型权重的步长大小。具体来说，学习率决定了每次参数更新时应当沿着损失函数梯度方向移动的量。过小的学习率会导致收敛速度慢，模型可能需要很多次迭代才能达到较好的结果，同时容易陷入局部最优，而无法探索到全局更优解。过大的学习率表现不稳定，损失函数可能在震荡，导致无法收敛。模型可能会在损失函数的高处爆炸，导致失去学习效果。可以在0.1-0.0001之间逐渐调节，观察验证效果，取最优。
   - auto_data_statics：指BST模型内置的数据统计过程，并将统计后的数据加入到特征中来，比如每种行为出现的次数。
   - auto_heads以及num_heads：指是否自动进行多注意力头数量设置。如果设置为1时，会根据`window_size`和`sequence_length`进行自动取值，有一定概率出现显存不足的风险。设置为0时，可自行设置多注意力头数量（`num_heads`）。多注意力头是Transformer模型中的一个重要组成部分。它通过并行地利用多个注意力头来捕捉输入数据中不同的子空间信息，从而使得模型能够更好地学习和表示输入序列的复杂特征。增加注意力头数量，可以学习到更多的关系和特征，但有可能导致过拟合。减少注意力头数量，可能会导致模型简单化，无法捕捉到输入数据中的某些重要信息。通常需要通过实验来找到最佳的注意力头数量。可以从一个较小的值（如2或4）开始，逐渐增加，观察在验证集上的表现。
   - data_normalization：用于指定`x_value_cols`和`x_statics_cols`的指定列数据是否进行归一化操作。此归一化由BST自动完成，因此需要数据为整数或者浮点型，但会带来一定误差，因此建议用户在使用BST前自行手动对数据进行归一化。
   - remove_seq_adjacent_duplicates：用于对`x_seq_cols`的数据进行去重操作，比如`'[1,1,2,2,3,3,1,2,3]'`，去重后为`'[1,2,3,1,2,3]'`。用于去除冗余数据，提高向量计算准确性。
   - x_seq_cols：一般是统计类的序列特征，例如每种道具出现的次数等。
   - x_value_cols：一般是离散类的数值特征，例如最大等级、行为次数等。

3. 模型评估

   PolarDB for AI支持直接调用Evaluate算子进行模型效果评估，生成预测数据集后可跳过Predict环节，直接将预测数据集作为输入进行评估（该算子将输出预测结果的OSS下载链接和评估指标）。

   1. 待评估的数据表示例如下：

      | **train_start_date** | **train_end_date** | **test_start_date** | **test_end_date** | **user_id** | **is_prepay** | **target** | **part_date** | **event_list**       | **stats_item_list** | **stats_event_list** | **num_event** | **max_level** | **max_viplevel** |
      | -------------------- | ------------------ | ------------------- | ----------------- | ----------- | ------------- | ---------- | ------------- | -------------------- | ------------------- | -------------------- | ------------- | ------------- | ---------------- |
      | 2024/7/20            | 2024/7/26          | 2024/7/27           | 2024/8/9          | example001  | 1             | 0          | 2024/7/20     | [1,12,2,1]           | 0,1,1               | 1,2,32               | 4             | 43            | 600              |
      | 2024/7/21            | 2024/7/27          | 2024/7/28           | 2024/8/10         | example002  | 1             | 0          | 2024/7/21     | [1,12,2,134,23]      | 3,1,5               | 8,90,3               | 5             | 3             | 600              |
      | 2024/7/26            | 2024/8/1           | 2024/8/2            | 2024/8/15         | example007  | 1             | 1          | 2024/7/26     | [1,12,2,134,23,2,12] | 1,2,3               | 3,4,5                | 7             | 2             | 1200             |

      **说明**

      分区时间为20240728，`target`已知。

   2. 对待评估的数据表进行模型评估：

       

      ```sql
      /*polar4ai*/SELECT user_id,target FROM EVALUATE (MODEL GameName_7to14_train_val_lose_20240720_20240726, 
      SELECT * FROM GameName_predict_lose_7_to_14_2024_07_28_2024_07_28) WITH 
      (x_cols = 'event_list,max_level,max_viplevel,num_event,stats_item_list,stats_event_list',y_cols='target',s_cols='user_id,target',metrics='Fscore');
      ```

      **说明**

      - MODEL GameName_7to14_train_val_lose_20240720_20240726：表示模型名称是GameName_7to14_train_val_lose_20240720_20240726，是之前创建模型脚本中指定的模型名称。
      - x_cols：表示需要用到的特征列，通常要和创建模型时用到的xcols一致。
      - y_cols：表示标记列，即用户是否流失的标记。
      - s_cols：表示需要最后结果中要带的列，一般会把user_id带出来，方便后续的数据分析。
      - metrics：评估的标准指标。分类算法推荐用Fscore或者AUC。
      - 运行后会生成一个Task，记录好`taskid`。

   3. 执行如下SQL：

       

      ```sql
      /*polar4ai*/ SHOW TASK <taskid>;
      ```

      可以得到评估的结果。通常输出会是一个Fscore的值，Fscore越高效果越好。

      **说明**

      结果指标说明：

      - 准确率（ Precision ）：用户流失预测模型中，准确率指模型识别出来的流失人数且真实付费/模型识别出来的总流失人数。
      - 召回率（Recall）：用户流失预测模型中，召回率指模型识别出来流失且真实流失人数与真实付费总人数。
      - F1 分数（FScore）：指准确率和召回率的调和平均值，用于综合考虑模型的准确性和召回能力。FScore=2×（Precision×Recall）/（ Precision+Recall）。

      例如：

      总样本数：100人。模型预测付费人数：80（其中70人真实付费，10人真实未付费），预测不付费人数：20人（其中15人真实未付费，5人真实付费）。

      则准确率=70/80=87.5%；召回率=70/（70+5）=93.3%；Fscore=2*（0.875*0.933）/（ 0.875+0.933 ）=90.3%。

4. 模型推理

   - 待预测表：GameName_predict_lose_7_to_14_2024_07_28_2024_07_28
   - 预测结果表：res_GameName_predict_lose_7_to_14_2024_07_28_2024_07_28
   - 使用模型名：GameName_7to14_train_val_lose_20240720_20240726

   数据表示例如下：

   | **train_start_date** | **train_end_date** | **test_start_date** | **test_end_date** | **user_id** | **is_prepay** | **target** | **part_date** | **event_list** | **stats_item_list** | **stats_event_list** | **num_event** | **max_level** | **max_viplevel** |
   | -------------------- | ------------------ | ------------------- | ----------------- | ----------- | ------------- | ---------- | ------------- | -------------- | ------------------- | -------------------- | ------------- | ------------- | ---------------- |
   | 2024/7/28            | 2024/8/3           | 2024/8/4            | 2024/8/17         | example001  | 1             | 0          | 2024/7/28     | [1,2,3,3,3]    | 0,1,2               | 1,2,3                | 5             | 43            | 600              |
   | 2024/7/28            | 2024/8/3           | 2024/8/4            | 2024/8/17         | example002  | 1             | 0          | 2024/7/28     | [2,23,4]       | 4,5,2               | 3,4,5                | 3             | 3             | 600              |
   | 2024/7/28            | 2024/8/3           | 2024/8/4            | 2024/8/17         | example003  | 0             | 0          | 2024/7/28     | [9,1,2,3]      | 1,3,2               | 1,2,45               | 4             | 39            | 1200             |

   **说明**

   由于`target`的区间不存在（未知），默认全部置为0。

   离线预测

   在线预测

   支持3种模式得到离线预测的结果数据：

   - 离线预测不写表：预测的结果会存储到一个OSS文件中，可以手动下载OSS地址对应的文件。适用于把数据结果嵌入到已有系统中。

      

     ```sql
     /*polar4ai*/SELECT user_id,target FROM PREDICT (MODEL GameName_7to14_train_val_lose_20240720_20240726, 
     SELECT * FROM GameName_predict_lose_7_to_14_2024_07_28_2024_07_28) WITH 
     (x_cols= 'event_list,max_level,max_viplevel,num_event,stats_item_list,stats_event_list', s_cols='user_id,target', mode='async');
     ```

     **说明**

     运行后会生成一个Task，记录好`taskid`。

     执行以下命令，如果任务完成（Finish）后，会得到一个OSS地址，OSS文件即结果文件：

      

     ```sql
     /*polar4ai*/ SHOW TASK <taskid>;
     ```

   - 离线预测写入数据库表：预测的结果会存储到PolarDB for AI数据库下的指定数据表中。

      

     ```sql
     -- 结果存在polar4ai数据库中
     /*polar4ai*/SELECT user_id,target FROM PREDICT (MODEL GameName_7to7_train_val_charge_sum_20240720_20240730,SELECT * FROM GameName_predict_lose_7_to_14_2024_07_28_2024_07_28) WITH (x_cols= 'event_list,max_level,max_viplevel,num_event,stats_item_list,stats_event_list',s_cols='user_id,target', mode='async', into_type='regular',primary_key='user_id') into res_GameName_predict_lose_7_to_14_2024_07_28_2024_07_28;
     ```

     polar4ai.res_GameName_predict_lose_7_to_14_2024_07_28_2024_07_28是结果表。

      

     ```sql
     /*polar4ai*/show task `your-task-id`;
     SELECT COUNT(*) FROM polar4ai.res_GameName_predict_lose_7_to_14_2024_07_28_2024_07_28;
     SELECT * FROM polar4ai.res_GameName_predict_lose_7_to_14_2024_07_28_2024_07_28;
     ```

     **重要**

     - 需在控制台建立名为`polar4ai`数据库，并对当前操作账号与AI节点账号配置`polar4ai`数据库的读写权限。
     - 预测结果数据将先生成OSS下载链接，再执行表更新操作，如果更新失败会抛出错误信息，但不会返回具体数据行。通常需要查看待预测的表中是否存在脏数据。
     - `SELECT`要指明选择的列以及主键，不能使用`SELECT *`，也不能写入内容过长的列（例如`event_list`，1000条数据不大于3M），否则会导致写入热存表失败。
     - 因为是异步写表逻辑，不会返回写表结束终止条件，需要通过`SELECT COUNT(*) FROM polar4ai.your_table_name;`来判断写入行数是否完整。
     - 写数据库表需持续占用AI节点（不能同时进行模型训练和预测）。

   - 离线预测写冷存表：预测的结果会存储到`polar4ai`数据库下的一个冷存表中，存储价格会相对便宜，但查询性能会慢一些。更多信息，请参见[将AI模型推理结果写回数据库](https://help.aliyun.com/zh/polardb/polardb-for-mysql/user-guide/bring-ai-generated-content-to-a-database-table-through-aat)。

      

     ```sql
     -- 结果存在polar4ai数据库中
     /*polar4ai*/SELECT user_id,target FROM PREDICT (MODEL GameName_7to7_train_val_charge_sum_20240720_20240730,
     SELECT * FROM GameName_predict_lose_7_to_14_2024_07_28_2024_07_28) WITH 
     (x_cols= 'event_list,max_level,max_viplevel,num_event,stats_item_list,stats_event_list',s_cols='user_id,target', mode='async', into_type='db') into res_GameName_predict_lose_7_to_14_2024_07_28_2024_07_28;
     ```

     执行以下命令，如果任务完成（Finish）后，则证明写入冷存表成功：

      

     ```sql
     /*polar4ai*/ SHOW TASK `94xxxxxx-xxxx-xxxx-xxxx-xxxxxxd0e18`;
     ```
