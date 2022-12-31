---
slug: see-theory
date: 2020-04-19 20:41:53 UTC+08:00
tags: Probabilities 
category: Mathematics
link: 
description: 
type: text 
has_math: true
---

Here are some notes from [see-theory](https://seeing-theory.brown.edu/) on probability theory.

<!-- TEASER_END -->

[TOC]

# 1 Basic Probability

## Sample space

A **probabilistic experiment** has severval components. The **sample space** is the set of all possible **outcomes** in the experiment. We usually denote the sample space by $\Omega$ .

## Events

Collections of outcomes in the sample space $\Omega$ are called **events**.

## Probability measure

A **probability measure** P is a **function** that maps subsets of the **state space** $\Omega$ to numbers in the interval $[0,1]$ . 

The probabilities in a probabilistic experiment are not arbitrary, the must satisfy a set of rules or **axioms** :

- All probabilities must be nonnegative.
- The sum of the probabilisties of all the outcomes in $\Omega$ must be 1.
- The probability of an event is the sum of the probabilities of the outcomes it comprises.

## Independence

If two events A and B do not influence or give any information about the other, we say A and B are **independent**.

Let A and B both be subsets of our sample space $\Omega$. Then we say A and B are independent if 
$$
P(A \cap B)=P(A)P(B)
$$

## Expectation

The expected value, or **expectation** of X, denoted by $E(X)$, is defined to be 
$$
E(X) = \sum_{x \in X(\Omega)}{xP(X=x)}
$$

Properties of expectation:

- If X and Y are two random variables, then 
$$
E(X+Y) = E(X)+E(Y)
$$
- If X is a random variable and c is a constant, then 
$$
E(cX) = cE(X)
$$
- If X and Y are independent random variables, then 
$$
E(XY) = E(X)E(Y)
$$

## Variance

The variance of a random variable X is a nonnegative number that summarizes on average how much X differs from its mean, or expectation.

The variance of X, denoted by $Var(X)$ is defined to be 
$$
Var(X)=E[(x-EX)^2]
$$

Properties of variance:

- If X is a random variable with mean $EX$ and $c$ is a real number,
  - $Var(X) \ge 0$.
  - $Var(cX) = c^2Var(X)$.
  - $Var(X) = E(X^2)-E(X)^2$.
  - If $X$ and $Y$ are independent random variables, then 
  $$
  Var(X+Y) = Var(X) + Var(Y)
  $$

## Markov's Inequality

Suppose $X$ is a nonnegative random variable and $a$ is a positive constant. Then
$$
P(X \ge a) \le \frac{EX}{a}
$$

## Chebyschev's Inequality

Let $X$ be a random variable. Then
$$
P(|X-EX|\ge \epsilon) \le \frac{Var(X)}{\epsilon^2}
$$

切比雪夫不等式阐释了这样一个事实，随机变量大幅偏离期望的概率较小。

## Estimation

**Estimator** is a function or expression to **make inferences** about a population given data from a subset of that population.

### Consistency of Estimators

We say an estimator $\hat{p}$ is  a **consistent** estimator of $p$ if for any $\epsilon >0$, 
$$
lim_{n \to \infty}P(|\hat{p}-p|>\epsilon)=0.
$$

# 2 Compound Probability

## Set Theory

### Basic Definitions

A **set** is a collections of items, or elements, with no repeats. Usually we write a set $A$ using curly brackets and commas to distinguish elements, shown below
$$
A = \{a_0, a_1, a_2\}
$$
The size of the set $A$ is denoted $|A|$ and is called the **cardinality** of $A$. The **empty set** is denoted $\emptyset$.

### Intersection, Union and Complementation

- $A \cap B = \{x \in \Omega : x \in A \ and \  x \in B \}$
- $A \cup B = \{x \in \Omega : x \in A \ or \ x \in B \}$
- $A^c = \{x \in \Omega : x \notin A \}$

### Disjointness

For two sets to be disjoint, they must share no common elements. We say two sets $A$ and $B$ are **disjoint** if 
$$
A \cap B = \emptyset
$$

## Frequentist inference

Frequentist inference is the process of determining properties of an underlying distribution via the observation of data.

### Point Estimation

One of the main goals of statistics is to estimate unknown parameters. To approximate these parameters, we choose an estimator, which is simply any function of randomly sampled observations.

### Confidence Interval

In contrast to point estimators, confidence intervals estimate a parameter by specifying a range of possible values. Such an interval is associated with a confidence level, which is the probability that the procedure used to generate the interval will produce an interval containing the true parameter.

# Bayesian Inference

Bayesian inference techniques specify how one should update one’s beliefs upon observing data.

极大似然估计：模型已定，参数未知，采样独立同分布