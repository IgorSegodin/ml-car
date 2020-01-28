from math_util import Point
from ui import UI
from world import World
from ai import Dqn

global ui
global world

brain = Dqn(5,3,0.9) # 5 sensors, 3 actions, gama = 0.9
action2rotation = [0,20,-20] # action = 0 => no rotation, action = 1 => rotate 20 degres, action = 2 => rotate -20 degres
last_reward = 0 # initializing the last reward
scores = [] # initializing the mean score curve (sliding window of the rewards) with respect to time



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
