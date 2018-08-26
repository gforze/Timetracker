import json

recordList=[]
beenRead=0
class Record(object):
    def __init__(self, date, task, duration):
        self.date = date
        self.task = task
        self.duration = duration

def jsonDefault(object):
    return object.__dict__


def getRecords():
    readRecords()
    printRec()
    
def readRecords():
    global recordList
    recordList=[]
    file = open("records.txt", "r")
    for line in file:
        try:
            a = json.loads(line)
            recordList.append(a)
        except ValueError:
            print("Fix records file")
    file.close()
    
    

def printRec():
    global recordList
    for p in recordList: print (p)


def sumTask(arg):
    sum=0
    global recordList
    
    readRecords()
    for a in recordList:
        if arg==a["task"]:
            sum += float(a["duration"])
               
    if sum==0:
        print("No tasks with this name")
    else:
        print("Total time spent on " + arg + " is " + str(sum) + " minutes")
    



