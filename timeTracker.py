from datetime import datetime
from pathlib import Path
import sys, time, json
import records, values

val=values.Values("","", 0, 0, 0)

def start(val):
    val.date=datetime.now().strftime("%d-%m-%y %H:%M")
    val.startTime= time.time()
    val.run=1
    print("Running...")
    

def stop(val):
        val.duration=format((time.time()- val.startTime)/60, '.2f')
        val.run =0
        timepassed=calculateTime(val.duration)
        print(val.taskname + " lasted for " + timepassed)

def action(arg, val):
    argArray=arg.split(" ")
    if argArray[0]=="start" and len(argArray)==2 and val.run==0:
        val.taskname=argArray[1]
        print (calculateTime(180))
        print (calculateTime(182.13))
        print (calculateTime(40))
        print (calculateTime(1645))
        start(val)
    elif argArray[0] == "stop" and val.run==1:
        stop(val)
        writeToRecords(val)
    elif argArray[0] == "status" and val.run==1:
        status(val)
    elif argArray[0] =="close":
        print("Good bye")
        sys.exit(0)
    elif argArray[0] =="r":
        file = Path("records.txt")
        if file.exists():
            records.getRecords()
        else:
            print("Records do not exist")
    elif argArray[0] =="help":
        help()
    elif argArray[0] == "time" and len(argArray)==2:
        records.sumTask(argArray[1])
    else:
        print("Wrong command")

def writeToRecords(val):
    record=records.Record(val.date, val.taskname, val.duration)
    
    file = Path("records.txt")
    if file.exists():
        file = open("records.txt", "a")
        file.write(json.dumps(record, default=records.jsonDefault) + "\n")
        file.close()
    else:
        file = open("records.txt", "w")
        file.write(json.dumps(record, default=records.jsonDefault) + "\n")
        file.close()

def status(val):
    val.duration = format((time.time()-val.startTime)/60 ,'.2f')
    print(val.taskname +" has been running for " + str(val.duration) + " minutes")

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

def help():
    print("\n")
    print("Possible commands:")
    print("start [arg] - starts the timer for a new task with the name arg")
    print("status - prints how long a task has been running")
    print("stop - stops the task and writes to records")
    print("r - prints records")
    print("time [arg]- sums time spent on task with the name arg")
    print("close - closes program")
    print("\n")

    
while True:
    action(input("Waiting for command: "), val)
  
