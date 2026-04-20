---
tags:
  - CS188
  - Q-Learning
  - "#Approximate_Q-Learning"
  - Reinforcement_Learning
  - "#Exploration_And_Exploitation"
source: "Note24(RL: Reinforcement Learning I (Cam))  Note25(RL: Reinforcement Learning II (Cam))"
---

# Approximate Q-learning
Q-learning虽然很有优势，但是缺乏了泛化能力。当pacman学习了`figure1`中的困境后，智能体是不会意识到`figure2,figure3`中的情景和`figure1`中的困境基本一样

![[notes/CS188/static/image.H1GYK3.png| 160]]![[notes/CS188/static/image.GJQWK3 1.png| 160]]![[notes/CS188/static/image.0WC4K3.png| 160]]

所以说`Q-Learning`很有局限性，这时候该算法就不再记下具体状态，而是记住状态特征，将状态表示为特征向量，比如pacman的特征向量就可以编码为
-  离最近ghost的距离
-  离最近food的距离
-  ghost的数量
-  pacman是否被困住了？0 or 1
Q函数建模为特征的线性组合：
$$
\LARGE
\begin{align*}
Q(s,a) &= w_1 f_1(s,a) + w_2 f_2(s,a) + \cdots + w_n f_n(s,a) = \vec{w}\cdot\vec{f}(s,a)
\end{align*}
$$
每一步需要计算`difference`,并且更新权重
$$
\LARGE
\begin{align*}
\text{difference} &= \big[ R(s,a,s') + \gamma \max_{a'} Q(s',a') \big] - Q(s,a)
\end{align*}
$$
$$
\LARGE
\begin{align*}
w_i &\leftarrow w_i + \alpha \cdot \mathrm{difference} \cdot f_i(s,a)
\end{align*}
$$
这样一来，我们的内存使用效率就极高，泛化能力也具备了。在这个过程中，相似状态会得到相似的Q值，即使没有被访问过得状态也能合理估计
# Exploration vs. Exploitation
在强化学习中，智能体（agent）需要在以下两者之间做出权衡：
- **Exploitation（利用）**：按照当前已知的最优策略行动，以最大化即时奖励。
- **Exploration（探索）**：尝试未知的动作，以发现可能更优的策略，从而获得长期收益。
如果只利用不探索，可能陷入局部最优；如果只探索不利用，则无法积累有效经验。因此，如何在两者之间取得平衡是强化学习的核心问题之一

# ε-Greedy Policies
一种很基础来强迫智能体做出`Exploration`的方法，给定一个0 < ε < 1
- 有 ε 的概率随机选择动作( Exploration )
- 有1- ε 的概率来选择当前最优动作( Exploitation )
非常的简单且有效，但是缺点也十分明显，在已经学习到最佳动作后仍然有很大的概率来做出随机行为。但是如果ε太小了的话，又会导致探索不足，学习速度过慢。一种简单解决问题的办法就是使ε随时间衰减
# Exploration Functions
这是一种更智能的选择，这种方式通过在Q值更新中引入"探索奖励"，Q值迭代表达式更新变为
$$
\LARGE
\begin{align*}
Q(s,a) &\leftarrow (1-\alpha)Q(s,a) + \alpha\big[ R(s,a,s') + \gamma \max_{a'} f(s',a') \big]
\end{align*}
$$
其中f( s, a )为探索函数，常见形式为
$$
\LARGE
\begin{align*}
f(s,a) &= Q(s,a) + \frac{k}{N(s,a)}
\end{align*}
$$
其中N( s, a )表示状态-动作对( s, a )被访问的次数。k表示偏好系数，即控制探索( Exploration )的强度
# RL Summary
## Model-based Learning（基于模型的学习）
在Note9中有详细介绍，[快速回顾](notes/CS188/Note/Note9.md#Model-Based%20Learning)
- 先估计环境的转移函数T和奖励函数R
- 再用这些估计值进行规划（如 [Value Iteration](notes/CS188/Note/Note8.md#Value%20Iteration) / [Policy Iteration](notes/CS188/Note/Note8.md#Policy%20Iteration)）
## Model-free Learning（无模型学习）
在Note9中有详细介绍，[快速回顾](notes/CS188/Note/Note9.md#Model-Free%20Learning)
- 不显式估计 TT 和 RR，直接学习值函数或策略

| 方法                                             | 描述                 | 特点                     |
| ---------------------------------------------- | ------------------ | ---------------------- |
| **Direct Evaluation**                          | 根据策略$π$统计每个状态的累计奖励 | 简单但收敛慢，忽略状态间转移信息       |
| **Temporal Difference Learning (TD Learning)** | 用指数移动平均更新值函数       | 在线学习，收敛更快，适合 on-policy |
| **Q-Learning**                                 | 用 Q 值迭代直接学习最优策略    | Off-policy，可容忍次优行为     |
| **Approximate Q-Learning**                     | 用特征表示状态，泛化能力强      | 适合大规模状态空间              |
## On-policy vs. Off-policy

| 类型             | 定义                | 例子                             |
| -------------- | ----------------- | ------------------------------ |
| **On-policy**  | 学习当前策略下的值函数       | Direct Evaluation, TD Learning |
| **Off-policy** | 学习最优策略，即使当前行为是次优的 | Q-Learning                     |
## Regret
还有一个重要概念叫做Regret，我们至今不知道如何评判一个智能体强化学习性能的好坏，无法评判智能体学习到了哪一步，不知道智能体在`Exploration vs. Exploitation`之间取舍是否理智，我们就引入了Regret
$$
\LARGE
Regret=最优策略累计奖励−算法实际累计奖励
$$
低 regret 表示算法在早期也能做出较好的决策
