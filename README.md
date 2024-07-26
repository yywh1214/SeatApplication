# SeatApplication

#### 介绍

模块化设计的自动排座位，支持自定义规则和特效（暂时只制作了cli）
[详细内容：](./doc/main.md)

#### 画饼区
1. [x] 内核部分制作
2. [x] CLI部分制作
3. [ ] GUI部分制作完善（制作中）
4. [ ] 动态概率以及历史存储访问

#### 编译安装教程

1.  安装virtualenv

```bash
python -m pip install virtualenv
```
2. 新建并运行env
```bash
python -m venv .env
.env/Scripts/activate
```

3.  安装环境

```bash
pip install requirements.txt -r
```

4.  开始使用！
```bash
cd src
python ./main.py
```
5. 编译
```bash
pip install pyinstaller 
pyinstaller -F ./src/main.py
```