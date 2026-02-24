---
tags:
  - CS188
  - "#Expectimax"
---
# Expectimax
- 问题：当对手**不是总是最优**、或者游戏包含**随机性(dice/cards)** 时，[Minimax](CS188/Note/Note5.md#Minimax) 太悲观。
- 想法：把“最小化节点”换成“**chance nodes（随机节点）**”，用**期望值**代替最小值。
**[Markov decision processes](CS188/Note/Note7.md#Markov%20decision%20processes)** 将有更详细的讨论具有内在随机性的内容
## Defination
$$
\Large
\begin{aligned}
&\forall\ \text{agent-controlled states}: && V(s)=\max_{s'\in\text{successors}(s)}V(s')\\
&\forall\ \text{chance states}: && V(s)=\sum_{s'\in\text{successors}(s)} p(s'\mid s)\,V(s')\\
&\forall\ \text{terminal states}: && V(s)=\text{known}
\end{aligned}
$$
## 伪代码
![[image.MYAIH3.png]]
## Example
![[image.OCQJH3.png]]
## Important Truth!
```text
As a final note on expectimax, it’s important to realize that, in general, it’s necessary to look at all the children of chance nodes – we can’t prune in the same way that we could for minimax.
```
Expectimax 一般**不能像 minimax 那样做 α-β 剪枝**（因为必须看所有子节点来计算期望，除非知道节点值的上下界）。
- - - 
# General games/Multi-agent utilities
- 并非所有游戏都是零和（zero-sum）。在多智能体情形，每个 agent 有自己的效用（utility tuple）。
- 每个 agent 在自己控制节点上**最大化自己的分量**，忽略别人的效用。最终根节点返回一个效用元组（例如 `(5,2,5)`）。这种设置会自然产生“合作/折中”行为。
![[image.M34GH3.png]]
- 上图最终返回一个效用元组(5,2,5)，具有多智能体效用的的博弈(General games with multi-agent utilities)是一个**behaviour through computatiaon**的一个很好的例子
#通过计算产生行为 
- - -
# Monte Carlo Tree Search
## 核心思想
- Evaluation by rollouts: From state s play many times using a policy (e.g. random) and count wins/losses. 统计胜率来估计该状态价值
- Selective search: explore parts of the tree, without constraints on the horizon, that will improve decision at the root.把计算资源集中在"有前途"或者"不确定"的分支上，而不是平均分
## UCB1(上置信界)准则
$$
\Large
\begin{align*}
\mathrm{UCB1}(n) &= \frac{U(n)}{N(n)} + C \times \sqrt{\frac{\log N(\mathrm{PARENT}(n))}{N(n)}}
\end{align*}
$$
- N(n)：从子节点 n 做过多少次 rollout（样本数）。
- U(n)：对于 Parent(n) 的赢的总次数（或者累积获利）。
- 第一项：当前估计（exploitation）。第二项：不确定性（exploration）。C 控制两者权重。
## UCT算法步骤
```text
1. The UCB criterion is used to move down the layers of a tree from the root node until an unexpanded leaf node is reached. 
2. A new child is added to that leaf, and we run a rollout from that child to determine the number of wins from that node. 
3. We update the numbers of wins from the child back up to the root node.
```
- **1.Selection**: 从根开始按 UCB 走下去，直到到达尚未展开的叶子节点
- **2.Expansion + Rollout**: 在该叶子扩展一个新子节点，然后从这个新子节点执行一次或多次 rollout（用某策略玩到底），记录输赢
- **3.Backpropagation**: 把 rollout 的结果沿路径回传，更新每个节点的 N 与 U
重复上述步骤很多次，最终选择访问次数N最大的子节点对应的动作
### 注意
```text
Note that because UCT inherently explores more promising children a higher number of times, as N → ∞, UCT approaches the behavior of a minimax agent.
```
随着样本数趋近无穷，UCT 的行为会逼近 minimax（因为更有前途的子树被反复探索）
- - -
# Summary
- **Minimax**：当对手**完全最优**时适用，可用 α-β 剪枝加速；策略保守（worst-case）
- **Expectimax**：当对手**随机或次优**时用概率加权平均，结果更“平均化”；通常无法像 minimax 那样剪枝
- **MCTS / UCT**：当**分支因子极大**或没有明确定义的启发评估函数时，用随机模拟 + 选择性扩展来估计最优动作；易并行化