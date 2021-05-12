#!/root/anaconda3/envs/env_dlib/bin/python

'''
@Description: 
@Author: caobin
@Date: 2019-12-21 23:12:40
@Github: https://github.com/bcao19
@LastEditors  : caobin
@LastEditTime : 2019-12-25 08:42:14
'''
import os
from PIL import Image
import face_recognition
import cv2
import numpy as np


# Open the input movie file
input_movie = cv2.VideoCapture("/root/test/1.mp4")
length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

# Save picture path
save_path = '/root/test/face/'




frame_number = 0
known_faces = []
face_times = []


while True:
    # Grab a single frame of video
    ret, frame = input_movie.read()
    frame_number += 1

    # Quit when the input video file ends
    if not ret:
        break

    if frame_number % 30 != 0:
        continue

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    if len(face_locations) == 0:
        continue

    
    i = 0
    for face_encoding in face_encodings:
        match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.50)
        if 1 in match:
            i = i+1
            face_times[match.index(1)].append(frame_number)
        else:
            known_faces.append(face_encoding)
            top, right, bottom, left = face_locations[i]
            face_image = rgb_frame[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
            pil_image.save(save_path + str(frame_number)+'_'+str(i)+'.jpg')
            i = i+1
            face_times.append([frame_number])


print(face_times)
face_times = np.array(face_times)
np.save('/root/test/face/face_times.npy', face_times)
print



