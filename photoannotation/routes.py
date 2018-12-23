import os
from PIL import Image
from flask import render_template, url_for, request
from photoannotation import app
from photoannotation.forms import UploadForm, AlbumForm, SearchForm
from photoannotation.face_recogniser import FaceRecogniser
from photoannotation.HistoCluster import HistoCluster
import time
from photoannotation.ImageMetaData import ImageMetaData
import photoannotation.GPSDATA as GPSDATA
from werkzeug.utils import secure_filename
#from pathlib import Path
import shutil

UPLOAD_FOLDER = r'E:/Study/12th sem/PhotoAnnotation/photoannotation/static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
@app.route('/album')
def album():
    dir_list = []
    form = AlbumForm()
    hist = HistoCluster(UPLOAD_FOLDER)
    cluster_data = hist.cluster_photos()
    # for index in cluster_data:
    #     print(index, cluster_data[index])
    #     for image in cluster_data[index]:
    #         print(image)
    # for root, directories, files in os.walk(UPLOAD_FOLDER):
    #     for dirs in directories:
    #         for file_list in os.listdir(os.path.join(root, dirs)):
    #             dir_list.append([dirs, file_list, len(dirs),])
    #             break
    #     break
    return render_template('user/album.html', form=form, dir_list=cluster_data)


@app.route('/album/<string:name>')
def showAlbum(name):
    image_list = []
    # for file in os.listdir(os.path.join(UPLOAD_FOLDER, name)):
    #     image_list.append(file)
    return render_template('user/show-album.html', form=form, album=name, image_list=image_list)


@app.route('/search')
def search():
    form = SearchForm()
    return render_template('user/search.html', form=form)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if request.method == 'POST':
        print("Reached")
        images = request.files.getlist("photo")
        for image in images:
            filename, ext = image.filename.split(".")
            f = app.config['UPLOAD_FOLDER'] + filename + "_" + str(time.time()) + "." + ext
            image.save(f)
            validImages = []
            imgMeta = ImageMetaData(image)
            imgExif = None
            imgGPS = None
            imgElevation = None
            if imgMeta is not None:
                imgExif = imgMeta.get_exif_data()
                if imgExif is not None:
                    '''Exif exists'''
                    imgGPS = imgMeta.get_gps()
                    '''imgGPS[0] = latitude
                       imgGPS[1] = longitude'''
                    if imgGPS[0] != 0:
                        '''call GPSDATA functions for gps related data'''
                        imgElevation = GPSDATA.get_elevation(imgGPS[0], imgGPS[1])
                        #imgWeather = GPSDATA.get_weather_info(imgGPS[0], imgGPS[1], imgExif['DateTime'])
                    else:
                        '''no gps'''
                        pass

                else:
                    '''Exif doesn't exist'''
                    isExif = False
            validImages.append({'ImgLocation': image, 'ExifData': imgExif, 'GpsData': imgGPS,
                                'ImgElevation': imgElevation})
            print(validImages)


    return render_template('user/upload.html', form=form)


@app.route('/read-exif')
def readExif():
    form = UploadForm()
    data = form.photoName.data
    return data


@app.route('/generate-caption', methods=['GET', 'POST'])
def generateCaption():
    if request.method == 'POST':
        img = Image.open(request.files['photo'])
        face = FaceRecogniser()
        response = face.face_recognise(img)
        return response
    pass


@app.route('/change-caption', methods=['GET', 'POST'])
def changeCaption():
    if request.method == "POST":
        print(request)
    return "asdf"


