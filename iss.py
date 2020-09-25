#!/usr/bin/env python

import requests
import turtle
import time

__author__ = "marcornett"


def get_astronauts():
    response = requests.get('http://api.open-notify.org/astros.json')
    data = response.json()

    info = []
    in_space = len(data['people'])
    for person in data['people']:
        info.append(f"{person['name']} is currently onboard {person['craft']}")
    print(f'Total astronauts in space: {in_space}')
    print('\n'.join(info))


def get_coordinates():
    response = requests.get('http://api.open-notify.org/iss-now.json')
    data = response.json()
    iss_position = data['iss_position']
    coordinates = dict(
        latitude=iss_position['latitude'],
        longitude=iss_position['longitude'],
        timestamp=data['timestamp']
    )
    return coordinates


def create_graphic():
    # Turn on for auto refresh
    # while True:
    coordinates = get_coordinates()

    screen = turtle.Screen()
    screen.mode('world')
    screen.setup(720, 360)
    screen.bgpic('map.gif')
    screen.setworldcoordinates(-180, -90, 180, 90)
    screen.register_shape('iss.gif')

    iss = turtle.Turtle()
    iss.color('blue')
    iss.hideturtle()
    iss.shape('iss.gif')
    iss.setheading(45)
    iss.penup()
    iss.goto(float(coordinates['longitude']),
             float(coordinates['latitude']))
    iss.showturtle()
    response = requests.get(
        f'http://api.open-notify.org/iss-pass.json?'
        f'lat={39.76838}&lon={-86.15804}')
    data = response.json()

    passover_time = time.ctime(data['response'][0]['risetime'])

    indianapolis = turtle.Turtle()
    indianapolis.hideturtle()
    indianapolis.shape('circle')
    indianapolis.shapesize(.3)
    indianapolis.color('yellow')
    indianapolis.penup()
    indianapolis.goto(-86.1580556, 39.7683333)
    indianapolis.showturtle()
    indianapolis.write(passover_time)
    indianapolis.speed(10)
    indianapolis.setheading(45)

    # Turn on for auto refresh
    # time.sleep(10)

    turtle.done()
    # screen.ontimer(create_graphic, 250)
    # screen.mainloop()


def main():
    get_astronauts()
    create_graphic()


if __name__ == '__main__':
    main()
