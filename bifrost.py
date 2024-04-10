class Constraint:
    constraintVariables = []
    variableModifiers = []
    upperBoundary = ""
    lowerBoundary = ""
    textForm = ""
    
    def __init__(self) -> None:
        pass

    def SetConstraintText(self, constraintTxt):
        try:
            self.textForm = constraintTxt
            print("Constraint text set to: %s" % self.textForm)
        except:
            print("Failed to set constraint")

    def SetLowerBoundary(self, lowBound):
        try:
            value = str(lowBound)
            self.lowerBoundary = value
            print("Lower Boundary set to: %s" % self.lowerBoundary)
        except:
            print("Failed to set Lower Boundary")
        
    def SetUpperBoundary(self, upBound):
        try:
            value = str(upBound)
            self.upperBoundary = value
            print("Upper Boundary set to: %s" % self.upperBoundary)
        except:
            print("Failed to set Upper Boundary")

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

    def SetConstraint(self, constraint):
        try:
            self.constraintArr.append(constraint)
            print(f"\nConstraint added at inded: {len(self.constraintArr)}")
        except:
            print("Failed to add constraint")

    def GetConstraintArraySize(self):
        print("Constraint Array Size: %d" %len(self.constraintArr))

    def GetVarArrSize(self):
        return (len(self.variableArr))
    
    def GetVariables(self):
        return (self.variableArr)
    
    def GetConstraints(self):
        constraintTextArr = []
        for i in range(len(self.constraintArr)):
            constraintTextArr.append(self.constraintArr[i].textForm)
        return  constraintTextArr