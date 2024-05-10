# face_recognition.py

import cv2
import mediapipe as mp
import os
from fastapi import FastAPI, HTTPException

mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

def process_image(file_path: str):
    image = cv2.imread(file_path)
    if image is None:
        print(f"Error: Unable to load image from path: {file_path}")
        return None, None

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = face_detection.process(image_rgb)

    if results.detections:
        for detection in results.detections:
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = image.shape
            bbox = (
                int(bboxC.xmin * iw),
                int(bboxC.ymin * ih),
                int(bboxC.width * iw),
                int(bboxC.height * ih)
            )

            cropped_face = image[bbox[1]:bbox[1] + bbox[3], bbox[0]:bbox[0] + bbox[2]]

            mp_face_mesh = mp.solutions.face_mesh
            face_mesh = mp_face_mesh.FaceMesh()
            results_mesh = face_mesh.process(image_rgb)

            face_landmarks = []

            if results_mesh.multi_face_landmarks:
                for face_landmark in results_mesh.multi_face_landmarks:
                    for landmark in face_landmark.landmark:
                        x, y = int(landmark.x * iw), int(landmark.y * ih)
                        face_landmarks.append((x, y))

            return cropped_face, face_landmarks
    else:
        print("No Face Detected!")
        return None,None

async def process_uploaded_image(file):
    try:
        with open(file.filename, "wb") as buffer:
            buffer.write(await file.read())

        cropped_face, face_landmarks = process_image(file.filename)
        os.remove(file.filename)
        if cropped_face is not None and face_landmarks is not None:
            return cv2.imencode('.png',cropped_face)[1].tobytes(),True
        else:
            return "No Face Detected",False
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
