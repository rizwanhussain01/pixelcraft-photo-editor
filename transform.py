import cv2

def resize(image,rp):
    h,w = image.shape[:2]
    new_w = int(w*rp/100)
    new_h = int(h*rp/100)
    resizedimg = cv2.resize(image,(new_w,new_h))
    return resizedimg

def rotate(image,rp):
    if rp == 0:
        return image
    (h1,w1) = image.shape[:2]
    center = (w1//2,h1//2)
    m = cv2.getRotationMatrix2D(center,rp,1.0)
    rotatedimg = cv2.warpAffine(image,m,(w1,h1))
    return rotatedimg 

def horizontal_flip(image):
    flipped_horizontal_img = cv2.flip(image,1)
    return flipped_horizontal_img

def vertical_flip(image):
    flipped_vertical_image = cv2.flip(image,0)
    return flipped_vertical_image
