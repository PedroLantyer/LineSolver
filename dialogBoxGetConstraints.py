import tkinter as tk
import styles
from bifrost import DataBridge
from bifrost import Constraint
from dataValidations import BoundaryValidations

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
        self.constraint = Constraint()
        self.boundValid = BoundaryValidations()

    def InitializeTkVars(self):
        self.currentConstraintValue = tk.StringVar(value="")
        self.infLowerBoundaryStatus = tk.IntVar(value=0)
        self.infUpperBoundaryStatus = tk.IntVar(value=0)

    def GetBoundaries(self, infLowerBoundaryStatus, infUpperBoundaryStatus, lowBoundStr, upBoundStr):
        boundaries = []
        if(infLowerBoundaryStatus == 1):
            boundaries.append(None)
        else:
            boundaries.append(lowBoundStr)

        if(infUpperBoundaryStatus == 1):
            boundaries.append(None)
        else:
            boundaries.append(upBoundStr)

        return boundaries

    def AddConstraint(self, constraintStr, lowBoundStr, upBoundStr, infLowerBoundary, infUpperBoundary):
        self.currentConstraintValue.set(constraintStr)

        #if(self.infLowerBoundaryStatus.get() == 1 and self.infUpperBoundaryStatus.get() == 1):
        if(infLowerBoundary == 1 and infUpperBoundary == 1):
            print("Constraint can't have both boundaries set to infinite")

        #elif(self.boundValid.ValidConstraintValue(self.currentConstraintValue.get()) and self.boundValid.ValidLowerBoundary(self.infLowerBoundaryStatus.get(), lowBoundStr) and self.boundValid.ValidUpperBoundary(self.infLowerBoundaryStatus.get(), upBoundStr)):
        elif(self.boundValid.ValidConstraintValue(self.currentConstraintValue.get()) and self.boundValid.ValidLowerBoundary(infLowerBoundary, lowBoundStr) and self.boundValid.ValidUpperBoundary(infUpperBoundary, upBoundStr)):
            self.constraint.SetConstraintText(self.currentConstraintValue.get())
            boundaries = self.GetBoundaries(infLowerBoundary, infUpperBoundary, lowBoundStr, upBoundStr)
            self.constraint.SetLowerBoundary(boundaries[0])
            self.constraint.SetUpperBoundary(boundaries[1])
            self.bridge.SetConstraint(self.constraint)
            self.bridge.GetConstraintArraySize()
            self.top.destroy()
                    
        else:
            print("Cannot pass down data under current circumstances")

            #FUNCTIONS TO SET INF BOUNDARY STATUS
    
    def SetInfLowerBoundaryStatus(self, entryLowBound):
        if (self.infLowerBoundaryStatus.get() == 1):
            entryLowBound.delete(0, tk.END)
            entryLowBound.config(state="disabled")
        else:
            entryLowBound.config(state="normal")

    def SetInfUpperBoundaryStatus(self, entryUpBound):
        if (self.infUpperBoundaryStatus.get() == 1):
            entryUpBound.delete(0, tk.END)
            entryUpBound.config(state="disabled")
        else:
            entryUpBound.config(state="normal")

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
        labelInsertLowerBoundary = self.dialog.Label(frame, text="Lower Boundary:", bg=labelStyles.bgColor, fg=labelStyles.fgColor, font=[labelStyles.font, labelStyles.fontSize])
        labelInsertExpression = self.dialog.Label(frame, text="Expression:", bg=labelStyles.bgColor, fg=labelStyles.fgColor, font=[labelStyles.font, labelStyles.fontSize])
        labelInsertUpperBoundary = self.dialog.Label(frame, text="Upper Boundary:", bg=labelStyles.bgColor, fg=labelStyles.fgColor, font=[labelStyles.font, labelStyles.fontSize])

        #CREATE TEXTBOXES
        entryLowBound = self.dialog.Entry(frame, bg=entryStyles.bgColor, fg= entryStyles.fgColor, disabledbackground=entryStyles.disabledBgColor, disabledforeground= entryStyles.disabledFgColor, font=[labelStyles.font, labelStyles.fontSize])
        entryConstraintExpression = self.dialog.Entry(frame, bg=entryStyles.bgColor, fg= entryStyles.fgColor, disabledbackground=entryStyles.disabledBgColor, disabledforeground= entryStyles.disabledFgColor, font=[labelStyles.font, labelStyles.fontSize])
        entryUpBound = self.dialog.Entry(frame, bg=entryStyles.bgColor, fg= entryStyles.fgColor, disabledbackground=entryStyles.disabledBgColor, disabledforeground= entryStyles.disabledFgColor, font=[labelStyles.font, labelStyles.fontSize])

        #FUNCTIONS FOR THE CHECKBOXES

        def InfLowerBoundaryChange():
            self.SetInfLowerBoundaryStatus(entryLowBound)

        def InfUpperBoundaryChange():
            self.SetInfUpperBoundaryStatus(entryUpBound)

        #CREATE CHECKBOXES
        checkBoxInfLowerBoundary = self.dialog.Checkbutton(frame, text="Inf Lower Boundary", bg=checkBoxStyles.bgColor, fg=checkBoxStyles.fgColor, font=[checkBoxStyles.font, checkBoxStyles.fontSize], variable=self.infLowerBoundaryStatus, offvalue=0, onvalue=1, command=InfLowerBoundaryChange)
        checkBoxInfUpperBoundary = self.dialog.Checkbutton(frame, text="Inf Upper Boundary", bg=checkBoxStyles.bgColor, fg=checkBoxStyles.fgColor, font=[checkBoxStyles.font, checkBoxStyles.fontSize], variable=self.infUpperBoundaryStatus, offvalue=0, onvalue=1, command=InfUpperBoundaryChange)


        #FUNCTION FOR THE SUBMIT BUTTON
        def buttonSubmitOnClick():
            self.AddConstraint(entryConstraintExpression.get(), entryLowBound.get(), entryUpBound.get(), self.infLowerBoundaryStatus.get(), self.infUpperBoundaryStatus.get())

        #CREATE BUTTON
        buttonSubmit = self.dialog.Button(frame, text="Add", bg=buttonStyles.bgColor, fg=buttonStyles.fgColor, font=[buttonStyles.font, buttonStyles.fontSize], relief=buttonStyles.relief, command=buttonSubmitOnClick)

        #PLACE ELEMENTS

        labelInsertLowerBoundary.pack()
        entryLowBound.pack()
        labelInsertExpression.pack()
        entryConstraintExpression.pack()
        labelInsertUpperBoundary.pack()
        entryUpBound.pack()
        checkBoxInfLowerBoundary.pack()
        checkBoxInfUpperBoundary.pack()
        buttonSubmit.pack()