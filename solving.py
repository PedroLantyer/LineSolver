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

    def SetObjective(self, objectiveStr, lowBoundEnabled, upBoundEnabled, lowBoundStr, upBoundStr):
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
        
    def CreatePulpVariables(self):
        pulpVars = []

        try:
            for i in range(len(self.bridge.variableArr)):
                varName = (self.bridge.variableArr[i].varName)
                
                if((self.bridge.variableArr[i].lowerBoundary) == "None" or (self.bridge.variableArr[i].lowerBoundary) == None): lowBound = None
                else: lowBound = int((self.bridge.variableArr[i].lowerBoundary))
                
                if((self.bridge.variableArr[i].upperBoundary) == "None" or (self.bridge.variableArr[i].upperBoundary) == None): upBound = None
                else: upBound = int((self.bridge.variableArr[i].upperBoundary))
                
                category = "Integer"
                variable = pulp.LpVariable(name=varName, lowBound=lowBound,upBound=upBound, cat=category)
                pulpVars.append(variable)
        
        except Exception as err: 
            print(err)
            return False
        
        else:
            print(f"Pulp variables created!\nVariable count: {len(pulpVars)}\n")
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


