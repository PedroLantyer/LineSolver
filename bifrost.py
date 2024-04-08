class DataBridge:
    variableArr = []
    variableBoundaries = []
    constraintArr = []
    constraintLowerLimits = []
    constraintUpperLimits = []

    def __init__(self) -> None:
        pass
    
    def SetVariable(self, variable):
        self.variableArr.append(variable)
        print(f"\nVariable set to: {variable}")
        print(f"Current Array Length: {len(self.variableArr)}")

    def SetBoundariesForVariable(self, boundaries):
        self.variableBoundaries.append(boundaries)
        print(f"\nBoundaries added at index: {len(self.variableArr)}")
        print(f"Values:\nLower Boundary: {boundaries[0]}\nUpper Boundary: {boundaries[1]}")
    
    def VarAlreadyExists(self, variable):
        for item in self.variableArr:
            if(variable == item): return True
        return False
    
    def ClearVarArray(self):
        self.variableArr.clear()
        print("Cleared variable array")

    def SetConstraint(self, constraintExp):
        self.constraintArr.append(constraintExp)
        print(f"\nConstraint added at inded: {len(self.constraintArr)}")
        print(f"Value:{constraintExp}")

    def SetBoundariesForConstraint(self, boundaries):
        self.constraintLowerLimits.append(boundaries[0])
        self.constraintUpperLimits.append(boundaries[1])
        print(f"\nConstraint lower limit addead at index: {len(self.constraintLowerLimits)}")
        print(f"Constraint upper limit addead at index: {len(self.constraintUpperLimits)}")
        print(f"Values:\nLower Boundary: {boundaries[0]}\nUpper Boundary: {boundaries[1]}")

    def ConstraintAlreadyExists(self, constraint):
        for item in self.constraintArr:
            if(constraint == item): return True
        return False