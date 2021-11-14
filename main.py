import pandas as pd
from building import Building
import math


def main():

    callsfile = "venv/Calls_a.csv"
    df = pd.read_csv(callsfile, header=None)

    print(building.Elevators[0]["_speed"])

    # for i in range(df.shape[0]):
    #     df[5][i] = 1
    # calls = [r for r in df.iterrows()]
    # print(df)
    # df.to_csv('new.csv',index =None, header=False)


if __name__ == '__main__':
    main()


# outfile =  input("insert a output file path")

# this function receive a up to 5 calls and assign them to the elevators
def allocate(call):
    pass


# this function gets an elevator,src and dest of a new call, and return
# the delayed caused by assigning this elevator for the new call
# def delayCalculator(calls,elev, src, dest):
#     pass

# this function get elevator and it's stops and calculate the time
# it take to complete them
def timeCalculator(stops: [[]], elev):
    bfile = "f.json"
    building = Building(bfile)
    stops.insert(0, [0, 0, 0, []])
    time = 0  # total waiting time of all the users
    onBoard = 0  # number of people(calls) on board
    elevator = building.Elevators[elev]

    for i in range(1, len(stops)):
        # add the traveling time times the travelers onboard
        time += onBoard * (stops[i][2] - stops[i - 1][2])
        # add the time users in stop i waited for the elevator
        for boardingTime in stops[i][3]:
            time += stops[i][2] - boardingTime

        onBoard += stops[i][1]

    return time


def getPos(stops, elev, time):
    bfile = "f.json"
    building = Building(bfile)
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
        isOnElev = true

    if isWaiting or isOnElev:
        departingTime = stops[index][2]
    else:
        departingTime = minBordingTime

    t = time - departingTime - (elevator["_closeTime"] + elevator["_startTime"])

    if t <= 0:
        return [stops[index][0], abs(t)]

    return [min(stops[index][0] + t * speed, stops[index + 1][0]), 0]


# this function insert a call to the stop list of given elevator by Boaz logic
# while taking into account the boarding time

def insert_call(stops: [[[]]], elev, src, dest, time):
    elevator = Building.Elevators[elev]
    floor_time = elevator["_closeTime"] + elevator["_openTime"] + elevator["_startTime"] + elevator["_stopTime"]
    speed = elevator["_speed"]
    if len(stops) == 0:
        stops[0][0] = src
        stops[0][1] = 1
        if src != 0:  # the first src is already 0
            stops[0][2] = abs(src) / speed + floor_time
        stops[0][3].append(time)
        stops[1][0] = dest
        stops[1][1] = -1
        stops[1][2] = abs(dest - stops) / speed + floor_time + stops[0][2]

    else:
        index = len(stops) - 1
        srcIndex = 0
        srcTime = 0
        destTime = 0
        destIndex = 0
        minBoardingTime = time
        for i in range(len(stops) - 1, 0):
            # if len(stops[i][3]) > 0:
            #    minBoardingTime = min([min(stops[i][3]), minBoardingTime])
            if stops[i][2] < time:
                index = i
                break

        for i in range(index, len(stops)):
            pos = getpos(elev, time)  # check order
            if i == len(stops) - 1:
                if src == stops[i]:
                    srcIndex = i
                    stops[i][1] += 1
                    stops[i][3].append(time)
                else:
                    srcIndex = i + 1
                    srcTime = abs(stops[i][0] - src) / speed + floor_time
                    stops.append([src, 1, srcTime, [time]])

            if i == index and (pos[0] <= src <= stops[i + 1][0] or pos[0] >= src >= stops[i + 1][0]):
                if src == pos[0] and pos[0] == stops[i][0]:
                    srcIndex = i
                    stops[i][1] += 1
                    stops[i][3].append(time)
                elif src == stops[i + 1][0]:
                    srcIndex = i + 1
                    stops[i + 1][1] += 1
                    stops[i + 1][3].append(time)
                else:
                    srcIndex = i + 1
                    srcTime = pos[1] + abs(pos[0] - src) / speed + elevator["_openTime"] + elevator["_stopTime"]
                    stops.insert(srcIndex, [src, 1, srcTime, [time]])
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
                    srcTime = abs(stops[i][0] - src) / speed + floor_time
                    stops.insert(srcIndex, [src, 1, srcTime, [time]])
                break

        for i in range(srcIndex, len(stops)):
            if i == len(stops) - 1:
                destTime = abs(stops[i][0] - dest) / speed + floor_time
                stops.append([dest, -1, destTime, []])

            if stops[i][0] <= dest <= stops[i + 1][0] or stops[i][0] >= dest >= stops[i + 1][0]:
                if dest == stops[i][0]:
                    stops[i][1] -= 1
                elif dest == stops[i + 1][0]:
                    stops[i + 1][1] -= 1
                else:
                    destTime = abs(stops[i][0] - dest) / speed + floor_time
                    stops.insert(i + 1, [dest, -1, destTime, []])
                break
