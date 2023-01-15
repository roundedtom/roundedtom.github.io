---
slug: hyperledger-fabric-install
date: 2022-02-09 13:27:01
tags: Fabric, Golang, Docker
category: TECH
description: hyperledger fabric 安装笔记
type: text
title: hyperledger fabric (v2.0) 安装过程记录
---

这篇文章记录安装 fabric(v2.0) 的过程。

<!-- TEASER_END -->

[TOC]

# 1 Go

# 1.1 下载安装

在 Golang [官网](https://golang.google.cn/dl/)下载 linux 版本的压缩文件，在终端切换目录至压缩文件所在目录（这里是 Downloads)，然后将压缩文件解压缩至 `usr/local` 目录下。命令如下:

```shell
cd Downloads
sudo tar -xzf go1.12.1.linux-amd64.tar.gz -C /usr/local
```

此时在 `usr/local` 下会生成一个 `go` 目录，可以通过 `ls` 命令查看：

```shell
cd /usr/local/go
ls
```

也可以用以下命令安装（ubuntu 系统）

```shell
mkdir /usr/local/go
cd /usr/local/go
wget https://dl.google.com/go/go1.14.2.linux-amd64.tar.gz
```

## 1.2 配置环境变量

### 1.2.1 安装 vim

在终端输入以下命令

```shell
sudo apt-get install vim
```

### 1.2.2 编辑 home/.profile 文件

先配置 GOROOT，即 go 的安装目录，编辑 `$HOME/.profile` 文件。利用 vim 打开文件，按 i 进入编辑，加入如下命令，保存并退出。

```shell
export GOROOT="usr/local/go"
```

然后配置 GOPAHT，GOPATH 是 go 项目代码存放的地方，是我们自己定义的目录。对于 Ubuntu 系统，默认使用 `Home/go` 目录作为 GOPATH。该目录下有三个子目录：src，pkg，bin。

```shell
export GOPATH=$HOME/go
```

配置 GOBIN，并将 GOBIN 添加至环境变量中。

```shell
export GOBIN=$GOROOT/bin
export PATH=$PATH:$GOBIN
```

最后在终端中输入如下命令，使环境变量生效：

```shell
source .profile
```

# 2 docker

## 2.1 安装 docker

### 2.1.1 下载安装

使用 docker 官网教程下载太慢，这里使用清华大学开源镜像，首先安装安装所需的依赖，在终端输入以下命令：

```shell
sudo apt-get install apt-transport-https ca-certificates curl gnupg2 software-properties-common
```

然后添加信任 docker 的 GPG 公钥：

```shell
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

然后添加软件仓库：

```shell
sudo add-apt-repository \
 "deb [arch=amd64] https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/ubuntu \
 $(lsb_release -cs) \
 stable"
```

最后安装最新版本的 Docker Engine-Community 和 containerd：

```shell
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

### 2.1.2 配置用户组

添加$user 到 docker 用户组，免除每次运行 docker 都需要使用 sudo root 权限，在终端输入以下命令：

```shell
sudo groupadd docker
sudo usermod -aG docker ${USER}
newgrp docker
```

### 2.1.3 配置阿里云镜像加速服务

由于 Docker 镜像服务器在国外，所以下载速度非常缓慢甚至失败，因此我们需要配置阿里云镜像加速服务。进入阿里云官网注册登录，在搜索框中搜索容器镜像服务，选择镜像加速器，获取自己的加速器地址，根据提示，在终端输入以下命令：

```shell
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
"registry-mirrors": ["你的加速器地址"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```

使用以下命令测试 docker 是否安装成功：

```shell
docker run hello-world
```

## 2.2 安装 docker-compose

在终端输入以下命令，安装 1.25.4 版本 docker-compose:

```shell
sudo curl -L https://github.com/docker/compose/releases/download/1.25.4/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

使用以下命令测试 docker-compose 是否安装成功：

```shell
docker-compose --version
```

# 3 fabric

首先下载 fabric 源码（fabirc v2.0），在终端输入以下命令：

```shell
cd /home/go/src/github.com/hyperledger/
git clone https://github.com/hyperledger/fabric.git
```

然后切换目录至 fabric/scripts 下，运行 bootstrap.sh 脚本，此脚本有两个作用：

- 克隆 hyperledger/fabric-samples 仓库
- 下载一些必要的二进制文件（hyperledger-fabric-linux-amd64-2.0.0.tar.gz)

  命令如下：

```shell
cd /home/go/src/github.com/hyperledger/fabric/scripts
./bootstrap.sh
```

由于墙的原因，可能导致如下报错，说明二进制文件下载失败（但一般 fabric-samples 可以下载成功）

```shell
==> There was an error downloading the binary file.
------> 2.0.0 platform specific fabric binary is not available to download <----
```

此时我们改为手动下载二进制文件，可以从我的百度云分享下载（https://pan.baidu.com/s/1ri8azrHUl1KNgxHon384jg，提取码：fhu2）。将hyperledger-fabric-linux-amd64-2.0.0.tar.gz（二进制文件）解压，将其中的config和bin文件夹拷贝至fabric根目录与fabric samples（在/fabric/scripts 目录下）根目录下。切换到/fabric samples/first network 目录，输入以下命令：

```shell
./byfn.sh up
```

当看到命令行如下显示时，表明 fabric 安装完成：

```shell

---

/ **_| |_ _| / \ | _ \ |\_ \_|
\_** \ | | / _ \ | |_) | | |
 **_) | | | / _** \ | _ < | |
|\_\_\_\_/ |_| /_/ \_\ |_| \_\ |\_|

Build your first network (BYFN) end-to-end test

Channel name : mychannel
Creating channel...
```

注意，若运行 byfn.sh 脚本报错，错误信息如下：

```shell
ERROR! Fabric Docker image version of 1.4.4 does not match this newer version of BYFN and is unsupported. Either move to a later version of Fabric or checkout an earlier version of fabric-samples.
```

这表明 fabric-samples 版本与 fabric docker 镜像版本不匹配，可以将 fabric-samples 替换为 1.4 版本（百度云文件中有），再次运行 byfn.sh 脚本。

# 4 参考资料

- https://golang.google.cn/doc/install
- https://mirrors.tuna.tsinghua.edu.cn/help/docker-ce
- https://www.runoob.com/docker/ubuntu-docker-install.html
- https://hlf.readthedocs.io/en/latest/prereqs.html
