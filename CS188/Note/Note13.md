# D-Separation
**D-separation** 是贝叶斯网络中的一个概念，用于**通过图结构判断随机变量之间的条件独立性**
首先需要回顾一下的是：在图中，只要给定了某个节点的所有父节点，那么该节点就与其所有祖先节点在逻辑上是相互独立的
```text
A node is conditionally independent of all its ancestor nodes in the
graph given all of its parents.
```
## Causal Chain( 因果链 )
- 没有被给定：
![[image.A7DLL3.png]]
这时X和Z不是独立的，因为信息可以沿着链来传递
- 给定Y：
![[image.SHOKL3.png]]
这时候X和Z关于Y**条件独立**(X⊥⊥Z∣Y)，这时候就用到了最开始提到的定理，只要给定了某个节点的所有父节点，那么该节点就与其所有祖先节点在逻辑上是相互独立的，此时X和Z是独立的
也可以通过公式来证明：
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

