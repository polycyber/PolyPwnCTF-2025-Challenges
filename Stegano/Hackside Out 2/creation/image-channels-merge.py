from PIL import Image
from sys import argv

red_channel = Image.open(argv[1]).split()[0]
green_channel = Image.open(argv[2]).split()[1]
blue_channel = Image.open(argv[3]).split()[2]

merged_image = Image.merge("RGB", (red_channel, green_channel, blue_channel))
merged_image.save(f"{argv[1].split('-red')[0]}-merged.png")
