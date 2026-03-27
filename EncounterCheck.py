import random
from random import randint as _Roll

def moraleCheck()-> list:
    returnList = []
    returnList.append("")
    builderString = 'Morale: '
    morResult = ( _Roll(1,6) + _Roll(1,6))
    match morResult:
        case 2:
            builderString += 'Even zealots'
        case 3|4:
            builderString += 'Even furious creatures'
        case 5|6:
            builderString += 'Those committed to the fight'
        case 7|8:
            builderString += 'If they were nervous, they'
        case 9|10:
            builderString += 'Scared creatures'
        case _:
            builderString += 'Only cowards'
        
    builderString += ' will attempt to flee.'
    returnList.append( builderString )
    returnList.append('')
    return returnList


def encounterCheck()-> list:
    returnList = []
    returnList.append('')
    encResult = _Roll(1,6)
    
    builderString = ''
    if encResult < 2:
        rngResult = (_Roll(1,6) + _Roll(1,6))
        builderString += 'Range: '
        match rngResult:
            case 2|3:
                builderString += 'Melee'
            case 4|5:
                builderString += 'Close'
            case 6|7:
                builderString += 'Medium'
            case 8|9:
                builderString += 'Far'
            case 10|11:
                builderString += 'Sight'
            case _:
                builderString += 'Sounds'
        builderString += '     Reaction: '
        reaResult = (_Roll(1,6) + _Roll(1,6))
        match reaResult:
            case 2:
                builderString += 'Fight!'
            case 3|4:
                builderString += 'Distrust'
            case 5|6:
                builderString += 'Wary'
            case 7:
                builderString += 'Neutral'
            case 8|9:
                builderString += 'Curious'
            case 10|11:
                builderString += 'Interested'
            case _:
                builderString += 'Helpful'
        returnList.append( builderString )

    builderString = 'Encounter Check: d6 ('
    builderString += str(encResult) + ')     '

    match encResult:
        case 1:
            builderString += 'Encounter!'
        case 2:
            builderString += 'Spoor'
        case _:
            builderString += 'All Quiet'

    returnList.append( builderString )
    returnList.append('')
    
    return returnList