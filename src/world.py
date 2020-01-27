import math_util


# TODO Add width, height
class World:

    def __init__(self, car_point, car_orientation):
        self._sand = []
        self._sensor_data = {
            'sensor_1': 0,
            'sensor_2': 0,
            'sensor_3': 0
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

    def update_sensor_data(self, sensor_1, sensor_2, sensor_3):
        self._sensor_data = {
            'sensor_1': sensor_1,
            'sensor_2': sensor_2,
            'sensor_3': sensor_3
        }

    def rotate_car(self, angle_delta_degrees):
        self._car['orientation'] = self.get_car_orientation() + angle_delta_degrees

    def process_tick(self, delta_time_millis):
        car_speed_per_sec = 10
        mag = car_speed_per_sec * delta_time_millis / 1000
        move_point = math_util.polar_to_cartesian(mag, self.get_car_orientation())
        self._set_car_point(
            self.get_car_point() + move_point
        )
