from ui import UI


def clean_canvas():
    print("Clean")


def save_model():
    print("Save")


def load_model():
    print("Load")


def put_sand(point):
    print("Sand " + str(point.x) + " " + str(point.y))


if __name__ == '__main__':
    UI(
        on_cls=clean_canvas,
        on_save=save_model,
        on_load=load_model,
        on_create_sand=put_sand
    ).loop()
