---
tags:
  - CS188
  - "#Bayes_Nets"
  - "#Probability"
source: 6.3 Bayesian Network Representation
---
# 问题引入
在Note11中我们提及到了[联合分布](notes/CS188/Note/Note11.md#Joint%20Ditribution(%20联合分布%20)),我们先要想的就是一个问题：如果我们有n个变量，每个变量有d种取值，那联合概率表一共需要$d^n$行，这是一个非常庞大的数据量，这时候就引入了贝叶斯网络。贝叶斯网络通过利用条件概率的概念来避免这一个问题，它并非将信息存储在一个巨大的表格中，而是将概率分布分布在多个较小的条件概率表中，并且搭配一个有向无环图使用( Directed acyclic graph )简称为`DAG`
# Bayes Net
A **Bayes Net** is defined as:
- A **directed acyclic graph (DAG)** where each node represents a random variable.
- Each node has a **conditional probability table (CPT)** that stores:
    - The probability of the variable given its parents:$$
    \LARGE
        P(X∣Parents(X))
    $$
    - The CPT includes columns for each parent, the variable itself, and the probability.

> DAG体现了条件独立性假设，这张图能让我们对联合分布进行分解。需要注意的是，箭头并不代表两个随机变量之间存在着因果关系，它们只是表示着概率上有关联
## 联合概率计算公式
给定一个贝叶斯网络，所有变量的取值组合的联合概率为：
$$
\LARGE
\begin{align*}
P(X_1,X_2,\dots,X_n) &= \prod_{i=1}^{n} P\bigl(X_i \mid \operatorname{Parents}(X_i)\bigr)
\end{align*}
$$
## Bayes Net实例
Variables (all binary):
- **B**: Burglary occurs
- **E**: Earthquake occurs
- **A**: Alarm goes off
- **J**： John calls
- **M**: Mary calls
DAG：
![[notes/CS188/static/5ef361bb6748b0402068a2e85b4d6f95.png]]
根据联合概率计算公式，我们可以得知
$$
\large
\begin{align*}
P(-b,-e,+a,+j,-m) &= P(-b)\cdot P(-e)\cdot P(+a\mid -b,-e)\cdot P(+j\mid +a)\cdot P(-m\mid +a)
\end{align*}
$$
总的来说，一个好的模型可能无法涵盖所有的变量，甚至无法涵盖变量之间的所有相互作用。但是
通过在图的结构中做出假设性设定，我们能够开发出极其高效的推理技术，这些技术往往比诸如枚举推理之类的简单方法更具实际应用价值。