import tkinter as tk
import styles
from bifrost import DataBridge
from bifrost import Variable
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

    def GetBoundaries(self, lowBoundStr, upBoundStr):
        boundaries = []
        if(self.lowBoundEnabled.get() == 0):
            boundaries.append(None)
        else:
            boundaries.append(lowBoundStr)

        if(self.upBoundEnabled.get() == 0):
            boundaries.append(None)
        else:
            boundaries.append(upBoundStr)

        return boundaries

    def PassVariable(self, varStr, lowBoundStr, upBoundStr):
        self.currentVarValue.set(varStr)

        if(self.bridge.VarAlreadyExists(self.currentVarValue.get())):
            print("User attempted to add variable that already exists")

        else:
            if(self.lowBoundEnabled.get() == 0 and self.upBoundEnabled.get() == 0):
                print("Variable can't have both constraints set to infinite")

            elif(self.varValid.ValidVariableValue(self.currentVarValue.get()) and self.boundValid.ValidLowerBoundary(self.lowBoundEnabled.get(), lowBoundStr) and self.boundValid.ValidUpperBoundary(self.upBoundEnabled.get(), upBoundStr)):
                self.variable.SetVariableName(self.currentVarValue.get())
                boundaries = self.GetBoundaries(lowBoundStr, upBoundStr)
                self.variable.SetLowerBoundary(boundaries[0])
                self.variable.SetUpperBoundary(boundaries[1])
                self.bridge.SetVariable(self.variable)
                self.bridge.GetVarArrSize()
                self.top.destroy()
                
            else:
                print("Cannot pass down data under current circumstances")

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
            self.PassVariable(entryVariable.get(), entryLowBound.get(), entryUpBound.get())

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