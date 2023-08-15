from PIL import Image, ImageDraw

im = Image.new('RGB', (500, 300), (255, 255, 255))
draw = ImageDraw.Draw(im)

draw.line((100,200,300,300), fill=(0, 0, 0), width=1)

im.save("isometric.jpg")