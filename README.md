# SeatApplication-revamp

#### 介绍

基于 [SeatApplication](https://github.com/lkrkerry1/SeatApplication) 项目开发，添加了一些小功能

#### 画饼区
1. [x] 内核部分制作
2. [x] CLI部分制作
3. [ ] GUI部分制作完善（制作中）
4. [ ] 动态概率以及历史存储访问
5. [x] 可选择前调座位，优先往前靠
6. [ ] 修复黑白名单

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
pip install -r requirements.txt
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

#### 使用说明

1.  下载发布版后先解压！
2.  相关的配置文件在./assets/settings
3.  ./assets/settings/name.txt 存储所有名称
4.  ./assets/settings/rules.txt 存储所有用户自定义规则（格式见样例）
5.  ./assets/settings/table.txt 存储大组数（GroupNum），每组的列数（暂时只支持2），依次每组的行数（ColumnOfGroup），具体见样例
6.  ./assets/history/ 存储输出
7.  ./assets/audio/ 存储用到的多媒体
8.  ./assets/setting/amendment.txt 存储所有对于前调座位的占位控制图
9.  ./assets/setting/prioritization.txt 填写需要优先前调座位的人的名字

#### 警告
由于开发者超小杯技术，加入前调座位功能后没有考虑黑白名单，所以现在黑白名单形同虚设，等待未来修复

#### 参与贡献

1.  Fork 本仓库（或者下载）
2.  新建 Feat_xxx 分支，如果为修复，新建Fix_xxx
3.  提交代码
4.  新建 Pull Request合并到dev！
5.  等待代码合并

#### 乐子
先说结论：超小杯不建议抽取

开发者要上学只能周末搞开发被评为回转太慢，一次写出的有效代码太少dph过低，一周只能写出一点点dps过低，写代码前要酝酿很久初动太慢，综上评为***超小杯***
