from PIL import ImageGrab, Image, ImageTk, ImageFont, ImageDraw
import pytesseract
import numpy as np
import cv2
import pyautogui
import nameparse
import apicall
import time
from tkinter import Tk, Canvas, PhotoImage, NW
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
x = 0
game = []
team1 = []
team2 = []
ateam1 = 0
ateam2 = 0
kernel = np.ones((2,2),np.uint8)
scale = 4
custom_config = r'--psm 6'
img_height, img_width = 1440, 2560
n_channels = 3
transparent_img = np.zeros((img_height, img_width, n_channels), dtype=np.uint8)
root = Tk()
root.attributes('-transparentcolor','black')
root.attributes('-fullscreen',True)
root.attributes('-topmost', 'true')
# Canvas
canvas = Canvas(root, width=2560, height=1440)
canvas.pack()

# Image
img = ImageTk.PhotoImage(image=Image.fromarray(transparent_img))
canvas.create_image(0, 0, anchor=NW, image=img)

# Store newly created image
images=[]

# Define a function to make the transparent rectangle
def create_rectangle(x,y,a,b,**options):
   if 'alpha' in options:
      # Calculate the alpha transparency for every color(RGB)
      alpha = int(options.pop('alpha') * 255)
      # Use the fill variable to fill the shape with transparent color
      fill = options.pop('fill')
      fill = root.winfo_rgb(fill) + (alpha,)
      image = Image.new('RGBA', (a-x, b-y), fill)
      images.append(ImageTk.PhotoImage(image))
      canvas.create_image(x, y, image=images[-1], anchor='nw')
      canvas.create_rectangle(x, y,a,b, **options)


def outGame():
  global x
  global ateam1
  global ateam2
  transparent_img = np.zeros((img_height, img_width, n_channels), dtype=np.uint8)
  cv2.imwrite("overlayimg.jpg", transparent_img)
  img= Image.open("overlayimg.jpg")
  np_img = np.array(img)
  # imagemask = cv2.inRange(np_img, (0,0,0), (50,50,50))
  # np_img[imagemask>0]=[255,255,255]
  photoim =  ImageTk.PhotoImage(image=Image.fromarray(np_img))
  canvas.create_image(0, 0, anchor=NW, image=photoim)
  canvas.update()
  root.attributes('-topmost', 'true')
  objectlocation = pyautogui.locateCenterOnScreen('randomdice.png', confidence = 0.6)#If the file is not a png file it will not work
  print("running")
  print(objectlocation)
  if str(objectlocation)!='None':
    if(objectlocation.x>700 and objectlocation.x<800 and objectlocation.y>400 and objectlocation.y<500):
      time.sleep(0.5)
      screenshot = ImageGrab.grab(bbox=(777,550,996,836))
      screenshot.save("team1.png")
      screenshot = ImageGrab.grab(bbox=(1568,550,1787,836))
      screenshot.save("team2.png")
      team1img = cv2.imread('team1.png')
      team1img = cv2.resize(team1img, None, fx = scale, fy = scale)
      team1img = cv2.cvtColor(team1img, cv2.COLOR_BGR2GRAY)
      ret, team1img = cv2.threshold(team1img,127,255,cv2.THRESH_BINARY)
      team1img = cv2.erode(team1img, kernel, iterations = 1)
      #team1img = cv2.bitwise_not(team1img)
      cv2.imwrite('team1.png', team1img)
      text = pytesseract.image_to_string(team1img, config='--psm 6')
      print(text)
      team1=nameparse.intoList(text)
      team2img = cv2.imread('team2.png')
      team2img = cv2.resize(team2img, None, fx = scale, fy = scale)
      team2img = cv2.cvtColor(team2img, cv2.COLOR_BGR2GRAY)
      ret, team2img = cv2.threshold(team2img,127,255,cv2.THRESH_BINARY)
      team2img = cv2.erode(team2img, kernel, iterations = 1)
      #team2img = cv2.bitwise_not(team2img)
      cv2.imwrite('team2.png', team2img)
      text = pytesseract.image_to_string(team2img, config='--psm 6')
      print(text)
      team2=nameparse.intoList(text)
      x=1
      team1 = nameparse.removeClanTag(team1)
      team2 = nameparse.removeClanTag(team2)
      ateam1=apicall.wrapper(team1)
      ateam2=apicall.wrapper(team2)
      print(ateam1)
      print(ateam2)
      return ateam1, ateam2
def inGame(ateam1,ateam2):
  transparent_img = np.zeros((img_height, img_width, n_channels), dtype=np.uint8)
  starty = 375
  transparent_img = cv2.rectangle(transparent_img, (2258,starty-30), (2258+290,starty+85), (51,51,51), -1)
  transparent_img = cv2.rectangle(transparent_img, (10,starty-30),(300,starty+85),(51,51,51),-1)
  #text
  cv2.putText(img=transparent_img,text='wr='+str(ateam1['winrate'])+'%', org=(20,starty),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1, color=(0,200,200), thickness=2)
  cv2.putText(img=transparent_img,text='wr='+str(ateam2['winrate'])+'%', org=(2350,starty),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1, color=(0,200,200), thickness=2)

  cv2.putText(img=transparent_img,text='spot='+str(ateam1['spotspergame']), org=(20,starty+25),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1, color=(0,200,255), thickness=2)
  cv2.putText(img=transparent_img,text='spot='+str(ateam2['spotspergame']), org=(2338,starty+25),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1, color=(0,200,255), thickness=2)

  cv2.putText(img=transparent_img,text='dr='+str(ateam1['damageratio']), org=(20,starty+50),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1, color=(50,150,225), thickness=2)
  cv2.putText(img=transparent_img,text='dr='+str(ateam2['damageratio']), org=(2373,starty+50),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1, color=(50,150,225), thickness=2)

  cv2.putText(img=transparent_img,text='kdr='+str(ateam1['killdeathratio']), org=(20,starty+75),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1, color=(100,100,200), thickness=2)
  cv2.putText(img=transparent_img,text='kdr='+str(ateam2['killdeathratio']), org=(2356,starty+75),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1, color=(100,100,200), thickness=2)

  cv2.imwrite("overlayimg.jpg", transparent_img)
  np_img = np.array(transparent_img)
  imagemask = cv2.inRange(np_img, (0,0,0,0), (50,50,50,255))
  print(imagemask.shape)
  print(np_img.shape)
  np_img[imagemask>0]=[0,0,0]
  photoim =  ImageTk.PhotoImage(image=Image.fromarray(np_img))
  canvas.create_image(0, 0, anchor=NW, image=photoim)
  canvas.update()
  root.attributes('-topmost', 'true')
while True:
  if(x==0):
    outGame()
  else:
    inGame(ateam1,ateam2)
