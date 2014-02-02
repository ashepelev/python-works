import MyPacket.module3
import time
import sys

def makeRatingPerPerson():
    d = {}
    for line in open("questionary.txt",mode='r',encoding='utf8'):
        songs = MyPacket.module3.getSongs(line)
        category = MyPacket.module3.getCategory(line)
        cat = MyPacket.module3.findCategory(category)
        nameSurname = getNameSurname(line)
        for i in range(0,5):
            writeSongIntoDict(songs[i],cat,d,nameSurname)
    return d


def getNameSurname(line):
    return line.split(':')[0]

def writeSongIntoDict(song, cat, d, nameSurname):
    if d.get(song,[0,0,0,0,[]]) == [0,0,0,0,[]]:
        d[song] = [0,0,0,0,[]]
    putSong(song,cat,d,nameSurname)
    return

def putSong(song,cat,d,nameSurname):
    d[song][cat-1]+=1
    d[song][4]+=[nameSurname]
    return

def buildResult(printToFile=False, fileName="Result3.txt",printToHtml=False,songsPerCat=3):
    if printToFile:
        form = open(fileName,mode='w',encoding='utf8')
    else:
        print("Вывод очень большой! Вывод только в файл!")        
    t1 = time.clock()
    d = makeRatingPerPerson()
    if printToFile:
        print("Categories: ","1: <20 M","2: <20 W", "3: >20 M", "4: >20 W", sep='\n',file=form)
    for i in range(0,4):
        d1 = sorted(d.items(),key=lambda student: student[1][i], reverse=True)
        count = 0
        if printToFile:
            print("Category ",i,':',sep='',file=form)
        for k in d1:
            for person in k[1][4]:
                if printToFile:
                    print("Person:",person,"voted for:",k[0],file=form)
            count+=1
            if count==10:
                break
    if printToFile:
        print("Work Time:",time.clock()-t1,"seconds",file=form)
    if printToFile:
        form.close()
    if printToHtml:
        buildResultAndPrintIntoHtml(d,songsPerCat)
    return

def buildResultAndPrintIntoHtml(d,songsPerCat=3):
    t1 = time.clock()
    htmlFile = open("Report3.html",mode='w',encoding='cp1251')
    htmlFile.write("<html><head><title>Report №3</title></head>")
    htmlFile.write("<body><h1>Отчет номер 3. Четыре отдельных списка \
с именами и фамилиями всех отвечающих, которые назвали на \
 первом месте одну из трёх композиций, наиболее популярных \
 в их категории.  </h1>")
    print("Категории: ","1: Мужчины младше 20 лет", \
                   "2: Женщины младше 20 лет", "3: Мужчины старше 20 лет", \
                   "4: Женщины старше 20 лет", sep='<br></br>',file=htmlFile)
    for i in range(0,4):
        d1 = sorted(d.items(),key=lambda student: student[1][i], reverse=True)
        count = 0
        htmlFile.write("<h2>Категория " + str(i+1) +"</h2>")
        for k in d1:
            htmlFile.write("<h2>Песня: " + k[0] + "</h2><ol>")
            for person in k[1][4]:
                htmlFile.write("<li>"+person+"</li>")
            htmlFile.write("</ol>")
            count+=1
            if count==songsPerCat:
                break
    htmlFile.write("Время создания веб-странички " + str(time.clock()-t1) + " секунд")
    htmlFile.write("</body></html>")
    htmlFile.close()
    return
