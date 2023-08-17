from PIL import Image, ImageDraw
import csv

name = ['bent']
position = [0, 0]
pose = [0, 0, 0]

im = Image.new('RGB', (500, 300), (255, 255, 255))
draw = ImageDraw.Draw(im)

if name[0] == 'bent':
    print('bent detection')
    draw.line((100, 200, 300, 300), fill=(0, 0, 0), width=1)

im.save("./data/Image/isometric.jpg")