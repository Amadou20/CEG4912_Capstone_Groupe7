import numpy as np


def get_depth_estimation(depth_map):
    block_dimension = (int(depth_map.shape[0] / 1), int(depth_map.shape[1] / 3))
    alertness_level = [0] * (1 * 3)

    percentile_threshold = 80
    threshold_levels = [50, 125, 200]

    for col in range(3):
        for row in range(1):
            index = row * 1 + col
            block = depth_map[
                    row * block_dimension[0]: row * block_dimension[0] + block_dimension[0],
                    col * block_dimension[1]: col * block_dimension[1] + block_dimension[1],
                    ]

            block_thresh = np.percentile(block, percentile_threshold)

            if block_thresh > threshold_levels[2]:
                # print('Very close on the %r ' % get_side(index))
                alertness_level[index] = 3
            elif block_thresh > threshold_levels[1]:
                # print('A little close on the %r ' % get_side(index))
                alertness_level[index] = 2
            elif block_thresh > threshold_levels[0]:
                # print('Far away on the %r ' % get_side(index))
                alertness_level[index] = 1

    return alertness_level


def get_text(level):
    if level == 1 or level == 0:
        return 'Safe'
    elif level == 2:
        return 'Close'
    elif level == 2:
        return 'Very close'
