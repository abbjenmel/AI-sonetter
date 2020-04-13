# Importing cv2 module 
#import cv2  
# bat.jpg is the batman image. 
#img = cv2.imread('shakespeare.jpg')   
# make sure that you have saved it in the same folder 
# You can change the kernel size as you want 
#blurImg = cv2.blur(img,(15,15))  
#cv2.imshow('blurred image',blurImg)
# cv2.imwrite('bluured_shakespeare.jpg',blurImg)
# cv2.waitKey(0) 
# cv2.destroyAllWindows() 


from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import sys
 
text = "hi"
 
img = Image.open("bluured_shakespeare.jpg")
draw = ImageDraw.Draw(img)
font = ImageFont.truetype('Lobster-Regular.ttf', 40)
draw.text((0, 0), text , (255, 255, 255), font=font)
img.save("test.jpg")