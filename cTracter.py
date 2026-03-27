import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

class badBlock(ttk.Frame):
    def __init__(self, container, name, hp, AC, dmg, move):
        super().__init__(container)
        self.maker = container
        self.gName = name
        self.gHP = hp
        self.gAr = AC
        self.gDie = dmg
        self.gMv = move

        #       Name Tag
        self.nameTag = ttk.Label(self, text=self.gName, font=("Helvetica", 14 ))
        self.nameTag.grid(row=0, rowspan=2,column=0, columnspan=2, padx=6)

        #       HP and Damage Die in column 2
        self.HPTag = ttk.Label(self, text="HP: "+str(self.gHP), font=("arial", 8) )
        self.HPTag.grid(row=0, column=2)
        self.DmgTag = ttk.Label(self, text="Damage: d"+str(self.gDie), font=("arial", 8) )
        self.DmgTag.grid(row=1, column=2)

        #       AC and Move Rate in column 3
        self.ArTag = ttk.Label(self, text="AC: "+str(self.gAr), font=("arial", 8) )
        self.ArTag.grid(row=0, column=3,padx=2)
        self.MvTag = ttk.Label(self, text="Move: "+str(self.gMv)+'"', font=("arial", 8) )
        self.MvTag.grid(row=1, column=3,padx=2)

        self.inBox = tk.Entry(self)
        self.inBox.grid(row=0, rowspan=2, column=6,columnspan=2)
        self.inBox.bind('<Return>', self.healHurt )
        # Add a 'entry' box, and 'on enter' subrtact contents from corresponding guy
    
    def healHurt(self,event):
        try:
            self.amount = int(self.inBox.get() )
        except:
            print("Empty Box Entered")
            self.amount = 0
        self.inBox.delete(0, tk.END)
        self.gHP -= self.amount
        # send to text box: If amount > 0 "hurt" if amount < 0 "healed"
        self.HPTag.config(text="HP: "+str(self.gHP))
        self.checkDead( self.amount )
    
    def checkDead(self,damage:int=0):
        if self.gHP < 1:
            builder = self.gName + " slain from the "
            builder += str( damage ) + " damage suffered."
            self.maker.master.master.master.addToTextView("   ***   ")
            self.maker.master.master.master.addToTextView(builder)
            self.destroy()
    



class scrTxtBox(ttk.Frame):
    def __init__(self,container):
        super().__init__(container)
        self.maxlinesOfText = 40
        self.curLinesOfText = 0
        self.frame = ttk.Frame(self)
        self.frame.pack(fill=tk.BOTH,expand=True)

        self.v_scroller = ttk.Scrollbar( self.frame )
        self.v_scroller.pack(side=tk.RIGHT, fill=tk.Y)

        # this will pull out to make room for list of ????
        self.text = tk.Text(self.frame, height=8, width=48)
        self.text.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.text['yscrollcommand']=self.v_scroller.set
        self.v_scroller.config( command=self.text.yview)

    def addToTextBox(self,strToAdd):
        temp:str = strToAdd.strip()
        self.curLinesOfText += 1
        if self.curLinesOfText > self.maxlinesOfText:
            self.curLinesOfText -= 1
            # delete the ### to end of self.text
            self.text.delete('end-1l','end')
        self.text.insert(1.0, temp+"\n")


class scrollBox(tk.Frame):
    def __init__(self, parent, scrollbar_width=16):
        super().__init__(parent) # Initialize as a standard Frame
        self.maker = parent
        self.scrollbar = tk.Scrollbar(self, width=scrollbar_width)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

        self.canvas = tk.Canvas(self, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.canvas.yview)

        # Configure the canvas to adjust to window resizing
        self.canvas.bind('<Configure>', self.__adjust_canvas_window)

        # The actual frame that will contain your widgets
        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas_window_item = self.canvas.create_window(0, 0, window=self.scrollable_frame, anchor=tk.NW)

        self.scrollable_frame.bind('<Enter>', self._bound_to_mousewheel)
        self.scrollable_frame.bind('<Leave>', self._unbound_to_mousewheel)


    def __adjust_canvas_window(self, event):
        "Adjust the canvas window item's width to match the canvas width"
        self.canvas.itemconfig(self.canvas_window_item, width=event.width)

    def update_scroll_region(self):
        "Update the canvas's scrollable region based on the contained frame's size"
        self.update_idletasks() # Process pending GUI updates
        self.canvas.config(scrollregion=self.canvas.bbox(self.canvas_window_item))
    
    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")






class buttonHolder(ttk.Frame):
    '''This class is the bottom frame, holding the buttons to ...'''
    def __init__(self, container):
        super().__init__(container)
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=0)

        # Event testMorale
        self.morButton = ttk.Button(self,text='Button',command=lambda:{ print("button!")})
        self.morButton.grid(row=0, column=0, rowspan=2, columnspan=2, sticky=tk.W)

        self.grid()



class ContainerFrame(ttk.Frame):
    '''this class splits the main window up into
    [top:figure lists] [mid:text update] [end:buttons]'''
    def __init__(self, container):
        super().__init__(container)
        self.grid_columnconfigure(0, weight=1)
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(3,weight=0)

        
        # Scrollbox for figure
        self.scroller = scrollBox(self, scrollbar_width=10)
        self.scroller.grid(row=0, column=0, sticky=tk.NW)
        #   swap around via initiative
        self.loadTheFigures()

        # textBox for update
        self.txtUpdater = scrTxtBox(self)
        self.txtUpdater.grid(row=1, column=0,sticky=tk.N)

        # Button Holder
        self.buttonsBox = buttonHolder(self)
        self.buttonsBox.grid(row=3, column=0,sticky=tk.SW)
        
        self.grid()

    def addToTextView(self, note:str):
        self.txtUpdater.addToTextBox( note )

    def setGoodieList(self):
        pass
    def setBaddieList(self):
        pass

    def loadTheFigures(self, goodsFirst:bool=True):
        '''sends the listOfBads and listOf Goods up to the scrollable Frame, in initiative order'''
        # clear the grid
        # for each in listOfBads: add to grid
        count = 1
        for i in range(4):
            guyA = badBlock(self.scroller.scrollable_frame,f"Good {i+1}",4,12,6,4)
            guyA.grid(row=i, column=0, pady=6)
            count += 1
        splitter = ttk.Separator(self.scroller.scrollable_frame,orient='horizontal')
        splitter.grid(row=count, sticky=tk.EW, pady=2)
        for i in range(4):
            guyA = badBlock(self.scroller.scrollable_frame,f"Bad {i+1}",4,12,6,4)
            guyA.grid(row=i+(count+1), column=0, pady=6)
        self.scroller.update_scroll_region()



#   This is the app we are creating, set the option for the main window here.
class App(tk.Tk):
    # Class varibles here
    def __init__(self):
        super().__init__()
        #   Configure the root window.
        self.title('Just a test')
        self.geometry('410x600')
        self.resizable(False,False)




if __name__ == "__main__":
    app = App()
    frame = ContainerFrame(app)
    app.mainloop()