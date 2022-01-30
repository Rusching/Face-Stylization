from PIL import Image
import os
import pickle
from collections import defaultdict

# extract the colors of one image and sort by requency. Keep the top 50 values.
# Travese all the images in one folder and save them using pickle.

def readImg(image_path):
    img = Image.open(image_path).convert('RGB')
    w, h = img.size
    return img, w, h

def extract_color(image_path):
    image, _, _ = readImg(image_path)
    colors = defaultdict(int)
    for pixel in image.getdata():
        colors[pixel] += 1
    colors = sorted(colors.items(), key=lambda x: x[1], reverse=True)
    colors = colors[:50]

    sim_color = list()
    for each in colors:
        sim_color.append(list(each[0]))
    # print(sim_color)
    return sim_color

def main():
    folder_path = 'WPAP\WPAP'
    color_table = list()
    for each in os.listdir(folder_path):
        image_path = os.path.join(folder_path, each)
        simple_image_color_list = extract_color(image_path)
        color_table.append(simple_image_color_list)
    with open('color_table.pkl', 'wb') as f:
        pickle.dump(color_table, f)

main()