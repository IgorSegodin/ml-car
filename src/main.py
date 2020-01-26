from math_util import Point
from ui import UI

global ui


def clean_canvas():
    print("Clean")


def save_model():
    print("Save")
    ui.draw_car(Point(50, 50), 0)


def load_model():
    print("Load")


def put_sand(point):
    print("Sand " + str(point.x) + " " + str(point.y))


if __name__ == '__main__':
    ui = UI(
        on_cls=clean_canvas,
        on_save=save_model,
        on_load=load_model,
        on_create_sand=put_sand
    )
    ui.loop()
