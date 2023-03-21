""" chatgpt.py: cartoonize by ChatGPT
"""

import cv2
import numpy as np

def convert_to_cartoon(image_path):
    # Load the input image
    img = cv2.imread(image_path)
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur to reduce noise
    gray = cv2.medianBlur(gray, 5)
    # Apply adaptive thresholding to detect edges
    edges = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    # Apply bilateral filter to smooth color and preserve edges
    color = np.copy(img)
    for i in range(5):
        color = cv2.bilateralFilter(color, 9, 300, 300)
    # Blend the color image with the edges mask to create the cartoon effect
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    # Return the output image
    return cartoon

# Test the function with an example image
input_image_path = './data/solvay_conference.jpeg'
output_image = convert_to_cartoon(input_image_path)

# Display the output image
cv2.imshow("Cartoon", output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()