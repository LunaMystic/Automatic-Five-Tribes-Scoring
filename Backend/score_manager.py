import cv2
import resources
from score_utils import ScoreSheet
from matching import multiple_match


def score(image_stream):
    img_cv = cv2.imdecode(image_stream, cv2.IMREAD_COLOR)
    score_sheet = ScoreSheet("yellow")
    score = score_helper(score_sheet, img_cv)
    return score


def score_helper(sheet, image):
    # Very boring detection of various merchandise
    for item in resources.ALL_MERCHANDISE:
        current_merc = len(multiple_match(item[0], image))
        if current_merc:
            sheet.merManager.inventory[item[1]] = current_merc
            print("Detecting ", current_merc, " ", item[1], " in Image")
    score = sheet.merManager.calculateScore()
    return score

if __name__ == "__main__":
    score_helper(ScoreSheet("yellow"), resources.TEST_TARGET)
