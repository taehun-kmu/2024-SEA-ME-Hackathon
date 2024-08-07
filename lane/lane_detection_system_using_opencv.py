# -*- coding: utf-8 -*-


### Importing Libraries


import cv2
import matplotlib.pyplot as plt
import numpy as np

### Preprocessing Of Image"""

# Reading colored image.
img = cv2.imread("img.jpeg")

# Convert into gray scale
def gray(image):
  image = np.asarray(image)
  return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# Applying gaussian filter to smoothen the image
def gauss(image):
  return cv2.GaussianBlur(image, (5, 5), 0)

# Applying Canny-Edge detection to detect edges
def canny(image, p1, p2):
  edges = cv2.Canny(image, p1, p2)
  return edges

# Isolating the region where lanes are present
def region(image):
  height, width = image.shape
  triangle = np.array([
          [(100, height), (475, 325), (width, height)]
  ])

  mask = np.zeros_like(image)
  mask = cv2.fillPoly(mask, triangle, 255)
  mask = cv2.bitwise_and(image, mask)

  return mask

def make_points(image, average):
  print(average)

  slope, y_int = average
  y1 = image.shape[0]
  y2 = int(y1 * (3/5))
  x1 = int((y1 - y_int) // slope)
  x2 = int((y2 - y_int) // slope)

  return np.array([x1, y1, x2, y2])

# To optimize and displaying lines
def average(image, lines):
  left = []
  right = []

  for line in lines:
    print(line)

    x1, y1, x2, y2 = line.reshape(4)
    parameters = np.polyfit((x1, x2), (y1,y2), 1)

    slope = parameters[0]
    y_int = parameters[1]

    if slope < 0:
      left.append((slope, y_int))
    else:
      right.append((slope, y_int))

  right_avg = np.average(right, axis=0)
  left_avg = np.average(left, axis=0)
  left_line = make_points(image, left_avg)
  right_line = make_points(image, right_avg)

  return np.array([left_line, right_line])

def display_lines(image, lines):
  lines_image = np.zeros_like(image)

  if lines is not None:
    for line in lines:
      x1, y1, x2, y2 = line

      cv2.line(lines_image, (x1, y1), (x2, y2), (255, 0, 0), 10)

  return lines_image

from google.colab.patches import cv2_imshow

copy = np.copy(img)
gray = gray(copy)
gaus = gauss(gray)
edges = canny(gaus, 50, 150)
isolated = region(edges)
# Hough line transform
lines = cv2.HoughLinesP(isolated, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)

averaged_lines = average(copy, lines)
black_lines = display_lines(copy, averaged_lines)
lanes = cv2.addWeighted(copy, 0.8, black_lines, 1, 1)
cv2_imshow(lanes)
cv2.waitKey(0)
