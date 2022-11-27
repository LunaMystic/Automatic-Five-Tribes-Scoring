import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse


def merge(component_dic, merge_list):
    new_idx_mapping = {}
    cnt_new_mapping = 0
    new_idx_mapping[cnt_new_mapping] = [0]
    cnt_new_mapping += 1
    for i in range(1, len(component_dic)):
        merged = False
        for j in range(len(merge_list)):
            if merge_list[j][1] == i:
                for k in range(0, i):
                    if merge_list[j][0] in new_idx_mapping[k] and i not in new_idx_mapping[k]:
                        new_idx_mapping[k].append(i)
                        merged = True
                        break

        if merged == False:
            new_idx_mapping[cnt_new_mapping] = [i]
            cnt_new_mapping += 1

    new_dic = {}
    for i in range(len(new_idx_mapping)):
        new_dic[i] = []
        for j in range(len(new_idx_mapping[i])):
            new_dic[i].extend(component_dic[new_idx_mapping[i][j]])

    return new_dic


def find_connected_components(grid_list):
    list_len = grid_list.shape[0]
    component_dic = {}
    dic_count = 0
    for i in range(list_len):
        find = False
        for j in range(dic_count):
            selected_component = component_dic[j]
            difference = selected_component - grid_list[i]
            if np.any(np.sum(np.abs(difference), axis=1) < 2) and not find:
                selected_component.append(grid_list[i])
                find = True
                continue

        if not find:
            component_dic[dic_count] = [grid_list[i]]
            dic_count += 1

    num_dic_1st = len(component_dic)
    merge_list = []
    for i in range(num_dic_1st):
        curr_list = component_dic[i]
        for elem in curr_list:
            for j in range(i + 1, num_dic_1st):
                difference = component_dic[j] - elem
                if np.any(np.sum(np.abs(difference), axis=1) < 2) and (i, j) not in merge_list:
                    merge_list.append((i, j))

    final_dic = merge(component_dic, merge_list)

    return final_dic, merge_list

def merc_multiple_match(template_img, target_img, 
    grid_size=100, voting_threshold=2, cluster_threshold=3):
    """
    " Calculate centroids of all matches merchandises 
    " arg template_color:
    """
    H, W = target_img.shape

    sift = cv2.SIFT_create()
    _, des_template = sift.detectAndCompute(template_img, None)
    kp_target, des_target = sift.detectAndCompute(target_img, None)

    bf_matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

    matches = bf_matcher.match(des_template, des_target)

    matches = sorted(matches, key=lambda x: x.distance)

    trainIdx_list = []
    col_grid = W // grid_size + 1
    row_grid = H // grid_size + 1
    voting_grid = np.zeros((col_grid, row_grid))

    for match in matches:
        trainIdx_list.append([kp_target[match.trainIdx].pt[0], kp_target[match.trainIdx].pt[1]])
        voting_grid[int(kp_target[match.trainIdx].pt[0] // grid_size)][
            int(kp_target[match.trainIdx].pt[1] // grid_size)] += 1

    sorted_kp = np.argsort(voting_grid, axis=None)
    voting_above_threshold = np.argwhere(voting_grid >= voting_threshold)
    kp_dic, merge_list = find_connected_components(voting_above_threshold)

    detected_list = []

    for i in range(len(kp_dic)):
        if len(kp_dic[i]) < cluster_threshold:
            continue
        clustered_pts = kp_dic[i]
        cluster_center = np.mean(clustered_pts, axis=0)
        detected_list.append(cluster_center)

    detected_list = np.array(detected_list) + 0.5

    return detected_list
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--template_img_name", type=str, default='./resources/merchandise/ivory.jpg',
                        help='specify name of the template input image')
    parser.add_argument("--target_img_name", type=str, default='./resources/result_mod.jpg',
                        help='specify name of the target input image')
    parser.add_argument("--voting_threshold", type=int, default=2,
                        help='threshold for a valid voting grid')
    parser.add_argument("--cluster_threshold", type=int, default=3,
                        help='threshold for the number of elements in a cluster for final detection')
    parser.add_argument("--grid_size", type=int, default=100,
                        help='size of voting grids')
    args = parser.parse_args()

    template_color = cv2.imread(args.template_img_name)
    target_color = cv2.imread(args.target_img_name)

    template_img = cv2.cvtColor(template_color, cv2.COLOR_BGR2GRAY)
    target_img = cv2.cvtColor(target_color, cv2.COLOR_BGR2GRAY)

    detected_list = merc_multiple_match(template_img, target_img)

    print("Final List: ")
    print(detected_list)

    plt.plot(detected_list[:, 0] * args.grid_size, detected_list[:, 1] * args.grid_size, 'r*', label='centroids')
    plt.axis('equal')
    plt.legend(shadow=True)

    plt.imshow(cv2.cvtColor(target_color, cv2.COLOR_BGR2RGB))
    plt.show()