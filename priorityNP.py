import heapq
#Non preemptive priority based.
def PriorityNP(process, n):
    Ready = []
    InputQ = []
    OutputQ = []

    i=0
    time = 0
    current = -1
    processorLeft = 0
    flag = False

    while True:
    #Phase 1 - Perform I/O
        #Arriving process
        while i<n and time == process[i]["arrivalTime"]:
            tempIndex = process[i]["index"]+1
            heapq.heappush(Ready, [process[i]["priority"], i, process[i]["operation"][tempIndex]])
            i += 1

        if len(InputQ) != 0:
            tempPriority, inputQProcess, inputLeft = InputQ[0]
        #Remove and add to ready if input operation complete
            if inputLeft == 0:
                process[inputQProcess]["index"] += 2
                tempIndex = process[inputQProcess]["index"]+1
                heapq.heappush(Ready, [tempPriority, inputQProcess, process[inputQProcess]["operation"][tempIndex]])
                InputQ.pop(0)


        if len(OutputQ) != 0:
            tempPriority, outputQProcess, outputLeft = OutputQ[0]
        #Remove and add to ready if output operation complete
            if outputLeft == 0:
                process[outputQProcess]["index"] += 2
                tempIndex = process[outputQProcess]["index"]+1
                heapq.heappush(Ready, [tempPriority, outputQProcess, process[outputQProcess]["operation"][tempIndex]])
                OutputQ.pop(0)

        #From input queue
        if len(InputQ) != 0:
            InputQ[0][2] -= 1
            
        if len(OutputQ) != 0:
            OutputQ[0][2] -= 1

        #print("Ready queue at start of t="+str(time))
        #print()    

    #Phase 2 - Select process to execute

        #No process executing
        if current == -1:
            #Take from ready and refill RRQuanta
            if len(Ready) != 0:
                tempPriority, current, processorLeft = Ready[0]
                if process[current]["responseTime"] == -1:
                    process[current]["responseTime"] = time-process[current]["arrivalTime"]
                heapq.heappop(Ready)
            #No process in ready, IDLE CPU

        time += 1

        #process in ready state were waiting
        for ind, p in enumerate(Ready):
            process[p[1]]["waitingTime"] += 1

        #Execute the process if any
        if current != -1:
            processorLeft -= 1
            #process state completes
            if processorLeft == 0:
                #check if any I/O
                process[current]["index"] += 2
                tempIndex = process[current]["index"]
                tempOperation = process[current]["operation"][tempIndex]

                #complete process done
                if tempOperation == -1:
                    process[current]["turnAroundTime"] = time-process[current]["arrivalTime"]
                else:
                    flag = True
                
                currentCopy = current
                current = -1
            else:
                tempOperation = None
        else:
            tempOperation = None



    #Phase 3 I/O and CPU for current time done, update.

        if flag and tempOperation == "I":
            tempIndex = process[currentCopy]["index"]+1
            InputQ.append([process[currentCopy]["priority"], currentCopy, process[currentCopy]["operation"][tempIndex]])
            flag = False

        elif flag and tempOperation == "O":
            tempIndex = process[currentCopy]["index"]+1
            OutputQ.append([process[currentCopy]["priority"], currentCopy, process[currentCopy]["operation"][tempIndex]])
            flag = False

        else:
            pass

        if (i, current, len(Ready), len(InputQ), len(OutputQ)) == (n, -1, 0, 0, 0):
            break


def main():
    inputFile = open("input.dat", "r")
    n = int(inputFile.readline())
    quanta = int(inputFile.readline())

    process = []

    for i in range(n):
        struct = dict()
        temp = inputFile.readline().split()
        struct["pid"] = int(temp[0])
        struct["priority"] = int(temp[1])
        struct["arrivalTime"] = int(temp[2])
        struct["operation"] = temp[3:]
        for i, item in enumerate(struct["operation"]):
            if not item in ["P", "I", "O"]:
                struct["operation"][i] = int(item)
        struct["index"] = 0
        struct["responseTime"] = -1
        struct["turnAroundTime"] = 0
        struct["waitingTime"] = 0
        process.append(struct)
    process = sorted(process, key=lambda x: (x["arrivalTime"], -x["priority"]))

    PriorityNP(process, n)

    stat = [0, 0, 0]

    print("Process ID | ResponseTime | WaitingTime | TurnAroundTime")
    for i, value in enumerate(process):
        t1 = value["pid"]
        t2 = value["responseTime"]
        t3 = value["waitingTime"]
        t4 = value["turnAroundTime"]
        stat[0] += t2
        stat[1] += t3
        stat[2] += t4
        print("{:^}     {:^}        {:^}        {:^} ".format(t1, t2, t3, t4))
        
    print("Average ResponseTime "+str(stat[0]/n))
    print("Average WaitingTime "+str(stat[1]/n))
    print("Average TurnAroundTime "+str(stat[2]/n))

if __name__ == "__main__":
    main()