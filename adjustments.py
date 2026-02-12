import cv2

def adjust(image, bl=0, cl=1.0):
    adjustimg = cv2.convertScaleAbs(image, alpha=cl,beta=bl)
    return adjustimg