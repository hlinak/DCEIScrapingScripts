# -*- coding: utf-8 -*-
"""
"""

from PIL import Image
import operator
from os import walk
from datetime import datetime
import pandas as pd

#area = 'ATL' # or "connector"
for area in ["DC"]:#, "connector"]:
    ##***** CHANGE img CROPPING **** Options so far are df_pickle, df_pickle_connector, and df_pickle_ATL
                              #The cropping parameters may need to change if the images were collected on a different computer...
                              #see crop below.

    columns = ['D','R','O','G','C']
    png_file_dir = r"""./screenshots/"""

    pngs = []
    for root, dirs, files in walk(png_file_dir):
        for file in files:
            if file.endswith('.png'):
                pngs.append(file)

    colnames = ["datetime", "D", "R", "O", "G", "C"]

    rgb_collection = []
    unique_rgb_collection = []
    for i, png in enumerate(pngs[:]):
        png_datetime_str = png.split(".")[0]
        png_datetime = datetime.strptime(png_datetime_str, "%Y%m%d_%H%M%S")
        print(png, i+1, "/", len(pngs))
        
        try:
            img1 = Image.open(png_file_dir+png_datetime_str+".png")
        except OSError:
            print("OSError!!!")
            continue

        ##crop image if needed
        if area == 'connector':
            img = img1.crop((904,465,956,508)) #connector
            img.save(r"""./screenshots_cropped_connector/connector_{0}.png""".format(png_datetime_str))
        else:
            #img = img1.crop((500,5,1190,760)) #ATL 1700x900 24 BPP
            img = img1.crop((600,65,1290,820)) #ATL 1920*1080 24 BPP
            #img.save(r"""E:/google_traffic_map/2018_ATL_screenshots_cropped/ATL_{0}.png""".format(png_datetime_str))
            img.save(r"""./screenshots_cropped_"""+area+"/"+area+"_{0}.png".format(png_datetime_str))

        this_rgb_df = pd.DataFrame({"RGB" : [pixel for pixel in img.getdata()]})
        this_unique_rgb_df = this_rgb_df.drop_duplicates()
        this_unique_rgb_df["datetime"] = png_datetime_str

        unique_rgb_collection.append(this_unique_rgb_df)

    all_rgb_collection_df = pd.concat(unique_rgb_collection)
    all_rgb_collection_df.to_csv("all_rgb_collection."+area+"_2022.csv", index=False)
    #all_rgb_collection_df.to_csv("all_rgb_collection.connector_2020.csv", index=False)

    all_unique_rgb_collection = all_rgb_collection_df[["RGB"]].drop_duplicates()
    all_unique_rgb_collection.to_csv("all_unique_rgb_collection."+area+"_2022.csv", index=False)
    #all_unique_rgb_collection.to_csv("all_unique_rgb_collection.connector_2020.csv", index=False)
