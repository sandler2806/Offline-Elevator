from simulator_tools import *
import pandas as pd
import sys


def main(argv):
    building = Building(argv[0])
    calls = [[[0, 0, 0, []]] for q in range(len(building.Elevators))]
    callsfile = argv[1]
    output = argv[2]
    callSize = 1
    counter = 0
    indices = []

    df = pd.read_csv(callsfile, header=None)
    rows = [r[1] for r in df.iterrows()]

    for i in range(pow(len(building.Elevators), callSize)):
        indices.append(decToBaseX(i, len(building.Elevators), callSize))
    callsList = []
    for c in rows:
        callsList.append(c)

        if len(callsList) == callSize:
            json_list = []
            for j in range(len(calls)):
                json_list.append(json.dumps(calls[j]))

            calls, assignments = allocate(callsList, indices, json_list, building, calls)
            for a in assignments:
                df[5][counter] = a
                counter += 1
            callsList = []

    json_list = []
    for j in range(len(calls)):
        json_list.append(json.dumps(calls[j]))
    if len(callsList) > 0:
        calls, assignments = allocate(callsList, indices, json_list, building, calls)
        for a in assignments:
            df[5][counter] = a
            counter += 1

    df.to_csv(output, index=None, header=False)


if __name__ == '__main__':
    main(sys.argv[1:])