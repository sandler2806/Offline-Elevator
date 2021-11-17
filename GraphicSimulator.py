from main import *
from building import Building
import turtle
import threading
import time
FLOOR_H = 60
FLOOR_W = 55
b1 = []



def main():
    global b1
    b1 = Building("Ex1_Buildings/B2.json")
    elevNum = len(b1.Elevators)
    floorsNum = b1.maxFloor - b1.minFloor
    wn = turtle.Screen()
    # wn.delay(int(100))
    wn.setup(elevNum *150, floorsNum * 140,0,0)
    wn.addshape("el2.gif")
    wn.screensize(elevNum *150, floorsNum * FLOOR_H *2.2)


    # draw building and floors
    build = drawBuilding(floorsNum + 1,elevNum)
    turtle.tracer(False)
    for i in range(floorsNum + 1):
        drawx(FLOOR_H * i,i + b1.minFloor,elevNum)
        turtle.update()

    turtle.tracer(True)

    #create elevators
    val = 30
    elevs = []
    for i in range(elevNum):
        t = create_Elev(i, val)
        t.speed(b1.Elevators[i]["_speed"])
        elevs.append(t)
        val += 55
    t = elevs[0]

    thread0 = threading.Thread(target=goto, args=(elevs[0], [5, 7, 1, 5, 10, 0, 1, 68, 11, ],))
    # thread0.daemon = True
    thread0.start()

    # thread2 = threading.Thread(target=goto, args=(elevs[2], [1,6,2,7,9,0],))
    # # thread2.daemon = True
    # thread2.start()

    # thread3 = threading.Thread(target=goto, args=(elevs[3], [1,2,6,2,9],))
    # # thread3.daemon = True
    # thread3.start()

    thread1 = threading.Thread(target=goto, args=(elevs[1], [5, 7, 1, 5, 10, 0, 1, 68, 11, ],))
    # thread1.daemon = True
    thread1.start()

    # thread5 = threading.Thread(target=goto, args=(elevs[4], [5, 7, 1, 5, 10, 0, 1, 68, 11, ],))
    # # thread5.daemon = True
    # thread5.start()

    # while True:
    #     goto(elevs[2], 2)
    #     goto(elevs[4], 5)
    #     goto(elevs[0], 1)
    #     goto(elevs[3], 4)
    #     goto(elevs[3], 4)
    #     goto(elevs[1], 7)






    wn.mainloop()



def drawBuilding(floors, elevators):
    # drawing first side
    floors = floors * FLOOR_H
    elevators = FLOOR_W * elevators
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(20)

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
    t.sety(35 + 55 *  abs(b1.minFloor))
    t.shape("el2.gif")
    t.pendown()

    return t

def drawx(val,i, elevNum):
    # line
    trtl = turtle.Turtle()
    trtl.hideturtle()
    trtl.speed(50)
    trtl.forward(elevNum * FLOOR_W)

    # set position
    trtl.up()
    trtl.setpos(elevNum * FLOOR_W, val)
    trtl.down()

    # another line
    trtl.backward(elevNum * FLOOR_W)

    # set position again
    trtl.up()
    trtl.setpos(0, val + 10)
    trtl.down()
    trtl.write(f'{i}')

def goto(turt, floors):
    for f in floors:
        turt.penup()
        turt.sety(30 +FLOOR_H * f )
        turt.pendown()
        time.sleep(3.5)


if __name__ == '__main__':
    main()