import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def match_helper(template, image, threshold):
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    (yCoords, xCoords) = np.where(result >= threshold)
    return zip(xCoords, yCoords)


# We will implement non-maximum suppression in future
def remove_duplicate(coords_zip, threshold):
    coords_dict = set()
    for (x, y) in coords_zip:
        flag = True
        for (cx, cy) in coords_dict:
            if np.linalg.norm(np.array((x, y)) - np.array((cx, cy))) < threshold:
                flag = False
        if flag:
            coords_dict.add((x, y))
    return coords_dict


def multiple_match(template, image):
    return remove_duplicate(match_helper(template, image, 0.7), template.shape[0] / 2)


if __name__ == "__main__":
    datadir = 'resources/'
    target = cv2.cvtColor(cv2.imread(datadir + 'result_img.jpg'), cv2.COLOR_BGR2GRAY)
    source = cv2.cvtColor(cv2.imread(datadir + 'merchandise/spice.jpg'), cv2.COLOR_BGR2GRAY)

    res = multiple_match(source, target)
    # Visualization
    fig, ax = plt.subplots()

    ax.imshow(target, cmap='gray')
    for (x, y) in res:
        rect = patches.Rectangle((x, y), source.shape[1], source.shape[0], linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

    plt.show()
    print(len(res))
