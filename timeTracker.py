from datetime import datetime
from pathlib import Path
import sys, time, json
import records, values
import shutil

val=values.Values("","", 0, 0, 0)

def start(val):
    val.date=datetime.now().strftime("%d-%m-%y %H:%M")
    val.startTime= time.time()
    val.run=1
    print(getTime() + "  --Tracking "+val.taskname)

def stop(val):
        val.duration=format((time.time()- val.startTime)/60, '.2f')
        val.run =0
        timepassed=calculateTime(val.duration)
        records.writeToRecords(val)
        print(getTime() +"  --Tracking stopped, "+val.taskname + " lasted for " + timepassed)

def status(val):
    val.duration = format((time.time()-val.startTime)/60 ,'.2f')
    timepassed=calculateTime(val.duration)
    print(getTime() + "  --Task "+val.taskname +" has been running for " + timepassed) 

def recordTask(name):
    records.recordsTaskname(name)
    sumTask(name)

def sumTask(arg):
    summedTime=records.sumTask(arg)
    if(summedTime==False):
        print("No tasks with this name")
    else:
        print(getTime() + "  --Total time spent on " + arg + " is "+ calculateTime(summedTime)) 



def action(arg, val):
    argArray=arg.split(" ")
    if (argArray[0]=="go" or argArray[0]=="g") and len(argArray)==2 and val.run==0:
        val.taskname=argArray[1]
        start(val)
    elif (argArray[0] == "end" or argArray[0]=="e") and val.run==1:
        stop(val)
    elif (argArray[0] == "status" or argArray[0]=="s") and val.run==1:
        status(val)
    elif argArray[0] =="close" or argArray[0]=="quit" or argArray[0]=="q":
        sys.exit(0)
    elif argArray[0] =="r":
        file = Path("records.txt")
        if file.exists():
            if(len(argArray)==2): 
                records.getRecords(argArray[1])
            else:
                records.getRecords(0)
        else:
            print(getTime() +"  --Records does not exist")
    elif argArray[0] =="help":
        help()
    elif argArray[0] == "time" and len(argArray)==2:
        sumTask(argArray[1])
    elif argArray[0]=="task":
        records.getTasks()
    elif argArray[0]=="rt" and len(argArray)==2:
        recordTask(argArray[1])
    else:
        print("Wrong command")

def getTime():
    return datetime.now().strftime("%H:%M")

def doesitExist():
    file = Path("records.txt")
    if file.exists():
        return True
    else:
        return False




def calculateTime(time):
    time=float(time)
    if time>=1:
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
    else:
        return ("under a minute")

def help():
    print("\n")
    print("Possible commands:")
    print("go [arg] - starts the timer for a new task with the name arg")
    print("status - prints how long a task has been running")
    print("end - stops the task and writes to records")
    print("r [arg] - prints arg number of  records from the newest. Arg = 0 or nothing writes all")
    print("rt [arg] - lists all records for chosen arg") 
    print("time [arg]- sums time spent on task with the name arg")
    print("task - prints all tasks headers on record")
    print("close or quit - closes program")
    print("\n")

def welcome():
    columns = shutil.get_terminal_size().columns

    print("\n")
    print("\n")
    print("Welcome to TT a simple timetracking application".center(columns))
    print("\n")
    print ("##### TT v0.5 #####".center(columns))
    print("\n")
    print("\n")

    if(doesitExist()):
        records.readRecords()
        
        print("Records exists and are loaded".center(columns))
    else:
        print("No records found, write  help in console for list of commands".center(columns))
        print("If it is your first time running the application a records file will be created for you".center(columns))

    print("\n")
    print("\n")

def main():
    welcome()

    while True:
        action(input("~ "), val)

if __name__ == "__main__":
    main()  
