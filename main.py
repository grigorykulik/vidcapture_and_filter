import cv2
import numpy as np
import sys

cap=cv2.VideoCapture(0);
if (cap.isOpened())==False:
    print("Error opening video stream")

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))

def apply_invert(frame):
    return cv2.bitwise_not(frame)

def verify_alpha_channel(frame):
    try:
        frame.shape[3]
    except IndexError:
        frame=cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    return frame

def apply_color(frame, intensity):
    frame=verify_alpha_channel(frame)
    frame_h, frame_w, frame_c=frame.shape
    blue=0
    green=0
    red=200
    color_bgra=(blue, green, red, 1)
    overlay=np.full((frame_h, frame_w, 4), color_bgra, dtype="uint8")
    cv2.addWeighted(overlay, intensity, frame, 1.0, 0, frame)
    frame=cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    return frame

def apply_sepia(frame, intensity):
    frame=verify_alpha_channel(frame)
    frame_h, frame_w, frame_c=frame.shape
    blue=20
    green=66
    red=112
    sepia_bgra=(blue, green, red, 1)
    overlay=np.full((frame_h, frame_w, 4), sepia_bgra, dtype="uint8")
    cv2.addWeighted(overlay, intensity, frame, 1.0, 0, frame)
    frame=cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    return frame

def alpha_blend(frame_1, frame_2, mask):
    alpha=mask/255.0
    blended=cv2.convertScaleAbs(frame_1*(1-alpha)+frame_2*alpha)
    return blended

def apply_circle_focus_blur(frame, intensity):
    frame=verify_alpha_channel(frame)
    frame_h, frame_w, frame_c=frame.shape
    y=int(frame_h/2)
    x=int(frame_w/2)
    radius=int(y/2)
    center=(x,y)

    mask=np.zeros((frame_h, frame_w, 4), dtype="uint8")
    cv2.circle(mask, center, radius, (255, 255, 255), -1, cv2.LINE_AA)
    blurred=cv2.GaussianBlur(frame, (21, 21), 11)
    blended=alpha_blend(frame, blurred, 255-mask)
    frame=cv2.cvtColor(blended, cv2.COLOR_BGRA2BGR)
    return frame

intensity=0.0

while (True):
    ret, frame=cap.read()

    if cv2.waitKey(25)&0xFF==ord('h'):
        intensity+=.1
    elif cv2.waitKey(25)&0xFF==ord('l'):
        intensity-=.1

    if sys.argv[1]=="--invert":
        rendered_image=apply_invert(frame)
    elif sys.argv[1]=="--sepia":
        rendered_image=apply_sepia(frame, intensity)
    elif sys.argv[1]=="--reddish":
        rendered_image=apply_color(frame, intensity)
    elif sys.argv[1]=="--blur":
        rendered_image=apply_circle_focus_blur(frame, intensity)

    if ret==True:

        out.write(rendered_image)
        cv2.imshow("Frame", rendered_image)
        if cv2.waitKey(25)&0xFF==ord('q'):
            break

    else:
        break

cap.release()
out.release()

cv2.destroyAllWindows()