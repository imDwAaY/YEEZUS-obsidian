---
tags:
  - CS188
  - "#Probability"
source: Note10(Intro to Probability (Michael))
---
这一个Note包括的内容基本上与高中数学所涵盖的概率部分无差异，所以说下的功夫少一点，不过多解释了
# Probability Rundown
## Random Variables & Distributions
首先了解的就是概率的表示方式:`P(A)`表示未知事件A发傻鞥的概率，其中概率分布给每个可能的结果赋予了一个概率值，它们满足：
- 所有概率>=0
- 所有概率之和 = 1
## Joint Ditribution( 联合分布 )
`P(A, B, C)`表示A, B, C三个变量同时发生的概率，表示的顺序不影响结果
## Chain Rule( 链式法则 )
$$
\LARGE
\begin{align*}
P(A,B) &= P(A\mid B)\,P(B) = P(B\mid A)\,P(A)\\
P(A_1,A_2,\ldots,A_k) &= P(A_1)\,P(A_2\mid A_1)\cdots P(A_k\mid A_1,\ldots,A_{k-1})
\end{align*}
$$
## Marginalization( 边缘化 )
$$
\Large
\begin{align*}
P(A) = ∑_b P(A, B=b)\\
P(A,B) = ∑_c P(A,B,C=c)
\end{align*}
$$
## Normalization( 归一化 )
如果概率表求和不为1，将每个值除以总和使其成为合法分布
## Bayes' Rule
$$
\Large
\begin{align*}
P(A\mid B) &= \frac{P(B\mid A)\,P(A)}{P(B)}
\end{align*}
$$
## Independence( 独立性 )
- `A ⊥⊥ B`表示 `P(A,B) = P(A)P(B)`,即`P(A|B) = P(A)`
- `A ⟂⟂ B | C` 表示在已知 C 的情况下，A 和 B 独立
	-  `P(A,B|C) = P(A|C)P(B|C)`
	这个比较好理解，可以理解成C为一种绝对正确的公理，这样转化格式变为`P(A,B) = P(A)P(B)`  
	- `P(A|B,C) = P(A|C)`
# Inference by Enumeration

| Season | Temperature | Weather | Probability |
| ------ | ----------- | ------- | ----------- |
| summer | hot         | sun     | 0.30        |
| summer | hot         | rain    | 0.05        |
| summer | cold        | sun     | 0.10        |
| summer | cold        | rain    | 0.05        |
| winter | hot         | sun     | 0.10        |
| winter | hot         | rain    | 0.05        |
| winter | cold        | sun     | 0.15        |
| winter | cold        | rain    | 0.20        |
步骤：
1.  选择所有 `S = winter` 的行
2.  对 `T` 求和：
	- `sun`: 0.10 + 0.15 = 0.25  
	- `rain`: 0.05 + 0.20 = 0.25
3.  归一化
	- `sun`: 0.25 / (0.25+0.25) = 0.5
	- `rain`: 0.25 / 0.5 = 0.5
4. 结果
	P(W = sun | S = winter) = 0.5
	P(W = rain | S = winter) = 0.5