import cv2

right = cv2.VideoCapture(0, cv2.CAP_DSHOW)
left = cv2.VideoCapture(1, cv2.CAP_DSHOW)
num = 0

while True:

    res_left, left_cam = left.read()
    res_right, right_cam = right.read()

    k = cv2.waitKey(5)

    if k == 27:
        break
    elif k == ord('s'):  # wait for 's' key to save and exit
        leftStatus = cv2.imwrite('./images/stereoLeft/imageL' + str(num) + '.png', left_cam)
        rightStatus = cv2.imwrite('./images/stereoRight/imageR' + str(num) + '.png', right_cam)
        if leftStatus and rightStatus:
            print("images saved")

        num += 1

    cv2.imshow('left', left_cam)
    cv2.imshow('right', right_cam)

# Release and destroy all windows before termination
left.release()
right.release()

cv2.destroyAllWindows()
