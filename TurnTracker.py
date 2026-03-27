import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import filedialog as fd
from EncounterCheck import encounterCheck, moraleCheck
import CombatTracker as ct
import bodyLoot
#import dngRooms as DNGN

from random import randint as _Roll


''' TODO:

'''

class timerObject():
    '''Holds a name and an int'''
    def __init__(self, name: str, length: int):
        self.name = name
        self.length = length

    def getName(self)-> str:
        return self.name
    
    def getTimeLeft(self)-> int:
        return self.length

    def dec(self) -> bool:
        '''Returns True if there is still time left on the timer.'''
        self.length -= 1
        if self.length < 1:
            return False
        else:
            return True


class myTime():
    '''Holds the time, and increments it as needed'''
    someHours = 6
    someMins  = 0
    isNight   = False

    def addTurn(self):
        '''Adds 10 minutes to the current time.'''
        self.someMins += 10
        if self.someMins > 55:
            self.someHours += 1
            self.someMins = 0
        if self.someHours > 12:
            self.someHours = 1
            if self.isNight == False:
                self.isNight = True
            else:
                self.isNight = False
                showinfo(title='Nightly Popup', message='New day.\nHas the party Ate, Drank, Slept?')

    def setTime(self, hour: int, min: int, isNight: bool)-> str:
        self.someHours = hour
        self.someMins  = min
        self.isNight   = isNight
        return self.getTime()

    def getTime(self)-> str:
        '''Returns a string description of the current time in the
        format of '7:20 am' '''
        builderString = str(self.someHours) + ":"
        if self.someMins < 10:
            builderString += '0' + str(self.someMins)
        else:
            builderString += str(self.someMins)
        if self.isNight == False:
            builderString += ' am'
        else:
            builderString += ' pm'
        return builderString


class setTimeFrame(ttk.Frame):
    def __init__(self,container):
        super().__init__(container)
        self.host = container

        self.label1 = ttk.Label(self, text='hour')
        self.label2 = ttk.Label(self, text='minute')
        self.label1.grid(row=1, column=1)
        self.label2.grid(row=2, column=1)

        self.hourPicker = ttk.Combobox( self)
        self.hourPicker['values'] = (1,2,3,4,5,6,7,8,9,10,11,12)
        self.hourPicker.set(6)
        self.hourPicker.grid(row=1, column=2)

        self.minPicker = ttk.Combobox( self)
        self.minPicker['values'] = (00,10,20,30,40,50)
        self.minPicker.set(20)
        self.minPicker.grid(row=2, column=2)

        self.nightIsChecked = tk.BooleanVar()
        self.nightCheck = ttk.Checkbutton(self, text='Is Night?', variable= self.nightIsChecked,
                                          onvalue=True, offvalue=False)
        self.nightCheck.grid(row=3, column=2)

        self.closeButton = ttk.Button(self, text="OK", command=lambda: self.closeAndSet())
        self.closeButton.grid(row=2, column=4)

    def closeAndSet(self):
        App.timer.someHours = int(self.hourPicker.get())
        App.timer.someMins  = int(self.minPicker.get())
        App.timer.isNight = self.nightIsChecked.get()
        self.host.swapSetFrame()
        

class textFrame(ttk.Frame):
    maximumTextLines = 40
    currentTextLines = ['','']
    def __init__(self, container):
        super().__init__(container)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

        self.textBox = tk.Text(self, font=('Helvetica', 12))
        self.textBox.grid(row=1, column=1, sticky='nsew')
        self.rewrite()

    def rewrite(self):
        '''refreshes the textBox to what is currently held in the 
        class variable currentTextLines'''
        self.textBox.delete('1.0', tk.END)
        counter = 1.0
        for x in textFrame.currentTextLines:
            self.textBox.insert(counter, x + '\n')
            counter += 1.0

    def addLineToBox(self, lineToAdd: str):
        '''Adds the passed String element to the text frame, then
        updates the view by calling rewrite(). '''
        if len(textFrame.currentTextLines) >= textFrame.maximumTextLines:
            textFrame.currentTextLines.pop()
        textFrame.currentTextLines.insert(0, lineToAdd + '\n')
        self.rewrite()


class buttonHolder(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.creator = container
        self.addTurnButton = ttk.Button(self, text="add turn", command=lambda: self.creator.updateDisplayTime(True))
        self.addTurnButton.grid(row=0, column=1, columnspan=2)

        self.addHoursButton = ttk.Button(self, text='+hrs',
                                         command=lambda: {self.creator.addTimeByTurn(int(self.getText(self.textBox))*6),
                                                          self.textBox.delete('1.0',tk.END)})
        self.addHoursButton.grid(row=1, column=1)
        self.addMinsButton = ttk.Button(self, text='+turns',
                                        command=lambda: {self.creator.addTimeByTurn(int(self.getText(self.textBox))),
                                                         self.textBox.delete('1.0', tk.END)})
        self.addMinsButton.grid(row=1, column=2)

        self.textBox = tk.Text(self, height=1, width=4)
        self.textBox.bind('<Return>', 'break')
        self.textBox.bind('<Tab>','break')
        self.textBox.grid(row=2, column=1, columnspan=2, sticky=tk.EW)

        self.topSepar = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.topSepar.grid(row=3, column=1, columnspan=2, pady=8, sticky=tk.EW)

        self.encCheck = ttk.Button(self, text='Enc. Check', command=lambda: self.creator.addToTextBox(encounterCheck()))
        self.encCheck.grid(row=4, column=1)
        self.mrlCheck = ttk.Button(self, text='Combat', command=lambda: self.creator.setGridFight() )
        self.mrlCheck.grid(row=4, column=2)

        self.midSepar = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.midSepar.grid(row=5, column=1, columnspan=2, pady=8, sticky=tk.EW)

        self.tmrLbl = ttk.Label(self,text='Timer Name').grid(row=6, column=1, sticky=tk.E)
        self.tmrTrn = ttk.Label(self,text='Timer Turns').grid(row=7, column=1, sticky=tk.E)
        self.tmrTx1 = tk.Text(self,height=1,width=10)
        self.tmrTx1.grid(row=6, column=2, sticky=tk.W)
        self.tmrTx2 = tk.Text(self,height=1,width=10)
        self.tmrTx2.grid(row=7, column=2, sticky=tk.W)
        self.tmrTx1.bind('<Return>', 'break')
        self.tmrTx1.bind('<Tab>','break')
        self.tmrTx2.bind('<Return>', 'break')
        self.tmrTx2.bind('<Tab>','break')

        self.addTimerButton = ttk.Button(self, text='+tmr',
                                         command=lambda: {self.creator.addTimerToList(self.makeATimer()),
                                                          self.tmrTx1.delete('1.0',tk.END),
                                                          self.tmrTx2.delete('1.0',tk.END)})
        self.addTimerButton.grid(row=8, column=2)

        self.botSepar = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.botSepar.grid(row=9, column=1, columnspan=2, pady=8, sticky=tk.EW)

        self.dangerous = tk.BooleanVar()
        self.dangerCheck = ttk.Checkbutton(self, text="in the Danger Zone?", variable=self.dangerous,
                                           command=lambda: self.goToDangerZone() )
        self.dangerCheck.grid(row=10, column=1, columnspan=2)

        self.bot2separ = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.bot2separ.grid(row= 11,column=1,columnspan=2, pady=8, sticky=tk.EW)

        self.lootButton = ttk.Button(self, text='Loot', command=lambda: self.creator.addToTextBox( [ self.creator.lootList.getLoot(),"" ] ) )
        self.lootButton.grid(row=12, column=1, sticky=tk.W)

        self.nameButton = ttk.Button(self, text='Name', command=lambda: {self.creator.addToTextBox([self.creator.getName(),""]) })
        self.nameButton.grid(row=12, column=2, sticky=tk.E)
        '''
        self.roomButton = ttk.Button(self, text='Room', command=lambda:{self.creator.addToTextBox( self.creator.dungeon.display() ) })
        self.roomButton.grid(row=13, column=1, sticky=tk.W)

        self.stairButton = ttk.Button(self, text='Stairs', command=lambda:{ self.creator.addToTextBox( self.creator.dungeon.delve() )})
        self.stairButton.grid(row=13, column=2, sticky=tk.E)

        self.resetButton = ttk.Button(self, text='Rebuild',command=lambda:{ self.creator.dungeon.setup()})
        self.resetButton.grid(row=14, column=2, sticky=tk.E)'''

    def goToDangerZone(self):
        if self.dangerous.get() == True:
            self.creator.setDeadliness( 2 )
        else:
            self.creator.setDeadliness( 3 )

    def makeATimer(self)->timerObject:
        timer = timerObject(self.getText(self.tmrTx1),
                            int(self.getText(self.tmrTx2)))
        return timer

    def getText(self, whichBox: tk.Text)-> str:
        if len( whichBox.get('1.0',tk.END)) < 2:
            showinfo(title='Error', message='The text entry box is empty.')
        else:
            return whichBox.get('1.0',tk.END).rstrip()

        

class App(tk.Tk):
    timer = myTime()
    showingTimeEntry = False
    def __init__(self):
        super().__init__()
        self.deadliness = 3
        self.turnCount = 0
        self.timerList = []
        self.nameList = []

        self.title('Turn Tracker')
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)

        #   UL position
        self.myFrame = textFrame(self)

        #   LL position
        self.timeDisplay = ttk.Label(self, text=App.timer.getTime(), padding=12, font=('Helvetica', 24))

        #   UR position
        self.buttonDisplay = buttonHolder(self)

        #   LR position
        self.setTimeButton = ttk.Button(self, text='SetTime', command=lambda: self.swapSetFrame())
        self.timeSetter = setTimeFrame(self)

        #   Combat Tracker
        self.fightDisplay = ct.combatFrame(self)

        #   Loot List
        self.lootList = bodyLoot.LootList(True)

        #   Build a dungeon
        #self.dungeon = DNGN.ARandomDungeon()

        self.setGridTurns()
        self.loadNameList()

    def setGridTurns(self):
        self.fightDisplay.grid_forget()
        self.myFrame.grid(row=1, column=1,sticky='nsew')
        self.timeDisplay.grid( row=2, column=1, sticky=tk.SW)
        self.buttonDisplay.grid(row=1, column=2, sticky=tk.N)
        self.setTimeButton.grid(row=2, column=2, sticky=tk.SE, padx=12, pady=12)
    
    def setGridFight(self):
        self.myFrame.grid_forget()
        self.timeDisplay.grid_forget()
        self.buttonDisplay.grid_forget()
        self.setTimeButton.grid_forget()
        self.fightDisplay.grid(row=1, column=1)


    def setDeadliness(self, dangerZone: int):
        self.deadliness = dangerZone
        self.turnCount = 0
        self.myFrame.addLineToBox("Your deadliness is now " + str(self.deadliness))

    def addTimerToList(self, timer: timerObject):
        self.myFrame.addLineToBox('Added ' + timer.getName() + ' timer with ' +
                                  str(timer.getTimeLeft()) + ' turns.')
        self.timerList.append( timer )

    def decTimers(self):
        for x in self.timerList:
            self.myFrame.addLineToBox( str(x.getTimeLeft()) + ' turns left on '+ str( x.getName() ))
            if x.dec() == False:
                self.myFrame.addLineToBox( x.getName() + ' timer has ran out')
                self.timerList.remove(x)

    def checkForEncounter(self):
        self.turnCount += 1
        if self.turnCount == self.deadliness:
            self.turnCount = 0
            self.addToTextBox( encounterCheck() )
        elif self.turnCount > self.deadliness:
            self.turnCount = 0

    def addTimeByTurn(self, turns: int):
        counter = 0
        while counter < turns:
            counter += 1
            self.updateDisplayTime(False)

    def addToTextBox(self, linesToAdd: list):
        for x in linesToAdd:
            self.myFrame.addLineToBox(x)

    def updateDisplayTime(self, encCheck: bool):
        App.timer.addTurn()
        self.myFrame.addLineToBox( App.timer.getTime())
        self.myFrame.update()
        self.timeDisplay.config(text=App.timer.getTime())
        if encCheck != False:
            self.checkForEncounter()
        self.decTimers()
    
    def swapSetFrame(self):
        if App.showingTimeEntry == False:
            App.showingTimeEntry = True
            self.setTimeButton.grid_forget()
            self.timeSetter.grid( row=2, column=2)
            self.buttonDisplay.grid_forget()
        else:
            App.showingTimeEntry = False
            self.timeSetter.grid_forget()
            self.setTimeButton.grid(row=2, column=2, sticky=tk.SE, padx=12, pady=12)
            self.myFrame.addLineToBox( App.timer.getTime())
            self.myFrame.rewrite()
            self.timeDisplay.config(text=App.timer.getTime())
            self.buttonDisplay.grid(row=1, column=2, stick=tk.N)
    
    def loadNameList(self, fantasy=True):
        holderString = ''
        if fantasy:
            with open( 'Lists/Fantasy/~FantasyNames~.txt','r') as file:
                holderString = file.read()
        
        self.nameList = holderString.split(',')

    def getName(self)-> str:
        selection = _Roll(0, (len(self.nameList)-1) )
        return self.nameList[ selection ]


if __name__ == "__main__":
    app = App()
    app.mainloop()