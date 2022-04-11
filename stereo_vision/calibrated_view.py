import numpy as np
import cv2
import epipolar_lines as epipolar

# Camera parameters to undistort and rectify images
cv_file = cv2.FileStorage()
cv_file.open('stereoMap.xml', cv2.FileStorage_READ)

stereoMapL_x = cv_file.getNode('stereoMapR_x').mat()
stereoMapL_y = cv_file.getNode('stereoMapR_y').mat()
stereoMapR_x = cv_file.getNode('stereoMapL_x').mat()
stereoMapR_y = cv_file.getNode('stereoMapL_y').mat()

# Open both cameras
cap_left = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap_right = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:

    success_right, frame_right = cap_right.read()
    success_left, frame_left = cap_left.read()

    # Undistort and rectify images
    frame_right_r = cv2.remap(frame_right, stereoMapR_x, stereoMapR_y, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT, 0)
    frame_left_r = cv2.remap(frame_left, stereoMapL_x, stereoMapL_y, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT, 0)

    gray_right = cv2.cvtColor(frame_right_r, cv2.COLOR_BGR2GRAY)
    gray_left = cv2.cvtColor(frame_left_r, cv2.COLOR_BGR2GRAY)

    # Show the frames
    cv2.imshow("frame right", frame_right)
    cv2.imshow("frame left", frame_left)
    cv2.imshow("frame left-rectified", frame_left_r)
    cv2.imshow("frame right-rectified", frame_right_r)

    # Hit "q" to close the window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        status1 = cv2.imwrite('./rectified-images-samples/left.png', frame_left_r)
        status2 = cv2.imwrite('./rectified-images-samples/right.png', frame_right_r)
        epipolar.show_plot()
        break

# Release and destroy all windows before termination
cap_right.release()
cap_left.release()

cv2.destroyAllWindows()
