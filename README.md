# 🚗 Driver Drowsiness Detection (Eyes Closed + Yawning + Head Tilt)

This project detects driver drowsiness in real time using a webcam.
It monitors three key behaviors:

Eyes closed → detects drowsiness

Yawning → detects fatigue

Head tilt → detects inattentiveness

When any condition is triggered, the system raises an alarm sound.

# ✨ Features

Uses MediaPipe Face Mesh (468 landmarks) for face detection.

Computes:

Eye Aspect Ratio (EAR) → detects eye closure

Mouth Aspect Ratio (MAR) → detects yawning

Head Tilt Angle → detects unsafe head posture

Plays a looping alarm until driver corrects behavior.

Works with any webcam.

# 📐 Formulas

1. 👁️ Eye Aspect Ratio (EAR)
   
   EAR = ( |p2 - p6| + |p3 - p5| ) / ( 2 * |p1 - p4| )
   
   p1, p4 = horizontal eye corners
   
   p2, p3 = upper eyelid points
   
   p5, p6 = lower eyelid points
   

3. 👄 Mouth Aspect Ratio (MAR)
   
   MAR = |ptop - pbottom| / |pleft - pright|
   
   ptop = top lip center
   
   pbottom = bottom lip center
   
   pleft, pright = left and right mouth corners
   

3. 🤕 Head Tilt Angle (θ)
   
   θ = arctan( (y_right - y_left) / (x_right - x_left) ) * (180 / π)
   
   (x_left, y_left) = left ear landmark
   
   (x_right, y_right) = right ear landmark
   

# Steps to run

Clone repo

Create virtual env (optional)

pip install -r requirements.txt

Run alarm.py (only once) to generate alarm

Run driver.py for full detection
