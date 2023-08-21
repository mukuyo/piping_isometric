from PIL import Image, ImageDraw
import math

class Isometric:
    def __init__(self, output_path) -> None:
        self.__resolution = [640, 480]
        self.__img = Image.new('RGB', (self.__resolution[0], self.__resolution[1]), (255, 255, 255))
        self.__draw = ImageDraw.Draw(self.__img)

        self.__output_dir = output_path
    
    def run(self, pose_results: list) -> None:
        for result in pose_results:
            print(result.name, result.position, result.size, result.pose)
            self.__draw.point(result.position, fill=(0, 0, 0))
        self.__img.save(self.__output_dir)  