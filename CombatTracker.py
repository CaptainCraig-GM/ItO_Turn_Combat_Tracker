import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import filedialog as fd
from random import randint as _Roll
from EncounterCheck import moraleCheck


GadjectiveList = ['greasy', 'tattered shirt', 'missing an ear', 'flatulent', 'pirate patch', 'long moustache', 'sweet boots',
                  'buckly shirt', 'strong b.o.', 'wickedly attractive', 'very ugly', 'stooped', 'bad acne', 'mouth scars',
                   'face scars', 'dirty tattoos', 'cool tattoo', 'twitchy', 'shifty', 'patient', 'stolen uniform', 'muscly' ]

def roll3d6()-> int:
    return (_Roll(1,6)+_Roll(1,6)+_Roll(1,6))

class aBadGuy():
    def __init__(self, stats: str):
        self.statList = stats.split(',')
        self.name = self.statList[0]
        self.desc = self.statList[1]
        self.hp: tk.IntVar = int(self.statList[2])
        self.armour = int(self.statList[3])
        self.strength: tk.IntVar = int(self.statList[4])
        self.dexterity: tk.IntVar = int(self.statList[5])
        self.charisma: tk.IntVar = int(self.statList[6])
        self.numbAtks = int(self.statList[7])
        self.atkList: str = []
        self.abiList: str = []
        self.counter = 1
        self.atkListAsInt:int = []
        while self.counter <= self.numbAtks:
            self.atkList.append( self.statList[7 + self.counter])
            self.counter += 1
        self.buildAttacks()
        self.buildAbilities()
        self.tookCriticalDMG = False

    def checkForCD(self):
        d20roll = _Roll(1,20)
        if d20roll > self.strength:
            self.tookCriticalDMG = True

    def buildAttacks(self):
        funstring = ''
        for each in range( self.numbAtks ):
            funstring = self.atkList[each]
            if int(funstring[1]) == 2 and int(funstring[2]) == 0:
                self.atkListAsInt.append(20)
            elif int(funstring[1]) == 1:
                if int(funstring[2]) == 0:
                    self.atkListAsInt.append(10)
                else:
                    self.atkListAsInt.append(12)
            else:
                self.atkListAsInt.append( int(funstring[1]) )  

    def buildAbilities(self):
        abilCounter = 0
        if self.numbAtks == 1:
            abilCounter = 9
        else:
            abilCounter = 10
        while abilCounter < len( self.statList ):
            self.abiList.append( self.statList[ abilCounter ] )
            abilCounter += 1



    def getHurt(self, damage: int):
        dmg: int = damage
        dmg -= self.armour
        if self.hp > 0:
            while self.hp > 0 and dmg > 0:
                self.hp -= 1
                dmg -= 1

        if dmg > 0:
            while dmg > 0:
                self.strength -= 1
                dmg -= 1
            self.checkForCD()
                

def loadBaddieList(First=True)-> list:
    listOBaddies = []
    if First:
        listOBaddies.append( 'Dumb Dummy,Smells Bad,4,0,10,10,8,2,d6 knife,d4 stone,general bad attitude.')
    else:
        filetypes = ('text files', '*.txt'), ('all files', '*.*')
        file = fd.askopenfile(title='Chose a Monster List',filetypes=filetypes)
        for line in file:
            listOBaddies.append( line.replace('\n', '' ) )
    
    allBadGuys: list[aBadGuy] = []
    for each in listOBaddies:
        allBadGuys.append( aBadGuy(each))
    return allBadGuys

class baddieHolder(ttk.Frame):
    def __init__(self, container, stats: aBadGuy):
        super().__init__(container)
        self.creator = container
        self.theGuy = stats
        self.hasCD = False

        self.config(borderwidth= 1, padding=4, relief=tk.RAISED)
        self.columnconfigure( 5, weight=1 )

        self.name = ttk.Label(self, text=self.theGuy.name, font=('Helvetica',15))
        self.name.grid(row=1, column=1, columnspan=2, sticky=tk.SW )

        self.desc = ttk.Label(self, text=stats.desc, justify=tk.LEFT)
        self.desc.grid(row=1,column=3,columnspan=3, sticky=tk.SW)

        if self.theGuy.numbAtks == 2:
            self.atk1 = ttk.Button(self, text= stats.atkList[0],
                                   command=lambda: {self.creator.addLineToText(' '),
                                                    self.creator.addLineToText('result of ' + str(_Roll(1, self.theGuy.atkListAsInt[0]))),
                                                    self.creator.addLineToText('rolling d' + str(self.theGuy.atkListAsInt[0]))})
            self.atk1.grid(row=1, column=7, sticky=tk.S)
            self.atk2 = ttk.Button(self, text= stats.atkList[1],
                                   command=lambda: {self.creator.addLineToText(' '),
                                                    self.creator.addLineToText('result of ' + str(_Roll(1, self.theGuy.atkListAsInt[1]))),
                                                    self.creator.addLineToText('rolling d' + str(self.theGuy.atkListAsInt[1]))})
            self.atk2.grid(row=1, column=8, sticky=tk.S)
        else:
            self.atk1 = ttk.Button(self, text= stats.atkList[0],
                                   command=lambda: {self.creator.addLineToText(' '),
                                                    self.creator.addLineToText('result of ' + str(_Roll(1, self.theGuy.atkListAsInt[0]))),
                                                    self.creator.addLineToText('rolling d' + str(self.theGuy.atkListAsInt[0]))})
            self.atk1.grid(row=1, column=8, sticky=tk.S)
            

        self.HP = tk.Label(self, text=str(self.theGuy.hp)+'hp', justify=tk.RIGHT, width=4)
        self.HP.grid(row=2, column=1, sticky=tk.E)
        self.AR = tk.Label(self, text=str(self.theGuy.armour)+'a')
        self.AR.grid(row=2, column=2, sticky=tk.W)

        self.STR = tk.Label(self, text=self.theGuy.strength)
        self.STR.grid(row=2, column=3, sticky=tk.E)
        self.DEX = tk.Label(self, text=self.theGuy.dexterity)
        self.DEX.grid(row=2, column=4, sticky=tk.EW)
        self.CHA = tk.Label(self, text=self.theGuy.charisma)
        self.CHA.grid(row=2, column=5, sticky=tk.W)



        self.kill = ttk.Button(self, text='kill', command=lambda: self.dieDieDie() )
        self.kill.grid(row=2, column=8)
        self.hurt = ttk.Button(self, text='hurt', command=lambda: self.takeDamage() )
        self.hurt.grid(row=2, column=7)

        self.abilities: tk.Label = []
        self.abilityCounter = 0
        for x in self.theGuy.abiList:
            self.abilities.append( tk.Label(self, text=('     \u2022 ' + self.theGuy.abiList[ self.abilityCounter])))
            self.abilities[self.abilityCounter].grid( row=(3+self.abilityCounter), column=1, columnspan=8, sticky=tk.W )
            self.abilityCounter += 1

    def takeDamage(self):
        self.theGuy.getHurt( self.creator.getInputField())
        self.updateSelf()
        self.checkForCD()

    def checkForCD(self):
        if self.hasCD == False and self.theGuy.tookCriticalDMG == True:
            self.creator.addLineToText( self.theGuy.name + ' took Critical Damage!')
            self.hasCD = True

    def updateSelf(self):
        self.HP.config( text= str(self.theGuy.hp)+'hp')
        self.STR.config( text= self.theGuy.strength )

    def dieDieDie(self):
        name = self.theGuy.name
        self.creator.addLineToText( ' ')
        self.creator.addLineToText(name +' is destroyed.')
        self.destroy()



class combatFrame(ttk.Frame):
    def __init__(self,container):
        super().__init__(container)
        self.creator = container
        self.textBoxContents = ['']
        self.textLines = 1
        self.maxTextLines = 8
        
        self.topFrame = ttk.Frame(self)
        self.topFrame.grid(row=0,column=1, sticky=tk.EW)
        self.columnconfigure(1, weight=1)
        self.textBtn = ttk.Button(self.topFrame, text='make', command=lambda: self.addOneText())
        self.textBtn.grid(row=0, column=1)
        self.loadBtn = ttk.Button(self.topFrame,text='file', command=lambda: self.recreateBaddieList())
        self.loadBtn.grid(row=0, column=2)
        self.grntBtn = ttk.Button(self.topFrame, text='+Grunt', command=lambda: self.addOneJerk())
        self.grntBtn.grid(row=0, column=3)

        self.inputField = tk.Text(self.topFrame, width=36,height=1)
        self.inputField.grid(row=0,column=4,columnspan=4, sticky=tk.E)

        self.listOfJerks = loadBaddieList()
        self.listOfHolders: list[baddieHolder] = []
        for each in range( len(self.listOfJerks) ):
            self.listOfHolders.append( baddieHolder( self, self.listOfJerks[each]))
            self.listOfHolders[each].grid(row=(each+1), column=1, sticky=tk.EW)

        self.botFrame = ttk.Frame(self)
        self.botFrame.grid( row=200, column=1, sticky=tk.EW)
        self.botFrame.columnconfigure(7, weight=1)
        self.textBox = tk.Text(self.botFrame, height=3)
        self.textBox.grid(row=1,column=1,columnspan=7)
        self.updateTextBox()
        #   All the noble polyhederals
        self.d4button = ttk.Button(self.botFrame, text='d4', width=2, padding=0,
                                   command=lambda: self.addLineToText('Rolling d4: '+ str( _Roll(1,4))))
        self.d4button.grid(row=2, column=1, padx=0, pady=0)
        self.d6button = ttk.Button(self.botFrame, text='d6', width=2, padding=0,
                                   command=lambda: self.addLineToText('Rolling d6: '+ str( _Roll(1,6))))
        self.d6button.grid(row=2, column=2, padx=0, pady=0)
        self.d8button = ttk.Button(self.botFrame, text='d8', width=2, padding=0,
                                   command=lambda: self.addLineToText('Rolling d8: '+ str( _Roll(1,8))))
        self.d8button.grid(row=2, column=3, padx=0, pady=0)
        self.d10button = ttk.Button(self.botFrame, text='d10', width=3, padding=0,
                                   command=lambda: self.addLineToText('Rolling d10: '+ str( _Roll(1,10))))
        self.d10button.grid(row=2, column=4, padx=0, pady=0)
        self.d12button = ttk.Button(self.botFrame, text='d12', width=3, padding=0,
                                   command=lambda: self.addLineToText('Rolling d12: '+ str( _Roll(1,12))))
        self.d12button.grid(row=2, column=5, padx=0, pady=0)
        self.d20button = ttk.Button(self.botFrame, text='d20', width=3, padding=0,
                                   command=lambda: self.addLineToText('Rolling d20: '+ str( _Roll(1,20))))
        self.d20button.grid(row=2, column=6, sticky=tk.W)


        self.moraleButton = ttk.Button(self.botFrame, text='Morale', command=lambda: self.moraleCheck())
        self.moraleButton.grid(row=3, column=6)
        self.doneButton = ttk.Button(self.botFrame, text='End Combat',command=lambda: self.creator.setGridTurns())
        self.doneButton.grid(row=3,column=7, sticky=tk.E)

    def moraleCheck(self):
        for each in moraleCheck():
            self.addLineToText( each )

    def updateTextBox(self):
        self.textBox.delete('1.0',tk.END)
        counter = 1.0
        for each in self.textBoxContents:
            self.textBox.insert( counter, each)
            counter += 1.0

    def addLineToText(self, line:str):
        if self.textLines > self.maxTextLines:
            self.textBoxContents.pop()
            self.textLines -= 1
        self.textBoxContents.insert(0, line + '\n')
        self.textLines += 1
        self.updateTextBox()
    
    def getInputField(self)->int:
        holder = 0
        try:
            holder = int(self.inputField.get('1.0',tk.END))
        except ValueError:
            showinfo(title="Empty Text Widget", message="Put a number in dummy.")
        finally:
            return holder
    
    def getInputFieldString(self)->str:
        line = ''
        try: 
            line = self.inputField.get('1.0',tk.END)
        except ValueError:
            showinfo(title='Empty Text Widget', message='Paste in a monster line')
        finally:
            return line

    def addOneJerk(self):
        adj = GadjectiveList[ _Roll(1, len(GadjectiveList)-1)]
        self.listOfHolders.append( baddieHolder(self, aBadGuy( self.creator.getName() + ',' + adj + ',' + str(_Roll(1,6)) +
                    ',0,' + str(roll3d6()) + ',' + str(roll3d6()) + ',' + str(roll3d6()) + ',1,d6 weapon,Just another guy')))
        locater = len(self.listOfHolders)
        self.listOfHolders[locater-1].grid(row=locater, column=1, sticky=tk.EW)
    
    def addOneText(self):
        self.listOfHolders.append( baddieHolder(self, aBadGuy( self.getInputFieldString() )))
        locater = len(self.listOfHolders)
        self.listOfHolders[locater-1].grid(row=locater, column=1, sticky=tk.EW)
        self.inputField.delete('1.0', tk.END)

    def recreateBaddieList(self):
        self.textLines = 0
        self.textBoxContents = []
        self.updateTextBox()
        self.listOfJerks = []
        self.listOfJerks = loadBaddieList(False)
        for each in self.listOfHolders:
            each.destroy()
        self.listOfHolders: list[baddieHolder] = []
        for each in range( len(self.listOfJerks) ):
            self.listOfHolders.append( baddieHolder( self, self.listOfJerks[each]))
            self.listOfHolders[each].grid(row=(each+1), column=1, sticky=tk.EW)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('CombatTracking')
        self.geometry('500x500')
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

        self.battleWindow = combatFrame(self)
        self.battleWindow.grid(row=1, column=1, sticky=tk.NSEW)

    def endCombat(self):
        print('fight done')

if __name__ == "__main__":
    app = App()
    app.mainloop()