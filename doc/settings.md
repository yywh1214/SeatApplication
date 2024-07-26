# 设置文件说明

> 注意： 请在手动调整配置文件之前先进行 **备份** 。并 **严格按照** 此文件要求的格式进行修改。如果遇到乱码问题，请使用 `utf-8` 编码。


### 人名文件：`./assets/settings/name.yaml`
范例：
```yaml
Students:
  - name: 0
  - name: 1
  - name: 2
  - name: 3
  - name: 4

Groups:
  group1: [0, 1, 2, 3, 4]
```
其中 `Students` 表示学生列表，从上到下依次对应 `id` 为 $0$ 到 $n$ 的学生，每一个 `name` 属性代表了他（她）的名字。

`Groups` 表示每一个分组，其内部每一个名称表示小组名，小组名通过列表的形式传入学生的 `id`。

注意：  
1. `Students` 是一个 **列表** ，其每一个元素是一个 **字典** ，拥有一个相同的属性：`name`。不要遗漏 `name` 前面的 `-`。
2. `Groups` 是一个 **字典** ，其 keys 对应一个 **列表** 每个列表中包含了学生的 `id`。
3. 请使用半角符号如：`-` `:` `[` `]` 而不是：`——` `：` `【` `】`等。
4. 首字母需要大写。
5. 建议不要使用中文，其很有可能造成不必要的麻烦。


### 规则文件：`./assets/settings/rule.yaml`
范例：
```yaml
Whitelist: { 1: [2, 4], 2: [3, 5] }
Blacklist: { 1: [3, 5] }
# 注意: 这里的规则都是双向的，且如果规则为空，保留大括号
```

其中 `Whitelist` 表示一个学生 `id` 只能与特定的学生做同桌，`Blacklist` 表示一个学生 `id` 不能与特定的学生做同桌。
> 注意： 这里的每一条规则所表述的同学必须在 **同一个** 组内。


### 教室文件：`./assets/settings/table.yaml`
范例：
```yaml
GroupNum: 1 # 教室内总共的大组数量
ColumnOfDesk: 2 # 每一桌的人数（由于技术原因暂时只支持2）
RowOfGroup: [3] # 每一列的桌数
```
若教室的总位置（ $\sum RowOfGroup$ ）大于人数，将使用空位替代，并且若只有不超过一桌空位，它只会出现在教室的右下角。反之，报错并退出程序。你的 `GroupNum` 应当与 `RowOfGroup` 的大小相等。

### 日志文件：`./assets/settings/logging.yaml`
请依照 `logging` 库的相关要求书写或者复制默认文件：
```yaml
version: 1
disable_existing_loggers: False
formatters:
  simple:
    format: "[%(levelname)s] %(asctime)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s"
handlers:
  console:
    class: logging.StreamHandler
    level: DEBUG
    formatter: simple
    stream: ext://sys.stdout
  info_file_handler:
    class: logging.handlers.TimedRotatingFileHandler
    level: INFO
    formatter: simple
    filename: log/info.log
    when: H
    backupCount: 20
    encoding: utf8
  debug_file_handler:
    class: logging.handlers.TimedRotatingFileHandler
    level: DEBUG
    formatter: simple
    filename: log/debug.log
    when: H
    backupCount: 20
    encoding: utf8
  error_file_handler:
    class: logging.handlers.TimedRotatingFileHandler
    level: ERROR
    formatter: simple
    filename: log/errors.log
    when: H
    backupCount: 20
    encoding: utf8
loggers:
  my_module:
    level: ERROR
    handlers: [info_file_handler]
    propagate: no
root:
  level: INFO
  handlers: [console, info_file_handler, error_file_handler, debug_file_handler]
```