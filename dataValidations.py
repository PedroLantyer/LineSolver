class BoundaryValidations:
    def __init__(self) -> None:
         pass
        
    def ValidLowerBoundary(self, lowEnabled, lowBoundStr):
        if(lowEnabled == 1):
            if (lowBoundStr.isnumeric()):
                return True
            
            else:
                print("Invalid Lower Boundary Value Must Be Number")                    
                return False
            
        else:
            return True
        
    def ValidUpperBoundary(self, upBoundEnabled, upBoundStr):
        if(upBoundEnabled == 1):
            if (upBoundStr.isnumeric()):
                return True
            
            else:
                print("Invalid Upper Boundary! Value Must Be Number")                    
                return False
            
        else:
            return True
    
    def ValidConstraintValue(self, constraintStr):
        if(len(constraintStr.strip()) > 0):
            #CONSTRAINT VERIFICATION -> WORK IN PROGRESS
            return True
        else:
            print("User attempted to add empty constraint")
            return False
        
class VariableValidations:
    def ValidVariableValue(self, variableStr):
        if(len(variableStr.strip()) > 0):
            if(variableStr.isalpha()):
                return True
                #VARIABLE VERIFICATION -> WORK IN PROGRESS
            else:
                print("Invalid Variable Name")
                return False
        else:
            print("User attempted to add empty variable")
            return False