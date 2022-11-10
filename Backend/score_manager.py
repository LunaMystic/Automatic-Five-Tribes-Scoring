import cv2
import resources
from matching import multiple_match

def score(image_stream):
    img_cv = cv2.imdecode(image_stream, cv2.IMREAD_COLOR)
    return img_cv.shape

if __name__ == "__main__":
    print(len(multiple_match(resources.SPICE[0], resources.TEST_RESULT)))
    dict = {"m":1, "k":2}
    dict = {k: v-1 for k, v in dict.items() if v-1}
    print(dict)