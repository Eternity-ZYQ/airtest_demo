# airtest_testerhome

#### 项目介绍
对于airtest的封装和po项目

#### 软件架构

- base 除了底层库以外的方法
- util 工具类（包含移动端-拆分成游戏和非游戏，网页端）
- test_case:对应包名-test_*.py
- Conf:读取配置的
- test_files:处理数据的
- logs:接收日志 
- report:生成报告的
- 其他：望文生义都一样
只有二层，未来考虑是否在加1个中间处理的 :smile: 

#### 安装教程

1. pip改源  pip install -U Airtest
2. pip install -U pocoui  #poco 需要嵌入SDk到工程
3. pip install assertpy #高级断言库
4. pip install opencv-python #图形识别库

#### 使用说明

1. airtest支持基于图像识别的Airtest框架，适用于所有Android和Windows游戏
2. pocoui库  poco.drivers.对应不同的引擎名称


#### 参与贡献（有贡献代码操作一定数量的留名字）
- 陈子昂
1. 欢迎Fork 本项目
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request


#### 码云特技
