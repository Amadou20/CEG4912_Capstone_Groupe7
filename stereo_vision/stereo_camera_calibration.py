import cv2
import numpy as np
import cv2 as cv
import glob

############ FIND CHESSBOARD CORNERS - OBJECT POINTS AND IMAGE POINTS ##################

chessboardSize = (9, 6)
frameSize = (640, 480)

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboardSize[0], 0:chessboardSize[1]].T.reshape(-1, 2)

size_of_chessboard_squares_mm = 20
objp = objp * size_of_chessboard_squares_mm

# Arrays to store object points and image points from all the images.
objPoints = []  # 3d point in real world space
imgPointsL = []  # 2d points in image plane.
imgPointsR = []  # 2d points in image plane.

imagesLeft = sorted(glob.glob('./images/stereoLeft/*.png'))
imagesRight = sorted(glob.glob('./images/stereoRight/*.png'))

for imgLeft, imgRight in zip(imagesLeft, imagesRight):

    imgL = cv.imread(imgLeft)
    imgR = cv.imread(imgRight)
    # print(imgL.shape, imgR.shape)
    grayL = cv.cvtColor(imgL, cv.COLOR_BGR2GRAY)
    grayR = cv.cvtColor(imgR, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    retL, cornersL = cv.findChessboardCorners(grayL, chessboardSize,
                                              cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_FILTER_QUADS)
    retR, cornersR = cv.findChessboardCorners(grayR, chessboardSize,
                                              cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_FILTER_QUADS)

    # If found, add object points, image points (after refining them)
    if retL and retR == True:
        objPoints.append(objp)

        cornersL = cv.cornerSubPix(grayL, cornersL, (11, 11), (-1, -1), criteria)
        imgPointsL.append(cornersL)

        cornersR = cv.cornerSubPix(grayR, cornersR, (11, 11), (-1, -1), criteria)
        imgPointsR.append(cornersR)

        # Draw and display the corners
        cv.drawChessboardCorners(imgL, chessboardSize, cornersL, retL)
        cv.imshow('img left', imgL)
        cv.drawChessboardCorners(imgR, chessboardSize, cornersR, retR)
        cv.imshow('img right', imgR)
        cv.waitKey(1000)

cv.destroyAllWindows()

############## CALIBRATION #######################################################
# print(imgL.shape, imgR.shape)
retL, cameraMatrixL, distL, rvecsL, tvecsL = cv.calibrateCamera(objPoints, imgPointsL, frameSize, None, None)
heightL, widthL, channelsL = imgL.shape
newCameraMatrixL, roi_L = cv.getOptimalNewCameraMatrix(cameraMatrixL, distL, (widthL, heightL), 1, (widthL, heightL))

retR, cameraMatrixR, distR, rvecsR, tvecsR = cv.calibrateCamera(objPoints, imgPointsR, frameSize, None, None)
heightR, widthR, channelsR = imgR.shape
newCameraMatrixR, roi_R = cv.getOptimalNewCameraMatrix(cameraMatrixR, distR, (widthR, heightR), 1, (widthR, heightR))

########## Stereo Vision Calibration #############################################
flag = 0
# flags |= cv.CALIB_FIX_INTRINSIC
flag |= cv2.CALIB_USE_INTRINSIC_GUESS
# Here we fix the intrinsic camara matrixes so that only Rot, Trns, Emat and Fmat are calculated.
# Hence intrinsic parameters are the same

criteria_stereo = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# This step is performed to transformation between the two cameras and calculate Essential and Fundamenatl matrix
retStereo, newCameraMatrixL, distL, newCameraMatrixR, distR, rot, trans, essentialMatrix, fundamentalMatrix = cv.stereoCalibrate(
    objPoints, imgPointsL, imgPointsR, newCameraMatrixL, distL, newCameraMatrixR, distR, (widthL, heightL),
    criteria_stereo, flag)

########## Stereo Rectification #################################################
rectifyScale = 1
rectL, rectR, projMatrixL, projMatrixR, Q, roi_L, roi_R = cv.stereoRectify(newCameraMatrixL, distL, newCameraMatrixR,
                                                                           distR, (widthL, heightL), rot, trans,
                                                                           flags=cv2.CALIB_ZERO_DISPARITY, alpha=0.9)

stereoMapL_x, stereoMapL_y = cv.initUndistortRectifyMap(newCameraMatrixL, distL, rectL, projMatrixL,
                                                        (widthL, heightL), cv2.CV_32FC1)
stereoMapR_x, stereoMapR_y = cv.initUndistortRectifyMap(newCameraMatrixR, distR, rectR, projMatrixR,
                                                        (widthL, heightL), cv2.CV_32FC1)

print("Saving parameters!")
cv_file = cv.FileStorage('stereoMap.xml', cv.FILE_STORAGE_WRITE)

cv_file.write('stereoMapL_x', stereoMapL_x)
cv_file.write('stereoMapL_y', stereoMapL_y)
cv_file.write('stereoMapR_x', stereoMapR_x)
cv_file.write('stereoMapR_y', stereoMapR_y)
cv_file.write('Q', Q)

print(Q)

cv_file.release()
