---
title: WSL2+OhMyZsh+VSCode开发环境搭建
description: 这篇博客记录在 WSL2 中搭建开发环境，包括 Git、Zsh 配置和 Python 版本管理。
author: Tom
date: "2024-02-05"
toc: true  # 是否开启文章目录
toc-expand: true
code-block-bg: true  # 代码块背景颜色
highlight-style: atom-one  # 代码块语法高亮风格
categories:
  - 开发环境
image: code-snapshot.png
code-fold: false  # 代码块是否折叠
cold-line-numbers: true # 代码块是否显示行数
code-copy: true # true/false/hover
draft: false  # 博文是否为草稿，草稿不显示在博客中
html-math-method: katex # latex 引擎，默认是 MathJax
jupyter: python3
---

# 安装 WSL

```bash
wsl --install
```

## WSL 基本命令

```bash
# 查找可用发行版
wsl --list --online

# 安装发行版
wsl --install -d Ubuntu-22.04

# 列出已安装的发行版
wsl --list --verbose

# 设置默认的 Linux 发行版
wsl --set-default Ubuntu-22.04

# 更新 WSL
wsl --update

# 检查 WSL 状态
wsl --status

# 检查 WSL 版本
wsl --version

# 关闭
wsl --shutdown

# 终止运行
wsl --terminate Ubuntu-22.04

# 导出发行版
wsl --export <Distribution Name> <FileName>

# 导入发行版
wsl --import <Distribution Name> <InstallLocation> <FileName>
```

# 安装 Linux 发行版

安装指定版本的 Linux发行版，根据提示设置用户名和密码。

```bash
wsl --install -d Ubuntu-22.04
```

升级和更新包：

```bash
sudo apt update && sudo apt upgrade
```

# 安装 Git

```bash
 sudo apt-get install git
```

配置 Git 全局用户名和邮件地址：

```bash
git config --global user.name "Your Name"
git config --global user.email "youremail@yourdomain.com"
```

验证配置：

```bash
git config --list
```

配置文件被存储在`~/.gitconfig`文件：

```bash
[user]
    name = Your Name
    email = youremail@yourdomain.com
```

# 安装 Zsh

```bash
# 安装
sudo apt-get install zsh -y

# 查看 shells
cat /etc/shells

# 设置默认 shell
chsh -s /usr/bin/zsh	
```

设置默认 shell 后，重开一个窗口，zsh 会询问用户配置问题，选择 2 推荐配置，后续如果需要自己修改 `~/.zshrc`。

## 安装 [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting) 和 [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions)

```bash
# 安装 zsh-syntax-highlighting
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

# 安装 zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

修改 `~/.zshrc`：

```bash
plugins=(zsh-syntax-highlighting zsh-autosuggestions)
```

## 安装 oh-my-zsh

```bash
sh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

关于 oh-my-zsh 的一些常用命令：

```bash
# 更新
omz update

# 卸载
uninstall_oh_my_zsh
```

## 配置 [powerlevel10k](https://github.com/romkatv/powerlevel10k) 主题

```bash
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
```

编辑 `~/.zshrc` 配置文件：

```bash
ZSH_THEME="powerlevel10k/powerlevel10k"
```

根据提示配置主题，后续可通过  `p10k configure`自由配置。

# 安装 Python

有多种方式可以安装 Python，这里选择使用 PPA 安装。

```bash
# Update and Refresh Repository Lists
sudo apt update

# install software-properties-common
sudo apt install software-properties-common

# Add Deadsnakes PPA and update lists
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

# install Python
sudo apt install python3.12
```

Python 被安装在 `/usr/bin/python3.12`，可以在命令行进行测试：

```bash
python3.12 -V	
```

## 管理多版本 Python

Ubuntu 22.04 默认安装了 Python3.10（`/usr/bin/python3.10`），而我们自己安装了 Python3.12，我们可以使用 [`update-alternatives`](https://linux.die.net/man/8/update-alternatives?ref=hackersandslackers.com) 命令管理系统存在的多个版本的 Python。

```bash
# adding the system's default version of Python to update-alternatives
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

# Set alternative versions for Python3
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 2

# List installed versions of Python visible to update-alternatives
update-alternatives --list python3

# Swapping between versions
update-alternatives --config python3
```

# 参考资料

- https://learn.microsoft.com/zh-cn/windows/wsl/setup/environment
- https://docs.python-guide.org/starting/install3/linux/
- https://hackersandslackers.com/multiple-python-versions-ubuntu-20-04/
- https://phoenixnap.com/kb/how-to-install-python-3-ubuntu