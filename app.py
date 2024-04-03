#import keyboard
import dialogBoxGetVar
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

        #INITIALIZE THE FRAME
        self.frame = tk.Frame(master=master, bg=frameSyles.bgColor)
        self.frame.pack(fill="both", expand=True)

    def CreateWidgets(self):
        #GET DESIGNER CLASSES
        
        labelStyles = styles.Label()
        buttonStyles = styles.Button()
        radioStyles = styles.RadioButton()
        checkBoxStyles = styles.CheckBox()
        listBoxStyles = styles.ListBox()
        entryStyles = styles.Entry()

        #CREATE TK VARIABLES
        self.radioOption = tk.StringVar(value="Max")
        self.infLowerBoundary = tk.IntVar(value=0)
        self.infUpperBoundary = tk.IntVar(value=0)


        #CREATE LABELS
        toLabel = tk.Label(master=self.frame,text = "To:", bg=labelStyles.bgColor, fg=labelStyles.fgColor, font=[labelStyles.font, labelStyles.fontSize]).place(x=12, y=110)
        objectiveLabel = tk.Label(master=self.frame, text= "Objective:", bg=labelStyles.bgColor, fg=labelStyles.fgColor, font=[labelStyles.font,labelStyles.fontSize]).place(x=5, y=15)
        lowerBoundLabel = tk.Label(master=self.frame, text="Lower Boundary:", bg=labelStyles.bgColor, fg=labelStyles.fgColor, font=[labelStyles.font, labelStyles.fontSize]).place(x=227,y=45)
        upperBoundLabel = tk.Label(master=self.frame, text="Upper Boundary:", bg=labelStyles.bgColor, fg=labelStyles.fgColor, font=[labelStyles.font, labelStyles.fontSize]).place(x=227,y=77)
        
        #CREATE LIST BOXES
        listBoxVariables = tk.Listbox(master=self.frame, bg=listBoxStyles.bgColor, fg=listBoxStyles.fgColor, font=[listBoxStyles.font, listBoxStyles.fontSize], relief=listBoxStyles.relief)
        listBoxConstraints = tk.Listbox(master=self.frame, bg=listBoxStyles.bgColor, fg=listBoxStyles.fgColor, font=[listBoxStyles.font, listBoxStyles.fontSize], relief=listBoxStyles.relief)

        #CREATE SOLVE BUTTON:
        buttonSolve = tk.Button(master=self.frame, text="Solve", bg=buttonStyles.bgColor, fg= buttonStyles.fgColor, font=[buttonStyles.font, buttonStyles.fontSize], relief=buttonStyles.relief, state="disabled")

        #OPEN AddVarWindow
        def OpenAddVarWindow():
            getVarWindow = dialogBoxGetVar.getVariableWindow(text="Insert Variable")
            getVarWindow.top.wait_window() #WAIT FOR WINDOW TO CLOSE
            print("Window Closed, continuing...")
            if(len(DataBridge.variableArr) >= 2):
                buttonSolve.config(state="normal")


        #CREATE BUTTONS
        buttonAddVariables = tk.Button(master=self.frame, text="Add Variables", bg=buttonStyles.bgColor, fg= buttonStyles.fgColor, font=[buttonStyles.font, buttonStyles.fontSize], relief=buttonStyles.relief, command=OpenAddVarWindow)
        buttonAddConstants = tk.Button(master=self.frame, text="Add Constants", bg=buttonStyles.bgColor, fg= buttonStyles.fgColor, font=[buttonStyles.font, buttonStyles.fontSize], relief=buttonStyles.relief)
        buttonDelVariables = tk.Button(master=self.frame, text="Delete Variable", bg=buttonStyles.bgColor, fg= buttonStyles.fgColor, font=[buttonStyles.font, buttonStyles.fontSize], relief=buttonStyles.relief)
        buttonDelConstants = tk.Button(master=self.frame, text="Delete Constant", bg=buttonStyles.bgColor, fg= buttonStyles.fgColor, font=[buttonStyles.font, buttonStyles.fontSize], relief=buttonStyles.relief)

        #DEF RADIO OPTION RELATED FUNCTION
        def SetRadioOption():
            if(self.radioOption.get() == "ValueOf"):
                entryValueOf.config(state="normal")
            else:
                entryValueOf.config(state="disabled")


        #CREATE RADIO BUTTONS
        radioMin = tk.Radiobutton(master=self.frame, text="Min",bg = radioStyles.bgColor, fg=radioStyles.fgColor, font=[radioStyles.font, radioStyles.fontSize], variable=self.radioOption, value="Min", command=SetRadioOption)
        radioMax = tk.Radiobutton(master=self.frame, text="Max",bg = radioStyles.bgColor, fg=radioStyles.fgColor, font=[radioStyles.font, radioStyles.fontSize], variable=self.radioOption, value="Max", command=SetRadioOption)
        radioValueOf = tk.Radiobutton(master=self.frame, text="Value Of:",bg = radioStyles.bgColor, fg=radioStyles.fgColor, font=[radioStyles.font, radioStyles.fontSize], variable=self.radioOption, value="ValueOf", command=SetRadioOption)


        #CREATE ENTRIES
        entryValueOf = tk.Entry(master=self.frame, bg=entryStyles.bgColor, fg=entryStyles.fgColor, font=[entryStyles.font, entryStyles.fontSize], state="disabled", disabledbackground=entryStyles.disabledBgColor, disabledforeground=entryStyles.disabledFgColor, relief=entryStyles.relief)
        entryObjective = tk.Entry(master=self.frame, bg=entryStyles.bgColor, fg=entryStyles.fgColor, font=[entryStyles.font, entryStyles.fontSize], relief=entryStyles.relief)
        entryLowerBoundary = tk.Entry(master=self.frame, disabledbackground=entryStyles.disabledBgColor, disabledforeground=entryStyles.disabledFgColor ,bg=entryStyles.bgColor, fg=entryStyles.fgColor, font=[entryStyles.font, entryStyles.fontSize], relief=entryStyles.relief)
        entryUpperBoundary = tk.Entry(master=self.frame, disabledbackground=entryStyles.disabledBgColor, disabledforeground=entryStyles.disabledFgColor, bg=entryStyles.bgColor, fg=entryStyles.fgColor, font=[entryStyles.font, entryStyles.fontSize], relief=entryStyles.relief)

        def SetInfLowerBoundary():
            if(self.infLowerBoundary.get() == 1):
                entryLowerBoundary.delete(0,tk.END)
                entryLowerBoundary.config(state="disabled")
            else:
                entryLowerBoundary.config(state="normal")
        
        def SetInfUpperBoundary():
            if(self.infUpperBoundary.get() == 1):
                entryUpperBoundary.delete(0, tk.END)
                entryUpperBoundary.config(state="disabled")
            else:
                entryUpperBoundary.config(state="normal")

        #CREATE CHECKBOXES
        checkBoxInfLowerBoundary = tk.Checkbutton(master=self.frame, text="Infinite Lower Boundary", bg=checkBoxStyles.bgColor, fg=checkBoxStyles.fgColor, font=[checkBoxStyles.font,checkBoxStyles.fontSize], variable=self.infLowerBoundary, onvalue=1, offvalue=0, command=SetInfLowerBoundary)
        checkBoxInfUpperBoundary = tk.Checkbutton(master=self.frame, text="Infinite Upper Boundary", bg=checkBoxStyles.bgColor, fg=checkBoxStyles.fgColor, font=[checkBoxStyles.font,checkBoxStyles.fontSize], variable=self.infUpperBoundary, onvalue=1, offvalue=0, command=SetInfUpperBoundary)

        #PLACE BUTTONS
        buttonAddVariables.place(x=585, y=161, width=156, height=56)
        buttonAddConstants.place(x=585, y=223, width=156, height=56)
        buttonDelVariables.place(x=585, y=290, width=156, height=32)
        buttonDelConstants.place(x=585, y=328, width=156, height=32)
        buttonSolve.place(x=585, y=383, width=156, height=32)

        #PLACE RADIO BUTTONS
        radioMin.place(x=61, y=110, width=64, height=25)
        radioMax.place(x=131, y=110, width=64, height=25)
        radioValueOf.place(x=201, y=110, width=130, height=25)

        #PLACE ENTRIES
        entryValueOf.place(x=329, y=110, width=250, height=27)
        entryObjective.place(x=118, y= 12, width=623, height=27)
        entryLowerBoundary.place(x=375, y=42, width=78, height=27)
        entryUpperBoundary.place(x=375, y=75, width=78, height=27)

        #PLACE CHECKBOXES
        checkBoxInfLowerBoundary.place(x= 459, y=45, width=285, height=25)
        checkBoxInfUpperBoundary.place(x= 459, y=77, width=285, height=25)

        #PLACE LIST BOXES
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