import cv2

datadir = 'resources/'
FISH = (cv2.cvtColor(cv2.imread(datadir + 'merchandise/fish.jpg'), cv2.COLOR_BGR2GRAY), "fish")
GOLD = (cv2.cvtColor(cv2.imread(datadir + 'merchandise/gold.jpg'), cv2.COLOR_BGR2GRAY), "gold")
IVORY = (cv2.cvtColor(cv2.imread(datadir + 'merchandise/ivory.jpg'), cv2.COLOR_BGR2GRAY), "ivory")
JEWEL = (cv2.cvtColor(cv2.imread(datadir + 'merchandise/jewel.jpg'), cv2.COLOR_BGR2GRAY), "jewel")
PAPYRUS = (cv2.cvtColor(cv2.imread(datadir + 'merchandise/papyrus.jpg'), cv2.COLOR_BGR2GRAY), "papyrus")
POTTERY = (cv2.cvtColor(cv2.imread(datadir + 'merchandise/pottery.jpg'), cv2.COLOR_BGR2GRAY), "pottery")
SILK = (cv2.cvtColor(cv2.imread(datadir + 'merchandise/silk.jpg'), cv2.COLOR_BGR2GRAY), "silk")
SPICE = (cv2.cvtColor(cv2.imread(datadir + 'merchandise/spice.jpg'), cv2.COLOR_BGR2GRAY), "spice")
WHEAT = (cv2.cvtColor(cv2.imread(datadir + 'merchandise/wheat.jpg'), cv2.COLOR_BGR2GRAY), "wheat")

ALL_MERCHANDISE = [FISH, GOLD, IVORY, JEWEL, PAPYRUS, POTTERY, SILK, SPICE, WHEAT]

TEST_TARGET = cv2.cvtColor(cv2.imread(datadir + 'result_img.jpg'), cv2.COLOR_BGR2GRAY)