import numpy as np
import cv
import cv2
import argparse
import os

# from matplotlib import pyplot as plt
from PIL import Image
from operator import itemgetter
from scipy.spatial import KDTree

"""

"""

def cliArguments():
	ap = argparse.ArgumentParser()
	ap.add_argument("--images")

	return vars(ap.parse_args())

def auto_canny(image, sigma=0.33):
	v = np.median(image)

	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)

	return edged

def processImage(imagePath):
	orignalImage = cv2.imread(imagePath, cv2.CV_LOAD_IMAGE_COLOR)

	grayImage = cv2.cvtColor(orignalImage, cv2.COLOR_BGR2GRAY)

	blurredImage = cv2.GaussianBlur(grayImage, (3, 3), 0)

	edgedCorrectedImage = auto_canny(blurredImage)

	# ret,thresh = cv2.threshold(blurredImage,8,255,cv2.THRESH_BINARY)
	# thresh=cv2.inRange(grayImage,190,255);
	# contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	# croppedImage = removeWhiteSpace(edgedCorrectedImage, thresh, contours, hierarchy)

	# removeText(edgedCorrectedImage)

	ret,thresh = cv2.threshold(grayImage,127,255,cv2.THRESH_BINARY_INV)
	# contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	# cv2.drawContours(image, contours, -1, (0,255,0), 1)
	# print croppedImage

	newFile = open('data','w')

	fast = cv2.FastFeatureDetector(120)
	kp = fast.detect(grayImage,None)

	counter = 0

	i = 0
	kpArray = []

	for keyPoints in kp:
		kpArray.append(keyPoints.pt)

	kpArray = sorted(kpArray,key=itemgetter(0))

	prunedKpArray = pruningArray(kpArray)

	for ele in prunedKpArray:
		newFile.write('a'+str(i)+'=model.floorplan.newCorner('+str(ele[0])+','+str(ele[1])+');\n')
		counter+=1
		i+=1
		if counter%2 is 0 :
			i = 0
			newFile.write('model.floorplan.newWall(a0,a1);\n')
	# for keyPoints in kpArray:
	# 	newFile.write('a'+str(i)+'=model.floorplan.newCorner'+str(keyPoints.pt)+';\n')
	# 	counter+=1
	# 	i+=1
	# 	if counter%2 is 0 :
	# 		i = 0
	# 		newFile.write('model.floorplan.newWall(a0,a1);\n')



	newFile.close()
	# i = cv2.drawKeypoints(grayImage, prunedKpArray, color=(0,0,255))
	# cv2.imshow("Show",i)
	# cv2.waitKey(0)

def pruningArray(points) :
	print len(points)
	valid = []

	threshold = 100

	for v in points:
		x = v[0]
		y = v[1]

		tmpArray = [tmp for tmp in points if (x == tmp[0])]
		for tA in tmpArray:
			newX = tA[0]
			newY = tA[1]

			if (y + threshold < newY or y - threshold > newY):
				valid.append(tA)

			if y == newY and (x + threshold < newX or x - threshold > newX):
				valid.append(tA)

	print len(valid)
	return valid

def removeWhiteSpace(image, thresh=0, contours=0, hierarchy=0):
	# cnt = contours[0]
	# x,y,w,h = cv2.boundingRect(cnt)
	# crop = image[y:y+h,x:x+w]
	# cv2.drawContours(image, contours, -1, (0,255,0), 1)
	# cv2.imshow("Show",image)
	# cv2.waitKey(0)
	return image

def removeText(image):
	cv2.imshow("Show", image)
	cv2.waitKey(0)

if __name__ == "__main__":
	args = cliArguments()
	processImage(args['images'])
	cv2.destroyAllWindows()

