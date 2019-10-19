<a href="https://twitter.com/RobosatPink"><img src="https://img.shields.io/badge/Follow-%40RoboSatPink-ff69b4.svg" /></a>  <a href="https://gitter.im/RoboSatPink/community"><img src="https://img.shields.io/gitter/room/robosatpink/community.svg?color=ff69b4&style=popout" /></a> <a href="https://pepy.tech/project/robosat.pink"><img src="https://pepy.tech/badge/robosat-pink/month" align="right" /></a>

<h1 align='center'>RoboSat_geoc</h1>
<h2 align='center'>从标准WMTS影像中提取建筑物的深度学习框架</h2>
<h3 align='center'>forked by <a href="https://github.com/datapink/robosat.pink" >Robosat.pink</a></h3>
<p align=center>
  <a href="https://github.com/geocompass/robosat_geoc"><img src="https://raw.githubusercontent.com/geocompass/robosat_geoc/master/docs/img/readme/top_example.jpeg" alt="RoboSat_Geoc buildings segmentation from Imagery" /></a>
</p>



## 简介：

`RoboSat.geoc` 由 [mapbox/robosat](https://github.com/mapbox/robosat) 及 [Robosat.pink](https://github.com/datapink/robosat.pink)  fork 而来。

利用深度学习工具，可以很方便的使用标准WMTS影像对建筑物轮廓提取进行训练和预测。



目的:
---------
- `Mapbox/Robosat` 是非常不错的建筑物提取工具，`Robosat.pink` 对其做了重构和改造，使其易用性得到了提升。
- `Robosat.geoc` 在 `Robosat.pink` 的基础上，做了自动化和工程化改造，并可以结合 [rs_buildings_extraction](https://github.com/geocompass/rs_buildings_extraction) ，使用可视化界面和接口的方式进行训练和预测，很方便的用于生产环境。


主要功能:
--------------
- 继承了`RoboSat.pink` 的所有功能：
  - 提供了命令行工具，可以很方便的进行批处理
  - 遵循了 WMTS 服务标准，方便遥感影像数据的准备 
  - 内置了最先进的计算机视觉模型，并可以自行拓展
  - 支持RGB和多波段影像，并允许数据融合
  - 提供了 Web 界面工具，可以轻松的显示、对比、选择训练结果 
  - 高性能
  - 很松的能够拓展
  - 等等
- 将深度学习训练标注（`label`) 数据以PostGIS的方式存储，对 GISer 极其友好
- 提供了 WMTS 瓦片服务代理工具，可将天地图、谷歌影像等作为影像数据源（Robosat不支持类似 `http://this_is_host?x={}&y={y}&z={z}` 形式的URL，仅支持类似 `http://this_is_host/z/x/y` 
- 对 `RoboSat.pink` 做了自动化改造，无需手动逐个输入命令行，一键式训练或预测
- 简化调试方式，仅需提供待训练或预测的范围（`extent`）
- 自动化训练限定为 `PostgreSQL+PostGIS` 数据源作为深度学习标注



说明文档:
--------------

### 训练数据准备：

- 安装 `PostgreSQL+PostGIS`，创建数据库，添加 `PostGIS` 扩展 `create extension postgis;`
- 使用 `shp2pgsql` 等工具将已有的建筑物轮廓数据导入 `PostGIS` 作为深度学习标注数据，或者使用 `QGIS` 等工具连接 `PostGIS` 并加载遥感影像底图进行绘制建筑物轮廓

### 如何安装：
- 对于 MacOS 或 Linux：
  - 下载代码：`git clone https://github.com/geocompass/robosat_geoc.git`
  - 安装依赖：`python install -r requirements.txt` （若使用Anaconda需要注意 python 路径，后同）
- 对于 Windows：
  - 在 Windows 安装依赖时会报 `GLAL` 相关错误，目前没有比较好的解决办法 
  - 建议使用 WSL，[在Windows 中安装 Ubuntu SubLinux](https://docs.microsoft.com/zh-cn/windows/wsl/install-win10)
  - 配合 [Windows Terminal](https://www.microsoft.com/zh-cn/p/windows-terminal-preview/9n0dx20hk701) ，使用Ubuntu 命令行工具
  - 使用上述 MacOS 或 Linux安装方式进行部署

### 如何运行：

- 设置已有的建筑物轮廓标注数据
  - 设置 PostGIS连接： `robosat_pink/geoc/config.py` 中的 `POSTGRESQL`
  - 设置已有建筑物轮廓数据表：`robosat_pink/geoc/config.py` 中的 `BUILDING_TABLE`
- 后台运行 WMTS 代理工具：`python xyz_proxy.py &`
- 设置训练或预测范围：`./test.py` 中的 `extent`
- 开始训练或预测：`python test.py` 

### Windows 中如何开发：

- 使用VSCode：
  - 使用 [Remote-WSL](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl) 拓展连接WSL的Ubuntu，连接该项目文件夹进行开发
- 使用PyCharm：
  - 在 `Settings` 中[配置 Project Interpreter](https://www.jetbrains.com/help/pycharm/using-wsl-as-a-remote-interpreter.html) 的 WSL 参数。

### 如何作为packages：

- 构建：`python setup.py build`
- 安装：`python setup.py install`
- 在工程中调用：`from robosat_pink.geoc import RSPtrain` & `from robosat_pink.geoc import RSPpredict`


本项目作者:
--------
- 吴灿  [https://github.com/wucangeo](https://github.com/wucangeo)
- Liii18 [https://github.com/liii18](https://github.com/liii18)

## 欢迎 Issues

欢迎提一个 [Issue](https://github.com/geocompass/robosat_geoc/issues) 



```

```
