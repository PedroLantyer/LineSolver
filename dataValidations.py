class BoundaryValidations:
    def __init__(self) -> None:
         pass
        
    def ValidLowerBoundary(self, infLowerBoundary, lowBoundStr):
        if(infLowerBoundary == 0):
            if (lowBoundStr.isnumeric()):
                return True
            
            else:
                print("Invalid Lower Boundary Value Must Be Number")                    
                return False
            
        else:
            return True
        
    def ValidUpperBoundary(self, infUpperBoundary, upBoundStr):
        if(infUpperBoundary == 0):
            if (upBoundStr.isnumeric()):
                return True
            
            else:
                print("Invalid Upper Boundary! Value Must Be Number")                    
                return False
            
        else:
            return True