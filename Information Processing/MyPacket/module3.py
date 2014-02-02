from MyPacket.module2 import getSongs
import time
import sys

def getCategory(line):
    d = []
    ss = line.split(':')
    d += [ss[1]]
    d += [ss[2]]
    return d

def makeRatingPerCategory():
    d = {}
    for line in open("questionary.txt",mode='r',encoding='utf8'):
        songs = getSongs(line)
        category = getCategory(line)
        cat = findCategory(category)
        for i in range(0,5):
            putSongIntoCategory(songs[i],cat, d)
    return d

#1: <20 M
#2: <20 W
#3: >20 M
#4: >20 W
def putSongIntoCategory(song, cat, dictionary):
    if dictionary.get(song,[0,0,0,0]) == [0,0,0,0]:
        dictionary[song] = [0,0,0,0]
    dictionary[song][cat-1] += 1
    return

        
def findCategory(category):
    if category[0] <= str(20):
        if category[1] == 'm':
            return 1
        else:
            return 2
    else:
        if category[1] == 'm':
            return 3
        else:
            return 4
        

def buildResult(printToFile=False, fileName="Result2.txt",printToHtml=False):
    if printToFile:
        form = open(fileName,mode='w',encoding='utf8')
    else:
        form = sys.stdout
    t1 = time.clock()
    d = makeRatingPerCategory()
    print("Categories: ","1: <20 M","2: <20 W", "3: >20 M", "4: >20 W", sep='\n',file=form)
    for i in range(0,4):
        d1 = sorted(d.items(),key=lambda student: student[1][i], reverse=True)
        count = 0
        print("Category ",i,':',sep='',file=form)
        for k in d1:
            print("Song:",k[0],"| Votes:",k[1][i],file=form)
            count+=1
            if count==10:
                break
    print("Work Time:",time.clock()-t1,"seconds",file=form)
    if printToFile:
        form.close()
    if printToHtml:
        buildResultAndPrintIntoHtml(d)
    return

def buildResultAndPrintIntoHtml(d):
    t1 = time.clock()
    htmlFile = open("Report2.html",mode='w',encoding='cp1251')
    htmlFile.write("<html><head><title>Report №2</title></head>")
    htmlFile.write("<body><h1>Четыре списка из 10 композиций каждый, \
наиболее популярных в каждой из категорий участников.</h1>")
    print("Категории: ","1: Мужчины младше 20 лет", \
                   "2: Женщины младше 20 лет", "3: Мужчины старше 20 лет", \
                   "4: Женщины старше 20 лет", sep='<br></br>',file=htmlFile)
    
    for i in range(0,4):
        d1 = sorted(d.items(),key=lambda student: student[1][i], reverse=True)
        count = 0
        htmlFile.write("<h2>Категория " + str(i+1) +"</h2><ol>")        
        for k in d1:
            htmlFile.write("<li>Песня:  " + k[0] + " | Голосов: " + str(k[1][i])+"</li>")
            count +=1
            if count==10:
                break
        htmlFile.write("</ol>")
    htmlFile.write("Время создания веб-странички " + str(time.clock()-t1) + " секунд")
    htmlFile.write("</body></html>")
    htmlFile.close()
    return
