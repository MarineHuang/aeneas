# This is a dockerfile for aeneas.
# aeneas is a Python/C library and a set of tools to automagically synchronize audio and text (aka forced alignment).
# Step1: Build a docker image: docker build -t aeneas:v1 .
# In the above command, aeneas is the name of image will builded, v1 is the TAG of image.
# Step2: Create a new container: docker run -it -p 8888:22 --name aeneas aeneas:v1
# In the above command, map container's 22 port to hoster's 8888 port.
# From this dockerfile you can build a docker image which containing
# Ubuntu 18.04
# git
# Miniconda3 and python3.8
# 

FROM ubuntu:18.04
MAINTAINER MarineHuang

# 修改源为国内源
RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && \
  sed -i 's/security.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && \
  apt-get clean && apt-get update && apt-get upgrade
  
# 添加管理员账户marine，设置工作目录
RUN useradd -s /bin/bash marine && \
    adduser marine sudo && \
    echo "marine:admin"|chpasswd && \
    echo "root:admin"|chpasswd


# install some tools: vim wget ssh git
# vimrc
# 修改ssh配置文件，文件位置/etc/ssh/sshd_config
# 添加允许所有主机连接
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y apt-utils && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y sudo vim wget openssh-server git && \
  DEBIAN_FRONTEND=noninteractive wget https://raw.githubusercontent.com/MarineHuang/UsefulTools/master/conf/.vimrc_marinehuang -O /root/.vimrc && \
  DEBIAN_FRONTEND=noninteractive sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config && \
  DEBIAN_FRONTEND=noninteractive echo 'sshd:ALL' >> /etc/hosts.aldlow

# 开放22端口
EXPOSE 22

# Install Miniconda
# -b 静默安装 -p 指定安装目录
RUN \
 wget https://repo.anaconda.com/miniconda/Miniconda3-py38_4.10.3-Linux-x86_64.sh -O /tmp/Miniconda.sh && \
 DEBIAN_FRONTEND=noninteractive /bin/bash /tmp/Miniconda.sh -b -p /root/Miniconda3 && \
 rm /tmp/Miniconda.sh && \
 echo 'export PATH="/root/Miniconda3/bin:$PATH"' >>  /root/.bashrc && \
 /bin/bash -c 'source /root/.bashrc'

# 设置容器运行时执行的命令，启动ssh服务,并进入bash Shell
ENTRYPOINT sudo service ssh start && /bin/bash
