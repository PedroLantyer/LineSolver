import dialogBoxGetVar
import dialogBoxGetConstraints
import styles
import pulp
import tkinter as tk
from bifrost import DataBridge

class TkGUI:
    
    def __init__(self, master):

        #GET DESIGNER CLASSES
        mainStyles = styles.MainGUI()
        frameSyles = styles.AppFrame()

        #INITILIAZE WINDOW
        self.master = master
        self.master.title(mainStyles.title)
        self.master.geometry(mainStyles.dimension)
        self.master.config(bg=mainStyles.bgColor)

        self.InitializeClasses()
        self.CreateTkVars()

        #INITIALIZE THE FRAME
        self.frame = tk.Frame(master=master, bg=frameSyles.bgColor)
        self.frame.pack(fill="both", expand=True)

    def InitializeClasses(self):
        self.bridge = DataBridge()

    def CreateTkVars(self):
        self.radioOption = tk.StringVar(value="Max")
        self.infLowerBoundary = tk.IntVar(value=0)
        self.infUpperBoundary = tk.IntVar(value=0)
        self.variableList = tk.Variable(value= self.bridge.GetVariables())
        self.constraintList = tk.Variable(value= self.bridge.GetConstraints())

    def SetVariableList(self):
        self.variableList.set(self.bridge.GetVariables())
        print("Updated Variable List")

    def SetConstraintList(self):
        self.constraintList.set(self.bridge.GetConstraints())
        print("Updated Constraint List")

    def OpenAddVarWindow(self):
        getVarWindow = dialogBoxGetVar.GetVariableWindow(text="Insert Variable")
        getVarWindow.top.wait_window() #WAIT FOR WINDOW TO CLOSE
        print("Window Closed, continuing...")
        self.SetVariableList()

    def CheckEnoughVariables(self, buttonSolve):
        if(self.bridge.GetVarArrSize() >= 2):
            buttonSolve.config(state="normal")

    def OpenAddConstraintWindow(self):
            getConstraintWindow = dialogBoxGetConstraints.GetConstraintsWindow()
            getConstraintWindow.top.wait_window()
            print("Window Closed, continuing...")
            self.SetConstraintList()

    def SetInfLowerBoundary(self, entryLowerBoundary):
        if(self.infLowerBoundary.get() == 1):
            entryLowerBoundary.delete(0,tk.END)
            entryLowerBoundary.config(state="disabled")
        else:
            entryLowerBoundary.config(state="normal")

    def SetInfUpperBoundary(self, entryUpperBoundary):
        if(self.infUpperBoundary.get() == 1):
            entryUpperBoundary.delete(0, tk.END)
            entryUpperBoundary.config(state="disabled")
        else:
            entryUpperBoundary.config(state="normal")

    def SetRadioOption(self, entryValueOf):
        if(self.radioOption.get() == "ValueOf"):
            entryValueOf.config(state="normal")
        else:
            entryValueOf.delete(0, tk.END)
            entryValueOf.config(state="disabled")
    
    def CreateWidgets(self):
        #GET DESIGNER CLASSES
        labelStyles = styles.Label()
        buttonStyles = styles.Button()
        radioStyles = styles.RadioButton()
        checkBoxStyles = styles.CheckBox()
        listBoxStyles = styles.ListBox()
        entryStyles = styles.Entry()

        #CREATE LABELS
        toLabel = tk.Label(master=self.frame,text = "To:", bg=labelStyles.bgColor, fg=labelStyles.fgColor, font=[labelStyles.font, labelStyles.fontSize])
        objectiveLabel = tk.Label(master=self.frame, text= "Objective:", bg=labelStyles.bgColor, fg=labelStyles.fgColor, font=[labelStyles.font,labelStyles.fontSize])
        lowerBoundLabel = tk.Label(master=self.frame, text="Lower Boundary:", bg=labelStyles.bgColor, fg=labelStyles.fgColor, font=[labelStyles.font, labelStyles.fontSize])
        upperBoundLabel = tk.Label(master=self.frame, text="Upper Boundary:", bg=labelStyles.bgColor, fg=labelStyles.fgColor, font=[labelStyles.font, labelStyles.fontSize])
        
        #CREATE LIST BOXES
        listBoxVariables = tk.Listbox(master=self.frame, bg=listBoxStyles.bgColor, fg=listBoxStyles.fgColor, font=[listBoxStyles.font, listBoxStyles.fontSize], relief=listBoxStyles.relief, listvariable=self.variableList)
        listBoxConstraints = tk.Listbox(master=self.frame, bg=listBoxStyles.bgColor, fg=listBoxStyles.fgColor, font=[listBoxStyles.font, listBoxStyles.fontSize], relief=listBoxStyles.relief, listvariable=self.constraintList)

        #CREATE SOLVE BUTTON:
        buttonSolve = tk.Button(master=self.frame, text="Solve", bg=buttonStyles.bgColor, fg= buttonStyles.fgColor, font=[buttonStyles.font, buttonStyles.fontSize], relief=buttonStyles.relief, state="disabled")

        #CREATE FUNCTIONS FOR OPENING WINDOWS
        def buttonAddVariableOnClick():
            self.OpenAddVarWindow()
            self.CheckEnoughVariables(buttonSolve)

        def buttonAddConstraintsOnClick():   
            self.OpenAddConstraintWindow()

        #CREATE BUTTONS
        buttonAddVariables = tk.Button(master=self.frame, text="Add Variables", bg=buttonStyles.bgColor, fg= buttonStyles.fgColor, font=[buttonStyles.font, buttonStyles.fontSize], relief=buttonStyles.relief, command=buttonAddVariableOnClick)
        buttonAddConstraints = tk.Button(master=self.frame, text="Add Constraints", bg=buttonStyles.bgColor, fg= buttonStyles.fgColor, font=[buttonStyles.font, buttonStyles.fontSize], relief=buttonStyles.relief, command=buttonAddConstraintsOnClick)
        buttonDelVariables = tk.Button(master=self.frame, text="Delete Variable", bg=buttonStyles.bgColor, fg= buttonStyles.fgColor, font=[buttonStyles.font, buttonStyles.fontSize], relief=buttonStyles.relief)
        buttonDelConstraints = tk.Button(master=self.frame, text="Delete Constraints", bg=buttonStyles.bgColor, fg= buttonStyles.fgColor, font=[buttonStyles.font, buttonStyles.fontSize], relief=buttonStyles.relief)

        #DEF RADIO OPTION RELATED FUNCTION

        def RadioButtonOptionChange():
            self.SetRadioOption(entryValueOf)

        #CREATE RADIO BUTTONS
        radioMin = tk.Radiobutton(master=self.frame, text="Min",bg = radioStyles.bgColor, fg=radioStyles.fgColor, font=[radioStyles.font, radioStyles.fontSize], variable=self.radioOption, value="Min", command=RadioButtonOptionChange)
        radioMax = tk.Radiobutton(master=self.frame, text="Max",bg = radioStyles.bgColor, fg=radioStyles.fgColor, font=[radioStyles.font, radioStyles.fontSize], variable=self.radioOption, value="Max", command=RadioButtonOptionChange)
        radioValueOf = tk.Radiobutton(master=self.frame, text="Value Of:",bg = radioStyles.bgColor, fg=radioStyles.fgColor, font=[radioStyles.font, radioStyles.fontSize], variable=self.radioOption, value="ValueOf", command=RadioButtonOptionChange)

        #CREATE ENTRIES
        entryValueOf = tk.Entry(master=self.frame, bg=entryStyles.bgColor, fg=entryStyles.fgColor, font=[entryStyles.font, entryStyles.fontSize], state="disabled", disabledbackground=entryStyles.disabledBgColor, disabledforeground=entryStyles.disabledFgColor, relief=entryStyles.relief)
        entryObjective = tk.Entry(master=self.frame, bg=entryStyles.bgColor, fg=entryStyles.fgColor, font=[entryStyles.font, entryStyles.fontSize], relief=entryStyles.relief)
        entryLowerBoundary = tk.Entry(master=self.frame, disabledbackground=entryStyles.disabledBgColor, disabledforeground=entryStyles.disabledFgColor ,bg=entryStyles.bgColor, fg=entryStyles.fgColor, font=[entryStyles.font, entryStyles.fontSize], relief=entryStyles.relief)
        entryUpperBoundary = tk.Entry(master=self.frame, disabledbackground=entryStyles.disabledBgColor, disabledforeground=entryStyles.disabledFgColor, bg=entryStyles.bgColor, fg=entryStyles.fgColor, font=[entryStyles.font, entryStyles.fontSize], relief=entryStyles.relief)

        #CREATE FUNCTIONS FOR CHECKBOX
        def InfLowerBoundChange():
            self.SetInfLowerBoundary(entryLowerBoundary)

        def InfUpperBoundChange():
            self.SetInfUpperBoundary(entryUpperBoundary)

        #CREATE CHECKBOXES
        checkBoxInfLowerBoundary = tk.Checkbutton(master=self.frame, text="Infinite Lower Boundary", bg=checkBoxStyles.bgColor, fg=checkBoxStyles.fgColor, font=[checkBoxStyles.font,checkBoxStyles.fontSize], variable=self.infLowerBoundary, onvalue=1, offvalue=0, command=InfLowerBoundChange)
        checkBoxInfUpperBoundary = tk.Checkbutton(master=self.frame, text="Infinite Upper Boundary", bg=checkBoxStyles.bgColor, fg=checkBoxStyles.fgColor, font=[checkBoxStyles.font,checkBoxStyles.fontSize], variable=self.infUpperBoundary, onvalue=1, offvalue=0, command=InfUpperBoundChange)

        #PLACE ELEMENTS
        toLabel.place(x=12, y=110)
        objectiveLabel.place(x=5, y=15)
        lowerBoundLabel.place(x=227,y=45)
        upperBoundLabel.place(x=227,y=77)

        buttonAddVariables.place(x=585, y=161, width=180, height=56)
        buttonAddConstraints.place(x=585, y=223, width=180, height=56)
        buttonDelVariables.place(x=585, y=290, width=180, height=32)
        buttonDelConstraints.place(x=585, y=328, width=180, height=32)
        buttonSolve.place(x=585, y=383, width=180, height=32)

        radioMin.place(x=61, y=110, width=64, height=25)
        radioMax.place(x=131, y=110, width=64, height=25)
        radioValueOf.place(x=201, y=110, width=130, height=25)

        entryValueOf.place(x=329, y=110, width=250, height=27)
        entryObjective.place(x=118, y= 12, width=647, height=27)
        entryLowerBoundary.place(x=375, y=42, width=78, height=27)
        entryUpperBoundary.place(x=375, y=75, width=78, height=27)

        checkBoxInfLowerBoundary.place(x= 459, y=45, height=25)
        checkBoxInfUpperBoundary.place(x= 459, y=77, height=25)

        listBoxVariables.place(x=12, y=159, width=567, height=124)
        listBoxConstraints.place(x=12, y=289, width=567, height=124)

if __name__ == "__main__":
    #GUI
    master = tk.Tk()
    app = TkGUI(master = master)
    app.CreateWidgets()
    master.mainloop()





#SAMPLES:
"""
def SolveProblemA():
    #DEFINE PROBLEM
    ProblemA = pulp.LpProblem("Problem A", pulp.const.LpMaximize)

    #DEFINE VARIABLES
    A = pulp.LpVariable("A", lowBound = 0, cat = "Integer")
    B = pulp.LpVariable("B", lowBound = 0, cat = "Integer")
    C = pulp.LpVariable("C", lowBound = 0, cat = "Integer")
    D = pulp.LpVariable("D", lowBound = 0, cat = "Integer")

    #DEFINE OBJECTIVE
    ProblemA += (2*A) + B - (3*C) + (5*D)

    #DEFINE CONSTRAINTS
    ProblemA += A + (2*B) + (4*C) - D <= 6
    ProblemA += (2*A) + (3*B) - C + D <= 12
    ProblemA += A + B + C <= 4 

    #SOLVE PROBLEM
    status = ProblemA.solve()

    if(status == 1):
        varA, varB, varC, varD = A.varValue, B.varValue, C.varValue, D.varValue
        maxValue = (2 * varA) + varB - (3 * varC) + (5 * varD)
        
        stringPartOne = "Results for problem #1:\n"
        stringPartTwo = f"A: {varA}\nB: {varB}\nC: {varC}\nD: {varD}\n"
        stringPartThree = f"Max value : {maxValue}\n\n"
        result = f"{stringPartOne}{stringPartTwo}{stringPartThree}"

        return result
    else:
        stringPartOne = "Couldn't find optimal result for problem #1\n"
        stringPartTwo = f"Status: {pulp.LpSolution[status]}"
        result = f"{stringPartOne}{stringPartTwo}"

        return result
"""
#SAMPLES