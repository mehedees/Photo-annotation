import os, cv2, shutil
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from collections import Counter
from photoannotation.ImageMetaData import ImageMetaData
import photoannotation.GPSDATA as GPSDATA
import piexif

class HistoCluster:
    def __init__(self, dir_path):
        self.img_size = 50
        #self.photo_dir = r"E:/Study/12th sem/PhotoAnnotation/photoannotation/static/images"
        self.photo_dir = dir_path
        pass

    def clustering(self, img_array):
        img_array = pd.DataFrame(data=img_array)
        img_array = abs((img_array - img_array.min()) / (img_array.max() - img_array.min()))
        # print(photoData)
        img_array = img_array.values.astype("float64", copy=False)
        stscaler = StandardScaler().fit(img_array)
        img_array = stscaler.transform(img_array)
        i = 70
        # while i < 100
        dbsc = DBSCAN(eps=i, min_samples=5, metric='euclidean').fit(img_array)
        """print(i, " - ",Counter(dbsc.labels_))
        i += 1"""
        return dbsc.labels_

    def cluster_photos(self):
        photoData = []
        for files in os.listdir(self.photo_dir):
            #print(os.path.join(self.photo_dir, files))
            img_array = cv2.imread(os.path.join(self.photo_dir, files))
            img_array = cv2.resize(img_array, (self.img_size, self.img_size))
            # print(img_array)
            img_array1 = img_array.flatten()
            # print(img_array1)
            photoData.append(img_array1)
            pass
        labels = self.clustering(photoData)
        cluster_data = {}
        for index in Counter(labels):
            cluster_data[str(index)] = []
            pass
        for num, files in enumerate(os.listdir(self.photo_dir)):
            photo_path = self.photo_dir + files
            #print(str(labels[num]), photo_path)
            cluster_data[str(labels[num])].append(files)
        # for cluster in cluster_data:
        #     for img in cluster_data[cluster]:
        #         date_time = ""
        #         img_meta = ImageMetaData(self.photo_dir + img)
        #         imgExif = img_meta.get_exif_data()
        #         if imgExif is not None:
        #             # if imgExif['DateTime'] is not None or imgExif['DateTime'] is not "":
        #             #     #for imag in cluster_data[cluster]:
        #             #         '''write datetime in exif'''
        #
        #             #print(imgExif['DateTime'])
        #             continue
        #             pass
        #         else:
        #             pass
        #             # zeroth_ifd = {piexif.ImageIFD.Orientation: image_orientation,
        #             #               piexif.ImageIFD.ImageWidth: int(new_width),
        #             #               piexif.ImageIFD.ImageLength: int(new_height),
        #             #               piexif.ImageIFD.Software: u"piexif"
        #             #               }
        #             #
        #             # exif_dict = {"0th": zeroth_ifd}
        #             # exif_bytes = piexif.dump(exif_dict)
        #             #
        #             # with open(dest, 'r+b') as f:
        #             #     with Image.open(dest, 'r') as image:
        #             #         image.save(dest, "jpeg", exif=exif_bytes)
            pass
        print(cluster_data)
        return cluster_data

        # cluster_data = {}
        # for index in Counter(self.labels):
        #     cluster_data[str(index)] = []
        #     pass
        # for i in range(2):
        #     cluster_data["0"] = []
        #     cluster_data["-1"] = []
        #     for num, files in enumerate(os.listdir(self.photo_dir)):
        #         photo_path = self.photo_dir + "/" + files
        #         # print(photo_path)
        #         if self.labels[num] == 0:
        #             # cluster_data.append([labels[num], photo_path])
        #             cluster_data["0"].append(photo_path)
        #         elif self.labels[num] == -1:
        #             # cluster_data1.append([labels[num], photo_path])
        #             cluster_data["-1"].append(photo_path)
        #         else:
        #             cluster_data["1"].append(photo_path)
        #             pass
        #         pass
        #     photo_data = []
        #     #print(len(cluster_data["0"]), len(cluster_data["-1"]))
        #     for index in cluster_data["0"]:
        #         img_array = cv2.imread(index)
        #         img_array = cv2.resize(img_array, (self.img_size, self.img_size))
        #         # print(img_array)
        #         img_array1 = img_array.flatten()
        #         # print(img_array1)
        #         photo_data.append(img_array1)
        #         print(len(photo_data))
        #         pass
        #     print(len(photo_data))
        #     for index in cluster_data["-1"]:
        #         img_array = cv2.imread(index)
        #         img_array = cv2.resize(img_array, (self.img_size, self.img_size))
        #         # print(img_array)
        #         img_array1 = img_array.flatten()
        #         # print(img_array1)
        #         photo_data.append(img_array1)
        #         pass
        #     print(len(photo_data))
        #     self.labels = self.clustering(photo_data)
        #     print(Counter(self.labels))
        # print(cluster_data)
