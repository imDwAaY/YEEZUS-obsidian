---
tags:
  - CS188
  - Markov_Decision_Peocesses
  - MDPs
  - "#Policy_Iteration"
  - "#Value_Iteration"
source: "Note18(MDPs: Dynamic Programming (Cam))"
---
开始上强度了，Note8主要是在讲解MDP问题的解决方法，所以说要记住这个Note8围绕的是求解[policy(状态到动作的映射)](Note7.md#策略(%20Policy%20)与目标)
# Value Iteration
## 初步思路框架
首先想到的第一个方法就是评估每个状态的utility,之后用[Bellman方程](Note7.md#Bellman方程)来求解Q*( s, a )，即最优Q值，在状态 s **执行动作 a**后，再按最优策略能获得的期望折扣总奖励。最优Q值里面就带有了动作信息，从而求出最佳policy
$$
\LARGE
\begin{align*}
Q^{*}(s,a) &= \sum_{s'} T(s,a,s')\big[\,R(s,a,s') + \gamma\,U^{*}(s')\,\big]
\end{align*}
$$
一定要注意的是，Bellman方程的适用范围只有最优解即带有* 的变量
## 实现过程
在这个过程之中，每个状态的utility是通过动态规划的思想逐步更新的，直到收敛到最优值**U*(s)**
在进行公式表达之前，需要定义$\begin{align*}U_{k}(s)\end{align*}$为从状态s出发，走k布所能获得的效用值
- 初始设定：$\begin{align*}U_{0}(s)\end{align*}$ = 0,因为走0步不能或者任何奖励
- 迭代规则：
$$
\LARGE
\begin{align*}
U_{k+1}(s) &\leftarrow \max_a \sum_{s'} T(s,a,s')\big[R(s,a,s') + \gamma\, U_k(s')\big]
\end{align*}
$$
证明值迭代最终会收敛的过程省略，在原Note中有详细证明过程
## Value Iteration示例
![[image.OVUXI3.png]]
折扣因子γ = 0.5，最开始的初始状态所有状态的都是$\begin{align*}U_{0}(s)\end{align*}$ = 0，所以可以得到下面的表格

|       | cool | warm | overheated |
| ----- | ---- | ---- | ---------- |
| $U_0$ | 0    | 0    | 0          |
第一轮迭代计算如下
$$
\large
\begin{align*}
U_1(\text{cool}) &= \max\{1\cdot[1+0.5\cdot 0],\;0.5\cdot[2+0.5\cdot 0]+0.5\cdot[2+0.5\cdot 0]\} \\
&= \max\{1,2\} \\
&= \boxed{2} \\[6pt]
U_1(\text{warm}) &= \max\{0.5\cdot[1+0.5\cdot 0]+0.5\cdot[1+0.5\cdot 0],\;1\cdot[-10+0.5\cdot 0]\} \\
&= \max\{1,-10\} \\
&= \boxed{1} \\[6pt]
U_1(\text{overheated}) &= \max\{\} \\
&= \boxed{0}
\end{align*}
$$

|       | cool | warm | overheated |
| ----- | ---- | ---- | ---------- |
| $U_0$ | 0    | 0    | 0          |
| $U_1$ | 2    | 1    | 0          |
再进行下一轮的时候和这一轮一模一样
$$
\large
\begin{align*}
U_2(\text{cool}) \; &=\; \max\{1\cdot[1+0.5\cdot2],\;0.5\cdot[2+0.5\cdot2]+0.5\cdot[2+0.5\cdot1]\} \\
&=\; \max\{2,\;2.75\} \\
&=\; \boxed{2.75} \\[6pt]
U_2(\text{warm}) \; &=\; \max\{0.5\cdot[1+0.5\cdot2]+0.5\cdot[1+0.5\cdot1],\;1\cdot[-10+0.5\cdot0]\} \\
&=\; \max\{1.75,\,-10\} \\
&=\; \boxed{1.75} \\[6pt]
U_2(\text{overheated}) \; &=\; \max\{\} \\
&=\; \boxed{0}
\end{align*}
$$

|       | cool | warm | overheated |
| ----- | ---- | ---- | ---------- |
| $U_0$ | 0    | 0    | 0          |
| $U_1$ | 2    | 1    | 0          |
| $U_2$ | 2.75 | 1.75 | 0          |

<span class="bold darkred-text large">这里对于公式里折扣的那一部分一定要理解清楚，再观察一遍迭代公式</span>
$$
\LARGE
\begin{align*}
U_{k+1}(s) &\leftarrow \max_a \sum_{s'} T(s,a,s')\big[R(s,a,s') + \gamma\, U_k(s')\big]
\end{align*}
$$
其中$\begin{align*}U_{k}(s')\end{align*}$ 这一部分并不是发生在$\begin{align*}U_{k+1}(s)\end{align*}$前面的，可以根据状态变化看出来，s采取动作a变成了状态s'，在状态s时还有k+1步未走，到达状态s’后剩余k步，这里动态规划复用的是$\begin{align*}U_{k}(s')\end{align*}$ 来表明下一时刻的未来价值。
举个例子来说，在算$\begin{align*}U_{2}(cool)\end{align*}$的时候，假设采取的动作的是slow,$\begin{align*}U_{1}(cool)\end{align*}$表示的是站在$\begin{align*}U_{2}(cool)\end{align*}$的角度，下一步又回到了cool,从那一刻开始你还能再拿到的最佳期望收益，所以说$\begin{align*}U_{1}\end{align*}$不是已经发生的收益，而是未来的收益。我最开始只看例子误解了公式，因为折扣因子是和$\begin{align*}U_{1}(cool)\end{align*}$相乘的，让我误以为原本意图是给过去的效用上折扣，实际上不是
- --
# Policy Extraction
这一步就到了我在value iteration中提及到的求完Q*( s, a )后提取最优策略既$\begin{align*}\pi^*(s)\end{align*}$，下面是公式
$$
\Large
\begin{align*}
\pi^*(s) &= \arg\max_a Q^*(s,a)= \arg\max_a \sum_{s'} T(s,a,s')\big[ R(s,a,s') + \gamma U^*(s') \big]
\end{align*}
$$
原文中的一句话值得斟酌一下，揭露了MDP与expectimax搜索树之间的关系，概率分支的出现正是因为MDP的随机环境，在ecpectimax里面可以用机会节点来表示
```text
Storing only each U ∗ (s) means that we must recompute all necessary Q-values with the Bellman equation before applying argmax, equivalent to performing a depth-1 expectimax.
```
上述内容可以用下面的树来表达
```text
  Expectimax搜索树
        s
       / \
   slow   fast        ← MAX（选动作）
     |       |
   chance  chance     ← 概率分支
     |       |
    s'      s'
```
---
# Q-Value Iteration
这里就提及到了另外一种更直接地解决MDP问题的方法，就是不再计算状态的效用值了，直接来计算Q( s, a ),这样就直接用包含策略信息的Q值来求得policy,基本迭代思路还是和之前的大差不差
$$
\LARGE
\begin{align*}
Q_{k+1}(s,a) &\leftarrow \sum_{s'} T(s,a,s')\big[ R(s,a,s') + \gamma \max_{a'} Q_k(s',a') \big]
\end{align*}
$$
Q值迭代到最后也一定是收敛的，和Value Iteration的证明方法几乎一样。实际上，只要折扣因子
γ < 1, 那么iteration的结果到最后就会收敛。更新完Q*( s, a )后，直接用公式提取最优策略
$$
\LARGE
\begin{align*}
\pi^*(s) &= \arg\max_{a} Q^*(s,a)
\end{align*}
$$
---
# Policy Iteration
## 问题引入
引入Policy Iteration的问题就是，如果用value iteration,其时间复杂度过高。value iteration共有三层循环，对每个状态 |S|, 对每个动作 |A|, 对每个下一状态 |S′|, 综合在一起时间复杂度就是$\begin{align*}O\big(|S|^2|A|\big)\end{align*}$
所以说为了避免大量的功夫浪费在value iteration的不断数值计算上，就着重于策略的改进
## 核心思想
```text
固定一个策略 → 算这个策略的真实价值 → 用这个价值改进策略 → 重复直到策略不发生变化
```
## 实现过程
首先需要回顾一下Value Iteration中U的角标的含义，在这里$\begin{align*}U^{\pi}_{k}(s)\end{align*}$表示的是从状态s出发，一直采用策略${\pi}$走k步所能获得的效用值。在实现之前需要我们定义一个最初的policy,此时我们公式内容就不需要max了。核心公式如下
$$
\LARGE
\begin{align*}
U^{\pi}(s) &= \sum_{s'} T\bigl(s,\pi(s),s'\bigr)\bigl[ R\bigl(s,\pi(s),s'\bigr) + \gamma\, U^{\pi}(s') \bigr]
\end{align*}
$$
从本质上来说，这是一个方程组，因为每个状态包含一个未知数$U^{\pi}(s)$, 每个状态都只有一个等式，一共有s个方程，所以说可以一次性解出来所有的值。解出来真实价值之后，我们就到了第三步，就是用这个价值来改进策略，策略改进的公式如下
$$
\LARGE
\begin{align*}
\pi_{i+1}(s) &= \arg\max_{a} \sum_{s'} T(s,a,s')\big[ R(s,a,s') + \gamma\, U^{\pi_i}(s') \big]
\end{align*}
$$
如何来判断当前policy是不是最好呢？
$$
\large
\begin{align*}
\text{If }\pi_{i+1}=\pi_i,\ \text{the algorithm has converged, and we can conclude that }\pi_{i+1}=\pi_i=\pi^*.
\end{align*}
$$
## Policy Iteration示例
![[image.OVUXI3.png]]
依旧是汽车这个图，首先初始化policy为总是slow

|           | cool | warm | overheated |
| --------- | ---- | ---- | ---------- |
| ${\pi}_0$ | slow | slow | -          |
我们进行第二部计算策略真实价值，套用公式可以得到方程组
$$
\Large
\begin{align*}
U^{\pi_0}(\text{cool}) &= 1 \cdot [1 + 0.5 \cdot U^{\pi_0}(\text{cool})] \\
U^{\pi_0}(\text{warm}) &= 0.5 \cdot [1 + 0.5 \cdot U^{\pi_0}(\text{cool})] + 0.5 \cdot [1 + 0.5 \cdot U^{\pi_0}(\text{warm})]
\end{align*}
$$
解出结果可以得到策略真实价值

|             | cool | warm | overheated |
| ----------- | ---- | ---- | ---------- |
| $U^{\pi_0}$ | 2    | 2    | 0          |
然后进行第三步，用价值改变策略
$$
\begin{align*}
\pi_1(\text{cool}) &= \arg\max\{\ \text{slow}:1\cdot[1+0.5\cdot2],\ \text{fast}:0.5\cdot[2+0.5\cdot2]+0.5\cdot[2+0.5\cdot2]\ \}\\
&= \arg\max\{\ \text{slow}:2,\ \text{fast}:3\ \}\\
&= \boxed{\text{fast}}\\[6pt]
\pi_1(\text{warm}) &= \arg\max\{\ \text{slow}:0.5\cdot[1+0.5\cdot2]+0.5\cdot[1+0.5\cdot2],\ \text{fast}:1\cdot[-10+0.5\cdot0]\ \}\\
&= \arg\max\{\ \text{slow}:3,\ \text{fast}:-10\ \}\\
&= \boxed{\text{slow}}
\end{align*}
$$
重复上述步骤最终可以得到Policy最终收敛，迭代完毕

|           | cool | warm |
| --------- | ---- | ---- |
| ${\pi_0}$ | slow | slow |
| ${\pi_1}$ | fast | slow |
| ${\pi_2}$ | fast | slow |
