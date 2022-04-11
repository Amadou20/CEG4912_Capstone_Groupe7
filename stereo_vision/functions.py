import cv2
import imutils
import numpy as np


def find_depth(right_point, left_point, frame_right, frame_left, baseline, f, alpha):
    # CONVERT FOCAL LENGTH f FROM [mm] TO [pixel]:

    f_pixel = None
    height_right, width_right, depth_right = frame_right.shape
    height_left, width_left, depth_left = frame_left.shape

    if width_right == width_left:
        f_pixel = (width_right * 0.5) / np.tan(alpha * 0.5 * np.pi / 180)

    else:
        print('Left and right camera frames do not have the same pixel width')

    x_right = right_point[0]
    x_left = left_point[0]

    # CALCULATE THE DISPARITY:
    disparity = x_left - x_right  # Displacement between left and right frames [pixels]

    # CALCULATE DEPTH z:
    zDepth = (baseline * f_pixel) / disparity  # Depth in [cm]

    return zDepth


def find_circles(frame, mask):
    contours = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    center = None

    # Only proceed if at least one contour was found
    if len(contours) > 0:
        # Find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)  # Finds center point
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # Only proceed if the radius is greater than a minimum value
        if radius > 10:
            # Draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 0), -1)

    return center


def add_HSV_filter(frame, camera):
    # Blurring the frame
    blur = cv2.GaussianBlur(frame, (5, 5), 0)

    # Converting RGB to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    l_b_r = np.array([60, 110, 50])  # Lower limit for red ball
    u_b_r = np.array([255, 255, 255])  # Upper limit for red ball
    l_b_l = np.array([143, 110, 50])  # Lower limit for red ball
    u_b_l = np.array([255, 255, 255])  # Upper limit for red ball

    # l_b = np.array([140, 106, 0])        # LOWER LIMIT FOR BLUE COLOR!!!
    # u_b = np.array([255, 255, 255])

    # HSV-filter mask
    # mask = cv2.inRange(hsv, l_b_l, u_b_l)

    if camera == 1:
        mask = cv2.inRange(hsv, l_b_r, u_b_r)
    else:
        mask = cv2.inRange(hsv, l_b_l, u_b_l)

    # Morphological Operation - Opening - Erode followed by Dilate - Remove noise
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    return mask


def create_output(vertices, colors, filename):
    vert = vertices.reshape(-1, 3)
    col = colors.reshape(-1, 3)
    vert = np.hstack([vert, col])

    with open(filename, 'w') as f:
        np.savetxt(f, vert, '%f %f %f %d %d %d')



