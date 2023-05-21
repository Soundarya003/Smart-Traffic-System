import cv2
import numpy as np
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox
from numpy.lib.polynomial import poly
import time
from pyfirmata import Arduino, util, STRING_DATA
from time import strftime, time
import time

port = 'COM14'

board = Arduino(port)

score1,score2 = -1,-1
light1,light2 = 0,0

def timer(score):
  total = max(15, int(score*30))
  while total>0:
    board.send_sysex(STRING_DATA, util.str_to_two_byte_iter(str(total)))
    print(total)
    time.sleep(1)
    total -=1

def return_time(score):
  return max(15, int(score*30))

def count_img1():
    img = cv2.imread('pic1.jpg')
    img1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # plt.figure(figsize=(10,10))
    # plt.axis('off')
    # plt.imshow(img1)
    # plt.show()
    box, label, count = cv.detect_common_objects(img)
    output = draw_bbox(img, box, label, count)
    output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
    # plt.figure(figsize=(10,10))
    # plt.axis('off')
    print("Number of objects in this image are " + str(len(label)))
    global score1
    score1 = get_score(label, "1")
    print("Time alloted for Lane 1:",return_time(score1))
    # plt.imshow(output)
    # plt.show()
    return return_time(score1)

def count_img2():
    img = cv2.imread('pic2.jpg')
    #img1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # plt.figure(figsize=(10,10))
    # plt.axis('off')
    # plt.imshow(img1)
    # plt.show()
    box, label, count = cv.detect_common_objects(img)
    output = draw_bbox(img, box, label, count)
    output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
    # plt.figure(figsize=(10, 10))
    # plt.axis('off')
    print("Number of objects in this image are " + str(len(label)))
    global score2
    score2 = get_score(label, "2")
    print("Time alloted for Lane 2:",return_time(score2))
    print(label)
    # plt.imshow(output)
    # plt.show()
    return return_time(score2)

def get_score(label,lane):
  trucks = label.count('truck')
  cars = label.count('car')
  bikes = label.count('motorcycle')
  score = 0.42*trucks + 0.33*cars + 0.25*bikes
  print("Score of lane",lane,"is",score)
  return score

def light_func():
  global score1,score2,light1,light2
  if score1 < score2:
    light2 = 1

    print("Light1:",light1,"Light2:",light2)
    timer(score2)
    board.send_sysex(STRING_DATA, util.str_to_two_byte_iter("Lane 2 cleared"))
    print("Lane 2 has been cleared")
    light1,light2 = 1,0
    print("Light1:",light1,"Light2:",light2)
    timer(score1)
    board.send_sysex(STRING_DATA, util.str_to_two_byte_iter("Lane 1 cleared"))
    print("Lane 1 has been cleard")
    light1 = 0
    print("Light1:",light1,"Light2:",light2)
  else:
    light1 = 1
    print("Light1:",light1,"Light2:",light2)
    timer(score1)
    print("Lane 1 has been cleared")
    board.send_sysex(STRING_DATA, util.str_to_two_byte_iter("Lane 1 cleared"))
    light2,light1 = 1,0
    print("Light1:",light1,"Light2:",light2)
    timer(score2)
    print("Lane 2 has been cleard")
    board.send_sysex(STRING_DATA, util.str_to_two_byte_iter("Lane 2 cleared"))
    light1 = 0
    print("Light1:",light1,"Light2:",light2)

str1 = count_img1()
str2 = count_img2()
light_func()
