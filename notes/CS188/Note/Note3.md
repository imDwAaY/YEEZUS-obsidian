---
tags:
  - CS188
  - heuristics
  - "#Informed_Search"
---

## Informed Search(启发式搜索)
### 原文解释
- **If we have some notion of the direction in which we should focus our search, we can significantly improve performance and "hone in" on a goal much more quickly. This is exactly the focus of informed search.**

---

## Heuristics
- 定义：估计从当前状态到目标状态的距离的函数。  
  - 输入：state  
  - 输出：估计值（estimate）
- 特性：
  - **通常要求是低估（lower bound）**，保证 A* 的最优性。
  - 常通过“relaxed problem（放宽约束的问题）”得到，例如忽略迷宫墙壁。
- 例子：
  - Pacman 问题中常用 **Manhattan distance**：
```text
    Manhattan(x1, y1, x2, y2) = |x1 − x2| + |y1 − y2|
```
  - 用于估计从当前位置到目标位置的距离，忽略障碍。
### 来源：Relaxed Problem（放宽约束得到的确切代价）

- 常见做法：把原问题的一些限制移除（例如：去掉障碍物、允许穿墙、忽略某些约束），在放宽的问题上计算真实最短代价，这个代价即为对原问题的启发式估计。
    
- Example：网格路径问题（且只能上下左右）：把墙移除 → Manhattan distance 就是放松问题的真实代价。

---

## Admissibility vs. Consistency

### 原文解释
- **Admissibility vs. Consistency**: Remember, heuristics are just functions that take search states and return numbers that estimate the cost to a nearest goal. More effective heuristics will return values closer to the actual goal costs. To be _admissible_, the heuristic values must be lower bounds on the actual shortest path cost to the nearest goal (and non-negative). To be _consistent_, it must additionally hold that if an action has cost c, then taking that action can only cause a drop in heuristic of at most c.
### 两者关系
- 所有的一致 ( consistent ) 启发式必然可采纳 ( admissible )
- 可采纳 ( admissible ) 不一定一致 ( consistent )

| Admissibility   | 可采纳性    | 保证永远不高估真实代价                |
| --------------- | ------- | -------------------------- |
| **Consistency** | **一致性** | **每走一步，h的值最多只能下降这一步的cost** |

## Dominance
### Dominance 定义
- heuristic ha dominates hb iff ∀n: ha(n) ≥ hb(n)（且二者都 admissible）
- 胜出的启发式在所有节点上都给出更高（更接近真实）估计 → 平均会扩展更少节点 → 更快
### 合成技巧：max(h1, h2, …)

- 如果 h1, h2 都是 admissible（或 consistent），则 h = max(h1, h2) 仍然是 admissible（或 consistent）。
- 因为 max of numbers in [0, h*(n)] 仍在同一区间内。

![[notes/CS188/static/3fef52eb51522b8b65927b0e9ab4fe43.png| 150]]
### 应用
- 常把多种较弱启发式结合成一个更强的启发式（例如 Manhattan + linear conflict）。



