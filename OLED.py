import time

import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from random import randint

# Note you can change the I2C address by passing an i2c_address parameter like:
disp = Adafruit_SSD1306.SSD1306_128_64(rst='P9_12', i2c_address=0x3c, i2c_bus=2)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
font = ImageFont.truetype('Roboto-Regular.ttf', 40)

def disp_rpm(n):
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    rpmstr = '%.2f' % n
    draw.text((2, 16), rpmstr, font=font, fill=255)

    draw.rectangle((0, 0, int(n), 15), outline=255, fill=255)
    disp.image(image)
    disp.display()
