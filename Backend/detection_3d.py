import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--img_list", type=str, default='./foreground_black',
                        help='specify name of the template input image')
    parser.add_argument("--background_list", type=str, default='./images_black',
                        help='specify name of the template input image')
    parser.add_argument("--target_img_name", type=str, default='./IMG_0399.jpg',
                        help='specify name of the target input image')
    parser.add_argument("--target_empty_name", type=str, default='./tiles_empty_large.jpg',
                        help='specify name of the target input image')
    args = parser.parse_args()

    img_list = os.listdir(args.img_list)
    background_list = os.listdir(args.background_list)

    standard_W = 738
    standard_H = 612

    region_size = int((standard_W / 6 + standard_H / 5)/2)

    blur_kernel_size = 15

    sift = cv2.SIFT_create()
    target_color = cv2.imread(args.target_img_name)
    target_color = cv2.resize(target_color, (standard_W, standard_H))
    target_blur = cv2.GaussianBlur(target_color, (blur_kernel_size, blur_kernel_size), cv2.BORDER_DEFAULT)
    H, W, _ = target_color.shape
    target_img = cv2.cvtColor(target_color, cv2.COLOR_BGR2GRAY)

    target_empty_color = cv2.imread(args.target_empty_name)
    target_empty_color = cv2.resize(target_empty_color, (standard_W, standard_H))
    target_empty_blur = cv2.GaussianBlur(target_empty_color, (blur_kernel_size, blur_kernel_size), cv2.BORDER_DEFAULT)
    difference_target = np.mean(np.abs(target_blur / 255. - target_empty_blur / 255.), axis=2)

    difference_threshold = 0.2
    matching_threshold = 1.65

    mask = np.where(difference_target > difference_threshold, 255, 0)
    cv2.imwrite("mask.png", mask)
    mask = mask/255.
    kp_target, des_target = sift.detectAndCompute(target_img, None)

    match_list = []
    hist_vector = np.zeros((3, 256))
    for c in range(3):
        hist_list = []
        for i in range(len(img_list)):
            template_color = cv2.imread(os.path.join(args.img_list, img_list[i]))
            hist_foreground, bins = np.histogram(template_color[:, :, c].ravel(), 256, [0, 256])
            hist_foreground = hist_foreground / np.linalg.norm(hist_foreground)
            template_color_full = cv2.imread(os.path.join(args.background_list, background_list[i]))
            hist_background, bins = np.histogram(template_color_full[:, :, c].ravel(), 256, [0, 256])
            hist_background = hist_background / np.linalg.norm(hist_background)
            hist = np.clip(hist_foreground - hist_background, 0, None)
            hist = hist / np.linalg.norm(hist)
#            plt.plot(hist)
#            plt.show()
            hist_list.append(hist)
        hist_array = np.array(hist_list)
        hist_array_mean = np.mean(hist_array, axis=0)
        hist_array_mean = hist_array_mean / np.linalg.norm(hist_array_mean)
        hist_vector[c] = hist_array_mean

    background_target_vector = np.zeros((3, 256))
    for c in range(3):
        hist_target, bins = np.histogram(target_color[:, :, c].ravel(), 256, [0, 256])
        hist_target = hist_target / np.linalg.norm(hist_target)
        background_target_vector[c] = hist_target

    difference_list = []
    detected_list = []
    valid_ratio = 0.1
    patch_size = 50
    target_color_padded = np.zeros((H+patch_size*2, W+patch_size*2, 3))
    mask_padded = np.zeros((H+patch_size*2, W+patch_size*2))
    target_color_padded[patch_size:-patch_size, patch_size:-patch_size] = target_color
    mask_padded[patch_size:-patch_size, patch_size:-patch_size] = mask

    i_list = [patch_size + region_size, patch_size+region_size*2, patch_size+region_size*3, patch_size+region_size*4, patch_size+region_size*5]
    j_list = [patch_size + region_size, patch_size + region_size * 2, patch_size + region_size * 3, patch_size + region_size * 4, patch_size + region_size * 5, patch_size + region_size * 6]
    for i in i_list:
        for j in j_list:
            print(patch_size, region_size)
            mask_patch = mask_padded[i-patch_size:i, j-patch_size:j]
            if np.sum(mask_patch) < patch_size*patch_size*valid_ratio:
                continue
            patch_vector = np.zeros((3, 256))
            for c in range(3):
                patch = target_color_padded[i-patch_size:i, j-patch_size:j] * np.expand_dims(mask_patch, axis=2)
                hist_patch, bins = np.histogram(patch[:, :, c].ravel(), 256, [0, 256])
                hist_patch[0] = 0
                hist_patch = hist_patch / np.linalg.norm(hist_patch)
                patch_vector[c] = hist_patch

            difference = np.linalg.norm(hist_vector - patch_vector)
            difference_list.append(difference)
            if difference < matching_threshold:
                detected_list.append([i-patch_size-region_size/2, j-patch_size-region_size/2])
                print(i-patch_size, j-patch_size, difference)

    difference_list = np.array(difference_list)
    print(np.sort(difference_list))
    detected_list = np.array(detected_list)
#    print(detected_list)
    plt.plot(detected_list[:, 1], detected_list[:, 0], 'r*', label='centroids')
    plt.axis('equal')
    plt.legend(shadow=True)
#
    index = [2, 1, 0]
    plt.imshow(target_color[:, :, index])
    plt.show()
