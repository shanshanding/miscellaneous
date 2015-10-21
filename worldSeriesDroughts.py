# see http://shanshanding.github.io/projects/wsdroughts.html for exposition

from random import randint
from datetime import date
import numpy as np

def getNumTeams(endYear):
# year-by-year number of teams courtesy of
# http://www.seanlahman.com/baseball-archive/history-of-mlb-schedules/
    numTeams = {}
    numTeams.update(dict.fromkeys(list(range(1901,1961)), 16))
    numTeams.update(dict.fromkeys(list(range(1961,1962)), 18))
    numTeams.update(dict.fromkeys(list(range(1962,1969)), 20))
    numTeams.update(dict.fromkeys(list(range(1969,1977)), 24))
    numTeams.update(dict.fromkeys(list(range(1977,1993)), 26))
    numTeams.update(dict.fromkeys(list(range(1993,1998)), 28))
    numTeams.update(dict.fromkeys(list(range(1998,endYear+1)), 30))
    return numTeams

def getChampions(numTeams):
    champions = []
    for year in numTeams:
        champions.append(randint(1, numTeams[year]))
    return(champions)     

def drought(numTeams, originalTeams, numDroughts):
    champions = getChampions(numTeams)
    if len([i for i in originalTeams if i not in champions])>=numDroughts:
        return(1)
    else:
        return(0)
    
def droughtProbAny(startYear, endYear, numDroughts, numSims, condOnCubsDrought=False):
    if endYear>date.today().year or startYear<1901 or startYear>endYear:
        return -1
    
    numTeams =  {year:num for (year,num) in  getNumTeams(endYear).items() if year>=startYear}
    if condOnCubsDrought:
        for year in numTeams:
            numTeams[year] -= 1
    originalTeams = [i for i in range (1, numTeams[startYear]+1)]

    c=0
    for i in range(0,numSims):
        c += drought(numTeams, originalTeams, numDroughts)
    return(float(c)/numSims)

def droughtProbSpecific(startYear, endYear, numDroughts, condOnCubsDrought=False):
    if endYear>date.today().year or startYear<1901 or startYear>endYear:
        return -1
    
    numTeams =  {year:num for (year,num) in  getNumTeams(endYear).items() if year>=startYear}
    if condOnCubsDrought:
        for year in numTeams:
            numTeams[year] -= 1
    
    probList = [float(num-numDroughts)/num for num in numTeams.values()]
    return(reduce(lambda x, y: x*y, probList))

def droughtProbOriginal(startYear, endYear, numDroughts, numSims, condOnCubsDrought=False):
    if endYear>date.today().year or startYear<1901 or startYear>endYear or startYear>1960:
        return -1

    numTeams = 16
    if condOnCubsDrought:
        numTeams = 15

    originalTeams = [i for i in range (1, numTeams+1)]

    c=0
    for i in range(0,numSims):
        champions = np.random.choice(numTeams, endYear-startYear+1)+1
        if len([i for i in originalTeams if i not in champions])>=numDroughts:
            c+=1
    return(float(c)/numSims)
    
def main():
    print(droughtProbSpecific(1908, 2014, 1)) 
    print(droughtProbAny(1908, 2014, 1, 100000)) #one team's 107-year drought 
    print(droughtProbSpecific(1919, 2003, 2))
    print(droughtProbAny(1919, 2003, 2, 100000)) #two team's 85-year droughts
    print(droughtProbAny(1919, 2003, 3, 300000)) #three team's 85-year droughts

    print(droughtProbSpecific(1949, 2014, 1, True))
    print(droughtProbAny(1949, 2014, 1, 100000, True)) #one team's 66-year drought conditioning on the Cubs's drought

    print(droughtProbOriginal(1908, 2014, 1, 300000))   #one team's 107-year drought
                                                        #if expansion teams have had zero chance of winning 
    
if __name__ == "__main__":
    main()
