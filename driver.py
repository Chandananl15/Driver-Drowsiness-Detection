import os
import math
import cv2
import mediapipe as mp
import pygame
import numpy as np
from datetime import datetime

# --------------------------
# Config
# --------------------------
EAR_THRESHOLD = 0.25
EAR_FRAMES = 20

MAR_THRESHOLD = 0.6
TILT_THRESHOLD = 15  # degrees

ALARM_FILE = "alarm.wav"

# --------------------------
# Alarm setup
# --------------------------
pygame.mixer.init(frequency=44100, size=-16, channels=1)
pygame.mixer.music.load(ALARM_FILE)

def play_alarm():
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1)

def stop_alarm():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

# --------------------------
# Mediapipe setup
# --------------------------
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, max_num_faces=1)

# Eye landmark indices
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# Mouth landmarks
MOUTH_TOP = 13
MOUTH_BOTTOM = 14
MOUTH_LEFT = 61
MOUTH_RIGHT = 291

# Ear landmarks for tilt
LEFT_EAR = 234
RIGHT_EAR = 454

# --------------------------
# Utility functions
# --------------------------
def eye_aspect_ratio(landmarks, eye_points, w, h):
    p = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in eye_points]
    A = math.dist(p[1], p[5])
    B = math.dist(p[2], p[4])
    C = math.dist(p[0], p[3])
    return (A + B) / (2.0 * C)

def mouth_aspect_ratio(landmarks, w, h):
    top = (int(landmarks[MOUTH_TOP].x * w), int(landmarks[MOUTH_TOP].y * h))
    bottom = (int(landmarks[MOUTH_BOTTOM].x * w), int(landmarks[MOUTH_BOTTOM].y * h))
    left = (int(landmarks[MOUTH_LEFT].x * w), int(landmarks[MOUTH_LEFT].y * h))
    right = (int(landmarks[MOUTH_RIGHT].x * w), int(landmarks[MOUTH_RIGHT].y * h))
    A = math.dist(top, bottom)
    B = math.dist(left, right)
    return A / B

def head_tilt_angle(landmarks, w, h):
    left = (int(landmarks[LEFT_EAR].x * w), int(landmarks[LEFT_EAR].y * h))
    right = (int(landmarks[RIGHT_EAR].x * w), int(landmarks[RIGHT_EAR].y * h))
    dx, dy = right[0] - left[0], right[1] - left[1]
    angle = math.degrees(math.atan2(dy, dx))
    return angle

# --------------------------
# Main loop
# --------------------------
cap = cv2.VideoCapture(0)
counter = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    status = "OK"
    alert = False

    if results.multi_face_landmarks:
        lm = results.multi_face_landmarks[0].landmark

        # EAR (eyes)
        leftEAR = eye_aspect_ratio(lm, LEFT_EYE, w, h)
        rightEAR = eye_aspect_ratio(lm, RIGHT_EYE, w, h)
        ear = (leftEAR + rightEAR) / 2.0

        if ear < EAR_THRESHOLD:
            counter += 1
            if counter >= EAR_FRAMES:
                status = "DROWSY"
                alert = True
        else:
            counter = 0

        # MAR (mouth)
        mar = mouth_aspect_ratio(lm, w, h)
        if mar > MAR_THRESHOLD:
            status = "YAWNING"
            alert = True

        # Head tilt
        angle = head_tilt_angle(lm, w, h)
        if abs(angle) > TILT_THRESHOLD:
            status = "HEAD TILT"
            alert = True

        # HUD
        cv2.putText(frame, f"EAR: {ear:.3f}", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
        cv2.putText(frame, f"MAR: {mar:.3f}", (20, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
        cv2.putText(frame, f"Tilt Angle: {angle:.2f}", (20, 140),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    # Status & alarm
    color = (0,0,255) if alert else (0,200,0)
    cv2.putText(frame, f"Status: {status}", (20,40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    if alert:
        play_alarm()
    else:
        stop_alarm()

    cv2.imshow("Driver Monitor", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
stop_alarm()
cv2.destroyAllWindows()
