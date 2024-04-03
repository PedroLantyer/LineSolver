import tkinter as tk
import styles
from bifrost import DataBridge

class getVariableWindow:
    master = None

    def __init__(self, text):
        
        #CREATE WINDOW
        
        self.dialog = tk
        self.top = self.dialog.Toplevel(self.master)
        self.text = text
        
        self.InitializeElements()

    def InitializeElements(self):
        
        #INITIALIZE DATA BRIDGE CLASS
        bridge = DataBridge()

        #GET DESIGNER CLASSES
        frameStyles = styles.GetVarDialog()
        labelStyles = styles.Label()
        entryStyles = styles.Entry()
        checkBoxStyles = styles.CheckBox

        #CREATE FRAME
        frame = self.dialog.Frame(self.top, borderwidth=2, relief='ridge', bg=frameStyles.bgColor)
        frame.pack(fill='both', expand=True)

        #CREATE INSERT VARIABLE LABEL
        labelInsertVariable = self.dialog.Label(frame, text=self.text, bg=labelStyles.bgColor, fg=labelStyles.fgColor, font=[labelStyles.font, labelStyles.fontSize]).pack()

        #CREATE TK VARIABLE
        currentVarValue = tk.StringVar(value="")
        lowBoundEnabled = tk.IntVar(value=0)
        upBoundEnabled = tk.IntVar(value=0)
        lowerBoundary = tk.IntVar(value=0)
        upperBoundary = tk.IntVar(value=0)
        lowerBoundaryTemp = tk.StringVar(value="")
        upperBoundaryTemp = tk.IntVar(value="")
        
        #CREATE ENTRY VARIABLE
        entryVariable = self.dialog.Entry(frame, bg=entryStyles.bgColor, fg=entryStyles.fgColor, font=[entryStyles.font, entryStyles.fontSize], relief=entryStyles.relief)
        
        #SET FOCUS ON ENTRY FIELD
        entryVariable.focus_set()

        #CREATE ENTRIES FOR RECEIVING UPPER AND LOWER BOUNDARIES
        entryLowBound = self.dialog.Entry(frame, disabledbackground=entryStyles.disabledBgColor, disabledforeground=entryStyles.disabledFgColor, bg=entryStyles.bgColor, fg=entryStyles.fgColor, font=[entryStyles.font, entryStyles.fontSize], relief=entryStyles.relief, state="disabled")
        entryUpBound = self.dialog.Entry(frame, disabledbackground=entryStyles.disabledBgColor, disabledforeground=entryStyles.disabledFgColor, bg=entryStyles.bgColor, fg=entryStyles.fgColor, font=[entryStyles.font, entryStyles.fontSize], relief=entryStyles.relief, state="disabled")

        #CREATE FUNCTIONS TO SET THE STATE OF THE LOW BOUND AND UP BOUND ENTRIES
        def SetLowBoundaryEntryState():
            if(lowBoundEnabled.get() == 1):
                entryLowBound.config(state="normal")
            else:
                entryLowBound.delete(0, tk.END) #CLEAR THE VALUE OF THE LOWER BOUNDARY ENTRY
                entryLowBound.config(state="disabled")
                lowerBoundaryTemp.set("")
                print("Lower Boundary value set to None")
        
        def SetUpperBoundaryEntryState():
            if(upBoundEnabled.get() == 1):
                entryUpBound.config(state="normal")
            else:
                entryUpBound.delete(0, tk.END) #CLEAR THE VALUE OF THE UPPER BOUNDARY ENTRY
                entryUpBound.config(state="disabled")
                upperBoundaryTemp.set("")
                print("Upper Boundary value set to None")


        #CREATE FUNCTIONS TO VERIFY VALUES
        def ValidLowerBoundary():
            if(lowBoundEnabled.get() == 1):
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
            if(upBoundEnabled.get() == 1):
                if(entryUpBound.get().isnumeric()):
                    upperBoundary.set(int(entryUpBound.get()))
                    print(f"Upper Boundary value set to {upperBoundary.get()}")
                
                else:
                    print("Invalid Upper Boundary Value")
                    return False
            else:
                return True
            
        def ValidVariableValue():
            if(len(currentVarValue.get().strip()) > 0):
                #VARIABLE VERIFICATION -> WORK IN PROGRESS
                return True
            else:
                print("User attempted to add empty variable")
                return False


        def GetBoundaries(): #USED ONLY INSIDE PassVariable()
            boundaries = []
            if(lowBoundEnabled.get() == 0):
                boundaries.append(None)
            else:
                boundaries.append(lowerBoundary.get())

            if(upBoundEnabled.get() == 0):
                boundaries.append(None)
            else:
                boundaries.append(upperBoundary.get())

            return boundaries

        #CREATE FUNCTION FOR PASSING DATA
        def PassVariable():
            currentVarValue.set(entryVariable.get())

            if(bridge.VarAlreadyExists(variable=currentVarValue.get())):
                print("User attempted to add variable that already exists")

            else:
                if(ValidVariableValue() and ValidLowerBoundary() and ValidUpperBoundary()):
                    bridge.SetVariable(currentVarValue.get())
                    boundaries = GetBoundaries()
                    bridge.SetBoundariesForVariable(boundaries=boundaries)
                    self.top.destroy()
                
                else:
                    print("Cannot pass down data under current circumstances")
                    pass

        #CREATE CHECKBOXES
        checkBoxLowBound = self.dialog.Checkbutton(frame, text="Lower Boundary" , bg=checkBoxStyles.bgColor, fg=checkBoxStyles.fgColor, font=[checkBoxStyles.font, checkBoxStyles.fontSize], variable=lowBoundEnabled, onvalue=1, offvalue=0, command=SetLowBoundaryEntryState)
        checkBoxUpBound = self.dialog.Checkbutton(frame, text="Upper Boundary" , bg=checkBoxStyles.bgColor, fg=checkBoxStyles.fgColor, font=[checkBoxStyles.font, checkBoxStyles.fontSize], variable=upBoundEnabled, onvalue=1, offvalue=0, command=SetUpperBoundaryEntryState)
        
        #CREATE BUTTON
        buttonSubmit = self.dialog.Button(frame, text='Add', command=PassVariable)
        
        #PACK ENTRY
        entryVariable.pack()

        #PLACE CHECKBOXES AND ENTRIES FOR UPPER AND LOWER BOUNDARIES
        checkBoxLowBound.pack()
        entryLowBound.pack()
        checkBoxUpBound.pack()
        entryUpBound.pack()

        #PACK BUTTON
        buttonSubmit.pack()