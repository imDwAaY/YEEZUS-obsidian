---
tags:
  - CS188
  - "#Search_Problem"
---

## Search Problem的六要素
###### • A state space - The set of all possible states that are possible in your given world 
###### • A set of actions available in each state 
###### • A transition model - Outputs the next state when a specific action is taken at current state 
###### • An action cost - Incurred when moving from one state to another after applying an action 
###### • A start state - The state in which an agent exists initially 
###### • A goal test - A function that takes a state as input, and determines whether it is a goal state

## State Space Size

![[b2f8aa134bbd61eda2f20d78bcdcaa23.png]]

###### • Pacman positions - Pacman can be in 120 distinct (x, y) positions, and there is only one Pacman 
###### • Pacman Direction - this can be North, South, East, or West, for a total of 4 possibilities 
###### • Ghost positions - There are two ghosts, each of which can be in 12 distinct (x, y) positions 
###### • Food pellet configurations - There are 30 food pellets, each of which can be eaten or not eaten
整体数量：120 × 4 × 12² × 2³⁰    数量旁大无法存储

## State Space Graph vs Search Tree
![[c659ec7fec23e85c3484717cfe178a71.png]]
### State Space Graph（概念上的完整图）

- 每一个 state 只出现一次
- 边表示动作
- 边上可以存放代价
- 是一个**概念性的模型**，几乎从不完全构造出来  因为状态太多了

### Search Tree（实际搜索用的结构）

- 每一次搜索都会从起点不断扩展“路径”
- **同一个 state 可以出现多次，因为路径不同**  
    例：  
    从 A 到 C 可以走 A→B→C 或 A→D→C，这两条路径会产生两个不同的 Tree Node（尽管状态 C 相同）。

Search Tree 是 **路径树**，节点包含：
- 当前 state
- 到达该 state 的路径
- path cost（累计代价）
- parent（用于回溯路径）

## Uninformed Search
| 属性           | DFS    | BFS      | UCS            |
| ------------ | ------ | -------- | -------------- |
| Frontier     | Stack  | Queue    | Priority Queue |
| Completeness | No     | Yes      | Yes            |
| Optimal      | No     | Yes（等代价） | Yes            |
| Time         | O(b^m) | O(b^s)   | O(b^(C*/ε))    |
| Space        | O(bm)  | O(b^s)   | O(b^(C*/ε))    |
| 优点           | 空间低    | 找最短步数    | 最优解            |
| 缺点           | 容易迷路   | 空间爆炸     | 时间可能很高         |
**Tip:（C* = 最优路径代价，ε = 最小代价）**