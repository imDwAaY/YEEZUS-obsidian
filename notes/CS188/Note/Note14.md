---
tags:
  - CS188
  - "#Inference"
  - "#Variable_Elimination"
  - "#Inference_By_Enumeration"
  - "#Exact_Inference"
source: 6.6 Exact Inference in Bayes Nets
---
# Inference
在[Bayes Net](notes/CS188/Note/Note12.md#Bayes%20Net)中，Inference的目标是求解一个条件概率$\begin{align*}&P\big(Q_1 \ldots Q_k \mid e_1 \ldots e_k\big)\end{align*}$,也就是给出一些**观测的变量( evidence )**,计算**查询变量( query variables )** 的后验概率
比如$P(T \mid +e)$就表示着我们要求解当我们已经观察到事件e为真时，T为真的概率是多少？
我们首先能想到的最基础的方法就是，直接构造一个完整的[概率联合表]( notes/CS188/Note/Note11.md#Joint%20Ditribution(%20联合分布%20) )，然后我们用在Note11中提及到的[Inference by Enumeration方法](notes/CS188/Note/Note11.md#Inference%20by%20Enumeration),先选择与evidence一致的行再求和最后归一化。但是这样做的问题也很明显，问题就在于第一步构造完整概率联合表上，假设每个变量都是binary,如果有n个变量那么就会有$2^n$个rows，构造这样大的表很有难度。这就引出来了我们解决问题的方法`Variable Elimination`。我们在本讲引入的方法就是 #Exact_Inference
- - -
# Variable Elimination
首先我们需要定义`Factor`为一个未归一化的概率表，比如$P(A \mid B)$或者$P(A, B)$
## Variable Elimination实例
模型结构：
- T：是否拿宝藏
- C：是否触发陷阱
- S：是否触发蛇
- E：是否能逃脱
求$P(T \mid +e)$，即已知逃脱成功，求拿到宝藏的概率
![[notes/CS188/static/image.WUUML3.png|250]]
**Step1:首先列出所有因子**
- $P(T)$
- $P(C \mid T)$
- $P(S \mid T)$
- $P(+e \mid C, S)$

**Step2:Join所有包含C的factors以便下一步求和消除C**
包含C的因子有：
- $P(C \mid T)$
- $P(+e \mid C, S)$
Join后得到新的factor：$$\LARGE f_1(C, +e, T, S)$$
也可以写成$$ \LARGE P(C, +e \mid T, S)$$

**Step3:消除C**
$$
\LARGE
\begin{align*}
f_2(+e, T, S) &= \sum_{c} P(C \mid T)\,P(+e \mid C, S) = \sum_{c}f_1(C, +e, T, S)
\end{align*}
$$
用求和公式把C消除

**Step4：Join所有包含S的factors以便下一步求和消除S**
包含S的因子有：
- $P(S \mid T)$
- $f_2(+e, T, S)$
Join后得到新的factor
$$
\LARGE
f_3(+e, S, T)
$$

**Step5:消除S**
$$
\LARGE
\begin{align*}
f_4(+e, T) &= \sum_sf_3(+e, S, T)
\end{align*}
$$

**Step6:乘上剩余因子**
还剩下一个$P(T)$,就可以得到
$$
\LARGE
\begin{align*}
f_5(+e, T) &= P(T)f_4(+e, T)
\end{align*}
$$

**Step7:归一化**
## 伪代码实现
![[notes/CS188/static/image.DD6JL3.png]]

## 与Enumeration的本质区别
Enumeration:
$$
\LARGE
\begin{align*}
\alpha\sum_s\sum_cP(T)\,P(s \mid T)\,P(c \mid T)\,P(+e \mid c, s)
\end{align*}
$$
Variable Elimination：
$$
\LARGE
\begin{align*}
\alpha P(T)\sum_{s}P(s\mid T)\sum_{c}P(c\mid T)\,P(+e\mid c,s)
\end{align*}
$$
Variable Elimination 把：
> 与求和无关的项提前移出求和符号

这大大减少了中间表的大小。
同时需要注意的是如果先消除 S，可能中间因子大小会不同。通过合理选择消除顺序，可以使最大因子尽可能小，从而降低计算复杂度。通常我们会采用贪心策略：每次选择“最小规模”的变量进行消除，其中规模可定义为当前涉及该变量的因子合并后的大小。这被称为“最小缺陷”或“最小边”启发式。
