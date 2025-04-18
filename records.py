import json
from pathlib import Path
from datetime import datetime

recordList=[]
taskList = []

class Record(object):
    def __init__(self, date, task, duration, comment):
        self.date = date
        self.task = task
        self.duration = duration
        self.comment = comment

def jsonDefault(object):
    return object.__dict__


def getRecords(num):
    readRecords()
    printRec(num)

def getTwoday(date):
    global recordList
    readRecords()
    for p in recordList:
        dagensDato=p["date"].split(" ")[0]
        if date==dagensDato:
            print (p["date"] +  "     "+ p["task"] +"     "+ p["duration"] +"  "+p["comment"])


def readRecords():
    global recordList
    global taskList
    recordList=[]
    taskList=[]

    file = open("records.txt", "r")
    for line in file:
        try:
            a = json.loads(line)
            recordList.append(a)
        except ValueError:
            print("Fix records file")
    file.close()
    taskHeaders(recordList, taskList)
    
def taskHeaders(recList, taList):
     for p in recList:
        if(p["task"] not in taList):
            taList.append(p["task"])

def getTasks():
    for p in taskList: print (p)

 
def printRec(num):
    global recordList
    length=len(recordList)
   
    try:
        num= int(num) 
        if(num >=length or num==0):
            for p in recordList: print (p["date"] +  "     "+ p["task"] +"     "+ p["duration"] +"  "+p["comment"])
        else:
            for i in range(length-num, length):
                p=recordList[i]
                print (p["date"] +  "     "+ p["task"] +"     "+ p["duration"]+"  "+p["comment"])
    except ValueError:
        printRec(0)


def sumTask(arg):
    sum=0
    global recordList
    readRecords()

    for a in recordList:
        if arg==a["task"]:
            sum += float(a["duration"])
               
    if sum==0:
        return False
    else:
        return sum

def writeToRecords(val):
    record=Record(val.date, val.taskname, val.duration, val.comment)
    
    file = Path("records.txt")
    if file.exists():
        file = open("records.txt", "a")
        file.write(json.dumps(record, default=jsonDefault) + "\n")
        file.close()
    else:
        file = open("records.txt", "w")
        file.write(json.dumps(record, default=jsonDefault) + "\n")
        file.close()

def recordsTaskname(name):
    global taskList
    global recordList
    for p in recordList:
        if(name==p["task"]): 
            print (p["date"] +  "     "+ p["task"] +"     "+ p["duration"]+"  "+p["comment"])

"""def recordsDateSort(dateStart, dateEnd):
    global recordList

    for p in recordList:
        date=p["date"].split(" ")
        if(dateStart==date[0]):
            if(dateEnd != date[0]):
                print (p["date"] +  "     "+ p["task"] +"     "+ p["duration"]+"  "+p["comment"])
            else:
                break"""
        
    


