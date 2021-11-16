import json
import sys
from time import time
import cProfile

import pandas as pd
from building import Building
import math

temp = [0]
building = []
calls = []
counter_time = 0
counter_insert = 0
counter_allocate = 0
counter_getpos = 0
counter_base = 0
counterif = 0


# outfile =  input("insert a output file path")

# this function receive a up to 5 calls and assign them to the elevators
def allocate(callsList, indices: [[]], json_calls):
    global calls
    global counterif
    global counter_allocate
    counter_allocate += 1
    copys = [0] * 10
    elevatorNum = len(building.Elevators)
    minWaitingTime = 10000000000
    minSetup = []
    waitingTimes = []
    for j in range(elevatorNum):
        waitingTimes.append(timeCalculator(calls[j], j))
    for i in indices:
        for j in set(i):
            copys[j] = json.loads(json_calls[j])
        row = 0
        for j in i:
            if len(callsList) > row:
                insert_call(copys[j], j, callsList[row][2], callsList[row][3], math.ceil(callsList[row][1]))
            row += 1
        time = 0
        for j in range(elevatorNum):
            if j in i:
                time += timeCalculator(copys[j], j)
            else:
                time += waitingTimes[j]
        if time < minWaitingTime:
            counterif += 1
            minSetup = i
            minWaitingTime = time
    row = 0
    for m in minSetup:
        if len(callsList) > row:
            insert_call(calls[m], m, callsList[row][2], callsList[row][3], math.ceil(callsList[row][1]))
        row += 1
    return minSetup


# this function gets an elevator,src and dest of a new call, and return
# the delayed caused by assigning this elevator for the new call
# def delayCalculator(calls,elev, src, dest):
#     pass

# this function get elevator and it's stops and calculate the time
# it take to complete them
def timeCalculator(stops: [[]], elev):
    global counter_time
    counter_time += 1
    time = 0  # total waiting time of all the users
    onBoard = 0  # number of people(calls) on board
    elevator = building.Elevators[elev]

    # index = len(stops) - 1
    # if counter_time > 10:
    #     print("")
    #
    # for i in range(len(stops) - 1, -1, -1):
    #     # if len(stops[i][3]) > 0:
    #     #    minBoardingTime = min([min(stops[i][3]), minBoardingTime])
    #     if stops[i][2] < time:
    #         index = i
    #         break

    for i in range(1, len(stops)):
        # add the traveling time times the travelers onboard
        time += onBoard * (stops[i][2] - stops[i - 1][2])
        # add the time users in stop i waited for the elevator
        for boardingTime in stops[i][3]:
            time += stops[i][2] - boardingTime

        onBoard += stops[i][1]

    return time


def getPos(stops, elev, time):
    global counter_getpos
    counter_getpos += 1

    time = math.ceil(time)

    index = 0
    minBoardingTime = 10000000000
    travelersCounter = 0
    elevator = building.Elevators[elev]
    speed = elevator["_speed"]
    # we look for the
    for i in range(len(stops) - 1, -1, -1):
        if len(stops[i][3]) > 0:
            minBoardingTime = min([min(stops[i][3]), minBoardingTime])
        if stops[i][2] < time:
            index = i
            break
        travelersCounter += stops[i][1]

    # we check 2 things:
    # 1)is there someone currently waiting for the elevator
    isWaiting = (minBoardingTime <= stops[index][2])
    # 2)is there someone on the elevator
    isOnElev = False
    if len(stops[index][3]) == 0 and travelersCounter < 0:
        isOnElev = True

    if isWaiting or isOnElev:
        departingTime = stops[index][2]
    else:
        departingTime = minBoardingTime

    t = time - departingTime - (elevator["_closeTime"] + elevator["_startTime"])

    if t <= 0:
        return [stops[index][0], abs(t)]

    return [min(stops[index][0] + t * speed, stops[index + 1][0]), 0]


# this function insert a call to the stop list of given elevator by Boaz logic
# while taking into account the boarding time

def insert_call(stops: [[[]]], elev, src, dest, time):
    global counter_insert
    counter_insert += 1

    elevator = building.Elevators[elev]
    floor_time = elevator["_closeTime"] + elevator["_openTime"] + elevator["_startTime"] + elevator["_stopTime"]
    speed = elevator["_speed"]
    if len(stops) == 1:

        if src != 0:  # the first src is already 0
            stops.append([src, 1, time + abs(src) / speed + floor_time, [time]])
        else:
            stops.append([src, 1, time, [time]])
        stops.append([dest, -1, math.ceil(abs(dest - src) / speed + floor_time + stops[1][2]), []])

    else:
        index = len(stops) - 1
        srcIndex = 0
        srcTime = 0
        destTime = 0
        destIndex = 0
        minBoardingTime = time

        for i in range(len(stops) - 1, -1, -1):
            # if len(stops[i][3]) > 0:
            #    minBoardingTime = min([min(stops[i][3]), minBoardingTime])
            if stops[i][2] < time:
                index = i
                break

        for i in range(index, len(stops)):
            pos = getPos(stops, elev, time)  # check order
            # call added to the end of the list
            if i == len(stops) - 1:
                if src == stops[i]:
                    srcIndex = i
                    stops[i][1] += 1
                    stops[i][3].append(time)
                    break
                else:
                    srcIndex = i + 1
                    srcTime = math.ceil(abs(stops[i][0] - src) / speed + floor_time + max(stops[i][2], time))
                    stops.append([src, 1, srcTime, [time]])
                    break
            # special test for the first interval
            if i == index and (pos[0] <= src <= stops[i + 1][0] or pos[0] >= src >= stops[i + 1][0]):
                if src == pos[0] and pos[0] == stops[i][0] and pos[1] == 0:
                    srcIndex = i
                    stops[i][1] += 1
                    stops[i][3].append(time)
                elif src == stops[i + 1][0]:
                    srcIndex = i + 1
                    stops[i + 1][1] += 1
                    stops[i + 1][3].append(time)
                else:
                    srcIndex = i + 1
                    # warning: adding time might be an overfitting
                    srcTime = math.ceil(
                        max(stops[i][2], time) + pos[1] + abs(pos[0] - src) / speed + elevator["_openTime"] + \
                        elevator["_stopTime"])
                    stops.insert(srcIndex, [src, 1, srcTime, [time]])
                    # adding delay caused from the new stop
                    for p in range(srcIndex + 1, len(stops)):
                        stops[p][2] += floor_time
                break

            if stops[i][0] <= src <= stops[i + 1][0] or stops[i][0] >= src >= stops[i + 1][0]:
                if src == stops[i][0]:
                    srcIndex = i
                    stops[i][1] += 1
                    stops[i][3].append(time)
                elif src == stops[i + 1][0]:
                    srcIndex = i + 1
                    stops[i + 1][1] += 1
                    stops[i + 1][3].append(time)
                else:
                    srcIndex = i + 1
                    srcTime = math.ceil(abs(stops[i][0] - src) / speed + floor_time + max(stops[i][2], time))
                    stops.insert(srcIndex, [src, 1, srcTime, [time]])
                    # adding delay caused from the new stop
                    for p in range(srcIndex + 1, len(stops)):
                        stops[p][2] += floor_time
                break

        for i in range(srcIndex, len(stops)):
            if i == len(stops) - 1:
                destTime = math.ceil(abs(stops[i][0] - dest) / speed + floor_time + stops[i][2])
                stops.append([dest, -1, destTime, []])
                break

            if stops[i][0] <= dest <= stops[i + 1][0] or stops[i][0] >= dest >= stops[i + 1][0]:
                if dest == stops[i][0]:
                    stops[i][1] -= 1
                elif dest == stops[i + 1][0]:
                    stops[i + 1][1] -= 1
                else:
                    destTime = math.ceil(abs(stops[i][0] - dest) / speed + floor_time + stops[i][2])
                    stops.insert(i + 1, [dest, -1, destTime, []])
                    # adding delay caused from the new stop
                    for p in range(i + 2, len(stops)):
                        stops[p][2] += floor_time
                break


def decToBaseX(call_num, base, callSize):
    global counter_base
    counter_base += 1

    reminder = []
    for i in range(callSize):
        reminder.insert(0, call_num % base)
        call_num = math.floor(call_num / base)

    return reminder


def main(argv):
    start = time()
    global building
    global calls
    building = Building(argv[0])
    calls = [[[0, 0, 0, []]] for q in range(len(building.Elevators))]
    callsfile = argv[1]
    output = argv[2]

    df = pd.read_csv(callsfile, header=None)
    rows = [r[1] for r in df.iterrows()]

    callSize = 1
    counter = 0
    indices = []
    for i in range(pow(len(building.Elevators), callSize)):
        indices.append(decToBaseX(i, len(building.Elevators), callSize))
    temp = []
    for c in rows:
        temp.append(c)

        if len(temp) == callSize:
            json_list = []
            for j in range(len(calls)):
                json_list.append(json.dumps(calls[j]))

            # for i in range(len(calls)):
            #     calls[i]=calls[i][-10:]
            assignments = allocate(temp, indices, json_list)
            for a in assignments:
                df[5][counter] = a
                counter += 1
            temp = []

    json_list = []
    for j in range(len(calls)):
        json_list.append(json.dumps(calls[j]))
    if len(temp) > 0:
        assignments = allocate(temp, indices, json_list)
        for a in assignments:
            df[5][counter] = a
            counter += 1

    df.to_csv(output, index=None, header=False)
    end = time()
    print(f'It took {end - start} seconds!')
    print(f'time was called {counter_time} times')
    print(f'allocte was called {counter_allocate} times')
    print(f'insert was called {counter_insert} times')
    print(f'pos was called {counter_getpos} times')
    print(f'base was called {counter_base} times')
    print(f'if was called {counterif} times')



if __name__ == '__main__':
    cProfile.run('main(sys.argv[1:])',None, 1)