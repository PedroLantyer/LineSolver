class BoundaryValidations:
    def __init__(self) -> None:
         pass
        
    def ValidLowerBoundary(self, lowEnabled, lowBoundStr):
        if(lowEnabled == 1):
            if (lowBoundStr.isnumeric()): return True
            
            else:
                print("Invalid Lower Boundary Value Must Be Number")                    
                return False
            
        else: return True
        
    def ValidUpperBoundary(self, upBoundEnabled, upBoundStr):
        if(upBoundEnabled == 1):
            if (upBoundStr.isnumeric()): return True
            
            else:
                print("Invalid Upper Boundary! Value Must Be Number")                    
                return False
            
        else: return True

class ConstraintValidations:

    def __init__(self) -> None:
        self.textVerification = TextVerifications()
        pass

    def ValidConstraintValue(self, constraintStr):
        try:
            if(len(constraintStr.strip()) == 0): raise Exception("User Attempted to add empty constraint")
            previousChar = ''
            operatorCount, charCount, numCount = 0, 0, 0

            for char in constraintStr:

                if (char.isalpha()): charCount += 1 
                elif(self.textVerification.isOperator(char)): operatorCount += 1
                elif(char.isnumeric()): numCount += 1
                else: raise Exception("Constraint must be a collection of letters, numbers and operators with no whitespaces\nValid operators are: +, -, *, /")

                if(len(previousChar) == 0):
                    if(self.textVerification.isOperator(char) and (char != '-')): raise Exception("Invalid Constraint")

                else:
                    if(self.textVerification.isOperator(previousChar) and self.textVerification.isOperator(char)): raise Exception("Invalid Constraint")
                    if(char.isnumeric() and previousChar.isalpha()): raise Exception("Invalid Constraint")
                    if(char.isalpha() and previousChar.isnumeric()): raise Exception("Invalid Constraint")

                previousChar=char

            if (charCount == 0): raise Exception("Constrain must contain at least one variable.")
            if (charCount < 2 and numCount == 0): raise Exception("Constraints that don't contain any numbers must include at least two variables")
            if (operatorCount == 0): raise Exception("All constraints must include at least one operator")
            
        except Exception as err:
            print(err)
            return False
        
        else: return True
        
class VariableValidations:
    def __init__(self) -> None:
        pass
    
    def ValidVariableValue(self, variableStr):
        try:
            if(len(variableStr.strip()) == 0): raise Exception("User attempted to add empty variable")
            if not(variableStr.isalpha()): raise Exception("Variable must contain one or more letter with no whitespaces")
        
        except Exception as err:
            print(err)
            return False
        
        else: return True

class TextVerifications:
    operators = ['+','-','*', '/']
    
    def __init__(self) -> None:
        pass

    def isOperator(self, ch):
        for operator in self.operators:
            if ch is operator: return True
        return False
