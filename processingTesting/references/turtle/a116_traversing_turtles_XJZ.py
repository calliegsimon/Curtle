#   a117_traversing_turtles.py
#   Add code to make turtles move in a circle and change colors.
import turtle as trtl

# create an empty list of turtles
my_turtles = []

# use interesting shapes and colors
turtle_shapes = ["arrow", "turtle", "circle", "square", "triangle", "classic", "arrow", "turtle", "circle", "square", "triangle", "classic"]
turtle_colors = ["red", "blue", "green", "orange", "purple", "gold", "red", "blue", "green", "orange", "purple", "gold"]

for s in turtle_shapes:
  new_color = turtle_colors.pop()
  t = trtl.Turtle(shape=s)
  t.hideturtle()
  t.pencolor (new_color)
  t.fillcolor (new_color)
  my_turtles.append(t)
  
  

#  
startx = 0
starty = 0
direction = 90
move = 50
#
for t in my_turtles:
  t.setheading (direction)
  t.penup()
  t.goto(startx, starty)
  t.pendown()
  t.right(45)     
  t.showturtle()
  t.forward(move)
  move = move + 10
  direction = t.heading()
  

#	
  startx = t.xcor()
  starty = t.ycor()
  

wn = trtl.Screen()
wn.mainloop()