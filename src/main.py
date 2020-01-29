import math_util
from ai import Dqn
from math_util import Point
from ui import UI
from world import World

global ui
global world
global network

# action = 0 => no rotation, action = 1 => rotate 20 degres, action = 2 => rotate -20 degres
action2rotation = [0, 20, -20]
# initializing the mean score curve (sliding window of the rewards) with respect to time
scores = []
# initializing the last reward
last_reward = 0
last_distance = 0

goal = Point(250, 250)


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


def calc_distance_vector(car_point, goal_point):
    return math_util.cartesian_to_polar(
        goal_point.x - car_point.x,
        goal_point.y - car_point.y
    )


def calc_reward(last_distance, distance):
    if world.check_car_outside_border(border_width=10):
        return -1
    elif world.check_car_is_on_sand():
        # if the car is on the sand
        return -1
    elif distance < last_distance:
        # however if it getting close to the goal
        # it gets slightly positive reward 0.1
        return 0.1
    else:
        # it gets bad reward (-0.2)
        return -0.2


def loop(dtm):
    global last_reward
    global last_distance

    ui.draw_car(world.get_car_point(), world.get_car_orientation())

    dts = dtm / 1000
    world.update_sensor_data(1, ui.get_sensor_point(1))
    world.update_sensor_data(2, ui.get_sensor_point(2))
    world.update_sensor_data(3, ui.get_sensor_point(3))

    # direction of the car with respect to the goal
    # (if the car is heading perfectly towards the goal, then orientation = 0)
    distance_vector = calc_distance_vector(world.get_car_point(), goal)
    orientation = math_util.orientation_delta(world.get_car_orientation(), distance_vector.orientation)
    # our input state vector, composed of the three signals received by the three sensors,
    # plus the orientation and -orientation
    last_signal = [
        world.get_sensor_data(1),
        world.get_sensor_data(2),
        world.get_sensor_data(3),
        orientation,
        -orientation
    ]

    action = network.update(last_reward, last_signal)

    world.rotate_car(action2rotation[action] * dts)

    world.process_tick(dtm)

    # getting the new distance between the car and the goal right after the car moved
    distance = calc_distance_vector(world.get_car_point(), goal).magnitude

    last_reward = calc_reward(last_distance, distance)
    last_distance = distance

    print("Action: %s, Reward %s, Dist: %s, input: %s" % (action, last_reward, last_distance, last_signal))

    if distance > 50:
        ui.root.after(40, lambda: loop(1000))
    else:
        print('Destination reached')


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

    # 5 sensors, 3 actions, gama = 0.9
    network = Dqn(5, 3, 0.9)

    loop(0)

    ui.loop()
