from math_util import Point
from ui import UI
from world import World

global ui
global world


def clean_canvas():
    print("Clean")


def save_model():
    print("Save")


def load_model():
    print("Load")


def put_sand(point):
    print("Sand " + str(point.x) + " " + str(point.y))


def loop():
    ui.draw_car(world.get_car_point(), world.get_car_orientation())
    world.rotate_car(20)
    world.process_tick(1000)
    # TODO tick
    # TODO update sensor data

    ui.root.after(1000, loop)


if __name__ == '__main__':
    world = World(Point(50, 50), 0)

    ui = UI(
        on_cls=clean_canvas,
        on_save=save_model,
        on_load=load_model,
        on_create_sand=put_sand
    )

    loop()

    ui.loop()
