import tkinter as tk

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


class Point:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y


class UI:

    def __init__(self, on_cls, on_save, on_load, on_create_sand):
        self._call_on_cls = on_cls
        self._call_on_create_sand = on_create_sand

        self.root = tk.Tk()
        self.root.title('AI')
        # self.root.geometry('300x200')
        self.root.configure(bg='black')

        frame_canvas = tk.Frame(self.root)
        frame_canvas.pack()
        self._canvas_width = 300
        self._canvas_height = 300
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

    def draw_car(self, point, orientation):
        """
        Center point (East=Positive X, North=Positive Y)
        Orientation angle (East=0, North=90, West=180, South=270)
        """
        # TODO do not create if already exists
        self.canvas.find_withtag('car')

        self.canvas.create_polygon(
            self._format_points(car_points, point, car_size),
            outline='green',
            fill='green',
            tag='car'
        )
        self.canvas.create_polygon(
            self._format_points(car_sensor_1_points, point, car_size),
            outline='red',
            fill='red',
            tag='car_sensor_1'
        )
        self.canvas.create_polygon(
            self._format_points(car_sensor_2_points, point, car_size),
            outline='red',
            fill='red',
            tag='car_sensor_2'
        )
        self.canvas.create_polygon(
            self._format_points(car_sensor_3_points, point, car_size),
            outline='red',
            fill='red',
            tag='car_sensor_3'
        )

    def _format_points(self, polygon_points, center_point, size):
        formatted_points = []
        for i, p in enumerate(polygon_points):
            y_axis = i % 2 != 0
            p_s = polygon_points[i] * size
            p_t = p_s + (center_point.y if y_axis else center_point.x)
            formatted_points.append(p_t)
            # TODO rotate before axis flip: http://effbot.org/zone/tkinter-complex-canvas.htm
            # Y axis flip: source positive up -> target positive down
            if y_axis:
                formatted_points[i] = self._canvas_height - formatted_points[i]
        return formatted_points

    def loop(self):
        self.root.mainloop()
