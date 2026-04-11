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
这个问题基本上思路和Q2是一样的，只不过是for循环内部的逻辑稍微变动了一下。整体思路就是我们在[Note11](CS188/Note/Note11#Inference%20By%20Enumeration)提及到的`Inference By Enumeration`是一个思路
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
这个问题整体的思路就是在[Note14](CS188/Note/Note14#Variable%20Elimination)中提及到的`Variable Elimination`一模一样。
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
