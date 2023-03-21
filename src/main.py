""" main.py: cartoonize image
"""
import numpy as np
import cv2 as cv


class Cartoon():
    """Cartoonize image
    
    Args:
        path (str, optional): path to image. Defaults to "./data/solvay_conference.jpeg".
    
    Attributes:
        path (str): path to image
        img (numpy.ndarray): image - cv2.Mat
        gray (numpy.ndarray): gray image - cv2.Mat
        edge (None, optional): edge image
        style (None, optional): blurring style image
        
    Methods:
        threshold_edge(self, degree=9, sigma=9)
        blurring(self, degree=5, filter="bilateral")
        bit_and(self, degree=9, sigma=9)
        stylization(self, s=100, r=0.25)
    """
    def __init__(self, path="./data/solvay_conference.jpeg") -> None:
        self.path = path
        self.img = cv.imread(self.path)
        self.gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        self.edge = None
        self.style = None
        
    def threshold_edge(self, degree=9, sigma=9):
        # Apply adaptive thresholding to detect edges
        self.edge = cv.adaptiveThreshold(
            self.gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, degree, sigma)
        return self.edge
    
    def blurring(self, degree=5, filter="bilateral"):
        # Apply bilateral filter to smooth color and preserve edges
        if filter == "median":
            return cv.medianBlur(self.img, degree)
        if filter == "gaussian":
            return cv.GaussianBlur(self.img, (degree, degree), 0)
        if filter == "bilateral":
            return cv.bilateralFilter(self.img, degree, 75, 75)
        
    def bit_and(self, degree=9, sigma=9):
        # Blend the color image with the edges mask to create the cartoon effect
        if self.edge is None:
            self.threshold_edge(degree=degree, sigma=sigma)
        self.style = cv.bitwise_and(self.img, self.img, mask=self.edge)
        return self.style
    
    def stylization(self, s=150, r=0.25):
        # cv2 stylization function
        return cv.stylization(self.img, sigma_s=s, sigma_r=r)
    

if __name__=="__main__":
    # wait for 2 seconds each image
    cartoon = Cartoon()
    cv.imshow("original", cartoon.img)
    cv.waitKey(2000)
    cv.imshow("stylization", cartoon.stylization())
    cv.waitKeyEx(0)
    cv.waitKey(2000)
    cv.imshow("threshold edge", cartoon.threshold_edge())
    cv.waitKey(2000)
    cv.imshow("blurring", cartoon.blurring())
    cv.waitKey(2000)
    cv.imshow("bitwise and", cartoon.bit_and())
    cv.waitKey(2000)