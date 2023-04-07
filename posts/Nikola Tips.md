---
title: Nikola Tips
slug: nikola-tips
date: 2023-03-16 13:12
tags: Nikola, Blog
category: TECH
link:
description: Nikola 博客使用的一些技巧
type: text
status: draft
---

# 1 使用 Katex 渲染数学公式
- 使用 Katex 渲染公式，需要在博客 metadata 里添加 `has_math = true`
- 使用 Katex 渲染行间公式时，如果要换行，使用 `\\\`，而不是 `\\`
- 排列方程组可以使用 `aligned`，使用 `align` 会报错，示意如下：
```latex
\begin{aligned}
P(A/B) &= \frac{P(AB)}{P(B)} \\\
P(A/C) &= \frac{P(AC)}{P(C)} 
\end{aligned}
```
