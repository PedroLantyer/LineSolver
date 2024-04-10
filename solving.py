from bifrost import DataBridge
import pulp

class Solver:

    def __init__(self) -> None:
        self.bridge = DataBridge()
        pass

    def ValidateData(self):
        try:
            if not(self.bridge.ConstraintHasValidVariables()): raise Exception("One or more constraints don't have valid variables")
        
        except Exception as err:
            print(err)
            return False
        
        else: 
            print("Constraints are valid, continuing...")
            return True


