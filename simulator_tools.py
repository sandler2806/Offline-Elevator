import json
from building import Building
import math

building = Building("")
calls = []


def allocate(callsList, indices: [[]], json_calls, current_building, calls):
    """this function receive a number of calls and assign them to the best elevators"""

    global building
    building = current_building
    copys = [0] * 10
    elevatorNum = len(building.Elevators)
    minWaitingTime = 10000000000
    minSetup = []
    waitingTimes = []
    # saving the current waiting time
    for j in range(elevatorNum):
        waitingTimes.append(timeCalculator(calls[j], j))
    for i in indices:
        for j in set(i):
            copys[j] = json.loads(json_calls[j])
        row = 0
        for j in i:
            if len(callsList) > row:
                insert_call(copys[j], j, callsList[row][2], callsList[row][3], math.ceil(callsList[row][1]), building)
            row += 1
        time = 0
        for j in range(elevatorNum):
            if j in i:
                time += timeCalculator(copys[j], j)
            else:
                time += waitingTimes[j]
        if time < minWaitingTime:
            minSetup = i
            minWaitingTime = time
    row = 0
    for m in minSetup:
        if len(callsList) > row:
            insert_call(calls[m], m, callsList[row][2], callsList[row][3], math.ceil(callsList[row][1]), building)
        row += 1
    return calls, minSetup


def timeCalculator(stops: [[]], elev):
    """this function get elevator and it's stops and calculate the time it take to complete them"""

    total_time = 0  # total waiting time of all the users
    onBoard = 0  # number of people(calls) on board

    for i in range(1, len(stops)):
        # add the traveling time times the travelers onboard
        total_time += onBoard * (stops[i][2] - stops[i - 1][2])
        # add the time users in stop i waited for the elevator
        for boardingTime in stops[i][3]:
            total_time += stops[i][2] - boardingTime

        onBoard += stops[i][1]

    return total_time


def getPos(stops, elev, current_time, building):
    """this function get elevator and it's stops and calculate the location of the elevator at a given time"""

    current_time = math.ceil(current_time)
    index = 0
    minBoardingTime = 10000000000
    travelersCounter = 0
    elevator = building.Elevators[elev]
    speed = elevator["_speed"]
    # we check the last floor before the current time that the elevator stops in the list
    for i in range(len(stops) - 1, -1, -1):
        if len(stops[i][3]) > 0:
            minBoardingTime = min([min(stops[i][3]), minBoardingTime])
        if stops[i][2] < current_time:
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

    t = current_time - departingTime - (elevator["_closeTime"] + elevator["_startTime"])

    if t <= 0:
        return [stops[index][0], abs(t)]

    return [min(stops[index][0] + t * speed, stops[index + 1][0]), 0]


def insert_call(stops: [[[]]], elev, src, dest, time, building):
    """this function insert a call to the stop list of given elevator by Boaz logic
     while taking into account the boarding time"""

    elevator = building.Elevators[elev]
    floor_time = elevator["_closeTime"] + elevator["_openTime"] + elevator["_startTime"] + elevator["_stopTime"]
    speed = elevator["_speed"]
    if len(stops) == 1:

        if src != 0:  # the first src is already 0
            stops.append([src, 1, math.ceil(time + abs(src) / speed + floor_time), [time]])
        else:
            stops.append([src, 1, time, [time]])
        stops.append([dest, -1, math.ceil(abs(dest - src) / speed + floor_time + stops[1][2]), []])

    else:
        index = len(stops) - 1
        srcIndex = 0

        for i in range(len(stops) - 1, -1, -1):
            if stops[i][2] < time:
                index = i
                break

        for i in range(index, len(stops)):
            pos = getPos(stops, elev, time, building)
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
                    srcTime = math.ceil(
                        max(stops[i][2], time) + pos[1] + abs(pos[0] - src) / speed + elevator["_openTime"] + \
                        elevator["_stopTime"])
                    stops.insert(srcIndex, [src, 1, srcTime, [time]])
                    # adding delay caused from the new stop
                    for p in range(srcIndex + 1, len(stops)):
                        stops[p][2] += math.ceil(floor_time)
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
                        stops[p][2] += math.ceil(floor_time)
                break
            # check if the elevator switch her direction and the call fitting
            if i > index and stops[i - 1][0] < stops[i][0] > stops[i + 1][0] and stops[i][0] < src:
                srcIndex = i + 1
                srcTime = math.ceil(abs(stops[i][0] - src) / speed + floor_time + max(stops[i][2], time))
                stops.insert(srcIndex, [src, 1, srcTime, [time]])
                # adding delay caused from the new stop
                for p in range(srcIndex + 1, len(stops)):
                    stops[p][2] += math.ceil(floor_time)
                break

            if i > index and stops[i - 1][0] > stops[i][0] < stops[i + 1][0] and stops[i][0] > src:
                srcIndex = i + 1
                srcTime = math.ceil(abs(stops[i][0] - src) / speed + floor_time + max(stops[i][2], time))
                stops.insert(srcIndex, [src, 1, srcTime, [time]])
                # adding delay caused from the new stop
                for p in range(srcIndex + 1, len(stops)):
                    stops[p][2] += math.ceil(floor_time)
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
                        stops[p][2] += math.ceil(floor_time)
                break
            if stops[i - 1][0] < stops[i][0] > stops[i + 1][0] and stops[i][0] < dest:
                destTime = math.ceil(abs(stops[i][0] - dest) / speed + floor_time + stops[i][2])
                stops.insert(i + 1, [dest, -1, destTime, []])
                # adding delay caused from the new stop
                for p in range(i + 2, len(stops)):
                    stops[p][2] += math.ceil(floor_time)
                break

            if stops[i - 1][0] > stops[i][0] < stops[i + 1][0] and stops[i][0] > dest:
                destTime = math.ceil(abs(stops[i][0] - dest) / speed + floor_time + stops[i][2])
                stops.insert(i + 1, [dest, -1, destTime, []])
                # adding delay caused from the new stop
                for p in range(i + 2, len(stops)):
                    stops[p][2] += math.ceil(floor_time)
                break


def decToBaseX(call_num, base, callSize):
    """this function get a number, base and number of calls and return the number according the new base
    and fill the rest of the calls with zeros"""

    reminder = []
    for i in range(callSize):
        reminder.insert(0, call_num % base)
        call_num = math.floor(call_num / base)

    return reminder
