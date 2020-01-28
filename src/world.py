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

    def _update_sensor_data(self, sensor_1, sensor_2, sensor_3):
        self._sensor_data = {
            'sensor_1': sensor_1,
            'sensor_2': sensor_2,
            'sensor_3': sensor_3
        }

    def _calc_sensor_data(self, sensor_position):
        # TODO
        return 2
        # self.signal1 = int(
        #     np.sum(
        #         sand[
        #         int(self.sensor1_x) - 10: int(self.sensor1_x) + 10,
        #         int(self.sensor1_y) - 10: int(self.sensor1_y) + 10
        #         ]
        #     )
        # ) / 400.  # getting the signal received by sensor 1 (density of sand around sensor 1)
        #
        # if self.sensor1_x > longueur - 10 or self.sensor1_x < 10 or self.sensor1_y > largeur - 10 or self.sensor1_y < 10:  # if sensor 1 is out of the map (the car is facing one edge of the map)
        #     self.signal1 = 1.  # sensor 1 detects full sand

    def rotate_car(self, angle_delta_degrees):
        self._car['orientation'] = self.get_car_orientation() + angle_delta_degrees

    def process_tick(self, delta_time_millis):
        car_speed_per_sec = 10
        mag = car_speed_per_sec * delta_time_millis / 1000
        move_point = math_util.polar_to_cartesian(mag, self.get_car_orientation())
        self._set_car_point(
            self.get_car_point() + move_point
        )
