---
tags:
  - "#CS188"
source: "Project4: Ghostbusters"
---
这个project是入门CS144以来最难的一次，不仅思维难度高，而且问题还非常多，足足有14个，综合性也非常强。
# Q1.Bayes Net Structure
第一问是一个的构建简单的贝叶斯网络，这个题目不要求你细节全部实现，只要求完成以下三件事：
1. 把所有变量名称放进`variables`
2. 把图里的箭头放进`edges`
3. 给每个变量设置取值范围`variableDomainsDict`
## Q1代码实现
```python
def constructBayesNet(gameState: hunters.GameState):
    """
    Construct an empty Bayes net according to the structure given in Figure 1
    of the project description.

    You *must* name all variables using the constants in this function.

    In this method, you should:
    - populate `variables` with the Bayes Net nodes
    - populate `edges` with every edge in the Bayes Net. we will represent each
      edge as a tuple `(from, to)`.
    - set each `variableDomainsDict[var] = values`, where `values` is a list
      of the possible assignments to `var`.
        - each agent position is a tuple (x, y) where x and y are 0-indexed
        - each observed distance is a noisy Manhattan distance:
          it's non-negative and |obs - true| <= MAX_NOISE
    - this uses slightly simplified mechanics vs the ones used later for simplicity
    """
    # constants to use
    PAC = "Pacman"
    GHOST0 = "Ghost0"
    GHOST1 = "Ghost1"
    OBS0 = "Observation0"
    OBS1 = "Observation1"
    X_RANGE = gameState.getWalls().width
    Y_RANGE = gameState.getWalls().height
    MAX_NOISE = 7

    variables = []
    edges = []
    variableDomainsDict = {}

    "*** YOUR CODE HERE ***"
    variables = [PAC, GHOST0, GHOST1, OBS0, OBS1]
    edges = [(GHOST0, OBS0), (PAC, OBS0), (PAC, OBS1), (GHOST1, OBS1)]
    walls = gameState.getWalls()
    legalPositions = []
    for x in range(X_RANGE):
        for y in range(Y_RANGE):
            if (x, y) not in walls:
                legalPositions.append((x, y))
    variableDomainsDict[PAC] = legalPositions
    variableDomainsDict[GHOST0] = legalPositions
    variableDomainsDict[GHOST1] = legalPositions
    maxTrueDist = (X_RANGE - 1) + (Y_RANGE - 1)
    maxObsDist = maxTrueDist + MAX_NOISE
    variableDomainsDict[OBS0] = list(range(maxObsDist + 1))
    variableDomainsDict[OBS1] = list(range(maxObsDist + 1))
    "*** END YOUR CODE HERE ***"
    net = bn.constructEmptyBayesNet(variables, edges, variableDomainsDict)
    return net
```
---
# Q2.Join Factors
