#-*- encode:UTF-8#  -*-
# author : masaki
from PIL import Image
import argparse

class ConvertImage(object):
    def __init__(self, image=None, width=1, color='#000000', inFrame=False):
        self.image = image
        self.rim_width = width
        self.rim_color = self.rgb_to_cc(color)
        self.rim_in_frame = inFrame

    def rgb_to_cc(self, color):
        red   = int(color[1:3], 16)
        green = int(color[3:5],16)
        blue  = int(color[5:7],16)
        return (red, green, blue)

    def get_frame(self):
        width = self.image.width + self.rim_width * 2
        height = self.image.height + self.rim_width * 2
        return Image.new('RGB', (width, height), self.rim_color)

    def paste_image_to_frame(self):
        if not self.rim_in_frame:
            rim = self.rim_width
            width = self.image.width + rim
            height = self.image.height + rim

            frame = self.get_frame()
            frame.paste(self.image, (rim, rim, width, height), None)
            return frame
        else:
            # top rim
            for h in range(0, self.rim_width, 1):
                for w in range(0, self.image.width-1, 1):
                    self.image.putpixel((w, h), self.rim_color)

            # bottom rim
            for h in range(self.image.height-1, (self.image.height-1)-self.rim_width, -1):
                for w in range(0, self.image.width-1, 1):
                    self,image.putpixel((w, h), self.rim_color)
            # left rim
            for w in range(0, self.rim_width, 1):
                for h in range(0, self.image.height-1, 1):
                    self,image.putpixel((w, h), self.rim_color)

            # right rim
            for w in range(self.image.width-1, (self.image.width-1)-self.rim_width, -1):
                for h in range(0, self.image.height-1, 1):
                    self,image.putpixel((w, h), self.rim_color)
            return self.image

    def show_image(self):
        frame = self.paste_image_to_frame()
        frame.show()

if __name__ == "__main__":
    import sys
    parser = argparse.ArgumentParser(description="screenshot autorim")
    parser.add_argument('-f', '--file', type=str, help='    : destination file', required=True)
    parser.add_argument('-w', '--width', type=int, help='   : width of rim', default=1, required=False)
    parser.add_argument('-c', '--color', type=str, help='   : color code of rim', default='#FFFFFF', required=False)
    parser.add_argument('-in', dest='rimInFrame', action='store_true')
    parser.set_defaults(rimInFrame=False)

    # remove source file from parameter list
    params = parser.parse_args()
    # create an image
    image = Image.open(params.file)
    c_image = ConvertImage(image, params.width, params.color, params.rimInFrame)
    c_image.show_image()