from PIL import Image, ImageDraw

class Draw:
    def __init__(self) -> None:
        self.__resolution = [640, 480]
        self.__img = Image.new('RGB', (self.__resolution[0], self.__resolution[1]), (255, 255, 255))
        self.__draw = ImageDraw.Draw(self.__img)

    def draw_straight(self, point1, point2) -> None:
        self.__draw.line((point1[0], point1[1], point2[0], point2[1]), fill=(0, 0, 0), width=1) # connect
        