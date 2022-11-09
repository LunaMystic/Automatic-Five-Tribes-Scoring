import cv2

def score(image_stream):
    img_cv = cv2.imdecode(image_stream, cv2.IMREAD_COLOR)
    return img_cv.shape

if __name__ == "__main__":
    print("Scoring manager")