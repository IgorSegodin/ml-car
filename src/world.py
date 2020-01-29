import numpy as np

import math_util


class World:

    def __init__(self, width, height, car_point, car_orientation):
        self._width = width
        self._height = height
        self._sand = np.zeros((width, height))
        self._sensor_data = {
            'sensor_1': 0.,
            'sensor_2': 0.,
            'sensor_3': 0.
        }
        self._car = {
            'point': car_point,
            'orientation': car_orientation
        }

    def get_car_point(self):
        return self._car['point']

    def _set_car_point(self, point):
        self._car['point'] = point

    def get_car_orientation(self):
        return self._car['orientation']

    def rotate_car(self, angle_delta_degrees):
        self._car['orientation'] = self.get_car_orientation() + angle_delta_degrees

    def put_sand(self, point):
        self._sand[point.x, point.y] = 1

    def clear_sand(self):
        self._sand = np.zeros((self._width, self._height))

    def check_car_is_on_sand(self):
        car_point = self.get_car_point()
        x = int(car_point.x)
        y = int(car_point.y)
        size = 5

        x1 = x - size
        y1 = y - size
        x2 = x + size
        y2 = y + size
        return np.sum(self._sand[x1: x2, y1: y2]) > 0

    def check_car_outside_border(self, border_width=0):
        car_point = self.get_car_point()
        return (
                car_point.x < border_width
                or car_point.x > self._width - border_width
                or car_point.y < border_width
                or car_point.y > self._height - border_width
        )

    def get_sensor_data(self, sensor_number_id):
        return self._sensor_data['sensor_' + str(sensor_number_id)]

    def update_sensor_data(self, sensor_number_id, point):
        self._sensor_data['sensor_' + str(sensor_number_id)] = self._calc_sensor_data(point)

    def _calc_sensor_data(self, sensor_position):
        sensor_range = 10

        x1 = int(sensor_position.x) - sensor_range
        x2 = int(sensor_position.x) + sensor_range
        y1 = int(sensor_position.y) - sensor_range
        y2 = int(sensor_position.y) + sensor_range

        # getting the signal received by sensor (density of sand around sensor )
        sig = int(np.sum(self._sand[x1: x2, y1: y2])) / 400.

        # if sensor is out of the map (the car is facing one edge of the map)
        if sensor_position.x > self._width - 10 \
                or sensor_position.x < 10 \
                or sensor_position.y > self._height - 10 \
                or sensor_position.y < 10:
            sig = 1.  # sensor detects full sand

        return sig

    def process_tick(self, delta_time_millis):
        car_speed_per_sec = 10
        mag = car_speed_per_sec * delta_time_millis / 1000
        move_point = math_util.polar_to_cartesian(mag, self.get_car_orientation())

        previous_point = self.get_car_point()

        self._set_car_point(
            self.get_car_point() + move_point
        )

        if self.check_car_outside_border():
            self._set_car_point(
                previous_point
            )
