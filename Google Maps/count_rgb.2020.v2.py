# -*- coding: utf-8 -*-
"""
Created on Thu May 18 09:28:06 2017

@author: Trail1
"""

import os, os.path
from PIL import Image
from os import walk
from datetime import datetime
import pandas as pd
import numpy as np

rgbcode_dict = { (99, 214, 104, 255) : "G",
                 (255, 151, 77, 255) : "O",
                 (242, 60, 50, 255)  : "R",
                 (129, 31, 31, 255)  : "D",
                 (255, 255, 255, 255): "W"}

def str2tuple(tuple_str):
    r, g, b, alpha = tuple_str.replace("(","").replace(")","").split(",")
    return tuple([int(r), int(g), int(b), int(alpha)])
#rgb_df1 = pd.read_csv("rgb_traffic.csv")
#rgb_df1["rgb_code"] = rgb_df1["RGB"].apply(lambda x : str2tuple(x))

png_file_dir = r"""./screenshots_cropped_DC"""

png_flielist = []
for root, dirs, files in walk(png_file_dir):
    for file in files:
        if file.endswith('.png'):
            png_flielist.append(file)

png_flielist = png_flielist[:]

rgb_collection = []
unique_rgb_collection = []
for i, png in enumerate(png_flielist[:]):
    png_datetime_str = png.split(".")[0].split("_")[1]+"_"+png.split(".")[0].split("_")[2]
    png_datetime = datetime.strptime(png_datetime_str, "%Y%m%d_%H%M%S")
    print(png, i+1, "/", len(png_flielist))
    img1 = Image.open(os.path.join(png_file_dir,r"""DC_{0}.png""".format(png_datetime_str)))

    newimdata = []
    for color in img1.getdata():
        if color in [(99, 214, 104, 255), (255, 151, 77, 255), (242, 60, 50, 255), (129, 31, 31, 255)]:
            # G, O, R, D
            # D: (145, 59, 59, 255) - (R, G, B, alpha)
            #    (137, 45, 45, 255)
            #
        #if color in [(132, 202, 80, 255), (222, 241, 208, 255), (165, 216, 127, 255)]:
            #print("XXX")
            newimdata.append(color)
        else:
            newimdata.append((255, 255, 255, 255))

    img2 = Image.new(img1.mode,img1.size)
    img2.putdata(newimdata)
    #img2.save(r"""test_ATL_{0}.png""".format(png_datetime_str))

    df1 = pd.DataFrame({"rgb" : newimdata})
    df1["DROG"] = df1["rgb"].apply(lambda x : rgbcode_dict[x])
    df1["datetime"] = png_datetime_str
    df2 = pd.pivot_table(df1, values="rgb", index="datetime", columns="DROG", aggfunc="count").reset_index()
    rgb_collection.append(df2)

df3 = pd.concat(rgb_collection)

df3.to_csv("DC_screenshots_cropped_DROG_Counts.csv")
