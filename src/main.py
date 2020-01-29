from ai import Dqn
from math_util import Point
from ui import UI
from world import World

global ui
global world

# 5 sensors, 3 actions, gama = 0.9
brain = Dqn(5, 3, 0.9)
# action = 0 => no rotation, action = 1 => rotate 20 degres, action = 2 => rotate -20 degres
action2rotation = [0, 20, -20]
# initializing the last reward
last_reward = 0
# initializing the mean score curve (sliding window of the rewards) with respect to time
scores = []


def clean_canvas():
    world.clear_sand()


def save_model():
    print("Save")


def load_model():
    print("Load")


def put_sand(point):
    print("Sand " + str(point.x) + " " + str(point.y))
    for x, y in zip(range(point.x - 2, point.x + 3), range(point.y - 2, point.y + 3)):
        world.put_sand(Point(x, y))


def loop(dtm):
    ui.draw_car(world.get_car_point(), world.get_car_orientation())

    dts = dtm / 1000
    world.rotate_car(20 * dts)
    world.update_sensor_data(1, ui.get_sensor_point(1))
    world.update_sensor_data(2, ui.get_sensor_point(2))
    world.update_sensor_data(3, ui.get_sensor_point(3))
    world.process_tick(dtm)

    ui.root.after(100, lambda: loop(1000))


if __name__ == '__main__':
    world = World(
        width=300,
        height=300,
        car_point=Point(50, 50),
        car_orientation=0
    )

    ui = UI(
        width=300,
        height=300,
        on_cls=clean_canvas,
        on_save=save_model,
        on_load=load_model,
        on_create_sand=put_sand
    )

    loop(0)

    ui.loop()
