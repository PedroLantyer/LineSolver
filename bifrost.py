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

class Variable:
    lowerBoundary = ""
    upperBoundary = ""
    varName = ""
    
    def __init__(self) -> None:
        pass

    def SetVariableName(self, name):
        try:
            self.varName = name
            print("Variable Name set to: %s" % self.varName)
        except:
            print("Failed to set variable")

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
    constraintArr = []

    def __init__(self) -> None:
        pass
    
    def SetVariable(self, variable):
        try:
            self.variableArr.append(variable)
            print(f"\nVariable added at index: {self.GetVarArrSize()}")
        except:
            print("Failed to add variable")
    
    def VarAlreadyExists(self, variable):
        for i in range(len(self.variableArr)):
            if(variable.upper() == self.variableArr[i].varName.upper()): return True
        
        return False

    def ConstraintAlreadyExists(self, constraint):
        for i in range(len(self.constraintArr)):
            if(constraint.upper() == self.constraintArr[i].textForm.upper()): return True
        
        return False

    def SetConstraint(self, constraint):
        try:
            self.constraintArr.append(constraint)
            print(f"\nConstraint added at index: {self.GetConstraintArraySize()}")
        except:
            print("Failed to add constraint")

    def GetConstraintArraySize(self):
        print("Constraint Array Size: %d" %len(self.constraintArr))

    def GetVarArrSize(self):
        return (len(self.variableArr))
    
    def GetVariables(self):
        varTextArr = []

        for i in range(len(self.variableArr)):
            str = ""
            if(self.variableArr[i].lowerBoundary != "None"): str += f"{self.variableArr[i].lowerBoundary} <= "
            str += (self.variableArr[i].varName)
            if(self.variableArr[i].upperBoundary != "None"): str += f" <= {self.variableArr[i].upperBoundary}"
            varTextArr.append(str)

        return varTextArr

    def GetConstraints(self):
        constraintTextArr = []

        for i in range(len(self.constraintArr)):
            str = ""
            if(self.constraintArr[i].lowerBoundary != "None"): str += f"{self.constraintArr[i].lowerBoundary} <= "
            str += (self.constraintArr[i].textForm)
            if(self.constraintArr[i].upperBoundary != "None"): str += f" <= {self.constraintArr[i].upperBoundary}"

            constraintTextArr.append(str)
        return  constraintTextArr