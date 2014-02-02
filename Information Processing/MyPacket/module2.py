import time
import sys

def getSongs(line):
    ss = line.strip().split(':')
    S = []
    for i in range(3,8):
        S += [ss[i]]
    return S

def makeRatingDict():
    d = {}
    for line in open("questionary.txt",mode='r',encoding='utf8'):
        songs = getSongs(line)
        for i in range(0,5):
            if d.get(songs[i],(0,0)) == (0,0):
                d[songs[i]] = ((i+1),1)
            else:
                d[songs[i]] = d[songs[i]][0]+(5-i), d[songs[i]][1] + 1
    return d

def findMostPopular(printToFile=False,fileName="Result1.txt",printToHtml=False):    
    if printToFile:
        form = open(fileName,mode='w',encoding='utf8')
    else:
        form = sys.stdout
    t1 = time.clock()
    d = makeRatingDict()
    for elem in sorted(d,key=d.get, reverse=True):
        print("Song: {0}, Rating: {1}, Count: {2}".format(elem, d[elem][0],d[elem][1]),file=form)
    print("Work Time:",time.clock()-t1,"seconds",file=form)
    if printToFile:
        form.close()
    if printToHtml:
        buildResultAndPrintIntoHtml(d)
    return d

def buildResultAndPrintIntoHtml(d):
    t1 = time.clock()
    htmlFile = open("Report1.html",mode='w',encoding='cp1251')
    htmlFile.write("<html><head><title>Report №1</title></head>")
    htmlFile.write("<body><h1>Список композиций в порядке их популярности. \
Каждый элемент этого списка должен содержать число упоминаний при опросе. \
Композиции, которые не были упомянуты ни разу, из списка исключаются.</h1><ol>")
    for elem in sorted(d,key=d.get, reverse=True):
        htmlFile.write("<li>Песня: {0} | Рейтинг: {1} | Голосов: {2}</li>".format \
                       (elem, d[elem][0],d[elem][1]))
    htmlFile.write("</ol>")
    htmlFile.write("Время создания веб-странички " + str(time.clock()-t1) + " секунд")
    htmlFile.write("</body></html>")
    htmlFile.close()
    return

    

            
            
