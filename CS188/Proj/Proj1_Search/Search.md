---
tags:
  - CS188
  - heuristics
  - Informed_Search
  - Search_Problem
---

### Q1.深度优先搜索(DFS)

代码实现：
```python
def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
	"""Search the deepest nodes in the search tree first."""
    from util import Stack
    start_state = problem.getStartState()
    stack = Stack()
    stack.push((start_state,[]))
    visited = set()
    while not stack.isEmpty():
        current_state, actions = stack.pop()
        if current_state in visited:
            continue
        visited.add(current_state)
        if problem.isGoalState(current_state):
            return actions
        for next_state, action, cost in problem.getSuccessors(current_state):
            if next_state not in visited:
                stack.push((next_state, actions + [action]))
    return []
```

### Q2.广度优先搜索(BFS)

代码实现：
```python
def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue;
    start_state = problem.getStartState()
    queue = Queue()
    queue.push((start_state,[]))
    visited = set()
    while not queue.isEmpty():
        current_state, actions = queue.pop()
        if current_state in visited:
            continue
        visited.add(current_state)
        if problem.isGoalState(current_state):
            return actions
        for next_state, action, cost in problem.getSuccessors(current_state):
            if next_state not in visited:
                queue.push((next_state, actions + [action]))
    return []
```
[**BFS**,**DFS**和**UCS**](CS188/Note/Note2.md#Uninformed%20Search)在代码实现方面上来说本质差别并不是特别大，只是运用了不同的数据结构。
DFS运用的数据结构是Stack,遵循着先进后出（ LIFO ) 的原则。因为LIFO的特性，导致其扩展一个节点后，Successors会把当前节点的后继状态push到Stack中，Stack又会pop出来。所以会立马扩展刚刚被扩展的节点。越扩展越深即是DFS
BFS运用的数据结构是Queue,遵循着先进先出 ( FSFO ) 的原则。和DFS同理，Successors会把当前节点后继状态push到Queue中，但遵循先进先出的原则，会把当前节点后继状态扩展完再继续扩展后继状态的后继状态。
### Q3.统一成本搜索(UCS)

代码实现：
```python
def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***" 
    from util import PriorityQueue
    start_state = problem.getStartState()
    queue = PriorityQueue()
    queue.push((start_state, [], 0), 0)
    visited = set()
    while not queue.isEmpty():
        current_state, actions, current_cost = queue.pop()
        if current_state in visited:
            continue
        visited.add(current_state)
        if problem.isGoalState(current_state):
            return actions 
        for next_state, action, stepcost in problem.getSuccessors(current_state):
            if next_state not in visited: 
                new_cost = current_cost + stepcost
                queue.push((next_state, actions + [action], new_cost), new_cost)
    return []     
```
**在完成代码之前要看util.py文件详细了解每个数据结构的每个功能的操作都有哪些，以及返回值是什么**
UCS代码实现方面和A* 一样都采用了PriorityQueue的数据结构，和DFS&BFS采用了类似的代码框架，会优先挑选queue中具有最低( priority )的节点( 即最低cost )进行扩展。这样就实现了统一成本搜索。
### Q4.A* 搜索
代码实现：
```python
def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    start_state = problem.getStartState()
    queue = PriorityQueue()
    visited = set()
    queue.push((start_state, [], 0), heuristic(start_state, problem))
    while not queue.isEmpty():
        current_state, actions, current_cost = queue.pop()
        if current_state in visited:
            continue
        visited.add(current_state)
        if problem.isGoalState(current_state):
            return actions
        for next_state, action, stepcost in problem.getSuccessors(current_state):
            if next_state not in visited:
                new_cost = current_cost + stepcost
                h = heuristic(next_state, problem)
                f = h + new_cost
                queue.push((next_state, actions + [action], new_cost), f)
    return []
```
~~这是一种错误代码实现，因为会在环路或者多路径问题中忽略最优路径。~~
~~其本质错误是忽略了数据结构特性，因环路存在的最优解而提前执行visited.add(goal)导致真正最优路径未能进入核心for循环。~~
```text
   A
5 / \ 6
 B   C
5 \ / 2
   D
```
~~PriorityQueue本质上就是挑选队列中**最低priority**(即最低cost)的一种数据结构。当面对上图路径时，该数据结构将率先进行A -> B -> D的扩展，并在到达D时**visited.add(D)**。~~
~~因该图为简单图，在此时算法过程就已经结束了。但假设完整图有能扩展到C的机会，即终点并非D，此刻即便是A -> C -> D为最优到D路径，也会因为push阶段的visited检查导致该路径无法进入核心for循环，最终错失最优解。~~
<span class="red-text bold">这里是错误解读</span>,详细部分请看下方[新的思考](CS188/Proj/Proj1_Search/Search.md#新的思考)
```text
*** 	        1      1      6
*** 	    *Q ---> A ---> B ---> [G]
*** 	     |             ^
*** 	     |      3      |
*** 	     \-------------/
*** 	    The heuristic value of each state is:
*** 	    	Q 1.0
*** 	    	A 6.0
*** 	    	B 0.0
*** 	    	G 0.0
*** 	student expanded_states:	['Q', 'B', 'A']
*** 	correct expanded_states:	['Q', 'B', 'A', 'B']
```
上述代码无法pass这个test,就是因为visited.add(B)导致错失最佳路径拓展

正确代码实现：
```python
def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    start_state = problem.getStartState()
    queue= PriorityQueue()
    queue.push((start_state, [], 0), heuristic(start_state, problem))  # f = g+h, g=0
    visited = {}  # state -> g
    while not queue.isEmpty():
        state, actions, g = queue.pop()
        if state in visited and g >= visited[state]:
            continue
        visited[state] = g
        if problem.isGoalState(state):
            return actions
        for next_state, action, step_cost in problem.getSuccessors(state):
            new_g = g + step_cost  
            f = new_g + heuristic(next_state, problem)  # f = g + h
            queue.push((next_state, actions + [action], new_g), f)
    return []  
```
#### 新的思考
最后一版实现的代码仍然避免不了上图的环路问题，虽然autograder中能够拿到满分
```text
   A
5 / \ 6
 B   C
5 \ / 2
   D
```
queue中的过程如下，还是无法避免环路问题
```perl
初始：queue = [(A, 0)]
pop A → push B(g=5), C(g=6)
pop B(g=5) → push D_via_B(g=5)
pop D_via_B(g=5) → goal?  YES! return
```
主要问题出现在了判断isGoalState的判断上，C节点没有机会pop出来，D节点就已经被pop出来了并在循环中return actions结束函数。
<span class="bold darkred-text large">反复检查发现犯了两个很大的理解错误</span>
- PriorityQueue中的Priority并非是g(移动到当前state全部实际cost)，而是f, f = g + h。这个问题是有启发式的值的，启发式的值不是0
- queue中push进去的是new_g，也就是说push进去的g不是单步的cost,而是到达next_state的所有总和cost,所以说queue的正确过程需要ABCD每个点的heuristic值
**结论：第二版代码是正确的**
### Q5.遍历角落问题
代码实现：
```python
class CornersProblem(search.SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function
    """

    def __init__(self, startingGameState: pacman.GameState):
        """
        Stores the walls, pacman's starting position and corners.
        """
        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top, right = self.walls.height-2, self.walls.width-2
        self.corners = ((1,1), (1,top), (right, 1), (right, top))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                print('Warning: no food in corner ' + str(corner))
        self._expanded = 0 # DO NOT CHANGE; Number of search nodes expanded

    def getStartState(self):
        """
        Returns the start state (in your state space, not the full Pacman state
        space)
        """
        "*** YOUR CODE HERE ***"
        start_pos = self.startingPosition
        visited = (False, False, False, False)
        return (start_pos, visited)
        util.raiseNotDefined()

    def isGoalState(self, state: Any):
        """
        Returns whether this search state is a goal state of the problem.
        """
        "*** YOUR CODE HERE ***"
        position, visited = state
        return all(visited)
        util.raiseNotDefined()

    def getSuccessors(self, state: Any):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
            For a given state, this should return a list of triples, (successor,
            action, stepCost), where 'successor' is a successor to the current
            state, 'action' is the action required to get there, and 'stepCost'
            is the incremental cost of expanding to that successor
        """

        successors = []
        (x, y), visited = state
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if self.walls[nextx][nexty]:
                continue
            nextPos = (nextx, nexty)
            newVisited = list(visited)
            for i, corner in enumerate(self.corners):
                if nextPos == corner:
                    newVisited[i] = True
            newVisited  = tuple(newVisited)
            successors.append(((nextPos, newVisited), action, 1))
            # Add a successor state to the successor list if the action is legal
            # Here's a code snippet for figuring out whether a new position hits a wall:
            #   x,y = currentPosition
            #   dx, dy = Actions.directionToVector(action)
            #   nextx, nexty = int(x + dx), int(y + dy)
            #   hitsWall = self.walls[nextx][nexty]

            "*** YOUR CODE HERE ***"

        self._expanded += 1 # DO NOT CHANGE
        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999.  This is implemented for you.
        """
        if actions == None: return 999999
        x,y= self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
        return len(actions)
```
一个Search Problem有六要素，其中第一个就是[state space](CS188/Note/Note2.md#Search%20Problem的六要素)。
针对这个问题，第一个需要解决的就是state包括什么内容。其中最简单且不耗费资源的表达方式就是pacman的location和四个角是否被visited。
注释给的真的很详细..而且如果细看别的文件的话也能发现对新手很友好但是我仍然离不开AI  ^ _ ^
### Q6.遍历角落问题的启发式

- 首先要明确[Admissibility和Consistency](CS188/Note/Note3.md#Admissibility%20vs.%20Consistency)的区别
	- 所有的一致 ( consistent ) 启发式必然可采纳 ( admissible )
	- 可采纳 ( admissible ) 不一定一致 ( consistent )

| Admissibility   | 可采纳性    | 保证永远不高估真实代价                |
| --------------- | ------- | -------------------------- |
| **Consistency** | **一致性** | **每走一步，h的值最多只能下降这一步的cost** |
#### 代码实现
```python
def cornersHeuristic(state: Any, problem: CornersProblem):
    """
    A heuristic for the CornersProblem that you defined.

      state:   The current search state
               (a data structure you chose in your search problem)

      problem: The CornersProblem instance for this layout.

    This function should always return a number that is a lower bound on the
    shortest path from the state to a goal of the problem; i.e.  it should be
    admissible.
    """
    corners = problem.corners # These are the corner coordinates
    walls = problem.walls # These are the walls of the maze, as a Grid (game.py)

    "*** YOUR CODE HERE ***"
    from util import manhattanDistance
    position, visited = state
    remaining = [corners[i] for i, v in enumerate(visited) if not v]
    if not remaining:
        return 0
    
    current = position
    h = 0
    unused = remaining[:]

    while unused:
        dist, nearest = min((manhattanDistance(current, c), c) for c in unused)
        h += dist
        current = nearest
        unused.remove(nearest)
    return h # Default to trivial solution
```
运用的是greedy-TSP
### Q7:Eating All The Dots
#### 注意事项
如果和[Q6](CS188/Proj/Proj1_Search/Search.md#Q6.遍历角落问题的启发式)运用同一个启发式的话(greedy-TSP)，需要考虑**启发式跳变的问题**。这里的跳变指的是在空间位置上相邻的两个状态启发式差距过大。这样会违反[consistency原则](CS188/Note/Note3.md#Admissibility%20vs.%20Consistency)，即每走一步，h的下降最多只能下降这一步的cost。
这是在Eating All The Dots这个特定问题下产生的，是因为目标点数量不固定，布局复杂，点密集，**顺序变化**导致heuristic跳变。而Q6的CornersProblem就可以用greedy-TSP,贪心顺序基本不可能发生重排。
**不适用启发式的根本原因：Q6不是NP-hard问题，Q7才是**
#### 错误代码(仿照Q6版本)
```python
def foodHeuristic(state: Tuple[Tuple, List[List]], problem: FoodSearchProblem):
    "*** YOUR CODE HERE ***"
    position, foodGrid = state
    from util import manhattanDistance
    foodlist = foodGrid.asList()
    if not foodlist:
        return 0
    current = position
    h = 0
    food = foodlist[:]
    while food:
        dist, nearest = min((manhattanDistance(current, c), c) for c in food)
        h += dist
        current = nearest
        food.remove(nearest)
    return h
```

#### 正确代码实现
##### Version 1
```python
def foodHeuristic(state: Tuple[Tuple, List[List]], problem: FoodSearchProblem):
    "*** YOUR CODE HERE ***"
    position, foodGrid = state
    from util import manhattanDistance
    foodlist = foodGrid.asList()
    if not foodlist:
        return 0
    h = 0
    h = max(manhattanDistance(position, food) for food in foodlist)
    return h
```
**expanded code: 9551**
**Question 7 Grade: 3/4**
采用**曼哈顿到最远食物的max**
- **可采（admissible）**：启发式 `h(state)` 必须 ≤ 从该 state 到任意目标的真实最短代价（即不能高估）。考虑当前还有若干食物，其中有一个食物 `f*` 是离当前位置最远的食物（按真实路径长度）。为了收集所有食物，最终必须到达 `f*` 一次；因此从当前位置到达 `f*` 的真实最短距离是完成任务所需步数的下界。把所有食物的“距离”取最大，就是对所有这些下界取最大——仍然不会超过真实最短完成代价，所以**不高估**，即可采。  
（如果用曼哈顿距离而非真实迷宫距离，曼哈顿距离 ≤ 真实迷宫距离，故仍然是下界，依然可采。）
- **一致（consistent）**：若从状态 `n` 沿一步到达 `n'`（一步代价为 1），一致性要满足 `h(n) ≤ cost(n,n') + h(n')`。设 `h(n)` 是当前位置到所有食物曼哈顿距离的最大值。对于任一食物 `f`，当前位置到 `f` 的曼哈顿距离与向某个邻居移动后到 `f` 的曼哈顿距离差值最多为 1（因为曼哈顿距离每走一步最多减少 1）。所以各食物距离的最大值从 `n` 到 `n'` 也最多减少 1，即 `h(n) ≤ 1 + h(n')`。因此一致性成立。  
（同理若 `h` 用真实迷宫距离也是一致的，因为真实路径长度也满足三角不等式/单步变化上界 1。）
---
##### Version 2
```python
def foodHeuristic(state: Tuple[Tuple, List[List]], problem: FoodSearchProblem):
    position, foodGrid = state
    foodlist = foodGrid.asList()
    if not foodlist:
        return 0
    return max(mazeDistance(position, food, problem.startingGameState) for food in foodlist)
```
**expanded code: 4137**
**Question 7 Grade: 5/4**

mazeDistance在`searchAgents.py`文件中已经实现
```python
def mazeDistance(point1: Tuple[int, int], point2: Tuple[int, int], gameState: pacman.GameState) -> int:
    """
    Returns the maze distance between any two points, using the search functions
    you have already built. The gameState can be any game state -- Pacman's
    position in that state is ignored.

    Example usage: mazeDistance( (2,4), (5,6), gameState)

    This might be a useful helper function for your ApproximateSearchAgent.
    """
    x1, y1 = point1
    x2, y2 = point2
    walls = gameState.getWalls()
    assert not walls[x1][y1], 'point1 is a wall: ' + str(point1)
    assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
    prob = PositionSearchProblem(gameState, start=point1, goal=point2, warn=False, visualize=False)
    return len(search.bfs(prob))
```
**相比于manhattanDistance运用mazeDistance可以大幅提高启发式获得的信息量，极限贴近于真实代价**
### Q8: Suboptimal Search
#### 代码实现
```python
class ClosestDotSearchAgent(SearchAgent):
    "Search for all food using a sequence of searches"
    def registerInitialState(self, state):
        self.actions = []
        currentState = state
        while(currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(currentState) # The missing piece
            self.actions += nextPathSegment
            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    t = (str(action), str(currentState))
                    raise Exception('findPathToClosestDot returned an illegal move: %s!\n%s' % t)
                currentState = currentState.generateSuccessor(0, action)
        self.actionIndex = 0
        print('Path found with cost %d.' % len(self.actions))

    def findPathToClosestDot(self, gameState: pacman.GameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition()
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState)
        "*** YOUR CODE HERE ***"
        from search import breadthFirstSearch
        path = breadthFirstSearch(problem)
        return path
        util.raiseNotDefined()

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state: Tuple[int, int]):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x,y = state
        return self.food[x][y]
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()
```
#### 要点
- 这个Q8是基于[BFS](CS188/Note/Note2.md#Uninformed%20Search)实现的，具体实现代码请参考[BFS](CS188/Proj/Proj1_Search/Search.md#Q2.广度优先搜索(BFS))。BFS会遍历pacman周围的节点，第一时间遇到食物就会返回路径。
- 其中`AnyFoodSearchProblem` **定义了目标** → 任意一个食物点。

