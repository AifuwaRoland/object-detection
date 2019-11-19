#Written by Roland Aifuwa
# import the necessary packages
import numpy as np
import cv2
import imutils
#in inches
KNOWN_DISTANCE = 7.8747
KNOWN_WIDTH = 4.9212

cap= cv2.VideoCapture(0)

def distance_to_camera(knownWidth, focalLength, perWidth):
	# compute and return the distance from the maker to the camera
	return (knownWidth * focalLength) / perWidth


while True:
	# load the image, convert it to grayscale, and blur it
	#image = cv2.imread("pic2.png")
	_, image = cap.read()
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	cv2.imshow("Gray", gray)
	#cv2.waitKey(0)

	# detect edges in the image
	edged = cv2.Canny(gray, 30, 100)

	cv2.imshow("Edged", edged)
	#cv2.waitKey(0)

	# construct and apply a closing kernel to 'close' gaps between 'white'
	# pixels
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
	closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
	cv2.imshow("Closed", closed)
	#cv2.waitKey(0)

	# find contours
	(cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	# loop over the contours
	for c in cnts:
		# approximate the contour

		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)

		# if the approximated contour has four points, then assume that the
		# contour is a rectangle --  and thus has four vertices
		if len(approx) == 4:
			screenCnt = approx
			cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 4)
			#calculate distance from camera
			#marker = image
			#focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH

			#nches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])
			# display the output
			#print ("I found {0} books in that image".format(total))
			cv2.imshow("Output", image)
			#cv2.putText(image, "%.2fcm" % (inches *12),
				#(image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
				#2.0, (0, 255, 0), 3)
			key= cv2.waitKey(1)
			if key ==27:
				break

				cap.release()
				cv2.destroyAllWindows()
