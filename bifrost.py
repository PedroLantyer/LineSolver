from dataValidations import TextVerifications

class Boundaries:
    def __init__(self) -> None:
        pass

    def GetBoundaries(self, lowBoundEnabled, upBoundEnabled, lowBoundStr, upBoundStr):
        boundaries = []
        if(lowBoundEnabled == 0):
            boundaries.append(None)
        else:
            boundaries.append(lowBoundStr)

        if(upBoundEnabled == 0):
            boundaries.append(None)
        else:
            boundaries.append(upBoundStr)

        return boundaries

class Constraint:
    constraintVariables = []
    constraintPieces = []
    constraintNumModifiers = []
    upperBoundary = ""
    lowerBoundary = ""
    textForm = ""
    isObjective = False
    lpSense = -1

    def __init__(self, isObjective) -> None:
        self.isObjective = isObjective
        pass

    def InitializeClasses(self):
        self.textVerifications = TextVerifications()
        self.bridge = DataBridge()

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
    
    def SetLpSense(self):
        try:
            self.lpSense = self.bridge.GetLpSense()
        except Exception as err:
            print(f"Failed to change LpSense\n{err}")
        else:
            print(f"Changed LpSense to {self.lpSense}")
        

    def SetUpperBoundary(self, upBound):
        try:
            value = str(upBound)
            self.upperBoundary = value
            print("Upper Boundary set to: %s" % self.upperBoundary)
        except:
            print("Failed to set Upper Boundary")

    def ExtractPieces(self):
        var = ""
        num = ""
        previousChar = ''

        if(len(self.constraintPieces) > 0): self.constraintPieces.clear()
        if(len(self.constraintNumModifiers) > 0): self.constraintNumModifiers.clear()
        if(len(self.constraintVariables) > 0) :self.constraintVariables.clear()
        self.InitializeClasses()
        for i in range(len(self.textForm)):
            
            char = self.textForm[i]

            if(self.textVerifications.isOperator(char)):
                
                if(previousChar.isnumeric()):
                    self.constraintPieces.append(num)
                    self.constraintNumModifiers.append(int(num))
                    num = ""
                
                elif(previousChar.isalpha()):
                    self.constraintPieces.append(var)
                    self.constraintVariables.append(var)
                    var = ""
                
                if(char != '-'): self.constraintPieces.append(char)
            
            elif(char.isalpha()):
                if(len(previousChar) == 0):
                    self.constraintPieces.append("1")
                    self.constraintNumModifiers.append(1)

                if(previousChar.isnumeric()):
                    self.constraintPieces.append(num)
                    self.constraintNumModifiers.append(int(num))
                    num = ""

                elif(previousChar == '-'):
                    self.constraintPieces.append("-1")
                    self.constraintNumModifiers.append(-1)
                
                elif(self.textVerifications.isOperator(previousChar)):
                    self.constraintPieces.append("1")
                    self.constraintNumModifiers.append(1)
                
                var += char
            
            elif(char.isnumeric):
                if(previousChar.isalpha()):
                    self.constraintPieces.append(var)
                    self.constraintVariables.append(var)
                    var = ""
                elif(previousChar == '-'):
                    num += previousChar
                num += char
            
            previousChar = char
            
        
        if(len(num) > 0):
            self.constraintPieces.append(num)
            num = ""
        elif(len(var) > 0):
            self.constraintPieces.append(var)
            self.constraintVariables.append(var)
            var = ""

    def GetPieces(self):
        print("\nPieces:")
        for item in self.constraintPieces:
            print(item, end=" ")
        print("\n\n")

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
    variableNames = []
    lpSense = -1

    def __init__(self) -> None:
        pass

    def SetLpSense(self, lpSenseInt):
        try:
            self.lpSense = lpSenseInt
        except Exception as err:
            print(err)
        else:
            print(f"LpSense changed to {self.lpSense}")
    
    def GetLpSense(self):
        return self.lpSense

    def SetVariable(self, variable):
        try:
            self.variableArr.append(variable)
            self.variableNames.append(variable.varName.upper())
            print(f"\nVariable \"{variable.varName}\" added at index: {self.GetVarArrSize()}")
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
            if(constraint.isObjective == True): raise Exception("This function can only be used to add Constraints")
            self.constraintArr.append(constraint)
            print(f"\nConstraint added at index: {len(self.constraintArr)}")
        
        except Exception as err:
            print(err)
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
    
    def ConstraintHasValidVariables(self):
        try:
            for i in range(len(self.constraintArr)):
                for j in range(len(self.constraintArr[i].constraintVariables)):
                    if (self.variableNames.count(self.constraintArr[i].constraintVariables[j].upper())) == 0: raise Exception(f"Variable {self.constraintArr[i].constraintVariables[j]} not found")
        
        except Exception as err:
            print(err)
            return False
        
        else:
            return True
        
    def SetObjective(self, objective):
        try:
            self.objective = objective
            print(f"\nObjective \"{objective.textForm}\" set!")
        except:
            print("Failed to add objective")

    def ObjectiveHasValidVariables(self):
        try:
            for i in range(len(self.objective.constraintVariables)):
                if (self.variableNames.count(self.objective.constraintVariables[i].upper())) == 0: raise Exception(f"Variable {self.objective[0].constraintVariables[i]} not found")
        
        except Exception as err:
            print(err)
            return False
        
        else:
            return True