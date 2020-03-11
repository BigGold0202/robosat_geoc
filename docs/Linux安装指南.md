- linux环境准备
    - $ yum update
    - $ yum install git

- 下代码
  - git clone https://github.com/geocompass/robosat_geoc.git

- 安装anaconda
  - 下载 Anaconda.sh 64-Bit (x86) Installer (506 MB)
    - $ bash Anaconda3-4.4.0-Linux-x86_64.sh
  - 默认安装路径：/root/anaconda3
  - initialize conda？  $ yes
  - 增加环境变量 plan A 
    - $ source <path to conda>/bin/activate（官网推荐）
  - 增加环境变量 plan B
    - $ vim /root/.bashrc
  - added by Anaconda3 4.4.0 installer
  - export PATH="/root/anaconda3/bin:  - $PATH"
  - 保存退出
    - $ source /root/.bashrc
  - 检查是否安装成功   - $ conda customized
  - 更新   - $ conda update -n base -c defaults conda

- $ conda init或者退出xshell重连

- 创建虚拟环境
  - $ conda create -n robosat
  - $ conda activate robosat

- 安装pip
  - $ yum -y install epel-release
  - $ yum -y install python-pip

- 安装rtree

- 安装rtree依赖

  - 安装libspatialindex
    - $ conda install -c conda-forge libspatialindex=1.9.3
  - 若libspatial安装成功跳过此步，失败安装cmake
    - 下载cmake并移动到linux根目录：https://github.com/Kitware/CMake/releases/download/v3.13.2/cmake-3.13.2.tar.gz
      - $ tar -zxvf cmake-3.13.2.tar.gz
      - $ cd cmake-3.13.2
      - $ ./bootstrap && make && make install
      - $ cmake version 3.10.2（失败）

- 安装rtree
  - $ conda install rtree

- 安装torch
  - $ pip install torch
  - $ pip install torchvision

- 安装robosat_geoc依赖
  - $ pip install --upgrade pip
  - $ pip install -r requirements.txt (因为torch包700m下载过慢，放在安装依赖步骤最后，避免重复耗时)