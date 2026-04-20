---
tags:
  - CS188
  - "#Genetic_Algorithms"
  - "#Local_Search"
---
## Local Search
### Local Search的定义

- 局部搜索把“状态”定义为**一个完整的候选解（complete solution）**，不关心如何一步步到达这个解（path），而只关心最终的目标是否满足或目标函数的值是否最优。常用于约束满足问题（CSP）或优化问题（maximize/minimize objective）。
- 直观：从当前解出发，只在其邻域里寻找更好的解，直到达到某种停止条件（例如局部最优）。
![[notes/CS188/static/image.AQ9JH3.png]]
### Local Search覆盖的算法

- Hill-Climbing
- Simulated Annealing（模拟退火）
- Local Beam Search（局部光束搜索）
- Genetic Algorithms（遗传算法）
## Hill-Climbing
### 要点
- 每一步选择使目标函数（objective）增幅最大的邻居；
- 不保存搜索树，仅保存当前状态和当前值
- 容易陷入局部最优陷阱( local maxima ( see figure 4.1 ) )
### 伪代码实现
![[notes/CS188/static/image.JO6BH3.png| 550]]
### Variants(变体)
- Stochastic hill-climbing: randomly choose among uphill moves.
- Random sideways moves: allow non-improving moves occasionally.
- Random-restart hill-climbing: run many restarts from random starts and keep the best result.
**Hill Climbing是不完整的，但是Random-restart hill-climbing是完整的，因为随机选择的初始状态可以在某一点收敛到全局最大值。**

## Simulated Annealing Search(模拟退火)
### 要点
- 结合了**random walk**和**hill-climbing**来获得一个完整的和高效的算法
- 遇到higher objective value就接受，遇到smaller objective value有可能接受
- If temperature decreases slowly enough (theoretically), SA converges to global optimum with probability → 1.理论上，如果温度下降得足够慢，模拟退火算法将以接近1的概率达到全局最大值。
- **理论上的收敛性声明是关于"会被访问到"而不是”一直会被保留在当前状态“。所以要把"访问到"变成"保留"，就需要记录历史最优**
### 伪代码实现
![[notes/CS188/static/image.QT5FH3.png]]
## Local Beam Search
### 要点
- 是[HIll-climbing](notes/CS188/Note/Note4.md#Hill-Climbing)的variant(变体)
- 维护着k个并行状态(threads / beam width = k)
- 并不只是k个hill-climbing算法的副本，每一步都会在当前所有线程的所有successor state中选出k个最好的来作为下一代
- **每个thread线程信息共享，有着更高值的线程可以吸引其它线程向该区域探索**
### Variant
- Stochastic beam search可以避免Local Beam Search陷入局部最优陷阱( local maxima ( see figure 4.1 ) )

## Genetic Algorithms(GA)
### 要点
- 维护一个 population（大小 k），individuals(状态state) 用字符串来编码(finite alphabet)
### 伪代码实现
![[notes/CS188/static/image.UZC9G3.png| 720]]
### 实例(8-Queen)
#### 要点
- Representation: an array of length 8 where position i gives the row of the queen in column i (values 1..8).
- Fitness: number of non-attacking pairs (higher is better). Equivalent: maximize `C(8,2) - #conflicts`.
- GA process: select parents by fitness, crossover at random cut, mutate by randomly changing a gene.
![[notes/CS188/static/image.GZHEH3.png]]
**Why GA works well**: crossover can combine independently-evolved good substructures (building blocks) to produce better individuals.
The probability of choosing a state to “reproduce" is **proportional(正比)** to the value of that state.  We proceed to select pairs of states to reproduce by sampling from these probabilities (column (c) in Fig. 4.6). 
![[notes/CS188/static/image.UST4G3.png]]
#### Q1:Mutation 是不是“随机突变”？

**mutation 本质上就是随机突变**。  

> 它相当于给搜索过程加了一个“全局探索的噪声”，确保任何位置都有非零概率被探索到，避免搜索空间某些区域永远无法访问。

如果没有 mutation，整个算法最终会退化成一个“确定性的局部搜索”，甚至会比 hill-climbing 更容易陷入局部最优。
#### Q2:为什么Mutation不添加判断条件？

**不能。只要在 mutation 中加入“判断依据”，它就不再是 mutation，而变成了 hill-climbing / local search。**
- 带判断条件的mutation会让population让种群朝同一方向"收缩", 最终**过早收敛**，更容易陷入局部最优陷阱( local maxima ( see figure 4.1 ) )
- GA本质上是一种**启发式随机优化方法**，它的有效性依赖于
	- Crossover提供主要优化
	- Mutation提供少量探索

