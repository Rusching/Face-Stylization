from os import read
from git import base
import numpy as np
from PIL import Image, ImageDraw
from random import uniform as rn
from random import randint as ri
import pickle
import time
import argparse
import os
import triangle

def getColorsSchema():
    # load color schema. Now have 73 color schema, each has 50 colors, 
    # in the format of list: 73 * 50, each color is represented in R, G, B form
    
    colorSchema = 'color_table.pkl'
    with open(colorSchema, 'rb') as f:
        colorTable = pickle.load(f)
    return colorTable


def img2arr(img):
    return np.array(img)


def rgba2rgb(rgba_img):
    w, h = rgba_img.size
    rgb_img = Image.new('RGB', (w, h))
    rgb_img.paste(rgba_img)
    return rgb_img

def readImg(img_path):
    img = Image.open(img_path).convert('L')
    w, h = img.size
    return img, w, h

def calErr(srcImg, targetImg, pow=1):
    w, h = targetImg.size
    total_error = 0
    for i in range(w):
        for j in range(h):
            # for GRB mode
            # rt, gt, bt = targetImg.getpixel((i, j))
            # rs, gs, bs = srcImg.getpixel((i, j))
            # if pow == 1:
            #     total_error += ((rt-rs) + (gt-gs) + (bt-bs))
            # elif pow == 2:
            #     total_error += ((rt-rs)*(rt-rs) + (gt-gs)*(gt-gs) + (bt-bs)*(bt-bs))
            gt = targetImg.getpixel((i, j))
            st = srcImg.getpixel((i, j))
            if pow == 1:
                total_error += abs(gt - st)
            elif pow == 2:
                total_error += (gt - st) * (gt - st)
    return total_error


def generate_triangle(w, h):
    x1 = rn(0, w)
    x2 = rn(0, w)
    x3 = rn(0, w)
    y1 = rn(0, h)
    y2 = rn(0, h)
    y3 = rn(0, h)
    triangle_params = [(x1, y1), (x2, y2), (x3, y3)]
    while not triangle.is_valid(triangle_params):
        x1 = rn(0, w)
        x2 = rn(0, w)
        x3 = rn(0, w)
        y1 = rn(0, h)
        y2 = rn(0, h)
        y3 = rn(0, h)
        triangle_params = [(x1, y1), (x2, y2), (x3, y3)]
    return triangle_params


def coloring(triangle_list, w, h, basename):
    triangle_num = len(triangle_list)
    colored_image = Image.new('RGB', (w, h), (255, 255, 255))
    render = ImageDraw.Draw(colored_image)
    with open('color_table.pkl', 'rb') as f:
        color_table = pickle.load(f)
    color_schema = color_table[ri(0, len(color_table)-1)]
    for i, triangle in enumerate(triangle_list):
        render.polygon(triangle, tuple(color_schema[ri(0, len(color_schema)-1)]))
        print("adding {}th triangle to final image, process {}%".format(i+1, 100*(i+1)/triangle_num))
    colored_name = basename + '/' + basename + '_colored.png'
    colored_image.save(colored_name)
    triangle_list_name = basename + '/' + basename + '_triangles.pkl'
    with open(triangle_list_name, 'wb') as f:
        pickle.dump(triangle_list, f)
    

def generate_img(targetImagePath, count = 30):
    targetImage, w, h = readImg(targetImagePath)
    image = Image.new('L', (w, h), 255)
    draw = ImageDraw.Draw(image)
    beforeScore = calErr(image, targetImage)
    triangle_list = list()

    basename = os.path.splitext(os.path.basename(targetImagePath))[0]
    os.mkdir(basename)
    gray_out_name = basename + '/' + basename + '_gray.png'

    for i, _ in enumerate(range(count)):
        flag = True
        while(flag):
            imagePreview = image.copy()
            drawtest = ImageDraw.Draw(imagePreview)
            randomTriangle = generate_triangle(w, h)
            randomLightness = ri(0, 255)
            drawtest.polygon(randomTriangle, fill=randomLightness)
            afterScore = calErr(imagePreview, targetImage)
            if afterScore < beforeScore:
                flag = False
                draw.polygon(randomTriangle, fill=randomLightness)
                beforeScore = afterScore
                triangle_list.append(randomTriangle)
                print("adding {}th polygon, progress {}%".format(i+1, 100*(i+1)/count))

            del imagePreview, drawtest
            if i+1 % 5 == 0:
                image.save(basename + '/' + basename + '_gray_{}f.png'.format(i))
    image.save(gray_out_name)
    coloring(triangle_list, w, h, basename)


parse = argparse.ArgumentParser()
parse.add_argument("e")
args = parse.parse_args()

filename = args.e
start = time.time()
generate_img(filename, 200)
end = time.time()
taken = end - start
print ("total consumed {} seconds".format(taken))
