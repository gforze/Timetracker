from datetime import datetime
from pathlib import Path
import sys, time, json
import records, values
import shutil

val=values.Values("","", 0, 0, 0, "")

def start(val):
    val.date=datetime.now().strftime("%d-%m-%y %H:%M")
    val.startTime= time.time()
    val.run=1
    val.comment=""
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

def comment(val):
    if val.comment =="":
        print(getTime() + "  --Comment removed from "+val.taskname)
    else:
        print(getTime() + "  --Comment \"" + val.comment + " \" added to "+val.taskname)

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
    #Starts a new task, if one running stops and writes it to record
    if (argArray[0]=="start" or argArray[0] == "s") and len(argArray)==2:
        if val.run==0:
            val.taskname=argArray[1]
            start(val)
        elif val.run==1:
            stop(val)
            val.taskname=argArray[1]
            start(val)
    #Stops a running task and writes to record
    elif (argArray[0] == "stop" or argArray[0] == "end") and val.run==1:
        stop(val)
    #Adds a comment to task
    elif (argArray[0] == "c" or argArray[0]=="comment") and val.run==1:
        print (argArray)
        if len(argArray)==1:
            print ("Running task: " + val.taskname +"   Comment: "+ val.comment)
        elif len(argArray)==2 and argArray[1]=="rm":
            val.comment=""
            comment(val)
        elif len(argArray)>=2:
            val.comment=""
            for p in range(len(argArray)):
                if (p>0):
                    val.comment +=argArray[p] +" "
            comment(val)
        else:
            print("somthing wrong with format!")
    #Status writes elapsed time for running task
    elif argArray[0] == "status" and val.run==1:
        status(val)
    # r [arg] - prints arg number of  records from the newest. Arg = 0 or nothing writes all   
    elif argArray[0] =="r":
        file = Path("records.txt")
        if file.exists():
            if len(argArray)==2:
                if argArray[1]=="twoday":
                    records.getTwoday(getDate())
                else:  
                    records.getRecords(argArray[1])
            else:
                records.getRecords(0)
        else:
            print(getTime() +"  --Records does not exist")
    #rt - writes all task for twoday
    elif argArray[0]=="rt":
        records.getTwoday(getDate())
    #time [arg]- sums time spent on task with the name arg
    elif argArray[0] == "time" and len(argArray)==2:
        sumTask(argArray[1])
    #tasks - prints all tasks headers on record    
    elif argArray[0]=="tasks":
        records.getTasks()
    #rt [arg] - lists all records for chosen arg
    elif argArray[0]=="rtask" and len(argArray)==2:
        recordTask(argArray[1])
    #help - Complete list of commands
    elif argArray[0] =="help":
        help()
    # close or quit/q - writes running task to records and closes program   
    elif argArray[0] =="close" or argArray[0]=="quit" or argArray[0]=="q":
        if val.run==1:
            stop(val)
        sys.exit(0)
    else:
        print("Wrong input, try \"help\" for list of instructions")

def getTime():
    return datetime.now().strftime("%H:%M")

def getDate():
    return datetime.now().strftime("%d-%m-%y")

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
    print("start/s [arg] - starts the timer for a new task with the name arg")
    print("status - prints how long a task has been running")
    print("comment [arg] adds comment to running task")
    print("stop/end - stops the task and writes to records")
    print("r [arg] - prints arg number of  records from the newest. Arg = 0 or nothing writes all. arg=twoday writes all for twoday(rt)")
    print("rtask [task] - lists all records for chosen task") 
    print("time [arg]- sums time spent on task with the name arg")
    print("tasks - prints all tasks headers on record")
    print("close or quit/q - writes running task to records and closes program")
    print("help - Complete list of commands")
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
