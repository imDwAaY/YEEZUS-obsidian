---
tags:
  - CS188
  - "#Utilities"
  - "#Decision_Networks"
  - "#VPI"
source: 7.1( Utilities ) - 7.3 ( The Value of Perfect Information )
---
本次Note因为比CS188 2018Fall上课讲授内容增添了很多新内容，所以会比较详细一些。同时将[Bayes Net](CS188/Note/Note12#Bayes%20Net)和我们之前所学知识正式结合起来，有种受益匪浅的感觉
# Utilities
在我的Note中，最早提及到`Utility`这个概念是在[Note5](CS188/Note/Note5#Game%20Formulation),当时我们在定义成的时候简单理解为了得到的分数。现在我们进行正式定义`Utility`：
> `Utility`是一个数值，用来表示 agent 对某个结果的偏好程度。在决策理论中，agent 的目标是**最大化期望效用（Maximize Expected Utility, MEU）**。

## 偏好的数学表示
CS188用了一套标准符号：
- `A ≻ B`：更喜欢 A 胜过 B
- `A ∼ B`：对 A 和 B 无差别（indifferent）
- `L = [p, A; (1-p), B]`：一个 **lottery（彩票/随机结果）**
    - 以概率 `p` 得到 A
    - 以概率 `1-p` 得到 B
## 理性偏好的公理( Axioms of Rationality )
如果一个 agent 的偏好满足下面五条，那么它的行为就可以用**MEU**来描述。同时也将则存在一个**实值效用函数 U**，满足：
$$
\LARGE
\begin{gather}
U(A) \ge U(B) \iff A \succeq B \\
U\big([p_1,S_1;\dots;p_n,S_n]\big) = \sum_{i=1}^n p_i\,U(S_i)
\end{gather}
$$
### Orderability( 可排序性 )
公式：
$$
\LARGE
\begin{align*}
(A\succ B)\vee (B\succ A)\vee (A\sim B)
\end{align*}
$$
> 对任意两个选项 A 和 B，理性 agent 必须能比较它们。  要么 A 更好，要么 B 更好，要么二者无差别。

### Transitivity( 传递性 )
公式：
$$
\LARGE
\begin{align*}
(A \succ B) \land (B \succ C) \Rightarrow (A \succ C)
\end{align*}
$$
> 如果你喜欢 A 胜过 B，又喜欢 B 胜过 C，那你必须喜欢 A 胜过 C。
### Continuity( 连续性 )
公式：
$$
\LARGE
\begin{align*}
A \succ B \succ C \;\Rightarrow\; \exists p\;[\,p,A;\,(1-p),C\,]\sim B
\end{align*}
$$
> 如果 A 比 B 好，B 比 C 好，那么一定存在某个概率 ppp，使得  “以概率 ppp 得到 A、以概率 1−p1-p1−p 得到 C”  --这个 lottery 和 B 是等价的。
### Substitutability( 可替代性 )
公式：
$$
\LARGE
\begin{align*}
A \sim B &\Rightarrow [\,p, A;\ (1-p), C\,] \sim [\,p, B;\ (1-p), C\,]
\end{align*}
$$
> 如果 A 和 B 对你来说一样好, 那么在任何 lottery 里，把 A 换成 B，不应改变你的偏好。

### Monotonicity( 单调性 )
公式：
$$
\LARGE
\begin{align*}
A \succ B &\Rightarrow \bigl(p \ge q \iff [\,p, A; (1-p), B\,] \succeq [\,q, A; (1-q), B\,]\bigr)
\end{align*}
$$
> 如果 A 比 B 更好，那么在只涉及 A 和 B 的 lottery 中，  A 的概率越高，这个 lottery 就至少不更差。
## Risk Attitudes
Note给了我们一个例子,可以选择直接获取500$,也可以选择下面的lottery
$$
\LARGE
L=[0.5,$0; 0.5,$1000]
$$
- **Risk-neutral**：U(x) = x，对 lottery 和固定 $500 无差异
- **Risk-averse**：U(x) = √x，偏好固定 $500
- **Risk-seeking**：U(x) = x²，偏好 lottery
![[截屏2026-03-07 18.56.25.png|697]]
- - -
# Decision Networks
Decision Network 是 Bayes' Net 和 Expectimax 的结合，用来在不确定性下做决策。首先我们又重新回顾了一下节点图形的分类，原先的节点分类在[Note5](CS188/Note/Note5#Alpha-Beta%20Pruning%20Example)提及到过，在`Decision Networks`中包含了三类节点：
- **Chance nodes（椭圆形）**：表示随机变量，像 Bayes' net 中的节点。
- **Action nodes（矩形）**：表示 agent 可以选择的动作。
- **Utility nodes（菱形）**：表示效用值，依赖于其父节点（可以是 chance 或 action）。
## 目标
对每个`action`的`expected utility`:
$$
\LARGE
\begin{align*}
EU(a\mid e) &= \sum_{x_1,\dots,x_n} P(x_1,\dots,x_n\mid e)\,U(a,x_1,\dots,x_n)
\end{align*}
$$
> 假设我采取动作 a,世界可能出现很多情况，每种情况各有概率，每种情况配合这个动作又会带来不同 utility，全部加权平均，就是这个动作的 expected utility。

**MEU:**
$$
\LARGE
\begin{align*}
\operatorname{MEU}(e) &= \max_{a} EU(a\mid e)
\end{align*}
$$
## Decision Networks Example
![[截屏2026-03-07 19.21.13.png]]
$$
\LARGE
\begin{gather}
EU(\text{take}\mid \text{bad}) = 0.34\times 100 + 0.66\times 0 = 34\\
EU(\text{leave}\mid \text{bad}) = 0.34\times 20 + 0.66\times 70 = 53\\
MEU = \max(34,53)=53 \Rightarrow\ \text{最优动作是 leave}
\end{gather}
$$
- - -
# Outcome Tree( 结果树 )
Decision network 的决策过程可以展开为 **outcome tree**：
- 根节点是 **maximizer**（我们选择动作）
- 下一层是 **chance nodes**（根据概率分布）
- 叶子节点是 **utility values**
![[截屏2026-03-07 19.25.37.png]]
结果树本质上很像[Expectimax](CS188/Note/Note6#Expectimax):
- 我方节点取 max
- 随机节点取 expectation
但是不同的是outcome tree 会明确标出“当前知道什么 evidence”，课件里说是用大括号标记 what we know at any moment。
- - -
# Value of Perfect Information( VPI )
VPI 衡量的是：如果我们观察到一个新的证据，**期望最大效用的提升量**。
## 证明过程
当前EMU：
$$
\LARGE
\begin{align*}
\mathrm{MEU}(e) &= \max_{a} \sum_{s} P(s\mid e)\,U(s,a)
\end{align*}
$$
如果观察到新证据e',那么:
$$
\LARGE
\begin{align*}
\mathrm{MEU}(e,e') &= \max_{a}\sum_{s} P\bigl(s\mid e,e'\bigr)\,U(s,a)
\end{align*}
$$
但问题是，我们在观察之前，不知道会观察到什么,所以e‘其实是个随机变量 E’，并且取的是期望：
$$
\LARGE
\begin{align*}
MEU(e, E') &= \sum_{e'} P(e' \mid e)\, MEU(e, e')
\end{align*}
$$
这个地方有点难以理解，可以举个例子理解一下
$$
MEU(阴天,天气预报)=P(good∣阴天)⋅MEU(阴天,good)+P(bad∣阴天)⋅MEU(阴天,bad)
$$
最终我们得到了:
$$
\LARGE
\begin{align*}
VPI(E' \mid e) &= MEU(e, E') - MEU(e)
\end{align*}
$$
## VPI例子
![[截屏2026-03-07 19.57.21.png]]

![[截屏2026-03-07 20.00.17.png]]
![[截屏2026-03-07 20.00.32.png]]
## VPI的三个重要性质
1. **Nonnegativity（非负性）**：
$$
\LARGE
\begin{align*}
\mathrm{VPI}\bigl(E' \mid e\bigr) &\ge 0
\end{align*}
$$
2. **Nonadditivity（不可加性）**:
$$
\LARGE
\begin{align*}
VPI(E_j,E_k\mid e) &\neq VPI(E_j\mid e) + VPI(E_k\mid e)
\end{align*}
$$
3. **Order-independence（顺序无关性）**:
$$
\LARGE
\begin{align*}
VPI(E_j, E_k \mid e) &= VPI(E_j\mid e) + VPI(E_k\mid e, E_j) \\
&= VPI(E_k\mid e) + VPI(E_j\mid e, E_k)
\end{align*}
$$
注意⚠️：这里并没有违反了不可加性，因为顺序无关性阐述的是已经在知道第一个新信息的情况下再去观测第二个新信息的情况