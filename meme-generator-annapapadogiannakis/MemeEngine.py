""" We are editing a given image by changing the width to 500,
changing height according to the original image ratio, adding
text - quote and author- randomly placing inside the image,
and saving the file to output directory. We have used Pillow
library for image editing and adding texts.
"""

from PIL import Image, ImageDraw
import random


class MemeEngine():
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def make_meme(self, img_path, text1, author, width=500):
        img = Image.open(img_path)

        ratio = width / float(img.size[0])
        height = int(ratio * float(img.size[1]))
        img = img.resize((width, height), Image.NEAREST)

        # Removing (') character, otherwise PIL will not draw
        text1 = text1.replace("\u2019", "")
        author = author.replace("\u2019", "")

        rand_x = random.randint(0, int(width / 2))
        rand_y = random.randint(0, int(height / 2))

        draw = ImageDraw.Draw(img)
        draw.text((rand_x, rand_y), text1, fill='white')
        draw.text((rand_x, (rand_y + 30)), ('   -' + author), fill='white')

        out_file = (self.output_dir + '/' + str(random.randint(0, 1000)) + '.jpg')

        img.save(out_file, "JPEG")
        return (out_file)