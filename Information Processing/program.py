import MyPacket.module1
import MyPacket.module2
import MyPacket.module3
import MyPacket.module4
import time

import sys

def checkIfMakeFile():
    makeFileQuestion = str(input("Make file? {Y/N} "))
    while not (makeFileQuestion.startswith('Y') | makeFileQuestion.startswith('N')):
        print("Error: only Y or N!")
    if makeFileQuestion.startswith('Y'):
        return True
    else:
        return False

def getItem():
    correctItem = False
    while not correctItem:
        try:            
            chosenItem = int(input())
            correctItem = True
        except ValueError:
            print("Error: chosen item is Integer only!")
    return chosenItem

def checkIfMakeHtml():
    makeFileQuestion = str(input("Make HTML file? {Y/N} "))
    while not (makeFileQuestion.startswith('Y') | makeFileQuestion.startswith('N')):
        print("Error: only Y or N!")
    if makeFileQuestion.startswith('Y'):
        return True
    else:
        return False

print("0: Вы разархивировали документ, но в нем ничего нет - сделать все!")
print("1: Сгенерировать результаты опросов")
print("2: Список песен по популярности")
print("3: 10 самых популярных песен в каждой категории")
print("4: Люди, которым нравятся самые популярные песни в их категории")

chosenItem = getItem()

if chosenItem==0:
    t1 = time.clock()
    MyPacket.module1.makeList(needToWrite=True)
    MyPacket.module2.findMostPopular(printToFile=True,printToHtml=True)
    MyPacket.module3.buildResult(printToFile=True,printToHtml=True)
    MyPacket.module4.buildResult(printToFile=True,printToHtml=True)
    print("На всю работу ушло",time.clock()-t1,"секунд")
elif chosenItem==1:
    makeFile = checkIfMakeFile()
    if not makeFile:
        print("Нет задач")
        sys.exit(0)
    MyPacket.module1.makeList(needToWrite=makeFile)
elif chosenItem==2:
    makeHtml = checkIfMakeHtml()
    makeFile = checkIfMakeFile()
    MyPacket.module2.findMostPopular(printToFile=makeFile,printToHtml=makeHtml)
elif chosenItem==3:
    makeHtml = checkIfMakeHtml()
    makeFile = checkIfMakeFile()
    MyPacket.module3.buildResult(printToFile=makeFile,printToHtml=makeHtml)
elif chosenItem==4:
    makeHtml = checkIfMakeHtml()
    makeFile = checkIfMakeFile()
    if not (makeHtml | makeFile):
        print("Нет задач")
        sys.exit(0)
    print("Введите кол-во песен в категории для анализа")
    songCount = getItem()
    if songCount <= 0:
        print("Неверное число песен")
    MyPacket.module4.buildResult(printToFile=makeFile,printToHtml=makeHtml, \
                                 songsPerCat=songCount) 
else:
    print("Неверный пункт меню")
    
        

