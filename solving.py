from bifrost import DataBridge
from bifrost import Boundaries
from bifrost import Constraint
from dataValidations import BoundaryValidations
from dataValidations import ConstraintValidations
import pulp

class Solver:

    def __init__(self) -> None:
        self.bridge = DataBridge()
        self.objective = Constraint(True)
        self.boundaries = Boundaries()
        self.boundValid = BoundaryValidations()
        self.constraintValid = ConstraintValidations()
        pass

    def ValidateObjective(self, objectiveStr, lowBoundEnabled, upBoundEnabled, lowBoundStr, upBoundStr):
        try:
            if(lowBoundEnabled == 0 and upBoundEnabled == 0): raise Exception("Objective can't have both boundaries set to infinite")
            if not(self.constraintValid.ValidConstraintValue(objectiveStr)): raise Exception("Objective value isn't valid")
            if not(self.boundValid.ValidLowerBoundary(lowBoundEnabled, lowBoundStr)): raise Exception("Lower Boundary isn't valid")
            if not(self.boundValid.ValidUpperBoundary(upBoundEnabled, upBoundStr)): raise Exception("Upper Boundary isn't valid")
            if (self.boundValid.CheckBoundariesAreEqual(lowBoundStr, upBoundStr)): raise Exception("Upper and Lower Boundaries can't both have the same value")

            self.objective.SetConstraintText(objectiveStr)
            boundaries = self.boundaries.GetBoundaries(lowBoundEnabled, upBoundEnabled, lowBoundStr, upBoundStr)
            self.objective.SetLowerBoundary(boundaries[0])
            self.objective.SetUpperBoundary(boundaries[1])
            self.objective.ExtractPieces()
            self.objective.GetPieces()
            self.bridge.SetObjective(self.objective)

        except Exception as err: 
            print(err)
            return False
        
        else: return True

    def ValidateData(self):
        try:
            if not(self.bridge.ConstraintHasValidVariables()): raise Exception("One or more constraints don't have valid variables")
            if not(self.bridge.ObjectiveHasValidVariables()): raise Exception("Objective doesn't have valid variables")
        
        except Exception as err:
            print(err)
            return False
        
        else: 
            print("Data is valid! continuing...")
            return True
    
    def CreatePulpProblem(self, senseInt):
        try:
            self.pulpProblem = pulp.LpProblem(name="Problem", sense=senseInt) #function int is -1 for maximize problems and 1 for minimize
        except Exception as err:
            print(err)
            return False
        else:
            print("Problem created!")
            return True

    def CreatePulpVariables(self):
        self.pulpVars = []
        self.variableNames = []

        try:
            for i in range(len(self.bridge.variableArr)):
                varName = (self.bridge.variableArr[i].varName)
                
                if((self.bridge.variableArr[i].lowerBoundary) == "None" or (self.bridge.variableArr[i].lowerBoundary) == None): lowBound = None
                else: lowBound = int((self.bridge.variableArr[i].lowerBoundary))
                
                if((self.bridge.variableArr[i].upperBoundary) == "None" or (self.bridge.variableArr[i].upperBoundary) == None): upBound = None
                else: upBound = int((self.bridge.variableArr[i].upperBoundary))
                
                category = "Integer"
                variable = pulp.LpVariable(name=varName, lowBound=lowBound,upBound=upBound, cat=category)
                self.variableNames.append(varName.upper())
                self.pulpVars.append(variable)
        
        except Exception as err: 
            print(err)
            return False
        
        else:
            print(f"Pulp variables created!\nVariable count: {len(self.pulpVars)}\n")
            return True
        
    def AddVariables(self):
        try:
            for i in range(len(self.pulpVars)):
                self.pulpProblem.addVariable(self.pulpVars[i])

        except Exception as err:
            print(err)
            return False
        
        else:
            print("Variables added to problem")
            return True

    def GetVariableIndexes(self, constraintVarList):
        self.variableIndex = []

        try:
            for i in range(len(constraintVarList)):
                self.variableIndex.append(self.variableNames.index(constraintVarList[i].upper()))

        except Exception as err:
            print(err)
            return False
        else:
            print("Variable indexes acquired")
            return True
        
    def GetSpecificVarsList(self):
        self.specificVarsList = []
        
        try:
            for i in range (len(self.variableIndex)):
                self.specificVarsList.append(self.pulpVars[self.variableIndex[i]])
        except Exception as err:
            print(err)
            return False
        else:
            print("Created list with variables specific to constraint\n")
            return True
    
    def GetObjectiveVarIndexes(self, objectiveVarList):
        self.objectiveVarsIndex = []

        try:
            for i in range(len(objectiveVarList)):
                self.objectiveVarsIndex.append(self.variableNames.index(objectiveVarList[i].upper()))

        except Exception as err:
            print(err)
            return False
        
        else:
            print("Variable indexes acquired")
            return True

    def GetObjectiveVars(self):
        self.objectiveVariables = []

        try:
            for i in range(len(self.objectiveVarsIndex)):
                self.objectiveVariables.append(self.pulpVars[self.objectiveVarsIndex[i]])
        
        except Exception as err:
            print(err)
            return False
        else:
            print("Created list with variables speific to objective")
            return True

    def SetObjective(self, senseInt, equalToStr):
        try:
            if not(self.GetObjectiveVarIndexes(self.bridge.objective.constraintVariables)): raise Exception("Failed to get Variable Indexes")
            if not(self.GetObjectiveVars()): return Exception("Failed to get variables specific to objective")

            x = self.objectiveVariables
            a = self.bridge.objective.constraintNumModifiers
            lpSense = senseInt
            if(lpSense == 1): self.targetValue = int(self.bridge.objective.lowerBoundary)
            elif(lpSense == -1): self.targetValue = int(self.bridge.objective.upperBoundary)
            elif(lpSense == 0): self.targetValue = int(equalToStr)

            affine = pulp.LpAffineExpression( [x[k],a[k]] for k in range(len(self.objectiveVariables)))
            objectiveVar = pulp.LpConstraintVar(name= "Objective", sense=lpSense, rhs=self.targetValue, e=affine)
            #objectiveVar = pulp.LpConstraintVar(name= "Objective", rhs=targetValue, e=affine)
            
            print(f"LpSense for Objective: {lpSense}")
            print(f"Limit for objective = {self.targetValue}")

            self.pulpProblem.setObjective(objectiveVar)
        
        except Exception as err:
            print(err)
            return False
        
        else:
            print("Added Objective")
            return True

    def CreateConstraints(self): #HAVE TO ADJUST TARGET VALUE
        self.pulpConstraints = []
        self.affinedExpressions = []
        
        try:
            for i in range(len(self.bridge.constraintArr)):
                if not(self.GetVariableIndexes(self.bridge.constraintArr[i].constraintVariables)): raise Exception("Failed to get Variable Indexes")
                if not(self.GetSpecificVarsList()): return Exception("Failed to get variables specific to constraint")

                x = self.specificVarsList
                a = self.bridge.constraintArr[i].constraintNumModifiers
                lpSense = self.bridge.constraintArr[i].lpSense
                if(lpSense == 1): constraintLimit = int(self.bridge.constraintArr[i].lowerBoundary)
                elif(lpSense == -1): constraintLimit = int(self.bridge.constraintArr[i].upperBoundary)
                elif(lpSense == 0): constraintLimit = 990 #TEMPORARY
                else: raise Exception("Invalid LpSense Value")

                affine = pulp.LpAffineExpression( [x[k],a[k]] for k in range(len(self.specificVarsList)))
                self.affinedExpressions.append(affine)
                constraintName = f"Constraint {i}"

                constraintVar = pulp.LpConstraint(name=constraintName, sense=lpSense, rhs=constraintLimit, e=affine)
                self.pulpConstraints.append(constraintVar)

                print(f"Limit for constraint {i}: {constraintLimit}")
                print(f"LpSense for Constraint {i}: {lpSense}")

        except Exception as err:
            print(err)
            return False
        
        else:
            print("Constraints created")
            return True
    
    def ApplyConstraints(self):
        try:
            for i in range(len(self.pulpConstraints)):
                self.pulpProblem += self.pulpConstraints[i]
        
        except Exception as err:
            print(err)
            return False
        
        else:
            print("Constraints applied")
            return True
        
    def SolveProblem(self):
        try:
            status = self.pulpProblem.solve()
        except Exception as err:
            print(err)
            return False
        else:
            return True
        
    def PrintValues(self):
        try:
            for i in range(len(self.pulpVars)):
                print(f"Variable #{i}: {self.pulpVars[i].varValue}")

        except Exception as err:
            print(err)
            return False
        
        else:
            return True



#SAMPLES
    """
def SolveProblemA():
    #DEFINE PROBLEM
    ProblemA = pulp.LpProblem("Problem A", pulp.const.LpMaximize)

    #DEFINE VARIABLES
    A = pulp.LpVariable("A", lowBound = 0, cat = "Integer")
    B = pulp.LpVariable("B", lowBound = 0, cat = "Integer")
    C = pulp.LpVariable("C", lowBound = 0, cat = "Integer")
    D = pulp.LpVariable("D", lowBound = 0, cat = "Integer")

    #DEFINE OBJECTIVE
    ProblemA += (2*A) + B - (3*C) + (5*D)

    #DEFINE CONSTRAINTS
    ProblemA += A + (2*B) + (4*C) - D <= 6
    ProblemA += (2*A) + (3*B) - C + D <= 12
    ProblemA += A + B + C <= 4 

    #SOLVE PROBLEM
    status = ProblemA.solve()

    if(status == 1):
        varA, varB, varC, varD = A.varValue, B.varValue, C.varValue, D.varValue
        maxValue = (2 * varA) + varB - (3 * varC) + (5 * varD)
        
        stringPartOne = "Results for problem #1:\n"
        stringPartTwo = f"A: {varA}\nB: {varB}\nC: {varC}\nD: {varD}\n"
        stringPartThree = f"Max value : {maxValue}\n\n"
        result = f"{stringPartOne}{stringPartTwo}{stringPartThree}"

        return result
    else:
        stringPartOne = "Couldn't find optimal result for problem #1\n"
        stringPartTwo = f"Status: {pulp.LpSolution[status]}"
        result = f"{stringPartOne}{stringPartTwo}"

        return result
"""
#SAMPLES


