#!/usr/bin/env python3

# Program to run the webcam and do fun things with it.
#

import cv2
import time

from win32api import GetSystemMetrics

screen_size = screen_width, screen_height = GetSystemMetrics(0), GetSystemMetrics(1)
print(f"Screen Size: {screen_size}")

screen_aspect = float(screen_width) / screen_height
print(f"Screen aspect is {screen_aspect}")

target_size = target_width, target_height = int(screen_width * 0.9), int(
    screen_height * 0.9
)

cam_index = MAX_CAM = 1

exit_key_detected = False
while not exit_key_detected:
    cam_index = cam_index + 1 if cam_index < MAX_CAM else 0
    print(f"Opening {cam_index=}")
    start = time.time()
    cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
    stop = time.time()
    print(f"Open time is {stop-start=}")
    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError(f"Error opening cam: {cam_index}")

    image_size = image_width, image_height = int(cap.get(3)), int(cap.get(4))

    print(f"Capture Size: {image_size}")

    capture_aspect = float(image_width) / image_height

    print(f"Capture aspect is {capture_aspect}")

    if capture_aspect > screen_aspect:
        new_size = (target_width, int(target_height * capture_aspect))
    else:
        new_size = (int(target_width / capture_aspect), target_height)

    print(f"New size: {new_size}")

    # crop_left, crop_right, crop_top, crop_bottom = .3, .3, .2, .1
    # crop_aspect = float(1-crop_left-crop_right)/(1-crop_top-crop_bottom)

    while True:
        ret, frame = cap.read()

        if False:  # we'll crop the frame when we correct the aspect
            # crop the frame.  Note, width and height are reversed
            frame = frame[
                int(crop_top * image_height) : image_height
                - int(crop_bottom * image_height),
                int(crop_left * image_width) : image_width
                - int(crop_right * image_width),
            ]

        # frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        frame = cv2.resize(frame, new_size, interpolation=cv2.INTER_AREA)
        frame = cv2.flip(frame, 1)
        cv2.imshow("Press <esc> to exit.", frame)

        c = cv2.waitKey(1)
        if c < 0:
            continue
        print(f"{c=}")
        if c == 27:
            exit_key_detected = True
            break
        elif chr(c) in ["n", "N"]:
            break
        time.sleep(1)

    cap.release()
    cv2.destroyAllWindows()
