import json
from pathlib import Path
from datetime import datetime

recordList=[]
taskList = []
sortList=[]
taskTime=0

class Record(object):
    def __init__(self, date, task, duration):
        self.date = date
        self.task = task
        self.duration = duration

def jsonDefault(object):
    return object.__dict__


def getRecords(num):
    readRecords()
    printRec(num)
    
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
            for p in recordList: print (p["date"] +  "     "+ p["task"] +"     "+ p["duration"])
        else:
            for i in range(length-num, length):
                p=recordList[i]
                print (p["date"] +  "     "+ p["task"] +"     "+ p["duration"])
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
    record=Record(val.date, val.taskname, val.duration)
    
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
            print (p["date"] +  "     "+ p["task"] +"     "+ p["duration"])

def recordsDateSort(dateStart, dateEnd):
    global recordList
    global sortList

    try:
        sortList=[]
        startDate=datetime.strptime(dateStart, "%d-%m-%y").date()
        endDate=datetime.strptime(dateEnd, "%d-%m-%y").date()


        for p in recordList:
            temp=p["date"].split(" ")
            date=datetime.strptime(temp[0], "%d-%m-%y").date()
        
            if(date >= startDate and date <= endDate):
                sortList.append(p) 
                
    except ValueError:
        print("wrong input")

def sortListPrint(sd,ed):
    global sortList
    recordsDateSort(sd, ed)
    
    for p in sortList:
        print (p["date"] +  "     "+ p["task"] +"     "+ p["duration"])

def taskOnDates(taskname, dateStart, dateEnd):
    recordsDateSort(dateStart, dateEnd)
    global taskTime
    taskTime=0

    for p in sortList:
        if (taskname == p["task"]):
            taskTime += float(p["duration"])
            print (p["date"] +  "     "+ p["task"] +"     "+ p["duration"])

