import cv2
import numpy as np

# Create a sample NumPy array
height, width = 300, 400
image = np.full((height, width),255, dtype=np.uint8)

# Define a circle and a rotated rectangle
circle_center = (150, 150)
circle_radius = 50

rect_center = (250, 150)
rect_size = (100, 50)
rect_angle = 30

# Create masks for the circle and rotated rectangle
circle_mask = np.zeros_like(image)
cv2.circle(circle_mask, circle_center, circle_radius, 255, thickness=-1)

rect_mask = np.zeros_like(image)
rect_points = cv2.boxPoints(((rect_center[0], rect_center[1]), (rect_size[0], rect_size[1]), rect_angle))
rect_points = np.int0(rect_points)
cv2.drawContours(rect_mask, [rect_points], 0, 255, thickness=-1)

# Calculate reduction percentage
reduction_percentage = 20

# Identify background region
background_mask = np.ones_like(image) - (circle_mask + rect_mask)

# Apply reduction to the background
background_reduced = np.where(background_mask > 0, image * (1 - reduction_percentage / 100), image)

# Apply masks for the circle and rotated rectangle
image_with_objects = np.where(circle_mask + rect_mask > 0, image, background_reduced)

# Display the results
cv2.imshow("Original", image)
cv2.imshow("Image with Objects", image_with_objects)
cv2.waitKey(0)
cv2.destroyAllWindows()
