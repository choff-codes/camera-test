import cv2
import numpy

#Establish the images hash to store all photos
images = {}
img = cv2.imread('test-frame.png',0)
color_img = cv2.imread('test-frame.png')

#Import and store all the photos in a hash
for x in range(1, 16):
    images[x] = cv2.imread('Camera-images/photo-%d.png' % x,0)

accum = cv2.addWeighted(img,0.5,images[1],0.5,0)

#Average all photo values into one solid photo
for k in images.keys():
    accum = cv2.addWeighted(accum,0.5,images[k],0.5,0)

blurred_img = cv2.medianBlur(accum,101)

#Evaluate the average color and determine the margin to use
average_color_per_row = numpy.average(img, axis=0)
average_color = numpy.average(average_color_per_row, axis=0)
margin = (average_color * .1)
margin = int(round(margin))

#Change pixel color to black or white if it is darker than 10%
for i in xrange(accum.shape[0]):
    for j in xrange(accum.shape[1]):
        if int(blurred_img[i,j]) - int(accum[i,j]) > margin:
            accum[i,j] = 0
        else:
            accum[i,j] = 255

#Total the number of black pixels
num_black = (1600 * 1200) - cv2.countNonZero(accum)

#Invert the image and find the contours
inv_accum = cv2.bitwise_not(accum)
npaContours, npaHierarchy = cv2.findContours(inv_accum,
                                             cv2.RETR_EXTERNAL,
                                             cv2.CHAIN_APPROX_NONE)

#Iterate over the contours to draw rectangles on original image
for npaContour in npaContours:
    if cv2.contourArea(npaContour) >= 0:
        [intX, intY, intW, intH] = cv2.boundingRect(npaContour)
#If a contour diameter is larger than 11 the camera inherently fails
#Find the bigger value here and add it to a constant variable
#Then test that variable at the end to determine failure
        if intW > 11 or intH > 11:
            print "CAMERA FAILURE"

        cv2.rectangle(color_img,
              (intX - 10, intY - 10),                 # upper left corner
              (intX+intW+10,intY+intH+10),            # lower right corner
              (0, 0, 255),                            # red
              2)                                      # thickness

#Outdated test - requires the implementation set out above
if num_black > 22:
    print "CAMERA FAILURE"
else:
    print "CAMERA PASSES"

#cv2.imwrite("new_average.png", avg_img)

cv2.imwrite("test-avg.png", accum)
cv2.imwrite("blurred_img.png", blurred_img)
cv2.imwrite("outputRect.png", color_img)

#cv2.imwrite("diff.png", diff_img)
