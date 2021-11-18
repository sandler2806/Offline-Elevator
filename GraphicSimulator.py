from building import Building
from main import *
import turtle
import threading
import time

FLOOR_H = 60
FLOOR_W = 55
MIN_FLOOR = 0
WIN_W = 0
WIN_H = 0
b1 = []


def draw():
    global b1

    building = "Ex1_Buildings/B5.json"
    b1 = Building(building)
    global MIN_FLOOR
    MIN_FLOOR = b1.minFloor
    call_file = "Ex1_Calls/Calls_d.csv"
    calls = main([building, call_file, "new.csv"])
    calls = [c[1:] for c in calls]

    elevNum = len(b1.Elevators)
    floorsNum = b1.maxFloor - b1.minFloor
    wn = turtle.Screen()

    # wn.delay(int(100))
    wn.setup(0.5, 0.98, 0, 0)
    # turtle.setworldcoordinates(0,0,500,500)
    wn.addshape("pics\el2.gif")
    wn.screensize(elevNum * 150, floorsNum * FLOOR_H * 2.2)
    global WIN_H, WIN_W
    WIN_W = wn.window_width()
    WIN_H = wn.window_height()

    # draw building and floors
    build = drawBuilding(floorsNum + 1, elevNum)

    turtle.tracer(False)
    for i in range(floorsNum + 1):
        drawx(FLOOR_H * i - WIN_H / 2 + 40, i + b1.minFloor, elevNum)
        turtle.update()

    turtle.tracer(True)

    # create elevators
    val = 60 + -WIN_W / 2
    elevs = []
    for i in range(elevNum):
        t = create_Elev(i, val)
        t.speed(min(b1.Elevators[i]["_speed"], 6))
        elevs.append(t)
        val += 55
    t = elevs[0]

    for i in range(elevNum):
        threading.Thread(target=goto, args=(elevs[i], i, calls[i],)).start()

    wn.mainloop()


def drawBuilding(floors, elevators):
    # drawing first side
    floors = floors * FLOOR_H
    elevators = FLOOR_W * elevators
    t = turtle.Turtle()
    t.penup()
    t.sety(-WIN_H / 2 + 40)
    t.setx(-WIN_W / 2 + 40)
    t.pendown()
    t.hideturtle()
    t.speed(0)

    t.forward(elevators)  # Forward turtle by l units
    t.left(90)  # Turn turtle by 90 degree

    # drawing second side
    t.forward(floors)  # Forward turtle by w units
    t.left(90)  # Turn turtle by 90 degree

    # drawing third side
    t.forward(elevators)  # Forward turtle by l units
    t.left(90)  # Turn turtle by 90 degree

    # drawing fourth side
    t.forward(floors)  # Forward turtle by w units
    t.left(90)  # Turn turtle by 90 degree

    return t


def create_Elev(elev_num, val):
    t = turtle.Turtle()
    t.speed(0)
    t.penup()
    t.setx(val)

    t.sety(-WIN_H / 2 + 10 + (abs(MIN_FLOOR) + 1) * FLOOR_H)
    t.shape("pics\el2.gif")
    t.pendown()

    return t


def drawx(val, i, elevNum):
    trtl = turtle.Turtle()
    trtl.penup()
    trtl.sety(val)
    trtl.setx(-WIN_W / 2 + 40)
    trtl.pendown()
    trtl.hideturtle()
    trtl.speed(0)
    trtl.forward(elevNum * FLOOR_W)
    trtl.write(f'{i}')


def goto(turt, elev_num, floors: []):
    for f in floors:
        if floors[0][1] == floors[0][0]:
            floors.remove(1)
        turt.penup()
        origin = -WIN_H / 2 + 10 + (abs(MIN_FLOOR) + 1) * FLOOR_H
        turt.sety(origin + FLOOR_H * f[0])
        turt.pendown()
        time.sleep(3 + elev_num * 0.5)


if __name__ == '__main__':
    draw()
