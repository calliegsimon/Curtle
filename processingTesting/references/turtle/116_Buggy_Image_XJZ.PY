#   a116_buggy_image.py
import turtle as trtl

# create spider body
spider = trtl.Turtle()
spider.pensize(40)
spider.circle(20)

# create spider head
spider.pensize (30)
spider.goto(0, -30)
spider.circle(10)

# configure spider legs
num_legs = 8
leg_length = 70
angle = 360 / num_legs - 20
spider.pensize(5)

# draw spider legs
leg = 0
while (leg < num_legs):
  spider.penup()
  spider.goto(0,20)
  spider.pendown()
  if (leg < 4):
    spider.setheading(angle*leg - 45)
    spider.circle (100,45)
  else:
    spider.setheading(angle*leg - 130)
    spider.circle (100,-45)
  leg = leg + 1

# draw spider eyes
eye = 0
x_eye = -10
while eye < 2:
    spider.penup()
    spider.goto (x_eye, -30)
    spider.pendown()
    spider.pencolor ("red")
    spider.circle(5)
    eye += 1
    x_eye = x_eye + 15




spider.hideturtle()
wn = trtl.Screen()
wn.mainloop()