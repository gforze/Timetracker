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

def calculateTime(time):
    time=int(time)
    if time>=60:
        hours=int(time/60)
        minutes=time%60
        if hours>=24:
            days=int(hours/24)
            hours=hours%24
            return (str(days) + " day(s) " + str(hours) + " hour(s) and " + str(minutes) + " minutes")
        return (str(hours) + " hour(s) and " + str(minutes) + " minutes")
    return (str(time) + " minutes")


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
        totalTimespent=calculateTime(sum)
        print("Total time spent on " + arg + " is " + totalTimespent) 
    



