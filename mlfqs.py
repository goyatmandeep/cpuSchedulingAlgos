#Order to enter ready state - New process > Input > Output > Just Finished
def MLFQ(process, n, nQ, quantas, t1, t2):
    Ready = [[] for i in range(nQ)]
    InputQ = []
    OutputQ = []

    pointer=0
    time = 0
    current = -1
    processorLeft = 0
    RRQuanta = 0 #For the particular process in execution (RR)
    flag = False
    flagQ = False

    while True:
    #Phase 1 - Perform I/O

        #Arriving process
        while pointer<n and time == process[pointer]["arrivalTime"]:
            tempIndex = process[pointer]["index"]+1
            #id, operation left, time left in Q
            Ready[0].append([pointer, process[pointer]["operation"][tempIndex], t1])
            pointer += 1

        if len(InputQ) != 0:
            inputQProcess, inputLeft, t = InputQ[0]
        #Remove and add to ready if input operation complete
            if inputLeft == 0:
                process[inputQProcess]["index"] += 2
                tempIndex = process[inputQProcess]["index"]+1
                currentQ = process[inputQProcess]["Q"]
                Ready[currentQ].append([inputQProcess, process[inputQProcess]["operation"][tempIndex], t])
                InputQ.pop(0)
                    

        if len(OutputQ) != 0:
            outputQProcess, outputLeft, t = OutputQ[0]
        #Remove and add to ready if output operation complete
            if outputLeft == 0:
                process[outputQProcess]["index"] += 2
                tempIndex = process[outputQProcess]["index"]+1
                currentQ = process[outputQProcess]["Q"]
                Ready[currentQ].append([outputQProcess, process[outputQProcess]["operation"][tempIndex], t])
                OutputQ.pop(0)

        #From input queue
        if len(InputQ) != 0:
            InputQ[0][1] -= 1
            
        if len(OutputQ) != 0:
            OutputQ[0][1] -= 1

        #print("Ready queue at start of t="+str(time))
        #print()    

    #Phase 2 - Select process to execute

        #No process executing
        if current == -1:
            #Take from ready and refill RRQuanta
            for i in range(nQ):
                if len(Ready[i]) != 0:
                    current, processorLeft, T = Ready[i][0]
                    if process[current]["responseTime"] == -1:
                        process[current]["responseTime"] = time-process[current]["arrivalTime"]
                    RRQuanta = quantas[i]
                    Ready[i].pop(0)
                    break
            #No process in ready, IDLE CPU

        time += 1

        #process in ready state were waiting
        for i in range(nQ):
            for ind, p in enumerate(Ready[i]):
                process[p[0]]["waitingTime"] += 1

        #Execute the process if any
        if current != -1:
            RRQuanta -= 1
            processorLeft -= 1
            T = max(T-1, 0)

            #if time in q finsh, wait for quanta or process to finish.
            
            if processorLeft == 0:
                if T == 0:
                    flagQ = True
                    if process[current]["down"]:
                        process[current]["Q"] += 1
                        if process[current]["Q"] == nQ-1:
                            process[current]["down"] = False

                    else:
                        process[current]["Q"] -= 1
                        if process[current]["Q"] == 0:
                            process[current]["down"] = True
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

            elif RRQuanta == 0:
                #context switch
                if T == 0:
                    if process[current]["down"]:
                        process[current]["Q"] += 1
                        if process[current]["Q"] == nQ-1:
                            process[current]["down"] = False
                            T = t2
                        else:
                            T = t1

                    else:
                        process[current]["Q"] -= 1
                        if process[current]["Q"] == 0:
                            process[current]["down"] = True
                            T = t1
                        else:
                            T = t2
                currentQ = process[current]["Q"]
                Ready[currentQ].append([current, processorLeft, T])
                current = -1
                tempOperation = None
            else:
                tempOperation = None
        else:
            tempOperation = None



    #Phase 3 I/O and CPU for current time done, update.
        
        if flag and tempOperation == "I":
            tempIndex = process[currentCopy]["index"]+1
            if flagQ:
                if process[currentCopy]["down"]:
                    T = t1
                else:
                    T = t2
                flagQ = False
            InputQ.append([currentCopy, process[currentCopy]["operation"][tempIndex], T])
            flag = False

        elif flag and tempOperation == "O":
            tempIndex = process[currentCopy]["index"]+1
            if flagQ:
                if process[currentCopy]["down"]:
                    T = t1
                else:
                    T = t2
                flagQ = False
            OutputQ.append([currentCopy, process[currentCopy]["operation"][tempIndex], T])
            flag = False
        else:
            pass

        if (pointer, len(InputQ), len(OutputQ), current) == (n, 0, 0, -1):
            for i in range(nQ):
                if len(Ready[i]) == 0:
                    pass
                else:
                    break

                if i == nQ-1:
                    return




def main():
    inputFile = open("MLFQ.dat", "r")
    nQ = int(inputFile.readline())
    quantas = [int(x) for x in inputFile.readline().split()]
    t1, t2 = map(int, inputFile.readline().split())

    processes = inputFile.readlines()
    #print(processes)

    process = []
    n = 0

    for k in range(len(processes)):
        struct = dict()
        temp = processes[k].split()
        try:
            struct["pid"] = int(temp[0])
        except:
            break
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
        struct["Q"] = 0
        struct["down"] = True
        process.append(struct)
        n += 1

    process = sorted(process, key=lambda x: (x["arrivalTime"], -x["priority"]))

    #print(process)

    MLFQ(process, n, nQ, quantas, t1, t2)

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
        print("%4d     %9d        %9d        %9d "%(t1, t2, t3, t4))
        
    print("Average ResponseTime "+str(stat[0]/n))
    print("Average WaitingTime "+str(stat[1]/n))
    print("Average TurnAroundTime "+str(stat[2]/n))


if __name__ == "__main__":
    main()