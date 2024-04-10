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

        except Exception as err: print(err)

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
        



