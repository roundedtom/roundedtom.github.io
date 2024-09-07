---
title: 如何使用 Nikola 搭建个人博客
author: Tom
date: "2022-04-29"
toc: true
code-block-bg: true
highlight-style: arrow
categories: 
  - 网站博客
image: nikola.jpg
code-fold: false
html-math-method: katex
jupyter: python3
---

一直希望搭建一个博客，一方面是希望能有一个地方记录整理自己学过的知识，另一方面也希望能交到一些志同道合的朋友（有人可以讨论真是太棒了！）在各种鼓捣之后，我选择了 [Nikola](https://getnikola.com/)，因为它原生支持 Jupyter notebook。至于为什么选择静态博客，Nikola 官网这篇[文章](https://getnikola.com/handbook.html#why-static)写的很好。

关于如何使用 Nikola 搭建博客和个人网站，相关的中文资源比较少，这篇文章是我个人，来自一个非科班背景的踩坑经历。博客在 WSL2 上搭建，Windows 与 Mac 上搭建也类似，环境如下：

```Bash
WLS2 Ubuntu 20.04.3 LTS
Nikola Version: 8.2.1
Python 3.8.10
pip 20.0.2
```

# Nikola 安装与博客搭建  

这部分内容是对官方文档 [getting started](https://getnikola.com/getting-started.html) 的一个梳理。其实官方文档写的非常清晰，强烈建议大家去瞅一瞅。

## Nikola 安装

官方文档推荐使用虚拟环境来安装 Nikola，我们可以使用 Python 自带的 venv 模块来创建虚拟环境。

```Bash
# 首先新建一个博客目录
mkdir myblog

# 然后进入到 myblog 目录下，创建虚拟环境
cd myblog
python3 -m venv blog

# 进入到虚拟环境目录，激活虚拟环境
cd blog
source ./bin/activate

# 使用 pip 安装 Nikola
pip install -U pip setuptools wheel
pip install -U "Nikola[extras]"
```

官方文档推荐在安装时选择 Nikola[extras] 版本（可以体验一些额外的功能），但是你也可以选择安装 Nikola 版本。

## 初始化博客

在安装完 Nikola 之后，我们就可以使用 Nikola 提供的命令初始化博客了。

```Bash
nikola init --demo my_blog
```

这条命令会在当前目录下创建一个新的目录 `my_blog`，`--demo my_blog` 参数表示在初始化目录的时候创建一些 demo 文件（当然你也可以选择不创建 demo 文件，使用 `--quiet` 参数）。你会看到如下输出和提问：

```Bash
Creating Nikola Site
====================

This is Nikola v8.2.1.  We will now ask you a few easy questions about your new site.
If you do not want to answer and want to go with the defaults instead, simply restart with the `-q` parameter.
--- Questions about the site ---
Site title [My Nikola Site]:
```

回答命令行中的提问：

- Site title：网站名
- Site author：网站作者
- Site author's e-mail：联系邮箱
- Site description：网站描述，生成网站的 [meta description](https://moz.com/learn/seo/meta-description)
- Site URL：网页 URL
- Enable pretty URLs (/page/ instead of /page.html) that don't need web server configuration? [Y/n]：是否开启 [pretty URLs](https://en.wikipedia.org/wiki/Clean_URL)
- Language(s) to use [en]：选择网站显示语言
- Time zone [Asia/Shanghai]：选择时区
- Comment system：选择评论系统

当你看到以下提示时，就说明博客初始化成功了。

```Bash
That's it, Nikola is now configured.  Make sure to edit conf.py to your liking.
If you are looking for themes and addons, check out https://themes.getnikola.com/ and https://plugins.getnikola.com/.
Have fun!
[2022-04-29 16:09:00] INFO: init: A new site with example data has been created at my_blog.
[2022-04-29 16:09:00] INFO: init: See README.txt in that folder for more information.
```

我们可以看一下 `my_blog` 目录，这是我们的博客根目录。

```Bash
.
├── files
├── galleries
├── images  # 图片存放目录
├── listings
│   └── __pycache__
├── pages  # 页面存放目录
├── posts  # 文章存放目录
└── templates  # 生成站点的模板文件存放目录
```

## 新建博客

博客初始化完成之后，我们就可以添加第一篇博客了。

### 添加第一篇博客

如果你习惯使用命令行，可以使用命令 `nikola new_post -f markdown` 添加第一篇博客：

```Bash
Creating New Post
-----------------

Title: First post
Scanning posts........done!
[2022-04-29 20:50:04] INFO: new_post: Your post's text is at: posts/first-post.md
```

`-f` 参数指定文章格式，这里我们指定为 markdown 格式，该命令会在 posts 文件夹下新建一个 markdown 文件，你可以 `cd` 到 posts 目录下，继续编辑该博客。打开该博客，你会发现以下元信息：

```Bash
<!--
.. title: First post
.. slug: first-post
.. date: 2022-12-30 19:30:43 UTC+08:00
.. tags: 
.. category: 
.. link: 
.. description: 
.. type: text
-->
```

- title：文章标题
- [slug](https://www.semrush.com/blog/what-is-a-url-slug/)：固定链接地址，是 URL 最后一个反斜杠之后的那一部分。slug 如果不指定，Nikola 默认使用文章标题作为 slug。
- date：文章创建时间
- tags：文章标签
- category：文章分类
- link：Link to original source for content. May be displayed by some themes.（官方文档介绍，暂时没用过）
- description：页面描述
- type：文章类型

除此之外，另一个常用的元信息字段是 `has_math`。如果文章中有 latex 公式，就需要添加该字段。一般常用的 metadata 字段就这些，如果你想深入了解，推荐[官方文档](https://getnikola.com/handbook.html#metadata-fields)。

如果你不习惯使用命令行，也可以直接在 posts 目录下新建 markdown 文件，然后利用你喜欢的编辑器进行编辑，但需要手动添加元信息。除了 markdown，Nikola 也支持如下格式：

> - reStructuredText (default and pre-configured)
> - [Markdown](https://getnikola.com/handbook.html#markdown) (pre-configured since v7.8.7)
> - [Jupyter Notebook](https://getnikola.com/handbook.html#jupyter-notebook)
> - [HTML](https://getnikola.com/handbook.html#html)
> - [PHP](https://getnikola.com/handbook.html#php)
> - anything [Pandoc](https://getnikola.com/handbook.html#pandoc) supports (including Textile, DocBook, LaTeX, MediaWiki, TWiki, OPML, Emacs Org-Mode, txt2tags, Microsoft Word .docx, EPUB, Haddock markup)

### 生成静态文件

写完博客之后，下面我们使用命令 `nikola build` 生成静态文件。`nikola build` 会在博客根目录下新建一个 output 目录，这个目录就是你的站点资源目录，你的博客网站里所有显示的内容都来自于这个目录。我们来看下这个目录：

```Bash
.
├── 2012  # 博客归档目录，Nikola demo 文件中有一篇是 2012 年写的
├── archive.html  # 显示博客归档页面
├── assets  # css js fonts img 等资源目录
├── categories  # 博客分类
├── favicon.ico
├── galleries
├── images
├── index.html # 博客首页
├── listings
├── pages
├── posts  # 博客目录
├── robots.txt
├── rss.xml
├── sitemap.xml
└── sitemapindex.xml
```

这里，我们需要关注 posts 目录，`nikola build` 命令会将我们写的 markdown 文件转化为 html 文件并保存在该目录下。

### 本地调试

使用命令 `nikola serve -b` 会打开默认浏览器，方便我们进行本地调试。这里，由于我是在 WSL2 中搭建博客，键入 `nikola serve -b` 命令之后，`http://0.0.0.0:8000/ ` 显示拒绝访问，Windows 和 Mac 应该不存在这个问题。

解决方法是在 windows `C:\Users\Me` 目录下新建 `.wslconfig` 配置文件，并输入以下内容：

```Bash
[wsl2]
localhostForwarding=true
```

## 让 Nikola 支持 Jupyter Notebook

下面我们让 Nikola 支持 Jupyter Notebook，毕竟这是数据科学家的博客:)

首先我们需要在 `COMPILERS` 中定义 `ipynb` 文件。打开站点配置文件 `conf.py`，搜索 `COMPILERS`，如下定义 `ipynb` 文件：

```Python
COMPILERS = {                                                                               
    "rest": ['.rst', '.txt'],
    "markdown": ['.md', '.mdown', '.markdown'],
    "textile": ['.textile'],
    "txt2tags": ['.t2t'],
    "bbcode": ['.bb'],
    "wiki": ['.wiki'],
    "ipynb": ['.ipynb'],
    "html": ['.html', '.htm'],
    "php": ['.php'],
}
```

其次，我们需要在 `POSTS` 中定义 `.ipynb` 插件。编辑站点配置文件 `conf.py`，搜索 `POSTS`，如下定义 `.ipynb` 插件：

```Python
 POSTS = (                                                                              
     ("posts/*.rst", "posts", "post.tmpl"),
     ("posts/*.md", "posts", "post.tmpl"),
     ("posts/*.txt", "posts", "post.tmpl"),
     ("posts/*.html", "posts", "post.tmpl"),
     ("posts/*.ipynb", "posts", "post.tmpl"),
 )
```

使用 Jupyter Notebook 写博客与 markdown 类似，你可以在 posts 文件下新建 ipynb 文件，然后用 Jupyter Notebook 打开编辑。

我们可以使用字典向 Jupyter Notebook 中添加博客文章必需的元信息，方法为打开 Jupyter Notebook，菜单栏选择 _Edit -> Edit Notebook Metadata_，添加如下格式信息：

```json
{
  "nikola": {
    "title": "Example for Jupyter Notebook metadata configuration",
    "slug": "example-for-jupyter-notebook-metadata-configuration",
    "date": "2022-04-29 19:52:05 UTC"
  }
}
```

## markdown 支持

Nikola 默认使用 [python-markdown](https://python-markdown.github.io/reference/) 解析 markdown，你也可以选择使用 pandoc，这篇[博客](https://www.brainsorting.com/posts/create-a-blog-with-nikola/#using-markdown-for-your-post)讲的非常清楚。

另外，如果你喜欢使用 Pelican-style 风格添加博客元信息，需要添加 `markdown.extensions.meta` 插件。此外，你也可以使用 `markdown.extensions.toc` 插件自动解析文章目录。打开站点配置文件，编辑 markdown 插件配置选项：

```Python
 MARKDOWN_EXTENSIONS = [
     'markdown.extensions.meta',
     'markdown.extensions.fenced_code',
     'markdown.extensions.codehilite',
     'markdown.extensions.extra',
     'markdown.extensions.toc',  # 自动解析文章目录
 ]
```

## 数学公式支持

Nikola 默认使用 MathJax 显示数学公式，你可以使用 Katex。编辑站点配置文件，修改 `USE_KATEX=True`。Nikola 默认使用 `\(...\)` 渲染行内公式，使用 `\[...\]` 和 `$$...$$` 渲染行间公式。如果你习惯使用 `$...$` 渲染行内公式，需要修改配置文件，搜索 `KATEX_AUTO_RENDER` ，如下编辑：

```Python
KATEX_AUTO_RENDER = """
delimiters: [
    {left: "$$", right: "$$", display: true},
    {left: "\\\\[", right: "\\\\]", display: true},
    {left: "\\\\begin{equation*}", right: "\\\\end{equation*}", display: true},
    {left: "$", right: "$", display: false},
    {left: "\\\\(", right: "\\\\)", display: false}
]
"""
```

# 博客美化

相比于 Jekyll、Hugo 和 Hexo，Nikola 的不足是好看的主题比较少。官方提供了一些[主题](https://themes.getnikola.com/)，这里我们以 [bootstrap4](https://themes.getnikola.com/v8/bootstrap4/) 来演示。

## 更换主题

首先，我们需要下载主题。利用 `nikola theme -i bootstrap4` 命令下载主题。然后我们编辑站点配置文件 `conf.py`，搜索 `THEME`，将主题修改为 `bootstrap4`。

## 导航栏配置

我们可以通过修改 `THEME_CONFIG` 来修改导航栏配色。bootstrap4 导航栏默认是暗底，也可以自定义背景颜色，配置文件如下：

```Python
 THEME_CONFIG = {
      DEFAULT_LANG: {
          # Use a light navbar with dark text. Defaults to False.                                   
          'navbar_light': False,
          # Use a custom navbar color. If unset, 'navbar_light' sets text +
          # background color. If set, navbar_light controls only background
          # color. Supported values: bg-dark, bg-light, bg-primary, bg-secondary,
          # bg-success, bg-danger, bg-warning, bg-info, bg-white, bg-transparent.
          'navbar_custom_bg': '',
      }
 }
```

导航栏默认有博客归档、分类和 RSS 订阅栏目，我们可以通过修改 `NAVIGATION_LINKS` 来自定义导航栏目。其默认配置如下：

```Python
NAVIGATION_LINKS = {
    DEFAULT_LANG: (
        ("/archive.html", "Archive"),
        ("/categories/", "Tags"),
        ("/rss.xml", "RSS feed"),
    ),
}
```

这里 `/` 代表站点资源根目录，即 output 目录。我们可以通过指定资源目录，自定义导航栏。比如在 `categories/` 目录下，Nikola 生成了 `cat_nikola`、`cat_python` 等类别目录，我们可以指定这两个目录，新建一个多级 TECH 导航栏目。

```Python
NAVIGATION_LINKS = {
    DEFAULT_LANG: (
        ("/archive.html", "Archive"),
        ("/categories/", "Tags"),
        ("/rss.xml", "RSS feed"),
        (
          (
            ("/categories/cat_nikola/", "Nikola"),
            ("/categories/cat_python/", "Python")
          ),
          "TECH"
        ),
    ),
}
```

## 网页图标与 logo

首先我们进入博客根目录中的 files 目录，新建 assets 目录，再新建 img 目录，然后将网页图标 favicon 和 logo 文件拷贝到 img 目录中。`nikola build` 在生成静态文件时会将 files 文件下的资源都复制到 output 目录。

然后编辑站点配置文件 `conf.py` 搜索 `FAVICONS` 和 `LOGO`，如下配置：

```Python
FAVICONS = (
    ("icon", "/assets/img/favicon.ico", "16x16"),
)

LOGO_URL = '/assets/img/logo.jpg'
```

## 代码显示风格

Nikola 使用 [Pygments](https://pygments.org/) 进行语法高亮，你可以在 [Pygments styles](https://pygments.org/styles/) 选择自己喜欢的配色风格。我比较喜欢 `zenburn`，编辑站点配置文件 `conf.py` ，搜索 `CODE_COLOR_SCHEME` ，如下配置：

```Python
CODE_COLOR_SCHEME = 'zenburn'
```

## 目录美化

如果你使用了 `markdown.extensions.toc` 插件解析文章目录，你会发现这个目录比较丑。Nikola 使用 `post.tmpl` 模板文件来生成博客文章页面，我们可以修改这个模板文件，从而美化目录（这需要你懂一点前端和 Mako 模板引擎的知识:)

首先，我们将 `post.tmpl` 文件复制到博客根目录，命令行输入 `nikola theme -c post.tmpl`，该命令会将 `post.tmpl` 文件复制 templates 目录下，然后我们编辑这个文件。因为我们只是希望美化博客文章页面的目录，所以可以使用内部样式表，在 `<style>` 标签中定义样式。比如，我是这样美化的：

```CSS
@media screen and (min-width: 1024px) {
    .e-content {
        display: grid;
        grid-template-columns: 3fr 1fr;
        column-gap: 30px;
        position: relative;
    }

    .toc {
        grid-column: 2 / 3;
        grid-row: 1 / span 999;
        align-self: start;
        position: sticky;
        top: 20px;
    }
        
    .toc::before {
        content: "ON this page";
        background-color: #ffe70e;
        color: #444;
        font-size: 16px;
        font-weight: bold;
        font-style: italic;
        padding: 5px 5px;
        margin-left: 20px;
    }
}

@media screen and (max-width: 767px) {
    .e-content {
        display: grid;
        grid-template-columns: 1fr;
    }
            
    .toc {
        grid-column: 1 / 2;
    }
            
    .toc::before {
        content: "ON this page";
        background-color: #ffe70e;
        color: #444;
        font-size: 16px;
        font-weight: bold;
        font-style: italic;
        padding: 5px 5px;
        margin-left: 20px;
    }

}
```

## 定制样式

Nikola 支持定制样式，我们可以通过在 `files/assets/css/` 目录下，新建 `custom.css` 文件来定制全局字体，行距等样式。如果你觉得我的样式不错，也可以选择复制[我的](/listings/custom.css.html):)

## 个性化首页

Nikola 默认的首页是博客文章列表，并且是显示文章全部内容。我们可以通过修改配置文件 `INDEX_TEASERS=True`，然后在文章源文件中加入 `<!--- TEASER_END --->` 来选择显示部分内容。

首页默认显示 10 篇文章，我们可以通过编辑站点配置文件中的 `INDEX_DISPLAY_POST_COUNT` 来选择首页显示的文章数量。

此外，如果你希望定制首页，比如首页是一个 Greeting 页面，显示个人信息等等（像我这样:) 我强烈建议修改 `index.tmpl` 模板文件。如果你懂一点前端，可以在这里大显身手。使用命令 `nikola theme -c index.tmpl` 将模板文件复制到 templates 目录下，进行修改。

# 部署到 Github

- 在 Github 新建一个仓库，命名为 `[username].github.io`，username 就是你的 Github 账户名
- 在博客根目录 `git init` 创建版本仓库
- 添加远程仓库 `git remote add origin https://github.com/[username]/[username].github.io.git`
- 创建 `.gitignore` 文件

```Bash
cache
.doit.db*
__pycache__
output
.ipynb_checkpoints
.DS_Store
```

- 使用 `nikola github_deploy` 一键部署到 Github

解释一下 `nikola github_deploy`，这个[命令](https://getnikola.com/handbook.html#deploying-to-github)会创建一个 `src` 分支，用来保存博客目录的源文件，而 `master` 分支用来保存站点资源目录（即 output 目录）下的那些静态资源文件。这些配置也可以在站点配置文件 `conf.py` 中进行修改：

```Python
GITHUB_SOURCE_BRANCH = 'src'
GITHUB_DEPLOY_BRANCH = 'master'

# The name of the remote where you wish to push to, using github_deploy.
GITHUB_REMOTE_NAME = 'origin'

# Whether or not github_deploy should commit to the source branch automatically
# before deploying.
GITHUB_COMMIT_SOURCE = True
```

# 参考资料

- [The Nikola Handbook](https://getnikola.com/handbook.html#)
- https://randlow.github.io/posts/python/create-nikola-coding-blog/
- https://www.brainsorting.com/posts/create-a-blog-with-nikola/
- https://paulomarconi.github.io/blog/Nikola-guide/