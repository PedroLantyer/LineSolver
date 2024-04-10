import tkinter as tk
import styles
from bifrost import DataBridge
from bifrost import Variable
from bifrost import Boundaries
from dataValidations import BoundaryValidations
from dataValidations import VariableValidations

class GetVariableWindow:
    master = None

    def __init__(self, text):
        
        #CREATE WINDOW
        
        self.dialog = tk
        self.top = self.dialog.Toplevel(self.master)
        self.text = text
        
        self.InitializeClasses()
        self.InitializeTkVars()
        self.InitializeElements()

    def InitializeClasses(self):
        self.bridge = DataBridge()
        self.boundaries = Boundaries()
        self.boundValid = BoundaryValidations()
        self.varValid = VariableValidations()
        self.variable = Variable()

    def InitializeTkVars(self):
        self.currentVarValue = tk.StringVar(value="")
        self.lowBoundEnabled = tk.IntVar(value=1)
        self.upBoundEnabled = tk.IntVar(value=1)

    def SetLowBoundaryEntryState(self, entryLowBound):
        if(self.lowBoundEnabled.get() == 1):
            entryLowBound.config(state="normal")
        else:
            entryLowBound.delete(0, tk.END)
            entryLowBound.config(state="disabled")

    def SetUpperBoundaryEntryState(self, entryUpBound):
        if(self.upBoundEnabled.get() == 1):
            entryUpBound.config(state="normal")
        else:
            entryUpBound.delete(0, tk.END) #CLEAR THE VALUE OF THE UPPER BOUNDARY ENTRY
            entryUpBound.config(state="disabled")

    def AddVariable(self, varStr, lowBoundStr, upBoundStr):
        try:
            self.currentVarValue.set(varStr)
            if(self.lowBoundEnabled.get() == 0 and self.upBoundEnabled.get() == 0): raise Exception("Variable can't have both constraints set to infinite")
            if(self.bridge.VarAlreadyExists(self.currentVarValue.get())): raise Exception("User attempted to add variable that already exists")
            if not (self.varValid.ValidVariableValue(self.currentVarValue.get())): raise Exception("Variable value isn't valid")
            if not(self.boundValid.ValidLowerBoundary(self.lowBoundEnabled.get(), lowBoundStr)): raise Exception("Lower Boundary Isn't Valid")
            if not(self.boundValid.ValidUpperBoundary(self.upBoundEnabled.get(), upBoundStr)): raise Exception("Upper Boundary Isn't Valid")
            if (self.boundValid.CheckBoundariesAreEqual(lowBoundStr, upBoundStr)): raise Exception("Upper and Lower Boundaries can't both have the same value")

            self.variable.SetVariableName(self.currentVarValue.get())
            boundaries = self.boundaries.GetBoundaries(self.lowBoundEnabled.get(), self.upBoundEnabled.get(),lowBoundStr, upBoundStr)
            self.variable.SetLowerBoundary(boundaries[0])
            self.variable.SetUpperBoundary(boundaries[1])
            self.bridge.SetVariable(self.variable)
            self.bridge.GetVarArrSize()
            self.top.destroy()
        
        except Exception as err:
            print(err)

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

        #CREATE INSERT VARIABLE LABEL
        labelInsertVariable = self.dialog.Label(frame, text=self.text, bg=labelStyles.bgColor, fg=labelStyles.fgColor, font=[labelStyles.font, labelStyles.fontSize])
        
        #CREATE ENTRIES
        entryVariable = self.dialog.Entry(frame, bg=entryStyles.bgColor, fg=entryStyles.fgColor, font=[entryStyles.font, entryStyles.fontSize], relief=entryStyles.relief)
        entryLowBound = self.dialog.Entry(frame, disabledbackground=entryStyles.disabledBgColor, disabledforeground=entryStyles.disabledFgColor, bg=entryStyles.bgColor, fg=entryStyles.fgColor, font=[entryStyles.font, entryStyles.fontSize], relief=entryStyles.relief)
        entryUpBound = self.dialog.Entry(frame, disabledbackground=entryStyles.disabledBgColor, disabledforeground=entryStyles.disabledFgColor, bg=entryStyles.bgColor, fg=entryStyles.fgColor, font=[entryStyles.font, entryStyles.fontSize], relief=entryStyles.relief)

        #DEFINE FUNCTIONS
        def LowBoundEnabledChanged():
            self.SetLowBoundaryEntryState(entryLowBound)

        def UpBoundEnabledChanged():
            self.SetUpperBoundaryEntryState(entryUpBound)

        def ButtonSubmitOnClick():
            self.AddVariable(entryVariable.get(), entryLowBound.get(), entryUpBound.get())

        #CREATE CHECKBOXES
        checkBoxLowBound = self.dialog.Checkbutton(frame, text="Lower Boundary" , bg=checkBoxStyles.bgColor, fg=checkBoxStyles.fgColor, font=[checkBoxStyles.font, checkBoxStyles.fontSize], variable=self.lowBoundEnabled, onvalue=1, offvalue=0, command=LowBoundEnabledChanged)
        checkBoxUpBound = self.dialog.Checkbutton(frame, text="Upper Boundary" , bg=checkBoxStyles.bgColor, fg=checkBoxStyles.fgColor, font=[checkBoxStyles.font, checkBoxStyles.fontSize], variable=self.upBoundEnabled, onvalue=1, offvalue=0, command=UpBoundEnabledChanged)
        
        #CREATE BUTTON
        buttonSubmit = self.dialog.Button(frame, text='Add',bg=buttonStyles.bgColor, fg=buttonStyles.fgColor, font=[buttonStyles.font, buttonStyles.fontSize], relief=buttonStyles.relief, command=ButtonSubmitOnClick)
        
        #PLACE ELEMENTS
        labelInsertVariable.pack()
        entryVariable.pack()
        checkBoxLowBound.pack()
        entryLowBound.pack()
        checkBoxUpBound.pack()
        entryUpBound.pack()
        buttonSubmit.pack()