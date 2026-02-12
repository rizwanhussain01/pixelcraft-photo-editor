import cv2

def grayscale(image):
    updatedimg = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(updatedimg,cv2.COLOR_GRAY2BGR)
    return gray

def invert(image):
    invertimg = cv2.bitwise_not(image)
    return invertimg

def red_channel(image):
    red_channel_image = image.copy()
    red_channel_image[:,:,0] = 0
    red_channel_image[:,:,1] = 0
    return red_channel_image

def green_channel(image):
    green_channel_image = image.copy()
    green_channel_image[:,:,0] = 0
    green_channel_image[:,:,2] = 0
    return green_channel_image

def blue_channel(image):
    blue_channel_image = image.copy()
    blue_channel_image[:,:,1] = 0
    blue_channel_image[:,:,2] = 0
    return blue_channel_image
    

def normal_blur(image,k):
    normalblurimg = cv2.blur(image,(k,k))
    return normalblurimg

def gaussian_blur(image,k):
    gaussianblurimg = cv2.GaussianBlur(image,(k,k),0)
    return gaussianblurimg

def median_blur(image,k):
    medianblurimg = cv2.medianBlur(image,k)
    return medianblurimg


