---
title: Ubuntu18.04安装与配置
author: Tom
date: "2019-04-19"
toc: true
code-block-bg: true
highlight-style: atom-one
categories:
  - 开发环境
image: ubuntu.png
code-fold: false
html-math-method: katex
jupyter: python3
---

这篇博客记录了 Ubuntu 18.04 的安装、配置与美化过程。

# 安装 Ubuntu

## 引导盘

- 下载 Ununtu 18.04 的镜像文件，将U盘格式化为 FAT32，然后解压操作系统的镜像文件至U盘根目录，完成刻录。
- 下载 Ubuntu 18.04 的镜像文件，使用 Rufus 进行刻录。（使用默认设置即可）

## 关闭 Windows 的快速启动

进入控制面板 -> 电源选项 -> 选择关闭电源按钮功能 -> 更改当前不可用设置：关闭启用快速启动，保存设置。

## 安装系统

重启计算机，在开机画面出现之前，狂按 f12 进入 bios 启动界面，选择从U盘启动，选择 install Ubuntu。

一些注意事项：

- 安装时选择最小安装；
- 安装过程中选择使用语言时选择英语，便于在命令行中使用 cd 命令；
- 选择区域和城市：Asia/Shanghai。

# 必要配置

## 更换软件源

Ununtu 18.04 默认使用的是国外的软件源，因为使得我们在下载和更新软件时速度较慢，这里我们替换为国内的阿里云软件源：

点击 Software&Updates -> Ununtu Software -> 点击 download from 右边的下拉框，选择 Other -> 在弹出的界面中选择阿里云软件源。

## 全面更新

在进一步操作之前，我们先把已经安装的软件包都升级到最新版，在终端输入：

```Bash
sudo apt update
sudp apt upgrade
```
点击 settings -> language -> Manage Installed Language，完成语言列表的更新，然后注销重启。

## 显卡配置

如果电脑带 Nvidia 独立显卡，点击 Software&Updates -> Additional Drivers 里选择对应的 N 卡私有的驱动程序并应用更改。

## 更换终端类型

更换默认终端为fish[https://launchpad.net/~fish-shell/+archive/ubuntu/release-3]。

在终端输入以下命令：

```Bash
sudo apt-add-repository ppa:fish-shell/release-3
sudo apt-get update
sudo apt-get install fish
```

# Ubuntu 美化

## 安装 Gnome-tweak-tool

Ubuntu 18.04 默认使用的桌面为 gnome3。打开终端执行：

```Bash
sudo apt-get install gnome-tweak-tool
```

## User theme 插件安装

使 shell 主题可以使用桌面主题。

## 改变桌面主题与图标主题

- [桌面主题](https://github.com/vinceliuice/vimix-gtk-themes)
- [图标主题](https://github.com/vinceliuice/vimix-icon-theme)
- [壁纸](https://wallhaven.cc/)

进入 Github 下载源文件，解压到目录并进入，右键点击空白处选择在终端中打开，执行安装。待安装完成后在 Gnome-tweak-tool 里选择桌面主题与图标主题。

## 安装搜狗输入法

搜狗输入法依托fcitx输入法框架，因此我们首先安装 fcitx 框架。打开终端执行：

```Bash
sudo apt install fcitx -y
```
然后进入搜狗输入法官网下载搜狗输入法的 deb 安装包。安装搜狗输入法。

打开 gnome-tweaks，在开机启动推荐中添加 fcitx。