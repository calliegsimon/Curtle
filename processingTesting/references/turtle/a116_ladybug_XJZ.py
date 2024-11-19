#   
import turtle as trtl

# create ladybug head
ladybug = trtl.Turtle()
ladybug.pensize(40)
ladybug.circle(5)

# leg config
num_legs = 6
leg_length = 60
angle = 360 / num_legs -30
ladybug.pensize(5)
  
# legs
leg = 0
while (leg < num_legs):
  ladybug.goto(0,-30)
  if (leg < 3):
    ladybug.setheading(angle*leg - 30)
  else:
    ladybug.setheading(angle*leg + 60)
  ladybug.forward(leg_length)
  leg = leg + 1

ladybug.setheading (0)

# and body
ladybug.penup()
ladybug.goto(0, -55) 
ladybug.color("red")
ladybug.pendown()
ladybug.pensize(40)
ladybug.circle(20)
ladybug.setheading(270)
ladybug.color("black")
ladybug.penup()
ladybug.goto(0, 5)
ladybug.pensize(2)
ladybug.pendown()
ladybug.forward(75)

# config dots
num_dots = 0
xpos = -20
ypos = -55
ladybug.pensize(10)

# draw two sets of dots
while (num_dots < 2 ):
  num_dots = num_dots + 1

  ladybug.penup()
  ladybug.goto(xpos, ypos)
  ladybug.pendown()
  ladybug.circle(3)

  ladybug.penup()
  ladybug.goto(xpos + 30, ypos + 20)
  ladybug.pendown()
  ladybug.circle(2)

  # position next dots
  ypos = ypos + 25
  xpos = xpos + 5 



ladybug.hideturtle()

wn = trtl.Screen()
wn.mainloop()