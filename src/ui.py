import tkinter as tk

import math_util
from math_util import Point

# ------------------
# |                |
# |    Canvas      |
# |                |
# ------------------
# Clear | Save | Load


car_points = [
    -2, 1,
    1, 1,
    2, 0,
    1, -1,
    -2, -1
]
car_sensor_1_points = [
    1 + 0.3, 1,
    1 + 0.7, 1,
    1 + 0.7, 1 - 0.4,
    1 + 0.3, 1 - 0.4
]
car_sensor_2_points = [
    2, 0.2,
    2 + 0.4, 0.2,
    2 + 0.4, -0.2,
    2, -0.2
]
car_sensor_3_points = [
    1 + 0.3, -1,
    1 + 0.7, -1,
    1 + 0.7, -1 + 0.4,
    1 + 0.3, -1 + 0.4
]

car_size = 5


class UI:

    def __init__(self, width, height, on_cls, on_save, on_load, on_create_sand):
        self._call_on_cls = on_cls
        self._call_on_create_sand = on_create_sand

        self.root = tk.Tk()
        self.root.title('AI')
        # self.root.geometry('300x200')
        self.root.configure(bg='black')

        frame_canvas = tk.Frame(self.root)
        frame_canvas.pack()
        self._canvas_width = width
        self._canvas_height = height
        self.canvas = tk.Canvas(frame_canvas, width=self._canvas_width, height=self._canvas_height)
        self.canvas.config(bg='black')
        self.canvas.bind("<B1-Motion>", self._paint)
        self.canvas.pack()

        frame_btn = tk.Frame(self.root)
        frame_btn.pack()
        cls_btn = tk.Button(frame_btn,
                            text="Clear",
                            command=self._clean)
        cls_btn.pack(side=tk.LEFT)

        save_btn = tk.Button(frame_btn,
                             text="Save",
                             command=on_save)
        save_btn.pack(side=tk.LEFT)

        load_btn = tk.Button(frame_btn,
                             text="Load",
                             command=on_load)
        load_btn.pack(side=tk.LEFT)

    def _clean(self):
        self.canvas.delete("all")
        self._call_on_cls()

    def _paint(self, event):
        radius = 2
        x = event.x
        y = event.y
        x1 = x - radius
        y1 = y - radius
        x2 = x + radius
        y2 = y + radius

        overlapping_items = self.canvas.find_overlapping(x1, y1, x2, y2)

        if len(overlapping_items) == 0:
            self.canvas.create_oval(x1, y1, x2, y2, fill='yellow', outline='yellow', tag='sand')

            # Y axis flip: source positive down -> target positive up
            self._call_on_create_sand(Point(x, self._canvas_height - y))

    def draw_car(self, center_point, orientation):
        """
        Center point (East=Positive X, North=Positive Y)
        Orientation angle (East=0, North=90, West=180, South=270)
        """

        self._create_or_update(
            self._format_points(car_points, center_point, orientation, car_size),
            'green',
            'car'
        )
        self._create_or_update(
            self._format_points(car_sensor_1_points, center_point, orientation, car_size),
            'red',
            'car_sensor_1'
        )
        self._create_or_update(
            self._format_points(car_sensor_2_points, center_point, orientation, car_size),
            'red',
            'car_sensor_2'
        )
        self._create_or_update(
            self._format_points(car_sensor_3_points, center_point, orientation, car_size),
            'red',
            'car_sensor_3'
        )

    # TODO move sensor coords to World
    def get_sensor_point(self, sensor_number_id):
        existing_ids = self.canvas.find_withtag('car_sensor_' + str(sensor_number_id))
        item_id = existing_ids[0]
        points = self.canvas.coords(item_id)

        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0

        for i, p in enumerate(points):
            y_axis = i % 2 != 0

            if i <= 2:
                if y_axis:
                    y1 = p
                    y2 = p
                else:
                    x1 = p
                    x2 = p
            else:
                if y_axis:
                    y1 = min(y1, p)
                    y2 = max(y2, p)
                else:
                    x1 = min(x1, p)
                    x2 = max(x2, p)

        x = x1 + (x2 - x1) / 2
        y = y1 + (y2 - y1) / 2

        return Point(x, self._canvas_height - y)

    def _create_or_update(self, points, color, tag):
        existing_ids = self.canvas.find_withtag(tag)

        if len(existing_ids) == 0:
            self.canvas.create_polygon(
                points,
                outline=color,
                fill=color,
                tag=tag
            )
        else:
            item_id = existing_ids[0]
            self.canvas.coords(item_id, points)
            self.canvas.itemconfig(
                item_id,
                outline=color,
                fill=color,
                tag=tag
            )

    def _format_points(self, polygon_points, center_point, orientation, size):
        rotated_points = self._rotate_points(polygon_points, orientation)
        formatted_points = []
        for i, p in enumerate(rotated_points):
            y_axis = i % 2 != 0
            p_s = rotated_points[i] * size
            p_t = p_s + (center_point.y if y_axis else center_point.x)
            formatted_points.append(p_t)
            # Y axis flip: source positive up -> target positive down
            if y_axis:
                formatted_points[i] = self._canvas_height - formatted_points[i]
        return formatted_points

    def _rotate_points(self, points, angle):
        rotated_points = []
        for i, p in enumerate(points):
            y_axis = i % 2 != 0
            if y_axis:
                rp = math_util.rotate_point(Point(points[i - 1], points[i]), angle)
                rotated_points.append(rp.x)
                rotated_points.append(rp.y)

        return rotated_points

    def loop(self):
        self.root.mainloop()
