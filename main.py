from simulator_tools import *
import pandas as pd
import sys


def main(argv):
    # scan the parameters and create the building,calls file and the output file
    building = Building(argv[0])
    calls = [[[0, 0, 0, []]] for q in range(len(building.Elevators))]
    callsfile = argv[1]
    output = argv[2]
    callSize = 1
    counter = 0
    indices = []

    df = pd.read_csv(callsfile, header=None)
    rows = [r[1] for r in df.iterrows()]
    # passing a list of calls we want to assign with elevator, the number of calls may vary
    for i in range(pow(len(building.Elevators), callSize)):
        indices.append(decToBaseX(i, len(building.Elevators), callSize))
    callsList = []
    for c in rows:
        callsList.append(c)

        if len(callsList) == callSize:
            json_list = []
            for j in range(len(calls)):
                json_list.append(json.dumps(calls[j]))
            # write the allocations into the dataframe
            calls, assignments = allocate(callsList, indices, json_list, building, calls)
            for a in assignments:
                df[5][counter] = a
                counter += 1
            callsList = []

    df.to_csv(output, index=None, header=False)
    # return calls for the graphic simulator
    return calls


if __name__ == '__main__':
    main(sys.argv[1:])
