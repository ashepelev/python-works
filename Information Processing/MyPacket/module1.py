import random
import time

def readMaleNames():
    S=[]
    for line in open("male_names.txt",mode='r',encoding='utf8'):
        S = S + [line.strip()]
    return S

def readFemaleNames():
    S=[]
    for line in open("female_names.txt",mode='r',encoding='utf8'):
        S = S + [line.strip()]
    return S

def readSongs():
    S=[]
    for line in open("songs.txt",mode='r',encoding='utf8'):
        S += [line.strip()]
    return S

def readSurnames():
    S=[]
    for line in open("surnames.txt",mode='r',encoding='utf8'):
        S = S + [line.strip()]
    return S

def makeFemaleSurname(surname):
    return surname + 'a'

def makeRandomSongsList(songs):
    S=[]
    for i in range(0,5):
        S += [songs[random.randint(0,499)]]
    return S

def makeRandomSex():
    return 'm' if random.randint(0,1)==1 else 'w'

def makeRandomAge():
    return random.randint(6,60)

def makeRandomNameSurname(maleNames, femaleNames, sex, surnames):
    res = ''
    if sex=='w':
        res = femaleNames[random.randint(0,135)] + ' '
        res = res + makeFemaleSurname(surnames[random.randint(0,249)])
    elif sex=='m':
        res = maleNames[random.randint(0,142)] + ' '
        res = res + surnames[random.randint(0,249)]
    return res

def makeList(maleNames=readMaleNames(), femaleNames=readFemaleNames(), \
             songs=readSongs(), surnames=readSurnames(), needToWrite=False, file='questionary.txt'):
    listResult = []
    t1 = time.clock()
    if needToWrite:
        form = open(file,mode='w',encoding='utf8')
        form.close()
        form = open(file,mode='a',encoding='utf8')
    for i in range(0,50000):
        age = makeRandomAge()
        sex = makeRandomSex()
        randSongs = makeRandomSongsList(songs)
        name_sur = makeRandomNameSurname(maleNames,femaleNames,sex,surnames)
        
        resultStr = "{0}:{1}:{2}".format(name_sur,age,sex)
        for i in range(0,5):
            resultStr += ":{0}".format(randSongs[i])
        resultStr += '\n'

        listResult += [resultStr]
                
        if needToWrite:
            print(resultStr,end='',file=form)            
    if needToWrite:
        print("Questionary generating time:",time.clock()-t1,"seconds")
        form.close()
    return listResult

