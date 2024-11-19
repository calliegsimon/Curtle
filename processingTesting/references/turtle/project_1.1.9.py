# start
import turtle as trtl

# Lists for making stars
stars = []
star_color = ["red", "yellow", "blue", "red", "yellow", "blue", "red", "yellow", "blue", "red", "yellow", "blue", "red", "yellow", "blue", "red", "yellow", "blue","red", "yellow", "blue", "red", "yellow", "blue"]
star_shape = ["arrow", "turtle", "triangle", "classic", "arrow", "turtle", "triangle", "classic", "arrow", "turtle", "triangle", "classic", "arrow", "turtle", "triangle", "classic"]

# star time set up
x = -350
y = 300
hit = 0 

# loading
print("Booting up stars.")

#star time create
for shape in star_shape: 
  s = trtl.Turtle(shape)
  s.penup()
  s.setheading(90)
  s.hideturtle()
  stars.append(s)
  new_color = star_color.pop()
  s.fillcolor(new_color)
  s.goto(x,y)
  s.showturtle()
  x = x + 200
  if x >= 450:
    y = y - 100
    x = -250
    if y == 100:
      x = -350

# land line
starship = trtl.Turtle("square")
starship.hideturtle()
starship.penup()
starship.goto(-400,-200)
starship.pendown()
starship.forward(750)

# intructions 
print("Welcome to Starships! Your objective in this game is to shoot at the stars in the sky. You have 3 tries so go ahead.")

# starship set up
ship_color = input("Choose a color for your starship. ")
starship.fillcolor(ship_color)
starship.goto(0,-200)
starship.showturtle()
starship.pendown()

# 3 tries
fires = 0
while fires < 3:
  fires = fires + 1

# ask for angle

  angle = int(input("Choose an angle from 0 to 180. "))
  if angle > 180:
    angle = int(input("Please choose another angle that is between 0 and 180. "))
  if angle < 0:
    angle = int(input("Please choose another angle that is between 0 and 180. "))

# blast off 
  blast = 0
  while blast < 130:
    blast = blast + 1
    starship.setheading(angle)
    starship.forward(5)
    #checking for colisions
    for star in stars:
      x = abs(starship.xcor() - star.xcor())
      y = abs(starship.ycor() - star.ycor())
      #colision
      if x < 14:
        if y < 14:
          original_color = star.fillcolor()
          original_shape = star.shape()
          star.turtlesize(3)
          star.fillcolor("orange")
          star.shape("circle")
          star.turtlesize(1)
          star.fillcolor(original_color)
          star.shape(original_shape)
          star.setheading(-90)
          y = abs(star.ycor()) + 200
          star.forward(y)
          star.turtlesize(1.5)
          star.fillcolor("black")

          # for score
          hit = hit + 1

  #reset for next fire
  starship.hideturtle()
  starship.penup()
  starship.goto(0,-200)
  starship.pendown()
  starship.showturtle()

# points and end
print("Game End")
print("Your score is", hit * 1000)




  
  
  
wn = trtl.Screen()
wn.mainloop()