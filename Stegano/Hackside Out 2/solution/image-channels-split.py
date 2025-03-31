from PIL import Image

image = Image.open("captivating-painting.png")

red, green, blue = image.split()

red.save("red_channel.png")
green.save("green_channel.png")
blue.save("blue_channel.png")
