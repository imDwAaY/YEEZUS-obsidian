---
tags:
  - CS188
  - "#Sampling"
  - "#Approximate_Inference"
source: "6.7( Approximate Inference in Bayes Nets: Sampling ) - 6.8( Summary )"
---
#  问题引入
我们在Note14中提及到了两种解决计算条件概率$\begin{align*}&P\big(Q_1 \ldots Q_k \mid e_1 \ldots e_k\big)\end{align*}$的方法,分别是[Inference by Enumeration](CS188/Note/Note14#Inference)和[Variable Elimination](CS188/Note/Note14#Variable%20Elimination),这两种方法我们叫做精确推理，在面临网格结构复杂还有变量众多的情况下，其计算量会变得巨大。所以说我们就引入了一种近似推理的方法--**Sampling**，通过牺牲精度来换效率
# Prior Sampling
这个方法是在通过拓扑顺序来依次在CPT中随机抽样，进而生成一个完整样本。再之后不断重复这个过程，出现大量样本后，某个事件出现的频率会收敛至它出现的真实频率.每个样本 (x₁, x₂, ..., xₙ) 被抽中的概率正是网络的联合概率 P(x₁, x₂, ..., xₙ)，因为生成过程就是按照联合概率的分解[（Chain rule）](CS188/Note/Note11#Chain%20Rule(%20链式法则%20))依次采样。
它的缺点也很明显，在面临计算条件概率的问题时，会浪费大量的样本，进而导致效率十分低下
## Python实现
![[截屏2026-03-02 21.39.48.png|231]]
```python
import random
def get_t():
	if random.random() < 0.99:
		return True
	return False
def get_c(t):
	if t and random.random() < 0.95:
		return True
	return False
def get_sample():
	t = get_t()
	c = get_c(t)
	return [t, c]
```
# Rejection Sampling
这个方法相比Prior Sampling就改进了一点，就是在发现某个变量的取值和
```
