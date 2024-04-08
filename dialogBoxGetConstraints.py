import tkinter as tk
import styles
from bifrost import DataBridge

class GetConstraintsWindow:
    master = None

    def __init__(self) -> None:
        #CREATE WINDOW
        self.dialog = tk
        self.top = self.dialog.Toplevel(self.master)
        
        self.InitializeElements()

    def InitializeElements(self):
        #INITIALIZE DATA BRIDGE CLASS
        bridge = DataBridge()

        #GET DESIGNER CLASSES
        frameStyles = styles.GetVarDialog()
        labelStyles = styles.Label()
        entryStyles = styles.Entry()
        checkBoxStyles = styles.CheckBox()
        buttonStyles = styles.Button()

        #CREATE FRAME
        frame = self.dialog.Frame(self.top, borderwidth=2, relief='ridge', bg=frameStyles.bgColor)
        frame.pack(fill='both', expand=True)

        #CREATE TK VARIABLES
        currentConstraintValue = tk.StringVar(value="")
        infLowerBoundaryStatus = tk.IntVar(value=0)
        infUpperBoundaryStatus = tk.IntVar(value=0)
        lowerBoundary = tk.IntVar(value=0)
        upperBoundary = tk.IntVar(value=0)
        lowerBoundaryTemp = tk.StringVar(value="")
        upperBoundaryTemp = tk.IntVar(value="")

        #CREATE LABELS
        labelInsertLowerBoundary = self.dialog.Label(frame, text="Lower Boundary:", bg=labelStyles.bgColor, fg=labelStyles.fgColor, font=[labelStyles.font, labelStyles.fontSize])
        labelInsertExpression = self.dialog.Label(frame, text="Expression:", bg=labelStyles.bgColor, fg=labelStyles.fgColor, font=[labelStyles.font, labelStyles.fontSize])
        labelInsertUpperBoundary = self.dialog.Label(frame, text="Upper Boundary:", bg=labelStyles.bgColor, fg=labelStyles.fgColor, font=[labelStyles.font, labelStyles.fontSize])

        #CREATE TEXTBOXES
        entryLowBound = self.dialog.Entry(frame, bg=entryStyles.bgColor, fg= entryStyles.fgColor, disabledbackground=entryStyles.disabledBgColor, disabledforeground= entryStyles.disabledFgColor, font=[labelStyles.font, labelStyles.fontSize])
        entryConstraintExpression = self.dialog.Entry(frame, bg=entryStyles.bgColor, fg= entryStyles.fgColor, disabledbackground=entryStyles.disabledBgColor, disabledforeground= entryStyles.disabledFgColor, font=[labelStyles.font, labelStyles.fontSize])
        entryUpBound = self.dialog.Entry(frame, bg=entryStyles.bgColor, fg= entryStyles.fgColor, disabledbackground=entryStyles.disabledBgColor, disabledforeground= entryStyles.disabledFgColor, font=[labelStyles.font, labelStyles.fontSize])

        #FUNCTIONS TO SET INF BOUNDARY STATUS
        def SetInfLowerBoundaryStatus():
            if (infLowerBoundaryStatus.get() == 1):
                entryLowBound.delete(0, tk.END)
                entryLowBound.config(state="disabled")
            else:
                entryLowBound.config(state="normal")

        def SetInfUpperBoundaryStatus():
            if (infUpperBoundaryStatus.get() == 1):
                entryUpBound.delete(0, tk.END)
                entryUpBound.config(state="disabled")
            else:
                entryUpBound.config(state="normal")

        #CREATE CHECKBOXES
        checkBoxInfLowerBoundary = self.dialog.Checkbutton(frame, text="Inf Lower Boundary", bg=checkBoxStyles.bgColor, fg=checkBoxStyles.fgColor, font=[checkBoxStyles.font, checkBoxStyles.fontSize], variable=infLowerBoundaryStatus, offvalue=0, onvalue=1, command=SetInfLowerBoundaryStatus)
        checkBoxInfUpperBoundary = self.dialog.Checkbutton(frame, text="Inf Upper Boundary", bg=checkBoxStyles.bgColor, fg=checkBoxStyles.fgColor, font=[checkBoxStyles.font, checkBoxStyles.fontSize], variable=infUpperBoundaryStatus, offvalue=0, onvalue=1, command=SetInfUpperBoundaryStatus)

        #CREATE FUNCTIONS TO VERIFY VALUES
        def ValidLowerBoundary():
            if(infLowerBoundaryStatus.get() == 0):
                if (entryLowBound.get().isnumeric()):
                    lowerBoundary.set(int(entryLowBound.get()))
                    print(f"Lower Boundary value set to {lowerBoundary.get()}")
                    return True
                
                else:
                    print("Invalid Lower Boundary Value Must Be Number")                    
                    return False
            
            else:
                return True
            
        def ValidUpperBoundary():
            if(infUpperBoundaryStatus.get() == 0):
                if(entryUpBound.get().isnumeric()):
                    upperBoundary.set(int(entryUpBound.get()))
                    print(f"Upper Boundary value set to {upperBoundary.get()}")
                
                else:
                    print("Invalid Upper Boundary Value")
                    return False
            else:
                return True
            
        def ValidConstraintValue():
            if(len(currentConstraintValue.get().strip()) > 0):
                #CONSTRAINT VERIFICATION -> WORK IN PROGRESS
                return True
            else:
                print("User attempted to add empty constraint")
                return False
            
        def GetBoundaries(): #USED ONLY INSIDE PassVariable()
            boundaries = []
            if(infLowerBoundaryStatus.get() == 1):
                boundaries.append(None)
            else:
                boundaries.append(lowerBoundary.get())

            if(infUpperBoundaryStatus.get() == 1):
                boundaries.append(None)
            else:
                boundaries.append(upperBoundary.get())

            return boundaries
            
        #CREATE FUNCTION FOR PASSING DATA
        def PassVariable():
            currentConstraintValue.set(entryConstraintExpression.get())

            if(bridge.ConstraintAlreadyExists(constraint=currentConstraintValue.get())):
                print("User attempted to add a constraint that already exists")

            else:
                if(infLowerBoundaryStatus.get() == 1 and infUpperBoundaryStatus.get() == 1):
                    print("Constraint can't have both boundaries set to infinite")

                elif(ValidConstraintValue() and ValidLowerBoundary() and ValidUpperBoundary()):
                    bridge.SetConstraint(currentConstraintValue.get())
                    boundaries = GetBoundaries()
                    bridge.SetBoundariesForConstraint(boundaries=boundaries)
                    self.top.destroy()
                
                else:
                    print("Cannot pass down data under current circumstances")

        #CREATE BUTTON
        buttonSubmit = self.dialog.Button(frame, text="Add", bg=buttonStyles.bgColor, fg=buttonStyles.fgColor, font=[buttonStyles.font, buttonStyles.fontSize], relief=buttonStyles.relief, command=PassVariable)

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