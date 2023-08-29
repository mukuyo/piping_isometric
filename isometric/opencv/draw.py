from PIL import Image, ImageDraw

class Draw:
    """opencv draw class"""
    def __init__(self) -> None:
        self.__resolution = [640, 480]
        self.__img = Image.new('RGB', (self.__resolution[0], self.__resolution[1]), (255, 255, 255))
        self.__draw = ImageDraw.Draw(self.__img)

    def draw_straight(self, point1, point2) -> None:
        """draw straight line"""
        self.__draw.line((point1[0], point1[1], point2[0], point2[1]), fill=(0, 0, 0), width=1) # connect

    def draw_downward(self, point) -> None:
        """draw downward line"""
        self.__draw.line((point[0], point[1], point[0], point[1] - 1000), fill=(0, 0, 0), width=1) # connect

    def draw_upward(self, point) -> None:
        """draw upward line"""
        self.__draw.line((point[0], point[1], point[0], point[1] + 1000), fill=(0, 0, 0), width=1) # connect

    def line_2d(self, results, pose_results) -> None:
        """line_2d"""
        for result in results:
            self.draw_straight(result[0], result[1])
        self.__img.save('./data/isometric/results/2d_result.jpg')
    
    def isometric(self, results, pose_results) -> None:
        """isometirc drawing"""
        # print(results)
        self.__img.save('./data/isometric/results/iso_result.jpg')
