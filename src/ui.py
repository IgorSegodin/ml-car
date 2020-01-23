import tkinter as tk


# ------------------
# |                |
# |    Canvas      |
# |                |
# ------------------
# Clear | Save | Load

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
        self.canvas = tk.Canvas(frame_canvas, width=300, height=300)
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
            self._call_on_create_sand(Point(x, y))

    def draw_car(self, point, orientation):
        """Center point and orientation angle (East=0, North=90, West=180, South=270)"""
        # TODO http://effbot.org/zone/tkinter-complex-canvas.htm
        print('Not implemented')

    def loop(self):
        self.root.mainloop()
