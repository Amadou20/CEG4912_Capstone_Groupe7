import cv2
import numpy as np
import matix_and_motors as utils_functions
from functions import create_output

# Camera parameters to undistort and rectify images
cv_file = cv2.FileStorage()
cv_file.open('stereoMap.xml', cv2.FileStorage_READ)
stereoMapL_x = cv_file.getNode('stereoMapR_x').mat()
stereoMapL_y = cv_file.getNode('stereoMapR_y').mat()
stereoMapR_x = cv_file.getNode('stereoMapL_x').mat()
stereoMapR_y = cv_file.getNode('stereoMapL_y').mat()
Q_matrix = cv_file.getNode('Q').mat()

# Open both cameras
cap_left = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap_right = cv2.VideoCapture(0, cv2.CAP_DSHOW)


def mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        if d_values[y, x] > 0:
            depth = (4.1 * 7) / d_values[x, y]
            print("Disparity: %r" % disparity_image[x, y])


cv2.namedWindow('disparity-filtered', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('disparity-filtered', mouse_click)


def disparity_map(imgL, imgR):
    window_size = 5
    minDisparity = 2
    numDisparity = 130 - minDisparity
    left_matcher = cv2.StereoSGBM_create(
        minDisparity=minDisparity,
        numDisparities=numDisparity,
        blockSize=window_size,
        P1=8 * 3 * window_size,
        P2=32 * 3 * window_size,
        disp12MaxDiff=12,
        uniquenessRatio=10,
        speckleWindowSize=50,
        speckleRange=32,
        preFilterCap=63,
        mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY
    )

    right_matcher = cv2.ximgproc.createRightMatcher(left_matcher)

    # FILTER Parameters
    lmbda = 80000
    sigma = 1.8

    wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=left_matcher)
    wls_filter.setLambda(lmbda)

    wls_filter.setSigmaColor(sigma)
    disp_left = left_matcher.compute(imgL, imgR)
    disp_right = right_matcher.compute(imgR, imgL)
    disp_left = np.int16(disp_left)
    disp_right = np.int16(disp_right)
    filteredImg = wls_filter.filter(disp_left, imgL, None, disp_right)  # important to put "imgL" here!!!

    filteredImg = cv2.normalize(src=filteredImg, dst=filteredImg, beta=0, alpha=255,
                                norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    filteredImg = np.uint8(filteredImg)

    disparity = disp_left

    disparity_value = ((disparity.astype(np.float32) / 16) - minDisparity) / numDisparity

    disparity = cv2.normalize(src=disparity, dst=disparity, beta=0, alpha=255,
                              norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    return filteredImg, disparity, disparity_value


while True:
    success_right, frame_right = cap_right.read()
    success_left, frame_left = cap_left.read()

    frame_right = cv2.remap(frame_right, stereoMapR_x, stereoMapR_y, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT, 0)
    frame_left = cv2.remap(frame_left, stereoMapL_x, stereoMapL_y, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT, 0)

    # Show the frames
    gray_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2GRAY)
    gray_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2GRAY)

    filtered_image, disparity_image, d_values = disparity_map(gray_left, gray_right)
    colored_image = cv2.applyColorMap(filtered_image, cv2.COLORMAP_JET)

    points_3D = cv2.reprojectImageTo3D(disparity=disparity_image, Q=Q_matrix, handleMissingValues=True)
    mask_map = disparity_image > disparity_image.min()

    output_points = points_3D[mask_map]
    output_colors = gray_left[mask_map]

    alert = utils_functions.get_depth_estimation(disparity_image)
    cv2.putText(frame_left, str(alert[0]), (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame_left, str(alert[1]), (300, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame_left, str(alert[2]), (600, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("frame left", frame_left)
    cv2.imshow("frame right", frame_right)
    cv2.imshow("disparity", disparity_image)
    cv2.imshow("disparity-filtered", filtered_image)
    cv2.imshow("disparity-colored", colored_image)
    # cv2.imshow("re-projection", output_points)

    # Hit "q" to close the window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # output_file = 'pointCloudDeepLearning.ply'
        # create_output(output_points, output_colors, output_file)
        break

# Release and destroy all windows before termination
cap_right.release()
cap_left.release()
cv2.destroyAllWindows()
