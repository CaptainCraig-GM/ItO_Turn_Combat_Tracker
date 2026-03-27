from random import randint as _Roll
import random

class LootList:
    def __init__(self,fantasy=True):
        self.EMPTY = []
        self.WEIRD = []
        self.RESOU = []
        self.TOOLS = []
        #Cash !
        self.TREAS = []
        if fantasy:
            with open( 'Lists/Fantasy/empty.txt','r')as file:
                self.EMPTY = file.read().split(',')
                for each in self.EMPTY:
                    each.strip()
            with open( 'Lists/Fantasy/weird.txt','r')as file:
                self.WEIRD = file.read().split(',')
                for each in self.WEIRD:
                    each.strip()
            with open( 'Lists/Fantasy/resources.txt','r')as file:
                self.RESOU = file.read().split(',')
                for each in self.RESOU:
                    each.strip()
            with open( 'Lists/Fantasy/tools.txt','r')as file:
                self.TOOLS = file.read().split(',')
                for each in self.TOOLS:
                    each.strip()
            with open( 'Lists/Fantasy/treasure.txt','r')as file:
                self.TREAS = file.read().split(',')
                for each in self.TREAS:
                    each.strip()
        else:
            with open( 'Lists/Qud/empty.txt','r')as file:
                self.EMPTY = file.read().split(',')
                for each in self.EMPTY:
                    each.strip()
            with open( 'Lists/Qud/weird.txt','r')as file:
                self.WEIRD = file.read().split(',')
                for each in self.WEIRD:
                    each.strip()
            with open( 'Lists/Qud/resources.txt','r')as file:
                self.RESOU = file.read().split(',')
                for each in self.RESOU:
                    each.strip()
            with open( 'Lists/Qud/tools.txt','r')as file:
                self.TOOLS = file.read().split(',')
                for each in self.TOOLS:
                    each.strip()
            with open( 'Lists/Qud/treasure.txt','r')as file:
                self.TREAS = file.read().split(',')
                for each in self.TREAS:
                    each.strip()

    def getCoin(self):
        match _Roll(1,6):
            case 1|2|3:
                return str( _Roll(1,20)+_Roll(1,20) ) + ' Coppers'
            case 4|5:
                return str( _Roll(1,20) ) + ' Silvers'
            case _:
                return str( _Roll(1,2) ) + ' Gold'
    
    def getLoot(self)->str:
        match _Roll(1,12):
            case 1|2:
                return random.choice( self.EMPTY )
            case 3:
                return random.choice( self.WEIRD )
            case 4|5|6:
                return random.choice( self.RESOU )
            case 7|8|9:
                return random.choice( self.TOOLS )
            case 10|11:
                return self.getCoin()
            case _:
                return random.choice( self.TREAS )    

