from math_util import Point
from ui import UI


def clean_canvas():
    print("Clean")


def save_model():
    print("Save")


def load_model():
    print("Load")


def put_sand(point):
    print("Sand " + str(point.x) + " " + str(point.y))


def loop():
    global car_orientation
    ui.draw_car(Point(50, 50), car_orientation)
    car_orientation = car_orientation + 20

    ui.root.after(1000, loop)


if __name__ == '__main__':
    global ui
    global car_orientation

    ui = UI(
        on_cls=clean_canvas,
        on_save=save_model,
        on_load=load_model,
        on_create_sand=put_sand
    )

    car_orientation = 0

    loop()

    ui.loop()
