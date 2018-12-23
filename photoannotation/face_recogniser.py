import os
import cv2 as cv
import numpy as np
import tensorflow as tf
from photoannotation import app

class FaceRecogniser:
    def __init__(self):
        self.checked = False
        path_list = os.path.join(os.path.dirname(app.root_path), "venv/Lib/site-packages/cv2/data")
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        self.face_cascade = cv.CascadeClassifier(path_list+"/haarcascade_frontalface_default.xml")
        self.model_name = 'E:/Study/12th sem/PhotoAnnotation/photoannotation/static/models/face-recogniser'
        self.model = tf.keras.models.load_model(self.model_name)
        self.categories = []
        with open('E:/Study/12th sem/PhotoAnnotation/photoannotation/static/models/name-list.txt') as f:
            for name in f:
                self.categories.append(name.split('\n')[0])
                pass
            pass
        pass

    def rotate_img(self, img):
        img = cv.resize(img, (500, 500))
        rows, cols, layer = img.shape
        M = cv.getRotationMatrix2D((cols / 2, rows / 2), 90, 1)
        rotated_img = cv.warpAffine(img, M, (cols, rows))
        # cv.imshow("Check", rotated_img)
        # cv.waitKey(0)
        # cv.destroyAllWindows()
        return rotated_img

    def face_recognise(self, img):
        face_list = []
        img = np.array(img)
        divider = 1
        if img.shape[0] > img.shape[1] and img.shape[0] > 700:
            divider = img.shape[0] / 500
            pass
        elif img.shape[1] > 700:
            divider = img.shape[1] / 500
            pass
        resized_img = cv.resize(img, (int(img.shape[1] / divider), int(img.shape[0] / divider)))
        gray_img = cv.cvtColor(np.array(resized_img), cv.COLOR_BGR2GRAY)
        # cv.imshow("Check", gray_img)
        # cv.waitKey(0)
        # cv.destroyAllWindows()
        faces = self.face_cascade.detectMultiScale(gray_img, 1.1, 5)
        if len(faces) == 0:
            if not self.checked:
                rotated_img = self.rotate_img(resized_img)
                self.checked = True
                return self.face_recognise(rotated_img)

        for num, (x, y, w, h) in enumerate(faces):
            crop_img = gray_img[y:y + h, x:x + w]
            img_array = cv.resize(crop_img, (100, 100))
            data = img_array.reshape(-1, 100, 100, 1)
            model_out = self.model.predict([data])
            faces_in_photo = []
            # print(np.amax(model_out))
            if np.amax(model_out) > 0.94:
                faces_in_photo.append(self.categories[np.argmax(model_out)])
            # print(faces_in_photo)
            # cv.imshow("test", img_array)
            # cv.waitKey(0)
            # cv.destroyAllWindows()
            if len(faces_in_photo) > 0:
                if faces_in_photo[0] not in face_list:
                    face_list.append(faces_in_photo[0])
                    pass
                pass
            pass
        if len(face_list) == 0:
            return "I think this photo contains no face"
        face_data = "This photo contains "
        for num, face_name in enumerate(face_list):
            if num < len(face_list) - 2:
                face_data += face_name + ", "
            elif num < len(face_list) - 1:
                face_data += face_name + " and "
            else:
                face_data += face_name
                pass
            pass
        return face_data
    pass
