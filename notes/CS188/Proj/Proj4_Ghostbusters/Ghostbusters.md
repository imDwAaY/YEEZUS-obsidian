---
tags:
  - "#CS188"
  - Bayes_Nets
  - "#Variable_Elimination"
  - Exact_Inference
  - Approximate_Inference
  - Particle_Filtering
source: "Project4: Ghostbusters"
---
这个project是入门CS144以来比较难的一次，不仅思维难度略高，而且问题还非常多，足足有14个，综合性比较强。
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
第二问也基本上没有实现难度，唯一需要注意的点就是传进去的参数`factors`不是`list`类型的，而是`dict_values`类型。它不能像列表一样用下标取值，只需要在开头进行显示类型转换即可。
`factors = list(factors)`
## 代码实现
```python
def joinFactors(factors: List[Factor]):
    """
    Input factors is a list of factors.  
    
    You should calculate the set of unconditioned variables and conditioned 
    variables for the join of those factors.

    Return a new factor that has those variables and whose probability entries 
    are product of the corresponding rows of the input factors.

    You may assume that the variableDomainsDict for all the input 
    factors are the same, since they come from the same BayesNet.

    joinFactors will only allow unconditionedVariables to appear in 
    one input factor (so their join is well defined).

    Hint: Factor methods that take an assignmentDict as input 
    (such as getProbability and setProbability) can handle 
    assignmentDicts that assign more variables than are in that factor.

    Useful functions:
    Factor.getAllPossibleAssignmentDicts
    Factor.getProbability
    Factor.setProbability
    Factor.unconditionedVariables
    Factor.conditionedVariables
    Factor.variableDomainsDict
    """

    # typecheck portion
    setsOfUnconditioned = [set(factor.unconditionedVariables()) for factor in factors]
    if len(factors) > 1:
        intersect = functools.reduce(lambda x, y: x & y, setsOfUnconditioned)
        if len(intersect) > 0:
            print("Factor failed joinFactors typecheck: ", intersect)
            raise ValueError("unconditionedVariables can only appear in one factor. \n"
                    + "unconditionedVariables: " + str(intersect) + 
                    "\nappear in more than one input factor.\n" + 
                    "Input factors: \n" +
                    "\n".join(map(str, factors)))
    "*** YOUR CODE HERE ***"
    factors = list(factors)
    unconditionedVars = set()
    conditionedVars = set()
    for factor in factors:
        unconditionedVars |= set(factor.unconditionedVariables())
        conditionedVars |= set(factor.conditionedVariables())
    conditionedVars -= unconditionedVars
    variableDomainDict = factors[0].variableDomainsDict()
    joinFactor = Factor(unconditionedVars, conditionedVars, variableDomainDict)
    for assignment in joinFactor.getAllPossibleAssignmentDicts():
        prob = 1.0
        for factor in factors:
            prob *= factor.getProbability(assignment)
        joinFactor.setProbability(assignment, prob)
    return joinFactor
    "*** END YOUR CODE HERE ***"
```
# Q3.Eliminate (not ghosts yet)
这个问题基本上思路和Q2是一样的，只不过是for循环内部的逻辑稍微变动了一下。整体思路就是我们在[Note11](notes/CS188/Note/Note11.md#Inference%20By%20Enumeration)提及到的`Inference By Enumeration`是一个思路
## 代码实现
```python
def eliminateWithCallTracking(callTrackingList=None):

    def eliminate(factor: Factor, eliminationVariable: str):
        """
        Input factor is a single factor.
        Input eliminationVariable is the variable to eliminate from factor.
        eliminationVariable must be an unconditioned variable in factor.
        
        You should calculate the set of unconditioned variables and conditioned 
        variables for the factor obtained by eliminating the variable
        eliminationVariable.

        Return a new factor where all of the rows mentioning
        eliminationVariable are summed with rows that match
        assignments on the other variables.

        Useful functions:
        Factor.getAllPossibleAssignmentDicts
        Factor.getProbability
        Factor.setProbability
        Factor.unconditionedVariables
        Factor.conditionedVariables
        Factor.variableDomainsDict
        """
        # autograder tracking -- don't remove
        if not (callTrackingList is None):
            callTrackingList.append(('eliminate', eliminationVariable))

        # typecheck portion
        if eliminationVariable not in factor.unconditionedVariables():
            print("Factor failed eliminate typecheck: ", factor)
            raise ValueError("Elimination variable is not an unconditioned variable " \
                            + "in this factor\n" + 
                            "eliminationVariable: " + str(eliminationVariable) + \
                            "\nunconditionedVariables:" + str(factor.unconditionedVariables()))
        
        if len(factor.unconditionedVariables()) == 1:
            print("Factor failed eliminate typecheck: ", factor)
            raise ValueError("Factor has only one unconditioned variable, so you " \
                    + "can't eliminate \nthat variable.\n" + \
                    "eliminationVariable:" + str(eliminationVariable) + "\n" +\
                    "unconditionedVariables: " + str(factor.unconditionedVariables()))

        "*** YOUR CODE HERE ***"
        unconditionedVars = set(factor.unconditionedVariables())
        conditionedVars = set(factor.conditionedVariables())
        unconditionedVars.remove(eliminationVariable)
        variableDomainDict = factor.variableDomainsDict()
        newFactor = Factor(unconditionedVars, conditionedVars, variableDomainDict)
        for assignment in newFactor.getAllPossibleAssignmentDicts():
            sumProb = 0.0
            for value in variableDomainDict[eliminationVariable]:
                fullAssignment = assignment.copy()
                fullAssignment[eliminationVariable] = value
                sumProb += factor.getProbability(fullAssignment)
            newFactor.setProbability(assignment, sumProb)
        return newFactor
        raiseNotDefined()
        "*** END YOUR CODE HERE ***"
```
# Q4.Variable Elimination
这个问题整体的思路就是在[Note14](notes/CS188/Note/Note14.md#Variable%20Elimination)中提及到的`Variable Elimination`一模一样。
一定需要注意的一点是，`facotrs`这个变量是`Bayesnet`中的所有概率表组成的list，在原文件`bayesNet.py`文件中声明了
```text
Returns a list of conditional probability tables (taking into
account evidence) for all variables in the bayes net.
```
还有就是`joinFactorsByVariable`函数的返回值是两个:第一个是没有被Join的表，第二个是Join后返回的整个表
## 代码实现
```python
def inferenceByVariableEliminationWithCallTracking(callTrackingList=None):

    def inferenceByVariableElimination(bayesNet: bn, queryVariables: List[str], evidenceDict: Dict, eliminationOrder: List[str]):
        """
        This function should perform a probabilistic inference query that
        returns the factor:

        P(queryVariables | evidenceDict)

        It should perform inference by interleaving joining on a variable
        and eliminating that variable, in the order of variables according
        to eliminationOrder.  See inferenceByEnumeration for an example on
        how to use these functions.

        You need to use joinFactorsByVariable to join all of the factors 
        that contain a variable in order for the autograder to 
        recognize that you performed the correct interleaving of 
        joins and eliminates.

        If a factor that you are about to eliminate a variable from has 
        only one unconditioned variable, you should not eliminate it 
        and instead just discard the factor.  This is since the 
        result of the eliminate would be 1 (you marginalize 
        all of the unconditioned variables), but it is not a 
        valid factor.  So this simplifies using the result of eliminate.

        The sum of the probabilities should sum to one (so that it is a true 
        conditional probability, conditioned on the evidence).

        bayesNet:         The Bayes Net on which we are making a query.
        queryVariables:   A list of the variables which are unconditioned
                          in the inference query.
        evidenceDict:     An assignment dict {variable : value} for the
                          variables which are presented as evidence
                          (conditioned) in the inference query. 
        eliminationOrder: The order to eliminate the variables in.

        Hint: BayesNet.getAllCPTsWithEvidence will return all the Conditional 
        Probability Tables even if an empty dict (or None) is passed in for 
        evidenceDict. In this case it will not specialize any variable domains 
        in the CPTs.

        Useful functions:
        BayesNet.getAllCPTsWithEvidence
        normalize
        eliminate
        joinFactorsByVariable
        joinFactors
        """

        # this is for autograding -- don't modify
        joinFactorsByVariable = joinFactorsByVariableWithCallTracking(callTrackingList)
        eliminate             = eliminateWithCallTracking(callTrackingList)
        if eliminationOrder is None: # set an arbitrary elimination order if None given
            eliminationVariables = bayesNet.variablesSet() - set(queryVariables) -\
                                   set(evidenceDict.keys())
            eliminationOrder = sorted(list(eliminationVariables))

        "*** YOUR CODE HERE ***"
        factors = bayesNet.getAllCPTsWithEvidence(evidenceDict)
        for eliminationVar in eliminationOrder:
            factors, joinedFactor = joinFactorsByVariable(factors, eliminationVar)
            if(len(joinedFactor.unconditionedVariables()) > 1):
                newFactor = eliminate(joinedFactor, eliminationVar)
                factors.append(newFactor)
        finalFactor = joinFactors(factors)
        return normalize(finalFactor)
        raiseNotDefined()
        "*** END YOUR CODE HERE ***"
```
# Q5a.DiscreteDistribution Class
第一部分实现`normalize`的函数没有难度。第二部分则是按照概率来采样，也没有什么难度，可以直接实现的函数。这是最基础最基础的一种采样思想，回顾之前的Note可以查看[Note15](notes/CS188/Note/Note15.md#问题引入)。
## 代码实现
```python
    ########### ########### ###########
    ########### QUESTION 5a ###########
    ########### ########### ###########

    def normalize(self):
        """
        Normalize the distribution such that the total value of all keys sums
        to 1. The ratio of values for all keys will remain the same. In the case
        where the total value of the distribution is 0, do nothing.

        >>> dist = DiscreteDistribution()
        >>> dist['a'] = 1
        >>> dist['b'] = 2
        >>> dist['c'] = 2
        >>> dist['d'] = 0
        >>> dist.normalize()
        >>> list(sorted(dist.items()))
        [('a', 0.2), ('b', 0.4), ('c', 0.4), ('d', 0.0)]
        >>> dist['e'] = 4
        >>> list(sorted(dist.items()))
        [('a', 0.2), ('b', 0.4), ('c', 0.4), ('d', 0.0), ('e', 4)]
        >>> empty = DiscreteDistribution()
        >>> empty.normalize()
        >>> empty
        {}
        """
        "*** YOUR CODE HERE ***"
        total = self.total()
        if total == 0:
            return
        for key in self:
            self[key] /= total
        "*** END YOUR CODE HERE ***"

    def sample(self):
        """
        Draw a random sample from the distribution and return the key, weighted
        by the values associated with each key.

        >>> dist = DiscreteDistribution()
        >>> dist['a'] = 1
        >>> dist['b'] = 2
        >>> dist['c'] = 2
        >>> dist['d'] = 0
        >>> N = 100000.0
        >>> samples = [dist.sample() for _ in range(int(N))]
        >>> round(samples.count('a') * 1.0/N, 1)  # proportion of 'a'
        0.2
        >>> round(samples.count('b') * 1.0/N, 1)
        0.4
        >>> round(samples.count('c') * 1.0/N, 1)
        0.4
        >>> round(samples.count('d') * 1.0/N, 1)
        0.0
        """
        "*** YOUR CODE HERE ***"
        total = self.total()
        r = random.random() * total
        cumulative = 0
        for key, value in self.items():
            cumulative += value
            if r < cumulative:
                return key
        "*** END YOUR CODE HERE ***"
```
# Q5b.Observation Probability
这个题有点小思考难度，但代码实现不难。
- 首先我们要明确的是，题目中传进来的`noisyDistance`就是我们的`observation`。 其次我们再来讨论一下这道题的思路，从这个函数的返回值入手，这个函数的返回值为：
$$
\LARGE
P(noisyDistance \mid pacmanPosition, ghostPosition)
$$
	题目中明确说明这道题有特殊情况：即`ghost`在jail里面，这时候传感器输出是确定的：
	- 如果`observation(noisyDistance) is None`，概率就是1。表示当`ghost`在jail里面我们肯定可以确定`noisyDistance`为None
	- 如果`observation不是None`，概率就是0。表示当`ghost`在jail里面我们观测到`noisyDistance`的可能性为0，因为`noisyDistance`肯定是None

然后我们再看`ghost`不在jail里面的情况：
- 首先给一个特判，当`noisyDistance`为None的时候，返回概率为0。因为当`ghost`不在jail的时候不可能出现`noisyDistance`为None的情况
- 然后我们就需要题目中已经给出的函数`busters.getObservationProbability(noisyDistance, trueDistance)`，它的返回值为
$$
\LARGE
P(noisyDistance \mid trueDistance)
$$
	这正是我们需要的原函数的返回值，直接用就行
## 代码实现
```python
    def getObservationProb(self, noisyDistance: int, pacmanPosition: Tuple, ghostPosition: Tuple, jailPosition: Tuple):
        """
        Return the probability P(noisyDistance | pacmanPosition, ghostPosition).
        """
        "*** YOUR CODE HERE ***"
        if ghostPosition == jailPosition:
            if noisyDistance is None:
                return 1.0
            else:
                return 0.0
        if noisyDistance is None:
            return 0.0
        trueDistance = manhattanDistance(pacmanPosition, ghostPosition)
        return busters.getObservationProbability(noisyDistance, trueDistance)
```
# Q6.Exact Inference Observation
这个题目没有思路难度，但是我耗费了大量的时间在公式推导上，原因就是我忘记了贝叶斯更新。在原文档中有个提示:
```text
Hint: You can assume `self.beliefs` holds the probability P(Ghost is at position (x, y)∣ All previous observation)P(Ghost is at position (x, y)∣ All previous observation) and `self.getObservationProb` holds the probability P(New Observation∣ Ghost is at position (x, y))P(New Observation∣ Ghost is at position (x, y)). If we need to update `self.beliefs` such that it gives us the probability P(Ghost is at position (x, y)∣ All Previous observations + new observation)P(Ghost is at position (x, y)∣ All Previous observations + new observation), what is the formula we need to use?
```
这相对应的`formula`就是贝叶斯更新
$$
\LARGE
\begin{align*}
P\!\bigl(X \mid \text{old obs},\ \text{new obs}\bigr) &\propto P\!\bigl(\text{new obs} \mid X\bigr)\cdot P\!\bigl(X \mid \text{old obs}\bigr)
\end{align*}
$$
它是由原式套贝叶斯公式得来的,可以回顾一下[Note11中的独立性性质](notes/CS188/Note/Note11.md#Independence(%20独立性%20))
$$
\LARGE
\begin{align*}
P\!\bigl(X \mid O_{\text{old}}, O_{\text{new}}\bigr) &= \frac{P\!\bigl(O_{\text{new}} \mid X, O_{\text{old}}\bigr)\,P\!\bigl(X \mid O_{\text{old}}\bigr)}{P\!\bigl(O_{\text{new}} \mid O_{\text{old}}\bigr)}
\end{align*}
$$
要注意的是`getObservationProb()`函数就是在枚举当前的情况，`ghost`在`position`，`pacman`在`pacmanPosition`，还有`jailPosition`的情况：观测到当前`observation`的概率是多少
## 代码实现
```python
    def observeUpdate(self, observation: int, gameState: busters.GameState):
        """
        Update beliefs based on the distance observation and Pacman's position.

        The observation is the noisy Manhattan distance to the ghost you are
        tracking.

        self.allPositions is a list of the possible ghost positions, including
        the jail position. You should only consider positions that are in
        self.allPositions.

        The update model is not entirely stationary: it may depend on Pacman's
        current position. However, this is not a problem, as Pacman's current
        position is known.
        """
        "*** YOUR CODE HERE ***"
        pacmanPosition = gameState.getPacmanPosition()
        jailPosition = self.getJailPosition()
        for position in self.allPositions:
            prob = self.getObservationProb(observation, pacmanPosition, position, jailPosition)
            self.beliefs[position] *= prob
        "*** END YOUR CODE HERE ***"
        self.beliefs.normalize()
```
# Q7.Exact Inference with Time Elapse
这个思考难度不大，着重理解一下原文档中对于`getPositionDistribution`的理解。原文档如下：
	Where `oldPos` refers to the previous ghost position. `newPosDist` is a `DiscreteDistribution` object, where for each position `p` in `self.allPositions`, `newPosDist[p]` is the probability that the ghost is at position `p` at time `t + 1`, given that the ghost is at position `oldPos` at time `t`. Note that this call can be fairly expensive, so if your code is timing out, one thing to think about is whether or not you can reduce the number of calls to `self.getPositionDistribution`.
要注意的是循环一次`newPosDist`，只包含了从`oldPosition`出发一步之后可能到达的位置坐标，而非全部位置坐标。
这一部分可以参考[Note18中的Time Elapse](notes/CS188/Note/Note18.md#Step1%20Time%20Elapse%20Update)
`newBeliefs[newPos] += oldProb * newProb`这一行代码的原理如下
$$
\LARGE
\begin{align*}
P(G_{t+1}=p) &= \sum_{\text{oldPos}} P\bigl(G_{t+1}=p \mid G_t=\text{oldPos}\bigr)\,P(G_t=\text{oldPos})
\end{align*}
$$
## 代码实现
```python
    def elapseTime(self, gameState: busters.GameState):
        """
        Predict beliefs in response to a time step passing from the current
        state.

        The transition model is not entirely stationary: it may depend on
        Pacman's current position. However, this is not a problem, as Pacman's
        current position is known.
        """
        "*** YOUR CODE HERE ***"
        newBeliefs = DiscreteDistribution()
        for oldPos in self.allPositions:
            oldProb = self.beliefs[oldPos]
            newPosDist = self.getPositionDistribution(gameState, oldPos)
            for newPos, newProb in newPosDist.items():
                newBeliefs[newPos] += oldProb * newProb
        self.beliefs = newBeliefs
        "*** END YOUR CODE HERE ***"
```
# Q8.Exact Inference Full Test
这个问题很基础，就是两次遍历寻找最小值的普通算法逻辑。实现也没有难度，直接上手写就行。
## 代码实现
```python
    def chooseAction(self, gameState: busters.GameState):
        """
        First computes the most likely position of each ghost that has
        not yet been captured, then chooses an action that brings
        Pacman closest to the closest ghost (according to mazeDistance!).
        """
        pacmanPosition = gameState.getPacmanPosition()
        legal = [a for a in gameState.getLegalPacmanActions()]
        livingGhosts = gameState.getLivingGhosts()
        livingGhostPositionDistributions = \
            [beliefs for i, beliefs in enumerate(self.ghostBeliefs)
             if livingGhosts[i+1]]
        "*** YOUR CODE HERE ***"
        ghostPosition = []
        for dist in livingGhostPositionDistributions:
            ghostPosition.append(dist.argMax())
        closestGhost = None
        closestDist = float('inf')
        for ghost in ghostPosition:
            dist = self.distancer.getDistance(pacmanPosition, ghost)
            if dist < closestDist:
                closestDist = dist
                closestGhost = ghost
        bestAction = None
        bestDist = float('inf')
        for action in legal:
            successorPosition = Actions.getSuccessor(pacmanPosition, action)
            newDist = self.distancer.getDistance(successorPosition, closestGhost)
            if newDist < bestDist:
                bestDist = newDist
                bestAction = action
        return bestAction
        "*** END YOUR CODE HERE ***"
```
# Q9.Approximate Inference Initialization and Beliefs
对于这部分的代码就开始和[Particle Filtering](notes/CS188/Note/Note18.md#Particle%20FIltering)的内容相关了。这个问题只是对于粒子的简单初始化。其中`initializeUniformly`实现的是列表`particle`的输入，函数`getBeliefDistribution`则是根据粒子分布推导出来信念分布。总体上来说没有什么思路难度，可以直接进行实现
## 代码实现
```python
    ########### ########### ###########
    ########### QUESTION 9  ###########
    ########### ########### ###########

    def initializeUniformly(self, gameState: busters.GameState):
        """
        Initialize a list of particles. Use self.numParticles for the number of
        particles. Use self.legalPositions for the legal board positions where
        a particle could be located. Particles should be evenly (not randomly)
        distributed across positions in order to ensure a uniform prior. Use
        self.particles for the list of particles.
        """
        "*** YOUR CODE HERE ***"
        self.particles = []
        numLegal = len(self.legalPositions)
        for i in range(self.numParticles):
            position = self.legalPositions[i % numLegal]
            self.particles.append(position)
        "*** END YOUR CODE HERE ***"

    def getBeliefDistribution(self):
        """
        Return the agent's current belief state, a distribution over ghost
        locations conditioned on all evidence and time passage. This method
        essentially converts a list of particles into a belief distribution.

        This function should return a normalized distribution.
        """
        "*** YOUR CODE HERE ***"
        beliefDistribution = DiscreteDistribution()
        for particle in self.particles:
            beliefDistribution[particle] += 1
        beliefDistribution.normalize()
        return beliefDistribution
        "*** END YOUR CODE HERE ***"
```
# Q10.Approximate Inference Observation
这部分就和`Particle Filtering`过程中的一步`ObserveUpdate`一模一样了，可以回顾[Note18](notes/CS188/Note/Note18.md#Step2%20Observation%20Update)中的相关知识。我们再回顾一下这这整个proj中的一个重要函数:
`getObservationProb`，这个函数一共接受了4个参数,`noisyDistance`, `pacmanPosition`, `ghostPosition`, `jailPosition`

> 其中`noisyDistance`就是我们所观测到的`observation`，这个函数返回的值正是当后面三个参数成立的时候观测到`observation`的概率

	这样我们就能再回顾一下`Particle Filtering`进行重采样的依据：我们是根据粒子的状态推算观测出现的可能性是多少，和函数`getObservationProb`是相对应的
## 代码实现
```python
    ########### ########### ###########
    ########### QUESTION 10 ###########
    ########### ########### ###########

    def observeUpdate(self, observation: int, gameState: busters.GameState):
        """
        Update beliefs based on the distance observation and Pacman's position.

        The observation is the noisy Manhattan distance to the ghost you are
        tracking.

        There is one special case that a correct implementation must handle.
        When all particles receive zero weight, the list of particles should
        be reinitialized by calling initializeUniformly. The total method of
        the DiscreteDistribution may be useful.
        """
        "*** YOUR CODE HERE ***"
        pacmanPosition = gameState.getPacmanPosition()
        jailPosition = self.getJailPosition()
        weightDistribution = DiscreteDistribution()
        for particle in self.particles:
            weightDistribution[particle] += self.getObservationProb(observation, pacmanPosition, particle, jailPosition)
        if weightDistribution.total() == 0:
            self.initializeUniformly(gameState)
            return
        newParticles = []
        for i in range(self.numParticles):
            newParticles.append(weightDistribution.sample())
        self.particles = newParticles
        "*** END YOUR CODE HERE ***"
```
# Q11.Approximate Inference with Time Elapse
还是要理解一下我们在`Q7`中运用的函数`getPositionDistribution`
	Where `oldPos` refers to the previous ghost position. `newPosDist` is a `DiscreteDistribution` object, where for each position `p` in `self.allPositions`, `newPosDist[p]` is the probability that the ghost is at position `p` at time `t + 1`, given that the ghost is at position `oldPos` at time `t`. Note that this call can be fairly expensive, so if your code is timing out, one thing to think about is whether or not you can reduce the number of calls to `self.getPositionDistribution`.
## 代码实现
这是我没仔细看写的第一版代码，能过autograder。我写成了`exact inference`而不是`approximate inference`。我是先算出了新的整体分布，然后再对分布做一次时间推进，再得到一个新的整体分布。再从整理分布采样`numParticles`次
```python
    ########### ########### ###########
    ########### QUESTION 11 ###########
    ########### ########### ###########

    def elapseTime(self, gameState):
        """
        Sample each particle's next state based on its current state and the
        gameState.
        """
        "*** YOUR CODE HERE ***"
        newParticles = []
        oldDistribution = self.getBeliefDistribution()
        newDistribution = DiscreteDistribution()
        for oldPos in self.allPositions:
            oldprob = oldDistribution[oldPos]
            newPosDist = self.getPositionDistribution(gameState, oldPos)
            for newPos, newprob in newPosDist.items():
                newDistribution[newPos] += oldprob * newprob
        for i in range(self.numParticles):
            newParticles.append(newDistribution.sample())
        self.particles = newParticles
        "*** END YOUR CODE HERE ***"
```
正确代码实现如下,整体思路很简单。这里需要注意的是，`newPosDist`数据结构也是`DiscreteDistribution`，而且`getPositionDistribution`返回值是多个可能状态，但是`sample()`函数只随机抽一个状态
```python
    def elapseTime(self, gameState):
        """
        Sample each particle's next state based on its current state and the
        gameState.
        """
        "*** YOUR CODE HERE ***"
        newParticles = []
        for oldPos in self.particles:
            newPosDist = self.getPositionDistribution(gameState,oldPos)
            newParticles.append(newPosDist.sample())
        self.particles = newParticles
        "*** END YOUR CODE HERE ***"
```
# Q12.Joint Particle Filter Initialization
这个题目没有思路难度，只要慢慢阅读题目理解题意就可以。题目中提及到的关键改变的一点是：

> 原先一粒`particle`存储的是一个`ghost`的位置信息，现在一粒`particle`代表的是所有`ghost`的位置信息

函数`itertools.product()`的传参要求自行查看，为什么要进行`shuffle`题目也说明的很清楚：因为`Note that, if you use this, the permutations are not returned in a random order.`当我们的`allParticles`样本数量很大的时候，如果不打乱的话，采样的时候会不均匀。
注意一下这道题和Q9的区别
## 代码实现
```python
    ########### ########### ###########
    ########### QUESTION 12 ###########
    ########### ########### ###########
    
    def initializeUniformly(self, gameState):
        """
        Initialize particles to be consistent with a uniform prior. Particles
        should be evenly distributed across positions in order to ensure a
        uniform prior.
        """
        self.particles = []
        "*** YOUR CODE HERE ***"
        legalPositions = self.legalPositions
        numGhosts = self.numGhosts
        allParticles = list(itertools.product(legalPositions, repeat= numGhosts))
        random.shuffle(allParticles)
        for i in range(self.numParticles):
            self.particles.append(allParticles[i % len(allParticles)])
        "*** END YOUR CODE HERE ***"
```
# Q13.Joint Particle Filter Observation
这个问题和Q10有点类似，部分代码可以借鉴过来一下。比如说特判情况的处理( 当所有的`particles`权重为0 )。整体思路就是一样的，直接上手写就行。实现难度不大。不了解的情况在原文档里面也都给出了，仔细阅读即可。
## 代码实现
```python
    ########### ########### ###########
    ########### QUESTION 13 ###########
    ########### ########### ###########

    def observeUpdate(self, observation, gameState):
        """
        Update beliefs based on the distance observation and Pacman's position.
        The observation is the noisy Manhattan distances to all ghosts you
        are tracking.
        There is one special case that a correct implementation must handle.
        When all particles receive zero weight, the list of particles should
        be reinitialized by calling initializeUniformly. The total method of
        the DiscreteDistribution may be useful.
        """
        "*** YOUR CODE HERE ***"
        pacmanPosition = gameState.getPacmanPosition()
        newParticles = []
        newDistribution = DiscreteDistribution()
        for particle in self.particles:
            weight = 1.0
            for i in range(self.numGhosts):
                jailPosition = self.getJailPosition(i)
                weight *= self.getObservationProb(observation[i], pacmanPosition, particle[i], jailPosition)
            newDistribution[particle] += weight
        if newDistribution.total() == 0:
            self.initializeUniformly(gameState)
            return
        for i in range(self.numParticles):
            newParticles.append(newDistribution.sample())
        self.particles = newParticles
        "*** END YOUR CODE HERE ***"
```
# Q14.Joint Particle Filter Time Elapse and Full Test
这道题思路依旧是和前面的类似，Q11也是Time Elapse。实现的代码很简短，三行就结束。
唯一需要注意的一点是，这里在函数`getPositionDistribution`传参的时候:
> each ghost should draw a new position conditioned on the positions of all the ghosts at the previous time step, 意思是要传`oldParticle`而不是`newParticle`。这样就会变成一边更新一边传递。这种错误过程其实有点像在上一个[Proj3](notes/CS188/Proj/Proj3_Reinforcement_Learning/Reinforcement%20Learning.md#Q1.Value%20Iteration)中我对`online`版本的阐述。
## 代码实现
```python
    ########### ########### ###########
    ########### QUESTION 14 ###########
    ########### ########### ###########

    def elapseTime(self, gameState):
        """
        Sample each particle's next state based on its current state and the
        gameState.
        """
        newParticles = []
        for oldParticle in self.particles:
            newParticle = list(oldParticle)  # A list of ghost positions

            # now loop through and update each entry in newParticle...
            "*** YOUR CODE HERE ***"
            for i in range(self.numGhosts):
                newPosDist = self.getPositionDistribution(gameState, oldParticle, i, self.ghostAgents[i])
                newParticle[i] = newPosDist.sample()
            """*** END YOUR CODE HERE ***"""
            newParticles.append(tuple(newParticle))
        self.particles = newParticles
```