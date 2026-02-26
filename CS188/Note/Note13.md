---
tags:
  - CS188
  - "#D_Separation"
  - "#Causal_Chain"
  - "#Common_Cause"
  - "#Common_Effect"
  - "#Active_Triples"
  - "#Inactive_Triples"
source: 6.5 D-Separation
---

# D-Separation
**D-separation** 是贝叶斯网络中的一个概念，用于**通过图结构([DAG](CS188/Note/Note12#Bayes%20Net))判断随机变量之间的条件独立性**
首先需要回顾一下的是：在图中，只要给定了某个节点的所有父节点，那么该节点就与其所有祖先节点在逻辑上是相互独立的
```text
A node is conditionally independent of all its ancestor nodes in the
graph given all of its parents.
```
## Causal Chain( 因果链 )
- 没有被给定：
![[image.A7DLL3.png | 500]]
这时X和Z不是独立的，因为信息可以沿着链来传递
- 给定Y：
![[image.SHOKL3.png | 500]]
这时候X和Z关于Y**条件独立**(X⊥⊥Z∣Y)，这时候就用到了最开始提到的定理，只要给定了某个节点的所有父节点，那么该节点就与其所有祖先节点在逻辑上是相互独立的，此时X和Z是独立的
也可以通过公式来证明：
HINT: 记得回顾一下[链式法则](CS188/Note/Note11#Chain%20Rule(%20链式法则%20))还有[独立性](CS188/Note/Note11#Independence(%20独立性%20))
$$
\large
\begin{align*}
P(X\mid Z,y) &= \frac{P(X,Z,y)}{P(Z,y)} 
= \frac{P(Z\mid y)P(y\mid X)P(X)}{\sum_x P(x,y,Z)} 
= \frac{P(Z\mid y)P(y\mid X)P(X)}{P(Z\mid y)\sum_x P(y\mid x)P(x)} \\
&= \frac{P(y\mid X)P(X)}{\sum_x P(y\mid x)P(x)} 
= P(X\mid y)
\end{align*}
$$

## Common Cause( 共同原因 )
- 没有被给定：
![[image.H4APL3.png | 300]]
X，Z**不是独立的**，因为他们共同受到了Y的影响。
- 给定Y：
![[image.UQ4TL3.png | 300]]
X 和 Z 关于 Y **条件独立** (X⊥⊥Z∣Y)。知道 Y 之后，X 和 Z 之间的关联被解释，再无其他联系，同样可以通过公式来证明：
$$
\LARGE
\begin{align*}
P(X\mid Z,y) &= \frac{P(X,Z,y)}{P(Z,y)}
= \frac{P(X\mid y)P(Z\mid y)P(y)}{P(Z\mid y)P(y)}
= P(X\mid y)
\end{align*}
$$
## Common Effect
- 没有被给定:
![[image.ZE8VL3.png | 300]]
X⊥⊥Z，没有任何给定，没有理由认为两个无关的原因有关联
- 给定Y：
![[image.H07ML3.png | 300]]
X和Z不独立，X和Z会对Y产生的原因产生`explaining away( 解释竞争 )`。
- - -
# D-Seperation判定算法
给定贝叶斯网络 G，节点 X和 Y，以及观测节点集合 Z={$Z_1$,…,$Z_k$}，要判断 X⊥⁣⊥Y∣Z是否**保证成立**（即 D-separate），步骤如下:
1. **阴影化观测节点**：在图中将Z 中的所有节点涂灰（代表它们已被观测）
2. **枚举 X 到 Y 的所有无向路径**：忽略箭头的方向，找出所有从 X 到 Y 的路径（节点不重复即可，不要担心循环，但通常考虑简单路径）
3.      - 将路径分解为连续的三节点片段。
	- 检查每个三节点片段是否是**活跃的**（根据上述规则）。
	- 如果**所有**片段都是活跃的，则该路径是活跃的（active path），它 **D-connects** X 和 Y，意味着 X 和 Y **不一定条件独立**。
4. **结论**:
    - 如果 **不存在任何活跃路径**，则 X⊥⊥Y∣Z被保证成立（D-separated）。
    - 如果 **存在至少一条活跃路径**，则不能保证条件独立（可能依赖，也可能不依赖，取决于具体概率值）。

> 主要需要留意的是：如果只有一条路径，这条路径上只要有一个三元组是`Inactive Triples`,那么这条路径就是Inactive的，条件一定是独立的。
> 如果有多条路径，只要有一条路径是Active,即便其它路径都是Inactive,也就是说不能忽略Active路径展示的相关性，不能证明条件是独立的
- - -
# Active triples
![[image.NI0UL3.png]]
- - -
# Inactive triples
![[image.FLEJL3.png]]
- - -
# Example
![[image.9IFPL3.png]]
![[Pasted image 20260227003932.png]]



