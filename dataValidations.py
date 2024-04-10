class BoundaryValidations:
    def __init__(self) -> None:
         pass
        
    def ValidLowerBoundary(self, infLowerBoundary, lowBoundStr):
        #TEMP
        print("Value: %d" % infLowerBoundary)
        #TEMP
        if(infLowerBoundary == 0):
            if (lowBoundStr.isnumeric()):
                return True
            
            else:
                print("Invalid Lower Boundary Value Must Be Number")                    
                return False
            
        else:
            return True
        
    def ValidUpperBoundary(self, infUpperBoundary, upBoundStr):
        #TEMP
        print("Value: %d" % infUpperBoundary)
        #TEMP
        if(infUpperBoundary == 0):
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