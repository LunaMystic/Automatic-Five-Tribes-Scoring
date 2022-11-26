import cv2
import resources
from score_utils import ScoreSheet
from matching import multiple_match
from match_cards import calculate_merchandise_match_centroids


def score(image_stream):
    img_cv = cv2.cvtColor(cv2.imdecode(image_stream, cv2.IMREAD_COLOR), cv2.COLOR_BGR2GRAY)
    score_sheet = ScoreSheet("yellow")
    score = score_helper(score_sheet, img_cv)
    return score


def score_helper(sheet, image):
    # Very boring detection of various merchandise
    for item in resources.ALL_MERCHANDISE:
        current_merc = len(calculate_merchandise_match_centroids(item[0], image))
        if current_merc:
            sheet.merManager.inventory[item[1]] = current_merc
            print("Detecting ", current_merc, " ", item[1], " in Image")
    score = sheet.merManager.calculateScore()
    print("Total Score is: ", score)
    return score

if __name__ == "__main__":
    score_helper(ScoreSheet("yellow"), resources.TEST_TARGET)
