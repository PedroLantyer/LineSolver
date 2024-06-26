import tkinter as tk
import styles
from bifrost import DataBridge
from bifrost import Constraint
from bifrost import Boundaries
from dataValidations import BoundaryValidations
from dataValidations import ConstraintValidations

class GetConstraintsWindow:
    master = None

    def __init__(self) -> None:
        #CREATE WINDOW
        self.dialog = tk
        self.top = self.dialog.Toplevel(self.master)

        self.InitializeTkVars()
        self.InitializeClasses()
        
        self.InitializeElements()
    
    def InitializeClasses(self):
        self.bridge = DataBridge()
        self.constraint = Constraint(isObjective=False)
        self.boundaries = Boundaries()
        self.boundValid = BoundaryValidations()
        self.constraintValid = ConstraintValidations()

    def InitializeTkVars(self):
        self.currentConstraintValue = tk.StringVar(value="")
        self.lowBoundEnabled = tk.IntVar(value=1)
        self.upBoundEnabled = tk.IntVar(value=0)

    def ClearValues(self):
        self.constraint.constraintVariables.clear()
        self.constraint.constraintPieces.clear()
        self.constraint.constraintNumModifiers.clear()
        self.currentConstraintValue.set("")

    def AddConstraint(self, constraintStr, lowBoundStr, upBoundStr):
        
        try:
            self.ClearValues()
            self.currentConstraintValue.set(constraintStr)
            if(self.lowBoundEnabled.get() == 0 and self.upBoundEnabled.get() == 0): raise Exception("Constraint can't have both boundaries set to infinite")
            if(self.bridge.ConstraintAlreadyExists(self.currentConstraintValue.get())): raise Exception(print("User tried to add constraint that already exists"))
            if not(self.constraintValid.ValidConstraintValue(self.currentConstraintValue.get())): raise Exception("Constraint value isn't valid")
            if not(self.boundValid.ValidLowerBoundary(self.lowBoundEnabled.get(), lowBoundStr)): raise Exception("Lower Boundary isn't valid")
            if not(self.boundValid.ValidUpperBoundary(self.upBoundEnabled.get(), upBoundStr)): raise Exception("Upper Boundary isn't valid")
            if (self.boundValid.CheckBoundariesAreEqual(lowBoundStr, upBoundStr)): raise Exception("Upper and Lower Boundaries can't both have the same value")

            self.constraint.SetConstraintText(self.currentConstraintValue.get())
            boundaries = self.boundaries.GetBoundaries(self.lowBoundEnabled.get(), self.upBoundEnabled.get(),lowBoundStr, upBoundStr)
            self.constraint.SetLowerBoundary(boundaries[0])
            self.constraint.SetUpperBoundary(boundaries[1])
            self.constraint.ExtractPieces()
            self.constraint.GetPieces()
            self.constraint.SetLpSense()
            self.bridge.SetConstraint(self.constraint)
            self.bridge.GetConstraintArraySize()
            self.top.destroy()
                    
        except Exception as err: print(err)
    
    def SetInfLowerBoundaryStatus(self, entryLowBound):
        if (self.lowBoundEnabled.get() == 0):
            entryLowBound.delete(0, tk.END)
            entryLowBound.config(state="disabled")
        else:
            entryLowBound.config(state="normal")
            entryLowBound.insert(0, "0")

    def SetInfUpperBoundaryStatus(self, entryUpBound):
        if (self.upBoundEnabled.get() == 0):
            entryUpBound.delete(0, tk.END)
            entryUpBound.config(state="disabled")
        else:
            entryUpBound.config(state="normal")
            entryUpBound.insert(0, "0")

    def InitializeElements(self):
        #GET DESIGNER CLASSES
        frameStyles = styles.GetVarDialog()
        labelStyles = styles.Label()
        entryStyles = styles.Entry()
        checkBoxStyles = styles.CheckBox()
        buttonStyles = styles.Button()

        #CREATE FRAME
        frame = self.dialog.Frame(self.top, borderwidth=2, relief='ridge', bg=frameStyles.bgColor)
        frame.pack(fill='both', expand=True)

        #CREATE LABELS
        labelInsertExpression = self.dialog.Label(frame, text="Expression:", bg=labelStyles.bgColor, fg=labelStyles.fgColor, font=[labelStyles.font, labelStyles.fontSize])

        #CREATE TEXTBOXES
        entryLowBound = self.dialog.Entry(frame, bg=entryStyles.bgColor, fg= entryStyles.fgColor, disabledbackground=entryStyles.disabledBgColor, disabledforeground= entryStyles.disabledFgColor, font=[labelStyles.font, labelStyles.fontSize], justify=entryStyles.justify)
        entryLowBound.insert(0, "0")
        entryConstraintExpression = self.dialog.Entry(frame, bg=entryStyles.bgColor, fg= entryStyles.fgColor, disabledbackground=entryStyles.disabledBgColor, disabledforeground= entryStyles.disabledFgColor, font=[labelStyles.font, labelStyles.fontSize], justify=entryStyles.justify)
        entryUpBound = self.dialog.Entry(frame, bg=entryStyles.bgColor, fg= entryStyles.fgColor, disabledbackground=entryStyles.disabledBgColor, disabledforeground= entryStyles.disabledFgColor, font=[labelStyles.font, labelStyles.fontSize], justify=entryStyles.justify, state="disabled")

        #FUNCTIONS FOR THE CHECKBOXES

        def InfLowerBoundaryChange():
            self.SetInfLowerBoundaryStatus(entryLowBound)

        def InfUpperBoundaryChange():
            self.SetInfUpperBoundaryStatus(entryUpBound)

        #CREATE CHECKBOXES
        checkBoxInfLowerBoundary = self.dialog.Checkbutton(frame, text="Lower Boundary", bg=checkBoxStyles.bgColor, fg=checkBoxStyles.fgColor, font=[checkBoxStyles.font, checkBoxStyles.fontSize], variable=self.lowBoundEnabled, offvalue=0, onvalue=1, command=InfLowerBoundaryChange)
        checkBoxInfUpperBoundary = self.dialog.Checkbutton(frame, text="Upper Boundary", bg=checkBoxStyles.bgColor, fg=checkBoxStyles.fgColor, font=[checkBoxStyles.font, checkBoxStyles.fontSize], variable=self.upBoundEnabled, offvalue=0, onvalue=1, command=InfUpperBoundaryChange)

        #FUNCTION FOR THE SUBMIT BUTTON
        def buttonSubmitOnClick():
            self.AddConstraint(entryConstraintExpression.get(), entryLowBound.get(), entryUpBound.get())

        #CREATE BUTTON
        buttonSubmit = self.dialog.Button(frame, text="Add", bg=buttonStyles.bgColor, fg=buttonStyles.fgColor, font=[buttonStyles.font, buttonStyles.fontSize], relief=buttonStyles.relief, command=buttonSubmitOnClick)

        #PLACE ELEMENTS

        labelInsertExpression.pack()
        entryConstraintExpression.pack()
        checkBoxInfLowerBoundary.pack()
        entryLowBound.pack()
        checkBoxInfUpperBoundary.pack()
        entryUpBound.pack()
        buttonSubmit.pack()