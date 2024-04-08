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
        infLowerBoundaryStatus = tk.IntVar(value=0)
        infUpperBoundaryStatus = tk.IntVar(value=0)

        #CREATE LABELS
        labelInsertLowerBoundary = self.dialog.Label(frame, text="Lower Boundary:", bg=labelStyles.bgColor, fg=labelStyles.fgColor, font=[labelStyles.font, labelStyles.fontSize])
        labelInsertExpression = self.dialog.Label(frame, text="Expression:", bg=labelStyles.bgColor, fg=labelStyles.fgColor, font=[labelStyles.font, labelStyles.fontSize])
        labelInsertUpperBoundary = self.dialog.Label(frame, text="Upper Boundary:", bg=labelStyles.bgColor, fg=labelStyles.fgColor, font=[labelStyles.font, labelStyles.fontSize])

        #CREATE TEXTBOXES
        entryLowerBoundary = self.dialog.Entry(frame, bg=entryStyles.bgColor, fg= entryStyles.fgColor, disabledbackground=entryStyles.disabledBgColor, disabledforeground= entryStyles.disabledFgColor, font=[labelStyles.font, labelStyles.fontSize])
        entryConstraintExpression = self.dialog.Entry(frame, bg=entryStyles.bgColor, fg= entryStyles.fgColor, disabledbackground=entryStyles.disabledBgColor, disabledforeground= entryStyles.disabledFgColor, font=[labelStyles.font, labelStyles.fontSize])
        entryUpperBoundary = self.dialog.Entry(frame, bg=entryStyles.bgColor, fg= entryStyles.fgColor, disabledbackground=entryStyles.disabledBgColor, disabledforeground= entryStyles.disabledFgColor, font=[labelStyles.font, labelStyles.fontSize])

        #FUNCTIONS TO SET INF BOUNDARY STATUS
        def SetInfLowerBoundaryStatus():
            if (infLowerBoundaryStatus.get() == 1):
                entryLowerBoundary.delete(0, tk.END)
                entryLowerBoundary.config(state="disabled")
            else:
                entryLowerBoundary.config(state="normal")

        def SetInfUpperBoundaryStatus():
            if (infUpperBoundaryStatus.get() == 1):
                entryUpperBoundary.delete(0, tk.END)
                entryUpperBoundary.config(state="disabled")
            else:
                entryUpperBoundary.config(state="normal")

        #CREATE CHECKBOXES
        checkBoxInfLowerBoundary = self.dialog.Checkbutton(frame, text="Inf Lower Boundary", bg=checkBoxStyles.bgColor, fg=checkBoxStyles.fgColor, font=[checkBoxStyles.font, checkBoxStyles.fontSize], variable=infLowerBoundaryStatus, offvalue=0, onvalue=1, command=SetInfLowerBoundaryStatus)
        checkBoxInfUpperBoundary = self.dialog.Checkbutton(frame, text="Inf Upper Boundary", bg=checkBoxStyles.bgColor, fg=checkBoxStyles.fgColor, font=[checkBoxStyles.font, checkBoxStyles.fontSize], variable=infUpperBoundaryStatus, offvalue=0, onvalue=1, command=SetInfUpperBoundaryStatus)

        #CREATE BUTTON
        buttonSubmit = self.dialog.Button(frame, text="Add", bg=buttonStyles.bgColor, fg=buttonStyles.fgColor, font=[buttonStyles.font, buttonStyles.fontSize], relief=buttonStyles.relief)

        #PLACE ELEMENTS

        labelInsertLowerBoundary.pack()
        entryLowerBoundary.pack()
        labelInsertExpression.pack()
        entryConstraintExpression.pack()
        labelInsertUpperBoundary.pack()
        entryUpperBoundary.pack()
        checkBoxInfLowerBoundary.pack()
        checkBoxInfUpperBoundary.pack()
        buttonSubmit.pack()